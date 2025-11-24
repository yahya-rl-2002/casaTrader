from __future__ import annotations

from typing import Any, Mapping

import requests

from app.core.logging import get_logger


logger = get_logger(__name__)


def get(url: str, headers: Mapping[str, str] | None = None, timeout: int = 30) -> requests.Response:
    logger.debug("HTTP GET", extra={"url": url})
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response



