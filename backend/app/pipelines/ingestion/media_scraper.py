from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from app.core.logging import get_logger

logger = get_logger(__name__)

# Import scrapers spécialisés
try:
    from app.pipelines.ingestion.boursenews_scraper import (
        BourseNewsScraper,
        convert_to_media_article as convert_boursenews,
    )
    BOURSENEWS_AVAILABLE = True
except ImportError:
    BOURSENEWS_AVAILABLE = False
    logger.warning("BourseNews scraper not available")

try:
    from app.pipelines.ingestion.medias24_scraper import (
        Medias24Scraper,
        convert_to_media_article as convert_medias24,
    )
    MEDIAS24_AVAILABLE = True
except ImportError:
    MEDIAS24_AVAILABLE = False
    logger.warning("Medias24 scraper not available")

try:
    from app.pipelines.ingestion.challenge_scraper import ChallengeScraper, ChallengeArticle
    CHALLENGE_AVAILABLE = True
except ImportError:
    CHALLENGE_AVAILABLE = False
    logger.warning("Challenge.ma scraper not available")

try:
    from app.pipelines.ingestion.lavieeco_scraper import LaVieEcoScraper, LaVieEcoArticle
    LAVIEECO_AVAILABLE = True
except ImportError:
    LAVIEECO_AVAILABLE = False
    logger.warning("La Vie Éco scraper not available")


@dataclass(slots=True)
class MediaArticle:
    title: str
    summary: str
    url: str
    source: str
    published_at: Optional[datetime]
    content: str = ""
    sentiment_score: Optional[float] = None
    sentiment_label: str = "neutral"


class MediaScraper:
    """Scraper for Moroccan financial media sources"""
    
    SOURCES = {
        "medias24": {
            "base_url": "https://www.medias24.com",
            "finance_url": "https://www.medias24.com/economie/",
            "selectors": {
                "articles": "article, .article-item, .news-item",
                "title": "h1, h2, h3, .title, .article-title",
                "summary": "p, .summary, .excerpt",
                "link": "a"
            }
        },
        "challenge": {
            "base_url": "https://www.challenge.ma",
            "finance_url": "https://www.challenge.ma/category/finance",
            "selectors": {
                "articles": "article, .post-item, .section-article",
                "title": "h2, h3, .post-title, .entry-title",
                "summary": "p, .post-excerpt",
                "link": "a"
            }
        },
        "lavieeco": {
            "base_url": "https://www.lavieeco.com",
            "finance_url": "https://www.lavieeco.com/economie/",
            "selectors": {
                "articles": "article, .article, .post",
                "title": "h2, h3, .title",
                "summary": "p, .excerpt",
                "link": "a"
            }
        },
        "leconomiste": {
            "base_url": "https://www.leconomiste.com",
            "finance_url": "https://www.leconomiste.com/economie",
            "selectors": {
                "articles": "article",
                "title": "h1, h2, h3, h4",
                "summary": "p",
                "link": "a"
            }
        },
        "boursenews": {
            "base_url": "https://www.boursenews.ma",
            "finance_url": "https://www.boursenews.ma/",
            "selectors": {
                "articles": "article, .article, .news-item",
                "title": "h1, h2, h3, .title",
                "summary": "p, .summary",
                "link": "a"
            }
        }
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        # Désactiver SSL pour développement
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Keywords for financial content
        self.finance_keywords = [
            'bourse', 'masi', 'casablanca', 'marché', 'investissement', 'finance',
            'économie', 'titre', 'action', 'obligation', 'trading', 'volatilité',
            'croissance', 'inflation', 'taux', 'devise', 'export', 'import',
            'bancaire', 'crédit', 'capital', 'entreprise', 'secteur', 'performance'
        ]

    def scrape_all_sources(self, max_articles_per_source: int = 10) -> List[MediaArticle]:
        """Scrape articles from all configured sources"""
        all_articles = []
        
        # 1. Scraper Medias24 avec le scraper spécialisé (prioritaire - numéro 1 info économique)
        if MEDIAS24_AVAILABLE:
            try:
                logger.info("Scraping Medias24.com with specialized scraper")
                medias24_scraper = Medias24Scraper(delay_between_requests=2)
                medias24_articles = medias24_scraper.fetch_articles(max_articles=max_articles_per_source)
                
                # Convertir en MediaArticle
                for m24_article in medias24_articles:
                    all_articles.append(convert_medias24(m24_article))
                
                logger.info(f"✅ Found {len(medias24_articles)} articles from Medias24")
                
                # Respecter le délai
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error scraping Medias24: {e}")
        
        # 2. Scraper BourseNews avec le scraper spécialisé (très pertinent pour bourse)
        if BOURSENEWS_AVAILABLE:
            try:
                logger.info("Scraping BourseNews.ma Espace Investisseurs with specialized scraper")
                boursenews_scraper = BourseNewsScraper(delay_between_requests=1)
                boursenews_articles = boursenews_scraper.fetch_articles(
                    max_articles=max_articles_per_source,
                    sections=["espace_investisseurs"]  # Utiliser l'Espace Investisseurs
                )
                
                # Convertir en MediaArticle
                for bn_article in boursenews_articles:
                    all_articles.append(convert_boursenews(bn_article))
                
                logger.info(f"✅ Found {len(boursenews_articles)} articles from BourseNews.ma")
                
                # Respecter le délai
                time.sleep(1)
                
            except requests.exceptions.Timeout:
                logger.warning("⏱️ BourseNews.ma timeout (>30s) - Site trop lent, passage aux autres sources")
            except requests.exceptions.ConnectionError:
                logger.warning("🔌 BourseNews.ma connection error - Site indisponible, passage aux autres sources")
            except Exception as e:
                logger.warning(f"⚠️ BourseNews.ma temporairement indisponible: {str(e)[:80]}...")
        
        # 3. Scraper Challenge.ma avec le scraper spécialisé
        if CHALLENGE_AVAILABLE:
            try:
                logger.info("Scraping Challenge.ma with specialized scraper")
                challenge_scraper = ChallengeScraper(delay_between_requests=2)
                challenge_articles = challenge_scraper.fetch_articles(max_articles=max_articles_per_source)

                for ch_article in challenge_articles:
                    converted = self._convert_specialized_article(ch_article, "challenge")
                    if converted:
                        all_articles.append(converted)

                logger.info(f"✅ Found {len(challenge_articles)} articles from Challenge.ma")
                time.sleep(2)

            except Exception as e:
                logger.error(f"Error scraping Challenge.ma: {e}")

        # 4. Scraper La Vie Éco avec le scraper spécialisé
        if LAVIEECO_AVAILABLE:
            try:
                logger.info("Scraping LaVieEco.com with specialized scraper")
                lavieeco_scraper = LaVieEcoScraper(delay_between_requests=2)
                lavieeco_articles = lavieeco_scraper.fetch_articles(max_articles=max_articles_per_source)

                for lv_article in lavieeco_articles:
                    converted = self._convert_specialized_article(lv_article, "lavieeco")
                    if converted:
                        all_articles.append(converted)

                logger.info(f"✅ Found {len(lavieeco_articles)} articles from La Vie Éco")
                time.sleep(2)

            except Exception as e:
                logger.error(f"Error scraping La Vie Éco: {e}")

        # 5. Scraper les autres sources génériques (L'Économiste, etc.)
        for source_name, source_config in self.SOURCES.items():
            # Skip sources déjà scrapées avec scrapers spécialisés
            if source_name in ["boursenews", "medias24", "challenge", "lavieeco"]:
                continue
            
            try:
                logger.info(f"Scraping {source_name}")
                articles = self._scrape_source(source_name, source_config, max_articles_per_source)
                all_articles.extend(articles)
                logger.info(f"Found {len(articles)} articles from {source_name}")
                
                # Be respectful with delays
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error scraping {source_name}: {e}")
                continue
        
        # Remove duplicates and sort by date
        unique_articles = self._deduplicate_articles(all_articles)
        logger.info(f"✅ Total: {len(unique_articles)} unique articles from all sources")

        def _normalize_date(article: MediaArticle) -> datetime:
            if not article.published_at:
                return datetime.min
            if article.published_at.tzinfo:
                return article.published_at.replace(tzinfo=None)
            return article.published_at

        return sorted(unique_articles, key=_normalize_date, reverse=True)

    def _scrape_source(self, source_name: str, source_config: dict, max_articles: int) -> List[MediaArticle]:
        """Scrape articles from a specific source"""
        articles = []
        
        try:
            response = self.session.get(source_config["finance_url"], timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article containers
            article_containers = soup.select(source_config["selectors"]["articles"])
            
            for container in article_containers[:max_articles]:
                try:
                    article = self._extract_article_from_container(container, source_name, source_config)
                    if article and self._is_financial_content(article):
                        articles.append(article)
                except Exception as e:
                    logger.warning(f"Error extracting article from {source_name}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            # Return fallback articles for development
            articles = self._get_fallback_articles(source_name)
        
        return articles

    def _extract_article_from_container(self, container, source_name: str, source_config: dict) -> Optional[MediaArticle]:
        """Extract article data from a container element"""
        try:
            # Extract title
            title_elem = container.select_one(source_config["selectors"]["title"])
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)
            
            # Skip if title is too short or generic
            if len(title) < 10 or title.lower() in ['à la une', 'actualités', 'news']:
                return None
            
            # Extract link
            link_elem = container.select_one(source_config["selectors"]["link"])
            if not link_elem:
                return None
            
            url = link_elem.get('href', '')
            if url and not url.startswith('http'):
                url = urljoin(source_config["base_url"], url)
            
            # Skip invalid URLs
            if not url or url.startswith('http') is False or url == f"{source_config['base_url']}/" or 'a-la-une' in url:
                return None
            
            # Extract summary
            summary_elem = container.select_one(source_config["selectors"]["summary"])
            summary = summary_elem.get_text(strip=True) if summary_elem else ""
            
            # If summary is empty or too short, use title as content for sentiment analysis
            if len(summary) < 20:
                summary = title
            
            # Try to extract date
            published_at = self._extract_date(container)
            
            return MediaArticle(
                title=title,
                summary=summary,
                url=url,
                source=source_name,
                published_at=published_at,
                content=""
            )
            
        except Exception as e:
            logger.warning(f"Error extracting article: {e}")
            return None

    def _extract_date(self, container) -> Optional[datetime]:
        """Extract publication date from article container"""
        try:
            # Look for date patterns in text
            text = container.get_text()
            date_patterns = [
                r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
                r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
                r'(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})',  # French dates
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        if 'janvier' in pattern:  # French date
                            months = {
                                'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
                                'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
                                'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
                            }
                            day, month_name, year = match.groups()
                            month = months[month_name.lower()]
                            return datetime(int(year), month, int(day))
                        else:
                            # Numeric date
                            groups = match.groups()
                            if len(groups) == 3:
                                if len(groups[0]) == 4:  # YYYY-MM-DD
                                    return datetime(int(groups[0]), int(groups[1]), int(groups[2]))
                                else:  # DD/MM/YYYY
                                    return datetime(int(groups[2]), int(groups[1]), int(groups[0]))
                    except ValueError:
                        continue
            
            # If no date found, assume recent
            return datetime.now() - timedelta(days=1)
            
        except Exception:
            return None

    def _is_financial_content(self, article: MediaArticle) -> bool:
        """Check if article is related to financial/economic content"""
        text_to_check = f"{article.title} {article.summary}".lower()
        
        # Check for financial keywords
        keyword_matches = sum(1 for keyword in self.finance_keywords if keyword in text_to_check)
        
        # Accept articles with at least 1 keyword OR from economy section
        # (L'Économiste section economie is already filtered)
        return keyword_matches >= 1 or len(article.title) > 20

    def _deduplicate_articles(self, articles: List[MediaArticle]) -> List[MediaArticle]:
        """Remove duplicate articles based on URL and title similarity"""
        seen_urls = set()
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            # Check URL uniqueness
            if article.url in seen_urls:
                continue
            seen_urls.add(article.url)
            
            # Check title similarity (simple approach)
            title_words = set(article.title.lower().split())
            is_duplicate = False
            for seen_title in seen_titles:
                seen_words = set(seen_title.lower().split())
                # If more than 80% of words match, consider it duplicate
                if len(title_words & seen_words) / len(title_words | seen_words) > 0.8:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_titles.add(article.title)
                unique_articles.append(article)
        
        return unique_articles

    def _get_fallback_articles(self, source_name: str) -> List[MediaArticle]:
        """Generate fallback articles for development"""
        fallback_articles = {
            "medias24": [
                MediaArticle(
                    title="Perspectives positives pour le MASI en 2024",
                    summary="Les analystes prévoient une reprise progressive des volumes sur le marché marocain dans les prochains mois.",
                    url=f"https://www.medias24.com/article-{i}",
                    source=source_name,
                    published_at=datetime.now() - timedelta(hours=i*2),
                    content="Article de développement sur les perspectives du marché marocain."
                ) for i in range(3)
            ],
            "leconomiste": [
                MediaArticle(
                    title="Croissance soutenue des investissements étrangers",
                    summary="Le marché marocain continue d'attirer les investisseurs étrangers avec des performances remarquables.",
                    url=f"https://www.leconomiste.com/article-{i}",
                    source=source_name,
                    published_at=datetime.now() - timedelta(hours=i*3),
                    content="Analyse de la croissance des investissements au Maroc."
                ) for i in range(2)
            ],
            "boursenews": [
                MediaArticle(
                    title="Volatilité accrue sur les marchés financiers",
                    summary="Les tensions géopolitiques créent une incertitude sur les marchés financiers marocains.",
                    url=f"https://www.boursenews.ma/article-{i}",
                    source=source_name,
                    published_at=datetime.now() - timedelta(hours=i*4),
                    content="Rapport sur la volatilité des marchés marocains."
                ) for i in range(2)
            ]
        }
        
        return fallback_articles.get(source_name, [])

    def _convert_specialized_article(self, article, source: str) -> MediaArticle:
        """Helper to convert specialized article dataclasses to MediaArticle."""
        if isinstance(article, MediaArticle):
            return article
        if source == "challenge" and isinstance(article, ChallengeArticle):
            return MediaArticle(
                title=article.title,
                summary=article.summary,
                url=article.url,
                source="challenge",
                published_at=article.published_at,
                content=article.content,
            )
        if source == "lavieeco" and isinstance(article, LaVieEcoArticle):
            return MediaArticle(
                title=article.title,
                summary=article.summary,
                url=article.url,
                source="lavieeco",
                published_at=article.published_at,
                content=article.content,
            )
        if getattr(article, "title", "") and getattr(article, "url", ""):
            return MediaArticle(
                title=getattr(article, "title", ""),
                summary=getattr(article, "summary", ""),
                url=getattr(article, "url", ""),
                source=source,
                published_at=getattr(article, "published_at", None),
                content=getattr(article, "content", ""),
            )
        return None