from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
import math
import statistics

import pandas as pd

from app.core.logging import get_logger
from app.services.dynamic_scaler import DynamicScalerService


logger = get_logger(__name__)


@dataclass(slots=True)
class ComponentScores:
    momentum: float
    price_strength: float
    volume: float
    volatility: float
    equity_vs_bonds: float
    media_sentiment: float
    as_of: datetime


class ComponentCalculator:
    """Calculate Fear & Greed Index components with dynamic normalization"""
    
    def __init__(self, use_dynamic_scaling: bool = True):
        self.logger = get_logger(__name__)
        self.use_dynamic_scaling = use_dynamic_scaling
        if use_dynamic_scaling:
            self.dynamic_scaler = DynamicScalerService(window_days=90)

    def calculate_all_components(
        self,
        historical_data: List,
        media_articles: List,
        current_date: Optional[date] = None
    ) -> ComponentScores:
        """Calculate all Fear & Greed Index components"""
        if current_date is None:
            current_date = date.today()
        
        current_datetime = datetime.combine(current_date, datetime.min.time())
        
        # Calculate each component (raw values)
        momentum = self._calculate_momentum(historical_data, current_date)
        price_strength = self._calculate_price_strength(historical_data, current_date)
        volume = self._calculate_volume(historical_data, current_date)
        volatility = self._calculate_volatility(historical_data, current_date)
        equity_vs_bonds = self._calculate_equity_vs_bonds(historical_data, current_date)
        media_sentiment = self._calculate_media_sentiment(media_articles, current_date)

        # Apply dynamic normalization if enabled
        if self.use_dynamic_scaling:
            raw_components = {
                "momentum": momentum,
                "price_strength": price_strength,
                "volume": volume,
                "volatility": volatility,
                "equity_vs_bonds": equity_vs_bonds,
                "media_sentiment": media_sentiment,
            }
            
            normalized = self.dynamic_scaler.normalize_all_components(
                raw_components, 
                current_date
            )
            
            momentum = normalized.get("momentum", momentum)
            price_strength = normalized.get("price_strength", price_strength)
            volume = normalized.get("volume", volume)
            volatility = normalized.get("volatility", volatility)
            equity_vs_bonds = normalized.get("equity_vs_bonds", equity_vs_bonds)
            media_sentiment = normalized.get("media_sentiment", media_sentiment)
            
            logger.info("Applied dynamic normalization to components")

        logger.debug(
            "Component breakdown",
            extra={
                "momentum": momentum,
                "price_strength": price_strength,
                "volume": volume,
                "volatility": volatility,
                "equity_vs_bonds": equity_vs_bonds,
                "media_sentiment": media_sentiment,
            },
        )
        
        return ComponentScores(
            momentum=momentum,
            price_strength=price_strength,
            volume=volume,
            volatility=volatility,
            equity_vs_bonds=equity_vs_bonds,
            media_sentiment=media_sentiment,
            as_of=current_datetime
        )

    def _calculate_momentum(self, historical_data: List, current_date: date) -> float:
        """Calculate momentum component (125-day vs 125-day previous)"""
        try:
            if len(historical_data) < 250:  # Need at least 250 days
                return 50.0  # Neutral score
            
            # Get last 125 days
            recent_data = historical_data[-125:]
            # Get previous 125 days
            previous_data = historical_data[-250:-125]
            
            if not recent_data or not previous_data:
                return 50.0
            
            # Calculate average prices
            recent_avg = statistics.mean([d.close_price for d in recent_data])
            previous_avg = statistics.mean([d.close_price for d in previous_data])
            
            if previous_avg == 0:
                return 50.0

            # Calculate momentum percentage
            momentum_pct = ((recent_avg - previous_avg) / previous_avg) * 100
            
            # Normalize to 0-100 scale
            # Positive momentum = higher score, negative = lower score
            normalized_score = 50 + (momentum_pct * 2)  # Scale factor of 2
            return max(0, min(100, normalized_score))
            
        except Exception as e:
            self.logger.error(f"Error calculating momentum: {e}")
            return 50.0

    def _calculate_price_strength(self, historical_data: List, current_date: date) -> float:
        """Calculate price strength (52-week highs vs lows)"""
        try:
            if len(historical_data) < 252:  # Need at least 1 year
                return 50.0
            
            # Get last 252 days (1 year)
            yearly_data = historical_data[-252:]
            
            # Find 52-week high and low
            high_price = max(d.high_price for d in yearly_data)
            low_price = min(d.low_price for d in yearly_data)
            current_price = yearly_data[-1].close_price
            
            if high_price == low_price:
                return 50.0
            
            # Calculate position between high and low
            position = (current_price - low_price) / (high_price - low_price)
            
            # Convert to 0-100 scale
            return position * 100
            
        except Exception as e:
            self.logger.error(f"Error calculating price strength: {e}")
            return 50.0

    def _calculate_volume(self, historical_data: List, current_date: date) -> float:
        """Calculate volume component (current vs 30-day average)"""
        try:
            if len(historical_data) < 30:
                return 50.0
            
            # Get last 30 days
            recent_data = historical_data[-30:]
            current_volume = recent_data[-1].volume
            avg_volume = statistics.mean([d.volume for d in recent_data])
            
            if avg_volume == 0:
                return 50.0
            
            # Calculate volume ratio
            volume_ratio = current_volume / avg_volume
            
            # Normalize to 0-100 scale
            # Higher volume = higher score
            normalized_score = min(100, volume_ratio * 50)  # Cap at 100
            return max(0, normalized_score)
            
        except Exception as e:
            self.logger.error(f"Error calculating volume: {e}")
            return 50.0

    def _calculate_volatility(self, historical_data: List, current_date: date) -> float:
        """Calculate volatility component (inverse relationship)"""
        try:
            if len(historical_data) < 30:
                return 50.0
            
            # Get last 30 days
            recent_data = historical_data[-30:]
            
            # Calculate daily returns
            returns = []
            for i in range(1, len(recent_data)):
                prev_close = recent_data[i-1].close_price
                if prev_close == 0:
                    continue
                daily_return = (recent_data[i].close_price - prev_close) / prev_close
                returns.append(daily_return)
            
            if not returns:
                return 50.0
            
            # Calculate standard deviation (volatility)
            volatility = statistics.stdev(returns) * math.sqrt(252)  # Annualized
            
            # Convert to Fear & Greed scale (inverse relationship)
            # Higher volatility = lower score (more fear)
            # Lower volatility = higher score (less fear)
            normalized_score = max(0, 100 - (volatility * 1000))  # Scale factor
            return min(100, normalized_score)
            
        except Exception as e:
            self.logger.error(f"Error calculating volatility: {e}")
            return 50.0

    def _calculate_equity_vs_bonds(self, historical_data: List, current_date: date) -> float:
        """Calculate equity vs bonds component (simplified)"""
        try:
            if len(historical_data) < 20:
                return 50.0
            
            # Get last 20 days
            recent_data = historical_data[-20:]
            
            # Calculate equity performance (simplified as MASI performance)
            equity_return = (recent_data[-1].close_price - recent_data[0].close_price) / recent_data[0].close_price
            
            # Simulate bond performance (typically lower and more stable)
            # In real implementation, this would use actual bond data
            bond_return = 0.02  # Assume 2% annual return for bonds
            
            # Calculate relative performance
            relative_performance = equity_return - bond_return
            
            # Normalize to 0-100 scale
            # Better equity performance = higher score
            normalized_score = 50 + (relative_performance * 1000)  # Scale factor
            return max(0, min(100, normalized_score))
            
        except Exception as e:
            self.logger.error(f"Error calculating equity vs bonds: {e}")
            return 50.0

    def _calculate_media_sentiment(self, media_articles: List, current_date: date) -> float:
        """Calculate media sentiment component"""
        try:
            if not media_articles:
                return 50.0
            
            # Filter articles from last 7 days
            cutoff_date = current_date - timedelta(days=7)
            recent_articles = [
                article for article in media_articles
                if article.published_at and article.published_at.date() >= cutoff_date
            ]
            
            if not recent_articles:
                return 50.0
            
            # Calculate average sentiment
            sentiment_scores = []
            for article in recent_articles:
                if hasattr(article, 'sentiment_score') and article.sentiment_score is not None:
                    sentiment_scores.append(article.sentiment_score)
            
            if not sentiment_scores:
                return 50.0
            
            avg_sentiment = statistics.mean(sentiment_scores)
            
            # Convert from -1 to 1 scale to 0 to 100 scale
            normalized_score = (avg_sentiment + 1) * 50
            return max(0, min(100, normalized_score))
            
        except Exception as e:
            self.logger.error(f"Error calculating media sentiment: {e}")
            return 50.0

    def calculate_composite_score(self, components: ComponentScores) -> float:
        """Calculate composite Fear & Greed Index score"""
        weights = {
            'momentum': 0.25,
            'price_strength': 0.25,
            'volume': 0.15,
            'volatility': 0.15,
            'equity_vs_bonds': 0.10,
            'media_sentiment': 0.10
        }
        
        composite_score = (
            components.momentum * weights['momentum'] +
            components.price_strength * weights['price_strength'] +
            components.volume * weights['volume'] +
            components.volatility * weights['volatility'] +
            components.equity_vs_bonds * weights['equity_vs_bonds'] +
            components.media_sentiment * weights['media_sentiment']
        )
        
        return round(composite_score, 2)

