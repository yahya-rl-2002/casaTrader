from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd


@dataclass(slots=True)
class PriceStrengthScore:
    as_of: date
    ratio: float
    normalized_score: float


class PriceStrengthProcessor:
    def compute(self, highs: int, lows: int, as_of: date) -> PriceStrengthScore:
        denominator = highs + lows
        ratio = 0.0
        if denominator:
            ratio = (highs - lows) / denominator

        normalized = (ratio + 1) / 2 * 100
        return PriceStrengthScore(
            as_of=as_of,
            ratio=ratio,
            normalized_score=normalized,
        )

    @staticmethod
    def normalize_series(series: pd.Series) -> pd.Series:
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return pd.Series([50.0] * len(series), index=series.index)
        return (series - min_val) / (max_val - min_val) * 100



