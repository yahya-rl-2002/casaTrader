from __future__ import annotations

from datetime import date, datetime
from typing import Callable, Coroutine, List, Optional, TypeVar
import asyncio
import time
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.database import get_session
from app.models.schemas import IndexScore, MediaArticle
from app.pipelines.ingestion.market_scraper import CasablancaMarketScraper, MASIHistoricalData
from app.pipelines.ingestion.media_scraper import MediaScraper
from app.services.sentiment_service import SentimentAnalyzer
from app.services.llm_sentiment_service import LLMSentimentAnalyzer
from app.services.component_calculator import ComponentCalculator
from app.pipelines.aggregator import IndexAggregator

T = TypeVar("T")


logger = get_logger(__name__)


class PipelineService:
    """Main service orchestrating the Fear & Greed Index pipeline"""
    
    def __init__(self, use_llm_sentiment: bool = True):
        self.market_scraper = CasablancaMarketScraper()
        self.media_scraper = MediaScraper()
        self.sentiment_analyzer = SentimentAnalyzer()  # Fallback
        self.llm_sentiment_analyzer = LLMSentimentAnalyzer() if use_llm_sentiment else None
        self.use_llm_sentiment = use_llm_sentiment
        self.component_calculator = ComponentCalculator()
        self.aggregator = IndexAggregator()
        self.max_retries = 3
        self.retry_backoff = 5  # seconds

    async def run_full_pipeline(self, target_date: Optional[date] = None) -> dict:
        """Run the complete Fear & Greed Index pipeline with retries."""
        if target_date is None:
            target_date = date.today()

        logger.info("Starting Fear & Greed Index pipeline for %s", target_date)

        try:
            logger.info("Step 1: Collecting market data")
            market_data = await self._collect_market_data(target_date)

            logger.info("Step 2: Collecting media data")
            media_data = await self._collect_media_data(target_date)

            logger.info("Step 3: Analyzing media sentiment")
            analyzed_media = await self._analyze_sentiment(media_data)

            logger.info("Step 4: Calculating index components")
            components = await self._calculate_components(market_data, analyzed_media, target_date)

            logger.info("Step 5: Aggregating final score")
            final_score = await self._aggregate_score(components)

            logger.info("Step 6: Saving results to database")
            await self._save_results(components, final_score, analyzed_media, target_date)

            logger.info("Pipeline completed successfully. Final score: %s", final_score)

            return {
                "success": True,
                "final_score": final_score,
                "components": components,
                "market_data_count": len(market_data),
                "media_articles_count": len(analyzed_media),
                "target_date": target_date,
            }

        except Exception as exc:
            logger.error("Pipeline failed: %s", exc, exc_info=True)
            return {
                "success": False,
                "error": str(exc),
                "target_date": target_date,
            }

    async def _collect_market_data(self, target_date: date) -> List[MASIHistoricalData]:
        """Collect market data with retries and detailed logging."""

        historical_data: List[MASIHistoricalData] = []
        live_data: List[MASIHistoricalData] = []

        try:
            historical_data = await self._fetch_with_retry(
                self.market_scraper.fetch_historical_data,
                "historical market data",
                days=252,
            )
        except Exception as exc:
            logger.error("Failed to collect historical market data after retries: %s", exc)

        try:
            live_data = await self._fetch_with_retry(
                self.market_scraper.fetch_live_data,
                "live market data",
            )
        except Exception as exc:
            logger.error("Failed to collect live market data after retries: %s", exc)

        logger.info(
            "Market data summary — historical: %s, live: %s",
            len(historical_data),
            len(live_data),
        )

        if not historical_data:
            logger.warning("Historical market data empty — components will fallback to defaults")
        if not live_data:
            logger.warning("Live market data empty — continuing with historical data only")

        return historical_data

    async def _collect_media_data(self, target_date: date) -> List[MediaArticle]:
        """Collect media articles with retries and logging."""
        try:
            articles = await self._fetch_with_retry(
                self.media_scraper.scrape_all_sources,
                "media articles",
                max_articles_per_source=10,
            )

            logger.info("Collected %s media articles", len(articles))
            return articles

        except Exception as exc:
            logger.error("Media scraping failed after retries: %s", exc)
            return []

    async def _analyze_sentiment(self, articles: List[MediaArticle]) -> List[MediaArticle]:
        """Analyze sentiment of media articles using LLM or fallback to dictionary"""
        try:
            if not articles:
                return []

            # Use LLM if available and enabled
            if self.use_llm_sentiment and self.llm_sentiment_analyzer and self.llm_sentiment_analyzer.enabled:
                logger.info("🤖 Using LLM (GPT) for sentiment analysis...")
                
                # Prepare articles for LLM
                articles_for_llm = [
                    {
                        'id': getattr(article, 'id', None),  # id might not exist yet
                        'title': article.title,
                        'summary': article.summary or ''
                    }
                    for article in articles
                ]
                
                # Analyze with LLM
                llm_results = self.llm_sentiment_analyzer.analyze_articles_batch(articles_for_llm)
                
                # Update articles with LLM results
                for article, llm_result in zip(articles, llm_results):
                    article.sentiment_score = llm_result.sentiment_score
                    article.sentiment_label = llm_result.sentiment_label
                
                logger.info("✅ LLM sentiment analysis completed for %s articles", len(articles))
                
                # Calculate average for logging
                if llm_results:
                    avg_sentiment = sum(r.sentiment_score for r in llm_results) / len(llm_results)
                    normalized_avg = (avg_sentiment + 1.0) * 50.0
                    logger.info(f"📊 Average sentiment (LLM): {avg_sentiment:+.3f} → {normalized_avg:.2f}/100")
                
            else:
                # Fallback to dictionary-based analysis
                logger.warning("⚠️ LLM not available, using dictionary-based sentiment analysis")
                sentiment_results = self.sentiment_analyzer.analyze_articles(articles)
                
                for article, sentiment in zip(articles, sentiment_results):
                    article.sentiment_score = sentiment.polarity
                    article.sentiment_label = self.sentiment_analyzer.get_sentiment_label(sentiment.polarity)
                
                logger.info("✅ Dictionary sentiment analysis completed for %s articles", len(articles))

            return articles
            
        except Exception as e:
            logger.error("❌ Error analyzing sentiment: %s", e, exc_info=True)
            # Fallback to dictionary if LLM fails
            if self.use_llm_sentiment:
                logger.warning("🔄 Falling back to dictionary-based sentiment...")
                try:
                    sentiment_results = self.sentiment_analyzer.analyze_articles(articles)
                    for article, sentiment in zip(articles, sentiment_results):
                        article.sentiment_score = sentiment.polarity
                        article.sentiment_label = self.sentiment_analyzer.get_sentiment_label(sentiment.polarity)
                except:
                    pass
            return articles

    async def _calculate_components(
        self, 
        market_data: List[MASIHistoricalData], 
        media_data: List[MediaArticle], 
        target_date: date
    ) -> dict:
        """Calculate all Fear & Greed Index components"""
        try:
            components = self.component_calculator.calculate_all_components(
                market_data, media_data, target_date
            )

            logger.info("Calculated components: %s", components)
            return components

        except Exception as e:
            logger.error("Error calculating components: %s", e, exc_info=True)
            # Return default components
            from app.services.component_calculator import ComponentScores
            return ComponentScores(
                momentum=50.0,
                price_strength=50.0,
                volume=50.0,
                volatility=50.0,
                equity_vs_bonds=50.0,
                media_sentiment=50.0,
                as_of=datetime.combine(target_date, datetime.min.time())
            )

    async def _aggregate_score(self, components) -> float:
        """Aggregate components into final Fear & Greed Index score"""
        try:
            components_dict = {
                "momentum": components.momentum,
                "price_strength": components.price_strength,
                "volume": components.volume,
                "volatility": components.volatility,
                "equity_vs_bonds": components.equity_vs_bonds,
                "media_sentiment": components.media_sentiment,
            }

            aggregate_result = self.aggregator.aggregate(
                components_dict,
                components.as_of,
            )

            score = round(aggregate_result.composite_score, 2)
            logger.info("Aggregated final score: %s", score)
            return score

        except Exception as e:
            logger.error("Error aggregating score: %s", e, exc_info=True)
            return 50.0  # Default neutral score

    async def _save_results(
        self, 
        components, 
        final_score: float, 
        media_articles: List[MediaArticle], 
        target_date: date
    ):
        """Save results to database"""
        try:
            db = get_session()

            existing_urls = {
                url for (url,) in db.query(MediaArticle.url).all()
            }

            index_score = IndexScore(
                as_of=datetime.combine(target_date, datetime.min.time()),
                score=final_score,
                momentum=components.momentum,
                price_strength=components.price_strength,
                volume=components.volume,
                volatility=components.volatility,
                equity_vs_bonds=components.equity_vs_bonds,
                media_sentiment=components.media_sentiment
            )
            
            db.add(index_score)

            new_articles = []
            for article in media_articles:
                if not article.url or article.url in existing_urls:
                    continue
                existing_urls.add(article.url)
                media_article = MediaArticle(
                    title=article.title,
                    summary=article.summary,
                    url=article.url,
                    source=article.source,
                    published_at=article.published_at,
                    sentiment_score=article.sentiment_score
                )
                new_articles.append(media_article)

            if new_articles:
                db.add_all(new_articles)

            db.commit()
            logger.info(
                "Saved results to database",
                extra={
                    "target_date": target_date,
                    "media_saved": len(new_articles),
                },
            )
            
        except Exception as e:
            logger.error("Error saving results: %s", e, exc_info=True)
            if 'db' in locals():
                db.rollback()

    async def _fetch_with_retry(
        self,
        func: Callable[..., T],
        description: str,
        **kwargs,
    ) -> T:
        """Execute a synchronous function with retry/backoff."""

        attempt = 0
        last_exception: Optional[Exception] = None

        while attempt < self.max_retries:
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, lambda: func(**kwargs))
                if attempt > 0:
                    logger.info("%s succeeded on retry #%s", description.capitalize(), attempt)
                return result
            except Exception as exc:  # noqa: BLE001
                attempt += 1
                last_exception = exc
                sleep_for = self.retry_backoff * attempt
                logger.warning(
                    "%s attempt %s/%s failed: %s — retrying in %ss",
                    description.capitalize(),
                    attempt,
                    self.max_retries,
                    exc,
                    sleep_for,
                )
                await asyncio.sleep(sleep_for)

        logger.error("%s failed after %s attempts", description.capitalize(), self.max_retries)
        if last_exception:
            raise last_exception
        raise RuntimeError(f"{description} failed without exception")

    async def get_latest_score(self) -> Optional[dict]:
        """Get the latest Fear & Greed Index score from database"""
        try:
            db = get_session()
            latest_score = db.query(IndexScore).order_by(IndexScore.as_of.desc()).first()
            
            if latest_score:
                return {
                    "score": latest_score.score,
                    "as_of": latest_score.as_of,
                    "components": {
                        "momentum": latest_score.momentum,
                        "price_strength": latest_score.price_strength,
                        "volume": latest_score.volume,
                        "volatility": latest_score.volatility,
                        "equity_vs_bonds": latest_score.equity_vs_bonds,
                        "media_sentiment": latest_score.media_sentiment
                    }
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting latest score: {e}")
            return None

