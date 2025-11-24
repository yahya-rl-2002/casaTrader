from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Optional
import statistics

from app.core.logging import get_logger


logger = get_logger(__name__)


@dataclass(slots=True)
class SimplifiedScore:
    """Simplified Fear & Greed score based on simpler metrics"""
    score: float
    volume_component: float
    llm_sentiment: float
    market_sentiment: float
    total_stocks: int
    as_of: datetime


class SimplifiedCalculator:
    """
    Simplified Fear & Greed Index Calculator
    Based on: (Volume + LLM Sentiment + Market Sentiment) / Total Stocks
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.total_masi_stocks = 76  # Nombre approximatif d'actions dans le MASI

    def calculate_simplified_score(
        self,
        historical_data: List,
        media_articles: List,
        current_date: Optional[date] = None
    ) -> SimplifiedScore:
        """Calculate simplified Fear & Greed Index"""
        
        if current_date is None:
            current_date = date.today()
        
        current_datetime = datetime.combine(current_date, datetime.min.time())
        
        # 1. Volume Component (normalized to 0-100)
        volume_component = self._calculate_volume_component(historical_data)
        
        # 2. LLM Sentiment Component (from news articles)
        llm_sentiment = self._calculate_llm_sentiment(media_articles, current_date)
        
        # 3. Market Sentiment Component (positive vs negative performance)
        market_sentiment = self._calculate_market_sentiment(historical_data)
        
        # Calculate final score
        # Formula: (Volume + LLM_Sentiment + Market_Sentiment) / Total_Stocks
        raw_score = (volume_component + llm_sentiment + market_sentiment) / self.total_masi_stocks
        
        # Normalize to 0-100 scale
        normalized_score = min(100, max(0, raw_score * 100))
        
        return SimplifiedScore(
            score=round(normalized_score, 2),
            volume_component=volume_component,
            llm_sentiment=llm_sentiment,
            market_sentiment=market_sentiment,
            total_stocks=self.total_masi_stocks,
            as_of=current_datetime
        )

    def _calculate_volume_component(self, historical_data: List) -> float:
        """
        Calculate volume component based on daily average volume
        Returns: Normalized score (0-100)
        """
        try:
            if len(historical_data) < 20:
                return 50.0
            
            # Get last 20 days of data
            recent_data = historical_data[-20:]
            
            # Calculate average daily volume
            volumes = [d.volume for d in recent_data]
            avg_volume = statistics.mean(volumes)
            
            # Current volume vs average
            current_volume = recent_data[-1].volume
            
            # Calculate ratio and normalize
            if avg_volume > 0:
                volume_ratio = current_volume / avg_volume
                # Normalize: ratio of 1.0 = 50, ratio of 2.0 = 100, ratio of 0.5 = 25
                normalized = min(100, max(0, volume_ratio * 50))
            else:
                normalized = 50.0
            
            self.logger.info(f"Volume component: {normalized:.2f} (current: {current_volume}, avg: {avg_volume:.0f})")
            return normalized
            
        except Exception as e:
            self.logger.error(f"Error calculating volume component: {e}")
            return 50.0

    def _calculate_llm_sentiment(self, media_articles: List, current_date: date) -> float:
        """
        Calculate LLM-based sentiment from news articles
        Returns: Normalized score (0-100)
        """
        try:
            if not media_articles:
                return 50.0
            
            # Filter recent articles (last 7 days)
            cutoff_date = current_date - timedelta(days=7)
            recent_articles = [
                article for article in media_articles
                if article.published_at and article.published_at.date() >= cutoff_date
            ]
            
            if not recent_articles:
                return 50.0
            
            # Use sentiment scores from articles
            sentiment_scores = []
            for article in recent_articles:
                if hasattr(article, 'sentiment_score') and article.sentiment_score is not None:
                    # Convert from -1 to 1 scale to 0 to 100 scale
                    normalized = (article.sentiment_score + 1) * 50
                    sentiment_scores.append(normalized)
            
            if not sentiment_scores:
                return 50.0
            
            # Calculate weighted average (more recent articles have more weight)
            weights = [1.0 / (i + 1) for i in range(len(sentiment_scores))]
            weighted_avg = sum(s * w for s, w in zip(sentiment_scores, weights)) / sum(weights)
            
            self.logger.info(f"LLM Sentiment: {weighted_avg:.2f} (from {len(sentiment_scores)} articles)")
            return round(weighted_avg, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating LLM sentiment: {e}")
            return 50.0

    def _calculate_market_sentiment(self, historical_data: List) -> float:
        """
        Calculate market sentiment based on positive vs negative performance
        Returns: Normalized score (0-100)
        """
        try:
            if len(historical_data) < 20:
                return 50.0
            
            # Get last 20 days
            recent_data = historical_data[-20:]
            
            # Count positive and negative days
            positive_days = 0
            negative_days = 0
            
            for i in range(1, len(recent_data)):
                daily_change = recent_data[i].close_price - recent_data[i-1].close_price
                if daily_change > 0:
                    positive_days += 1
                elif daily_change < 0:
                    negative_days += 1
            
            total_days = positive_days + negative_days
            
            if total_days == 0:
                return 50.0
            
            # Calculate sentiment: more positive days = higher score
            sentiment_ratio = positive_days / total_days
            market_sentiment = sentiment_ratio * 100
            
            self.logger.info(f"Market Sentiment: {market_sentiment:.2f} (positive: {positive_days}, negative: {negative_days})")
            return round(market_sentiment, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating market sentiment: {e}")
            return 50.0

    def calculate_advanced_score(
        self,
        historical_data: List,
        media_articles: List,
        current_date: Optional[date] = None
    ) -> dict:
        """
        Calculate both simplified and detailed scores
        Returns: Dictionary with both approaches
        """
        
        # Get simplified score
        simplified = self.calculate_simplified_score(historical_data, media_articles, current_date)
        
        # Calculate detailed breakdown
        breakdown = {
            "simplified_approach": {
                "score": simplified.score,
                "components": {
                    "volume": simplified.volume_component,
                    "llm_sentiment": simplified.llm_sentiment,
                    "market_sentiment": simplified.market_sentiment
                },
                "formula": f"({simplified.volume_component:.2f} + {simplified.llm_sentiment:.2f} + {simplified.market_sentiment:.2f}) / {simplified.total_stocks}",
                "total_stocks": simplified.total_stocks
            },
            "interpretation": self._interpret_score(simplified.score),
            "timestamp": simplified.as_of.isoformat()
        }
        
        return breakdown

    def _interpret_score(self, score: float) -> str:
        """Interpret the fear & greed score"""
        if score < 25:
            return "Extreme Fear - Peur Extrême"
        elif score < 45:
            return "Fear - Peur"
        elif score < 55:
            return "Neutral - Neutre"
        elif score < 75:
            return "Greed - Avidité"
        else:
            return "Extreme Greed - Avidité Extrême"







