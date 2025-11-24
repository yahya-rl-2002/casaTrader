from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.preprocessing import MinMaxScaler

from app.core.config import settings


@dataclass(slots=True)
class ScalingResult:
    value: float
    scaled: float


class ScalingService:
    def __init__(self, name: str, feature_range: tuple[float, float] = (0.0, 100.0)) -> None:
        self.name = name
        self.feature_range = feature_range
        self.scaler_path = Path(settings.models_dir) / f"{name}_scaler.pkl"
        self.scaler = self._load_scaler()

    def _load_scaler(self) -> MinMaxScaler:
        if self.scaler_path.exists():
            return joblib.load(self.scaler_path)

        scaler = MinMaxScaler(feature_range=self.feature_range)
        joblib.dump(scaler, self.scaler_path)
        return scaler

    def transform(self, value: float) -> ScalingResult:
        scaled_value = float(self.scaler.transform([[value]])[0][0])
        return ScalingResult(value=value, scaled=scaled_value)

    def partial_fit(self, value: float) -> None:
        self.scaler.partial_fit([[value]])
        joblib.dump(self.scaler, self.scaler_path)



