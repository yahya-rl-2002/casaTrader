from datetime import date
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.simplified_calculator import SimplifiedCalculator
from app.pipelines.ingestion.market_scraper import CasablancaMarketScraper
from app.pipelines.ingestion.media_scraper import MediaScraper
from app.services.sentiment_service import SentimentAnalyzer
from app.core.logging import get_logger


logger = get_logger(__name__)
router = APIRouter()


class SimplifiedScoreResponse(BaseModel):
    score: float
    volume_component: float
    llm_sentiment: float
    market_sentiment: float
    total_stocks: int
    interpretation: str
    formula: str
    timestamp: str


class ComparisonResponse(BaseModel):
    simplified_score: float
    traditional_score: float
    difference: float
    recommended_approach: str


@router.get("/score", summary="Get Simplified Fear & Greed Score", response_model=SimplifiedScoreResponse)
async def get_simplified_score():
    """
    Get Fear & Greed Index using simplified formula:
    (Volume + LLM_Sentiment + Market_Sentiment) / Total_Stocks
    """
    try:
        # Initialize calculators
        simplified_calc = SimplifiedCalculator()
        market_scraper = CasablancaMarketScraper()
        media_scraper = MediaScraper()
        sentiment_analyzer = SentimentAnalyzer()
        
        # Fetch data
        historical_data = market_scraper.fetch_historical_data(days=30)
        media_articles = media_scraper.scrape_all_sources(max_articles_per_source=10)
        
        # Analyze sentiment
        for article in media_articles:
            sentiment = sentiment_analyzer.analyze_text(f"{article.title} {article.summary}")
            article.sentiment_score = sentiment.polarity
        
        # Calculate simplified score
        result = simplified_calc.calculate_simplified_score(historical_data, media_articles)
        
        return SimplifiedScoreResponse(
            score=result.score,
            volume_component=result.volume_component,
            llm_sentiment=result.llm_sentiment,
            market_sentiment=result.market_sentiment,
            total_stocks=result.total_stocks,
            interpretation=simplified_calc._interpret_score(result.score),
            formula=f"({result.volume_component:.2f} + {result.llm_sentiment:.2f} + {result.market_sentiment:.2f}) / {result.total_stocks}",
            timestamp=result.as_of.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error calculating simplified score: {e}")
        raise


@router.get("/comparison", summary="Compare Simplified vs Traditional Approach")
async def compare_approaches():
    """
    Compare simplified approach with traditional multi-component approach
    """
    try:
        from app.services.component_calculator import ComponentCalculator
        
        # Initialize calculators
        simplified_calc = SimplifiedCalculator()
        traditional_calc = ComponentCalculator()
        market_scraper = CasablancaMarketScraper()
        media_scraper = MediaScraper()
        sentiment_analyzer = SentimentAnalyzer()
        
        # Fetch data
        historical_data = market_scraper.fetch_historical_data(days=252)
        media_articles = media_scraper.scrape_all_sources(max_articles_per_source=10)
        
        # Analyze sentiment
        for article in media_articles:
            sentiment = sentiment_analyzer.analyze_text(f"{article.title} {article.summary}")
            article.sentiment_score = sentiment.polarity
        
        # Calculate both scores
        simplified_result = simplified_calc.calculate_simplified_score(historical_data, media_articles)
        traditional_components = traditional_calc.calculate_all_components(historical_data, media_articles)
        traditional_score = traditional_calc.calculate_composite_score(traditional_components)
        
        # Calculate difference
        difference = abs(simplified_result.score - traditional_score)
        
        # Determine recommended approach
        if difference < 10:
            recommendation = "Both approaches agree - use simplified for simplicity"
        elif simplified_result.score > traditional_score:
            recommendation = "Simplified shows more optimism - consider market conditions"
        else:
            recommendation = "Traditional shows more optimism - consider component breakdown"
        
        return {
            "simplified_approach": {
                "score": simplified_result.score,
                "components": {
                    "volume": simplified_result.volume_component,
                    "llm_sentiment": simplified_result.llm_sentiment,
                    "market_sentiment": simplified_result.market_sentiment
                },
                "interpretation": simplified_calc._interpret_score(simplified_result.score)
            },
            "traditional_approach": {
                "score": traditional_score,
                "components": {
                    "momentum": traditional_components.momentum,
                    "price_strength": traditional_components.price_strength,
                    "volume": traditional_components.volume,
                    "volatility": traditional_components.volatility,
                    "equity_vs_bonds": traditional_components.equity_vs_bonds,
                    "media_sentiment": traditional_components.media_sentiment
                }
            },
            "comparison": {
                "difference": round(difference, 2),
                "correlation": "high" if difference < 10 else "medium" if difference < 20 else "low",
                "recommended_approach": recommendation
            }
        }
        
    except Exception as e:
        logger.error(f"Error comparing approaches: {e}")
        raise


@router.get("/explain", summary="Explain the Simplified Formula")
async def explain_formula():
    """
    Explain how the simplified Fear & Greed Index works
    """
    return {
        "formula": "(Volume + LLM_Sentiment + Market_Sentiment) / Total_Stocks",
        "components": {
            "volume": {
                "description": "Volume journalier moyen sur MASI",
                "calculation": "Ratio du volume actuel vs moyenne 20 jours",
                "range": "0-100",
                "interpretation": "Plus élevé = Plus d'activité = Plus de confiance"
            },
            "llm_sentiment": {
                "description": "Analyse LLM du degré d'optimisme des news",
                "calculation": "Moyenne pondérée des sentiments des articles récents",
                "range": "0-100",
                "interpretation": "Plus élevé = News plus positives = Plus d'optimisme"
            },
            "market_sentiment": {
                "description": "Sentiment de marché (performance positive vs négative)",
                "calculation": "Ratio des jours positifs vs jours négatifs sur 20 jours",
                "range": "0-100",
                "interpretation": "Plus élevé = Plus de jours positifs = Plus d'optimisme"
            },
            "total_stocks": {
                "description": "Nombre total d'actions dans le MASI",
                "value": 76,
                "role": "Normalization factor"
            }
        },
        "advantages": [
            "Simple et facile à comprendre",
            "Calcul rapide",
            "Focus sur les facteurs essentiels",
            "Moins sensible au bruit"
        ],
        "disadvantages": [
            "Moins de granularité",
            "Peut manquer des signaux subtils",
            "Dépend fortement du nombre d'actions"
        ],
        "use_cases": [
            "Vue rapide du sentiment du marché",
            "Décisions trading court terme",
            "Validation contre l'approche traditionnelle"
        ]
    }







