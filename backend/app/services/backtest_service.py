from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional, Tuple
import statistics

import pandas as pd
import numpy as np

from app.core.logging import get_logger
from app.models.database import SessionLocal
from app.models.schemas import IndexScore
from app.pipelines.ingestion.market_scraper import CasablancaMarketScraper


logger = get_logger(__name__)


@dataclass(slots=True)
class BacktestResult:
    """Résultat du backtest"""
    correlation_t1: float  # Corrélation score vs rendement T+1
    correlation_t5: float  # Corrélation score vs rendement T+5
    accuracy_t1: float  # % de prédictions correctes T+1
    accuracy_t5: float  # % de prédictions correctes T+5
    total_periods: int
    period_start: date
    period_end: date
    mean_score: float
    mean_return_t1: float
    mean_return_t5: float


class BacktestService:
    """
    Service de backtesting pour mesurer la corrélation entre le score
    Fear & Greed et les rendements futurs du marché.
    """

    def __init__(self):
        self.market_scraper = CasablancaMarketScraper()

    def run_backtest(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> BacktestResult:
        """
        Exécute un backtest complet.

        Args:
            start_date: Date de début (défaut: il y a 90 jours)
            end_date: Date de fin (défaut: aujourd'hui)

        Returns:
            BacktestResult avec les métriques de corrélation
        """
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = end_date - timedelta(days=90)

        logger.info(
            "Starting backtest from %s to %s",
            start_date,
            end_date,
        )

        # Récupérer les scores historiques
        scores_df = self._get_historical_scores(start_date, end_date)

        if scores_df.empty or len(scores_df) < 10:
            logger.warning("Not enough historical data for backtest")
            return BacktestResult(
                correlation_t1=0.0,
                correlation_t5=0.0,
                accuracy_t1=0.0,
                accuracy_t5=0.0,
                total_periods=0,
                period_start=start_date,
                period_end=end_date,
                mean_score=50.0,
                mean_return_t1=0.0,
                mean_return_t5=0.0,
            )

        # Récupérer les données de marché
        market_data = self._get_market_returns(start_date, end_date)

        if market_data.empty:
            logger.warning("No market data available for backtest")
            return BacktestResult(
                correlation_t1=0.0,
                correlation_t5=0.0,
                accuracy_t1=0.0,
                accuracy_t5=0.0,
                total_periods=len(scores_df),
                period_start=start_date,
                period_end=end_date,
                mean_score=scores_df["score"].mean(),
                mean_return_t1=0.0,
                mean_return_t5=0.0,
            )

        # Fusionner scores + rendements
        merged_df = self._merge_scores_and_returns(scores_df, market_data)

        if merged_df.empty or len(merged_df) < 5:
            logger.warning("Not enough merged data for backtest")
            return BacktestResult(
                correlation_t1=0.0,
                correlation_t5=0.0,
                accuracy_t1=0.0,
                accuracy_t5=0.0,
                total_periods=len(scores_df),
                period_start=start_date,
                period_end=end_date,
                mean_score=scores_df["score"].mean(),
                mean_return_t1=0.0,
                mean_return_t5=0.0,
            )

        # Calculer les corrélations
        corr_t1 = self._calculate_correlation(
            merged_df["score"].tolist(),
            merged_df["return_t1"].tolist(),
        )
        corr_t5 = self._calculate_correlation(
            merged_df["score"].tolist(),
            merged_df["return_t5"].tolist(),
        )

        # Calculer les accuracy (% de prédictions correctes)
        accuracy_t1 = self._calculate_accuracy(
            merged_df["score"].tolist(),
            merged_df["return_t1"].tolist(),
        )
        accuracy_t5 = self._calculate_accuracy(
            merged_df["score"].tolist(),
            merged_df["return_t5"].tolist(),
        )

        result = BacktestResult(
            correlation_t1=corr_t1,
            correlation_t5=corr_t5,
            accuracy_t1=accuracy_t1,
            accuracy_t5=accuracy_t5,
            total_periods=len(merged_df),
            period_start=start_date,
            period_end=end_date,
            mean_score=merged_df["score"].mean(),
            mean_return_t1=merged_df["return_t1"].mean(),
            mean_return_t5=merged_df["return_t5"].mean(),
        )

        logger.info(
            "Backtest completed: corr_t1=%.3f, corr_t5=%.3f, acc_t1=%.1f%%, acc_t5=%.1f%%",
            result.correlation_t1,
            result.correlation_t5,
            result.accuracy_t1,
            result.accuracy_t5,
        )

        return result

    def _get_historical_scores(
        self,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """Récupère les scores historiques depuis la DB."""
        with SessionLocal() as db:
            records = (
                db.query(IndexScore)
                .filter(IndexScore.as_of >= start_date)
                .filter(IndexScore.as_of <= end_date)
                .order_by(IndexScore.as_of.asc())
                .all()
            )

            data = [
                {"date": record.as_of.date(), "score": record.score}
                for record in records
            ]

            return pd.DataFrame(data)

    def _get_market_returns(
        self,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """Récupère les rendements du marché (MASI)."""
        try:
            # Étendre la période pour calculer T+5
            extended_end = end_date + timedelta(days=10)
            days_needed = (extended_end - start_date).days + 20

            historical_data = self.market_scraper.fetch_historical_data(days=days_needed)

            if not historical_data:
                return pd.DataFrame()

            # Convertir en DataFrame
            data = [
                {
                    "date": d.date if isinstance(d.date, date) else d.date,
                    "close": d.close_price,
                }
                for d in historical_data
            ]
            df = pd.DataFrame(data)
            df = df.sort_values("date")

            # Calculer les rendements futurs T+1 et T+5
            df["return_t1"] = df["close"].pct_change(periods=1).shift(-1)
            df["return_t5"] = df["close"].pct_change(periods=5).shift(-5)

            # Filtrer sur la période demandée
            df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

            return df

        except Exception as exc:
            logger.error("Error fetching market returns: %s", exc, exc_info=True)
            return pd.DataFrame()

    def _merge_scores_and_returns(
        self,
        scores_df: pd.DataFrame,
        market_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Fusionne les scores et les rendements sur la date."""
        merged = pd.merge(scores_df, market_df, on="date", how="inner")
        # Supprimer les lignes avec NaN (fin de période sans rendements futurs)
        merged = merged.dropna(subset=["return_t1", "return_t5"])
        return merged

    def _calculate_correlation(
        self,
        scores: List[float],
        returns: List[float],
    ) -> float:
        """Calcule la corrélation de Pearson."""
        if len(scores) < 2 or len(returns) < 2:
            return 0.0

        try:
            correlation = np.corrcoef(scores, returns)[0, 1]
            return float(correlation) if not np.isnan(correlation) else 0.0
        except Exception:
            return 0.0

    def _calculate_accuracy(
        self,
        scores: List[float],
        returns: List[float],
    ) -> float:
        """
        Calcule le % de prédictions correctes.
        - Score > 50 devrait prédire rendement positif
        - Score < 50 devrait prédire rendement négatif
        """
        if len(scores) != len(returns) or len(scores) == 0:
            return 0.0

        correct = 0
        for score, ret in zip(scores, returns):
            if (score > 50 and ret > 0) or (score < 50 and ret < 0):
                correct += 1

        return (correct / len(scores)) * 100.0

