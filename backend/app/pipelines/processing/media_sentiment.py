from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

import pandas as pd


@dataclass(slots=True)
class MediaSentimentScore:
    as_of: datetime
    positive_ratio: float
    neutral_ratio: float
    negative_ratio: float
    normalized_score: float


class MediaSentimentProcessor:
    def compute(self, sentiments: Iterable[tuple[datetime, float]]) -> MediaSentimentScore:
        df = pd.DataFrame(sentiments, columns=["timestamp", "polarity"])
        if df.empty:
            return MediaSentimentScore(
                as_of=datetime.utcnow(),
                positive_ratio=0.0,
                neutral_ratio=1.0,
                negative_ratio=0.0,
                normalized_score=50.0,
            )

        df["category"] = pd.cut(
            df["polarity"],
            bins=[-1.0, -0.05, 0.05, 1.0],
            labels=["negative", "neutral", "positive"],
        )

        counts = df["category"].value_counts(normalize=True)

        positive = float(counts.get("positive", 0.0))
        neutral = float(counts.get("neutral", 0.0))
        negative = float(counts.get("negative", 0.0))

        normalized = positive * 100 + neutral * 50

        latest_timestamp = df["timestamp"].max()

        return MediaSentimentScore(
            as_of=latest_timestamp,
            positive_ratio=positive,
            neutral_ratio=neutral,
            negative_ratio=negative,
            normalized_score=normalized,
        )



