from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(slots=True)
class VolatilityScore:
    as_of: date
    annualized_vol: float
    normalized_score: float


class VolatilityProcessor:
    def __init__(self, window: int = 30) -> None:
        self.window = window

    def compute(self, returns_series: Iterable[tuple[date, float]]) -> VolatilityScore:
        df = pd.DataFrame(returns_series, columns=["date", "returns"])
        df = df.sort_values("date")

        df["vol"] = df["returns"].rolling(window=self.window).std()
        df["annualized_vol"] = df["vol"] * np.sqrt(252)

        latest = df.iloc[-1]
        mean_vol = df["annualized_vol"].mean()

        # Higher volatility = lower score (fear)
        normalized = 100 - (latest["annualized_vol"] / mean_vol * 100) if mean_vol else 50
        normalized = float(np.clip(normalized, 0, 100))

        return VolatilityScore(
            as_of=latest["date"],
            annualized_vol=float(latest["annualized_vol"]),
            normalized_score=normalized,
        )



