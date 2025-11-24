from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Optional
import statistics

from app.core.logging import get_logger
from app.pipelines.ingestion.market_scraper import CasablancaMarketScraper, MASIHistoricalData
from app.pipelines.ingestion.media_scraper import MediaScraper
from app.services.sentiment_service import SentimentAnalyzer


logger = get_logger(__name__)


@dataclass(slots=True)
class SimplifiedIndexResult:
    """Résultat du calcul simplifié de l'indice"""
    score: float
    volume_moyen: float
    sentiment_news: float
    performance_marche: float
    nombre_actions: int
    date: date
    details: dict


class SimplifiedIndexCalculator:
    """
    Calculateur d'indice Fear & Greed simplifié basé sur la formule :
    
    Score = (Volume journalier moyen MASI + Sentiment news + Performance marché) / Nombre total d'actions
    
    Où :
    - Volume journalier moyen : Volume MASI sur 20 derniers jours, normalisé 0-100
    - Sentiment news : Degré d'optimisme des news (LLM/NLP), normalisé 0-100
    - Performance marché : (Actions positives - Actions négatives), normalisé 0-100
    - Nombre total d'actions : Nombre d'actions échangées sur MASI
    """

    def __init__(self):
        self.market_scraper = CasablancaMarketScraper()
        self.media_scraper = MediaScraper()
        self.sentiment_analyzer = SentimentAnalyzer()

    async def calculate_index(
        self,
        target_date: Optional[date] = None
    ) -> SimplifiedIndexResult:
        """
        Calcule l'indice Fear & Greed selon la formule simplifiée.
        
        Args:
            target_date: Date de calcul (défaut: aujourd'hui)
            
        Returns:
            SimplifiedIndexResult avec le score et les détails
        """
        if target_date is None:
            target_date = date.today()

        logger.info("Calculating simplified index for %s", target_date)

        # 1. Volume journalier moyen sur MASI (20 derniers jours)
        volume_moyen_score = await self._calculate_volume_moyen(target_date)

        # 2. Sentiment des news (degré d'optimisme via LLM/NLP)
        sentiment_news_score = await self._calculate_sentiment_news(target_date)

        # 3. Performance du marché (actions positives vs négatives)
        performance_marche_score = await self._calculate_performance_marche(target_date)

        # 4. Nombre total d'actions sur MASI
        nombre_actions = await self._get_nombre_actions_masi()

        # Calcul du score final selon la formule
        # (Volume + Sentiment + Performance) / Nombre d'actions
        numerateur = volume_moyen_score + sentiment_news_score + performance_marche_score
        
        if nombre_actions > 0:
            score_brut = numerateur / nombre_actions
            # Normaliser à l'échelle 0-100
            # On multiplie par un facteur pour ramener à une échelle lisible
            score_final = min(100, max(0, score_brut * 10))  # Facteur d'ajustement
        else:
            score_final = 50.0  # Neutre par défaut

        logger.info(
            "Simplified index calculated: score=%.2f, volume=%.2f, sentiment=%.2f, performance=%.2f, actions=%d",
            score_final,
            volume_moyen_score,
            sentiment_news_score,
            performance_marche_score,
            nombre_actions,
        )

        return SimplifiedIndexResult(
            score=round(score_final, 2),
            volume_moyen=volume_moyen_score,
            sentiment_news=sentiment_news_score,
            performance_marche=performance_marche_score,
            nombre_actions=nombre_actions,
            date=target_date,
            details={
                "numerateur": numerateur,
                "formule": f"({volume_moyen_score:.2f} + {sentiment_news_score:.2f} + {performance_marche_score:.2f}) / {nombre_actions}",
                "interpretation": self._interpret_score(score_final),
            }
        )

    async def _calculate_volume_moyen(self, target_date: date) -> float:
        """
        Calcule le volume journalier moyen sur les 20 derniers jours.
        Normalisé sur une échelle 0-100.
        """
        try:
            # Récupérer les 20 derniers jours de données
            historical_data = self.market_scraper.fetch_historical_data(days=20)

            if not historical_data or len(historical_data) < 5:
                logger.warning("Not enough historical data for volume calculation")
                return 50.0  # Neutre

            # Calculer le volume moyen
            volumes = [d.volume for d in historical_data if d.volume > 0]
            
            if not volumes:
                return 50.0

            volume_moyen = statistics.mean(volumes)
            
            # Normaliser : comparer au volume min/max de la période
            volume_min = min(volumes)
            volume_max = max(volumes)

            if volume_max == volume_min:
                return 50.0

            # Position du volume moyen dans la plage min-max
            volume_normalized = ((volume_moyen - volume_min) / (volume_max - volume_min)) * 100

            logger.info(
                "Volume moyen calculated: %.2f (min=%.2f, max=%.2f, normalized=%.2f)",
                volume_moyen,
                volume_min,
                volume_max,
                volume_normalized,
            )

            return round(volume_normalized, 2)

        except Exception as e:
            logger.error("Error calculating volume moyen: %s", e, exc_info=True)
            return 50.0

    async def _calculate_sentiment_news(self, target_date: date) -> float:
        """
        Analyse le degré d'optimisme des news publiées durant la journée.
        Utilise le sentiment analyzer (NLP/LLM) pour scorer les articles.
        Normalisé sur une échelle 0-100.
        """
        try:
            # Scraper les articles du jour (max 30 articles)
            articles = self.media_scraper.scrape_all_sources(max_articles_per_source=10)

            if not articles:
                logger.warning("No articles found for sentiment analysis")
                return 50.0  # Neutre

            # Filtrer les articles de la journée (dernières 24h)
            cutoff = target_date - timedelta(days=1)
            recent_articles = [
                article for article in articles
                if article.published_at and article.published_at.date() >= cutoff
            ]

            if not recent_articles:
                # Si pas d'articles du jour, utiliser les plus récents
                recent_articles = articles[:20]

            # Analyser le sentiment de tous les articles
            sentiment_results = self.sentiment_analyzer.analyze_articles(recent_articles)

            # Extraire les scores de polarité
            polarity_scores = [
                result.polarity for result in sentiment_results
                if result.polarity is not None
            ]

            if not polarity_scores:
                return 50.0

            # Calculer le score moyen de sentiment
            # Polarity est entre -100 et +100, on normalise à 0-100
            avg_polarity = statistics.mean(polarity_scores)
            sentiment_normalized = ((avg_polarity + 100) / 2)  # De [-100,+100] à [0,100]

            logger.info(
                "Sentiment news calculated: %.2f articles analyzed, avg_polarity=%.2f, normalized=%.2f",
                len(polarity_scores),
                avg_polarity,
                sentiment_normalized,
            )

            return round(sentiment_normalized, 2)

        except Exception as e:
            logger.error("Error calculating sentiment news: %s", e, exc_info=True)
            return 50.0

    async def _calculate_performance_marche(self, target_date: date) -> float:
        """
        Calcule la performance du marché basée sur :
        (Nombre d'actions en hausse - Nombre d'actions en baisse)
        Normalisé sur une échelle 0-100.
        
        Note : Actuellement, on utilise la performance globale du MASI
        car on n'a pas accès au détail de chaque action individuellement.
        """
        try:
            # Récupérer les 5 derniers jours pour calculer la tendance
            historical_data = self.market_scraper.fetch_historical_data(days=5)

            if not historical_data or len(historical_data) < 2:
                logger.warning("Not enough data for market performance calculation")
                return 50.0

            # Calculer le rendement sur les derniers jours
            returns = []
            for i in range(1, len(historical_data)):
                if historical_data[i-1].close_price == 0:
                    continue
                daily_return = (
                    (historical_data[i].close_price - historical_data[i-1].close_price)
                    / historical_data[i-1].close_price
                )
                returns.append(daily_return)

            if not returns:
                return 50.0

            # Calculer le % de jours positifs vs négatifs
            positive_days = sum(1 for r in returns if r > 0)
            negative_days = sum(1 for r in returns if r < 0)
            neutral_days = len(returns) - positive_days - negative_days

            # Score basé sur la proportion de jours positifs
            if len(returns) > 0:
                positive_ratio = positive_days / len(returns)
                performance_score = positive_ratio * 100
            else:
                performance_score = 50.0

            # Ajuster avec l'amplitude du rendement moyen
            avg_return = statistics.mean(returns)
            # Bonus/malus selon l'amplitude du rendement (max ±20 points)
            amplitude_adjustment = min(20, max(-20, avg_return * 1000))
            
            performance_final = performance_score + amplitude_adjustment
            performance_final = min(100, max(0, performance_final))

            logger.info(
                "Market performance calculated: positive=%d, negative=%d, avg_return=%.4f, score=%.2f",
                positive_days,
                negative_days,
                avg_return,
                performance_final,
            )

            return round(performance_final, 2)

        except Exception as e:
            logger.error("Error calculating market performance: %s", e, exc_info=True)
            return 50.0

    async def _get_nombre_actions_masi(self) -> int:
        """
        Retourne le nombre total d'actions cotées sur le MASI.
        
        Note : Le MASI (Moroccan All Shares Index) comprend environ 75-80 actions.
        Cette valeur est relativement stable mais peut être mise à jour.
        """
        # TODO : Scraper cette information depuis le site de la Bourse de Casablanca
        # Pour l'instant, on utilise une valeur approximative
        return 76  # Valeur approximative du nombre d'actions sur MASI

    def _interpret_score(self, score: float) -> str:
        """Interprète le score final."""
        if score >= 75:
            return "EXTREME GREED - Le marché est très optimiste"
        elif score >= 60:
            return "GREED - Le marché est optimiste"
        elif score >= 40:
            return "NEUTRAL - Le marché est équilibré"
        elif score >= 25:
            return "FEAR - Le marché est pessimiste"
        else:
            return "EXTREME FEAR - Le marché est très pessimiste"

