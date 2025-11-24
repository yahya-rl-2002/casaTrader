from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

import pandas as pd


@dataclass(slots=True)
class VolumeScore:
    as_of: date
    volume_ratio: float
    bullish_share: float
    normalized_score: float


class VolumeProcessor:
    def __init__(self, window: int = 50) -> None:
        self.window = window

    def compute(
        self,
        volume_series: Iterable[tuple[date, float, bool]],
    ) -> VolumeScore:
        df = pd.DataFrame(volume_series, columns=["date", "volume", "is_bullish"])
        df = df.sort_values("date")
        df["ma_volume"] = df["volume"].rolling(window=self.window).mean()
        df["volume_ratio"] = df["volume"] / df["ma_volume"]

        latest = df.iloc[-1]
        bullish_volume = df[df["is_bullish"]]["volume"].sum()
        total_volume = df["volume"].sum()
        bullish_share = bullish_volume / total_volume if total_volume else 0.5

        normalized = (latest["volume_ratio"] / df["volume_ratio"].max()) * 50
        normalized += bullish_share * 50

        return VolumeScore(
            as_of=latest["date"],
            volume_ratio=float(latest["volume_ratio"]),
            bullish_share=float(bullish_share),
            normalized_score=float(min(normalized, 100.0)),
        )



