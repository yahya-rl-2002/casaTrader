from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

import pandas as pd


@dataclass(slots=True)
class EquityVsBondsScore:
    as_of: date
    relative_return: float
    normalized_score: float


class EquityVsBondsProcessor:
    def __init__(self, window: int = 20) -> None:
        self.window = window

    def compute(
        self,
        masi_returns: Iterable[tuple[date, float]],
        bond_returns: Iterable[tuple[date, float]],
    ) -> EquityVsBondsScore:
        df_masi = pd.DataFrame(masi_returns, columns=["date", "return"])
        df_bond = pd.DataFrame(bond_returns, columns=["date", "return"])

        merged = pd.merge(df_masi, df_bond, on="date", how="inner", suffixes=("_masi", "_bond"))
        merged = merged.sort_values("date")

        merged["relative_return"] = (
            merged["return_masi"].rolling(self.window).mean()
            - merged["return_bond"].rolling(self.window).mean()
        )

        latest = merged.iloc[-1]
        min_val = merged["relative_return"].min()
        max_val = merged["relative_return"].max()
        normalized = 50.0
        if max_val > min_val:
            normalized = (latest["relative_return"] - min_val) / (max_val - min_val) * 100

        return EquityVsBondsScore(
            as_of=latest["date"],
            relative_return=float(latest["relative_return"]),
            normalized_score=float(normalized),
        )



