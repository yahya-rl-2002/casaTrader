from __future__ import annotations

from typing import Iterable


def ensure_non_empty(collection: Iterable) -> None:
    if not any(True for _ in collection):
        raise ValueError("Collection must not be empty")



