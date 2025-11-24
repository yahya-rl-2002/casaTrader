from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional
import statistics

from sklearn.preprocessing import MinMaxScaler
import numpy as np

from app.core.logging import get_logger
from app.models.database import SessionLocal
from app.models.schemas import IndexScore


logger = get_logger(__name__)


@dataclass(slots=True)
class DynamicScalingResult:
    raw_value: float
    scaled_value: float
    window_min: float
    window_max: float
    window_mean: float


class DynamicScalerService:
    """
    Service de normalisation dynamique basé sur des fenêtres glissantes.
    Recalcule les min/max sur les N derniers jours pour adapter le scaling
    aux conditions actuelles du marché.
    """

    def __init__(self, window_days: int = 90):
        self.window_days = window_days
        self.feature_range = (0.0, 100.0)

    def normalize_component(
        self,
        component_name: str,
        current_value: float,
        current_date: Optional[date] = None,
    ) -> DynamicScalingResult:
        """
        Normalise une composante en utilisant une fenêtre glissante.

        Args:
            component_name: Nom de la composante (momentum, volume, etc.)
            current_value: Valeur actuelle à normaliser
            current_date: Date de référence (défaut: aujourd'hui)

        Returns:
            DynamicScalingResult avec la valeur normalisée et les stats de fenêtre
        """
        if current_date is None:
            current_date = date.today()

        # Récupérer l'historique des valeurs de cette composante
        historical_values = self._get_historical_values(component_name, current_date)

        if not historical_values or len(historical_values) < 2:
            # Pas assez de données : retourner la valeur brute
            logger.warning(
                "Not enough historical data for %s, returning raw value",
                component_name,
            )
            return DynamicScalingResult(
                raw_value=current_value,
                scaled_value=current_value,
                window_min=current_value,
                window_max=current_value,
                window_mean=current_value,
            )

        # Calculer les statistiques de la fenêtre
        window_min = min(historical_values)
        window_max = max(historical_values)
        window_mean = statistics.mean(historical_values)

        # Normaliser la valeur actuelle
        if window_max == window_min:
            # Pas de variance : retourner 50 (neutre)
            scaled_value = 50.0
        else:
            # MinMaxScaler sur la fenêtre
            scaler = MinMaxScaler(feature_range=self.feature_range)
            scaler.fit(np.array(historical_values).reshape(-1, 1))
            scaled_value = float(
                scaler.transform([[current_value]])[0][0]
            )

        logger.info(
            "Dynamic scaling for %s: raw=%.2f, scaled=%.2f, window=[%.2f, %.2f], mean=%.2f",
            component_name,
            current_value,
            scaled_value,
            window_min,
            window_max,
            window_mean,
        )

        return DynamicScalingResult(
            raw_value=current_value,
            scaled_value=scaled_value,
            window_min=window_min,
            window_max=window_max,
            window_mean=window_mean,
        )

    def _get_historical_values(
        self,
        component_name: str,
        current_date: date,
    ) -> List[float]:
        """
        Récupère les valeurs historiques d'une composante sur la fenêtre glissante.

        Args:
            component_name: Nom de la composante
            current_date: Date de référence

        Returns:
            Liste des valeurs historiques
        """
        cutoff_date = current_date - timedelta(days=self.window_days)

        with SessionLocal() as db:
            records = (
                db.query(IndexScore)
                .filter(IndexScore.as_of >= cutoff_date)
                .filter(IndexScore.as_of <= current_date)
                .order_by(IndexScore.as_of.asc())
                .all()
            )

            # Extraire les valeurs de la composante demandée
            values = []
            for record in records:
                value = getattr(record, component_name, None)
                if value is not None:
                    values.append(float(value))

            return values

    def normalize_all_components(
        self,
        components: dict,
        current_date: Optional[date] = None,
    ) -> dict:
        """
        Normalise toutes les composantes d'un coup.

        Args:
            components: Dict {component_name: raw_value}
            current_date: Date de référence

        Returns:
            Dict {component_name: scaled_value}
        """
        normalized = {}
        for component_name, raw_value in components.items():
            if component_name == "as_of":
                continue
            result = self.normalize_component(component_name, raw_value, current_date)
            normalized[component_name] = result.scaled_value

        return normalized







