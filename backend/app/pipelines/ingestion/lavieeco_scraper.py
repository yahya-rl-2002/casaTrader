from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
import time
from urllib.parse import urljoin
import re

import requests
from bs4 import BeautifulSoup

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class LaVieEcoArticle:
    title: str
    summary: str
    url: str
    published_at: Optional[datetime]
    content: str = ""


class LaVieEcoScraper:
    BASE_URL = "https://www.lavieeco.com"
    SECTION_URLS = [
        f"{BASE_URL}/economie/",
        f"{BASE_URL}/affaires/",
    ]

    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]

    def __init__(self, delay_between_requests: float = 1.5):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.USER_AGENTS[0],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
        })
        self.delay = delay_between_requests
        self.last_request_ts = 0.0

    def _respect_rate_limit(self):
        elapsed = time.time() - self.last_request_ts
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_ts = time.time()

    def fetch_articles(self, max_articles: int = 10) -> List[LaVieEcoArticle]:
        articles: List[LaVieEcoArticle] = []

        per_section = max(1, max_articles // max(1, len(self.SECTION_URLS)))

        for url in self.SECTION_URLS:
            if len(articles) >= max_articles:
                break

            try:
                self._respect_rate_limit()
                response = self.session.get(url, timeout=20)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")
                article_containers = soup.select(
                    "article, .article, .post, .post-item, .jeg_post, .jeg_block_container"
                )

                count_section = 0
                for container in article_containers:
                    if len(articles) >= max_articles or count_section >= per_section:
                        break
                    article = self._parse_article(container)
                    if article:
                        articles.append(article)
                        count_section += 1

                logger.info("LaVieEcoScraper fetched %s articles from %s", len(articles), url)

            except Exception as exc:  # noqa: BLE001
                logger.error("Error scraping La Vie Éco (%s): %s", url, exc, exc_info=True)
                continue

        return articles

    def _parse_article(self, container) -> Optional[LaVieEcoArticle]:
        try:
            title_elem = container.select_one("h2 a, h3 a, .title a")
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)
            if len(title) < 10:
                return None

            url = title_elem.get("href")
            if not url:
                return None
            url = urljoin(self.BASE_URL, url)

            summary_elem = container.select_one("p, .excerpt")
            summary = summary_elem.get_text(strip=True) if summary_elem else title

            time_elem = container.find("time")
            published_at = None
            if time_elem and time_elem.get("datetime"):
                try:
                    dt = datetime.fromisoformat(time_elem["datetime"].replace('Z', '+00:00'))
                    # Normaliser: enlever le timezone
                    if dt.tzinfo:
                        published_at = dt.replace(tzinfo=None)
                    else:
                        published_at = dt
                except ValueError:
                    published_at = datetime.now() - timedelta(hours=3)
            else:
                text = container.get_text(" ", strip=True)
                match = None
                if text:
                    match = re.search(r"(\d+)\s+heure", text, re.IGNORECASE)
                if match:
                    published_at = datetime.now() - timedelta(hours=int(match.group(1)))
                else:
                    if text:
                        match = re.search(r"(\d+)\s+jour", text, re.IGNORECASE)
                    if match:
                        published_at = datetime.now() - timedelta(days=int(match.group(1)))
                    else:
                        published_at = datetime.now() - timedelta(hours=3)

            return LaVieEcoArticle(
                title=title,
                summary=summary,
                url=url,
                published_at=published_at,
                content=summary,
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug("Error parsing La Vie Éco article: %s", exc)
            return None

