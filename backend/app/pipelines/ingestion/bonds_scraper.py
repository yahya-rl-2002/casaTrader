from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import requests
from bs4 import BeautifulSoup

from app.core.logging import get_logger


logger = get_logger(__name__)


@dataclass(slots=True)
class BondYield:
    as_of: date
    maturity_years: int
    yield_percent: float


class BankAlMaghribScraper:
    BONDS_URL = "https://www.bkam.ma/Taux-indicatifs-du-marche-secondaire"

    def fetch(self) -> list[BondYield]:
        logger.info("Fetching bond yields", extra={"url": self.BONDS_URL})
        response = requests.get(self.BONDS_URL, timeout=30)
        response.raise_for_status()

        return self._parse(response.text)

    def _parse(self, html: str) -> list[BondYield]:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        if table is None:
            raise ValueError("Cannot locate bond yields table")

        yields: list[BondYield] = []
        for row in table.find_all("tr"):
            cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
            if len(cells) < 3:
                continue

            try:
                maturity = int(cells[0].split()[0])
                yield_percent = float(cells[2].replace(",", "."))
            except ValueError:
                logger.warning("Skipping bond row", extra={"row": cells})
                continue

            yields.append(
                BondYield(
                    as_of=date.today(),
                    maturity_years=maturity,
                    yield_percent=yield_percent,
                )
            )

        logger.info("Parsed %s bond yields", len(yields))
        return yields



