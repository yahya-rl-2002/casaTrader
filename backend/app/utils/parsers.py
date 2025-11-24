from __future__ import annotations

from datetime import datetime


def parse_float(value: str) -> float:
    cleaned = value.replace(" ", "").replace(",", ".")
    return float(cleaned)


def parse_int(value: str) -> int:
    cleaned = value.replace(" ", "").replace(",", "")
    return int(cleaned)


def parse_datetime(value: str, fmt: str = "%d/%m/%Y %H:%M") -> datetime:
    return datetime.strptime(value, fmt)



