from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Mapping


@dataclass(slots=True)
class ComponentAggregate:
    as_of: datetime
    components: Mapping[str, float]
    composite_score: float


class IndexAggregator:
    DEFAULT_WEIGHTS = {
        "momentum": 0.20,
        "price_strength": 0.15,
        "volume": 0.15,
        "volatility": 0.20,
        "equity_vs_bonds": 0.15,
        "media_sentiment": 0.15,
    }

    def __init__(self, weights: Mapping[str, float] | None = None) -> None:
        self.weights = dict(weights or self.DEFAULT_WEIGHTS)

    def aggregate(self, scores: Mapping[str, float], as_of: date | datetime) -> ComponentAggregate:
        total_weight = sum(self.weights.values())
        if not total_weight:
            raise ValueError("Total weight cannot be zero")

        composite = 0.0
        for name, weight in self.weights.items():
            value = scores.get(name)
            if value is None:
                raise ValueError(f"Missing component score: {name}")
            composite += value * weight

        composite /= total_weight

        return ComponentAggregate(
            as_of=as_of if isinstance(as_of, datetime) else datetime.combine(as_of, datetime.min.time()),
            components=scores,
            composite_score=composite,
        )



