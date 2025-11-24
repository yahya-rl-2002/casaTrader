from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

import pandas as pd


@dataclass(slots=True)
class MomentumScore:
    as_of: date
    raw_value: float
    normalized_score: float


class MomentumProcessor:
    def __init__(self, window: int = 125, lookback: int = 252) -> None:
        self.window = window
        self.lookback = lookback

    def compute(self, masi_series: Iterable[tuple[date, float]]) -> MomentumScore:
        df = pd.DataFrame(masi_series, columns=["date", "close"])
        df = df.sort_values("date")
        df["sma"] = df["close"].rolling(window=self.window).mean()
        df["momentum"] = (df["close"] - df["sma"]) / df["sma"] * 100

        latest = df.iloc[-1]
        window_df = df.tail(self.lookback)
        min_val = window_df["momentum"].min()
        max_val = window_df["momentum"].max()

        normalized = 50.0
        if max_val > min_val:
            normalized = (latest["momentum"] - min_val) / (max_val - min_val) * 100

        return MomentumScore(
            as_of=latest["date"],
            raw_value=float(latest["momentum"]),
            normalized_score=float(normalized),
        )



