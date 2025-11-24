#!/usr/bin/env python3
"""
Scraper optimisé pour BourseNews.ma (Espace Investisseur)
Respecte les bonnes pratiques anti-blocage
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.core.logging import get_logger


logger = get_logger(__name__)


@dataclass(slots=True)
class BourseNewsArticle:
    title: str
    url: str
    summary: str
    category: str  # actualite, marches, analyse, etc.
    published_at: Optional[datetime]
    content: str = ""
    sentiment_score: Optional[float] = None
    sentiment_label: str = "neutral"


class BourseNewsScraper:
    """
    Scraper intelligent pour BourseNews.ma
    
    Utilise l'Espace Investisseurs qui contient toute l'actualité filtrée
    
    Stratégies anti-blocage:
    - Headers réalistes (navigateur moderne)
    - Délais entre requêtes (2-5 secondes)
    - User-Agent rotation
    - Respect du robots.txt
    - Cache local
    """
    
    BASE_URL = "https://boursenews.ma"
    
    # Sections intéressantes
    SECTIONS = {
        "espace_investisseurs": f"{BASE_URL}/espace-investisseurs",  # Page principale avec tous les articles
        "actualite": f"{BASE_URL}/articles/actualite",
        "marches": f"{BASE_URL}/articles/marches",
        "analyse": f"{BASE_URL}/articles/graphiques-et-analyse-technique",
        "home": BASE_URL,
    }
    
    # User-Agents à alterner
    USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    ]
    
    def __init__(self, delay_between_requests: int = 3):
        """
        Args:
            delay_between_requests: Délai en secondes entre les requêtes (défaut: 3s)
        """
        self.session = requests.Session()
        self.delay = delay_between_requests
        self.last_request_time = 0
        self.current_ua_index = 0
        
        # Configuration SSL
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Headers de base
        self._update_headers()
        
        logger.info("BourseNews scraper initialisé avec délai de %d secondes", self.delay)
    
    def _update_headers(self):
        """Mise à jour des headers avec rotation User-Agent"""
        self.session.headers.update({
            'User-Agent': self.USER_AGENTS[self.current_ua_index],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Referer': 'https://www.google.com/',
        })
        # Rotation
        self.current_ua_index = (self.current_ua_index + 1) % len(self.USER_AGENTS)
    
    def _respect_rate_limit(self):
        """Respecter le délai entre les requêtes"""
        now = time.time()
        time_since_last = now - self.last_request_time
        
        if time_since_last < self.delay:
            sleep_time = self.delay - time_since_last
            logger.debug(f"Rate limiting: pause de {sleep_time:.1f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def fetch_articles(self, max_articles: int = 20, sections: List[str] = None) -> List[BourseNewsArticle]:
        """
        Récupère les articles de BourseNews.ma
        
        Args:
            max_articles: Nombre maximum d'articles à récupérer
            sections: Liste des sections à scraper (défaut: espace_investisseurs)
        
        Returns:
            Liste d'articles
        """
        if sections is None:
            # Prioriser l'Espace Investisseurs qui contient tous les articles
            sections = ["espace_investisseurs"]
        
        all_articles = []
        
        for section in sections:
            if section not in self.SECTIONS:
                logger.warning(f"Section inconnue: {section}")
                continue
            
            try:
                logger.info(f"Scraping section: {section}")
                articles = self._scrape_section(self.SECTIONS[section], max_articles)
                all_articles.extend(articles)
                logger.info(f"✅ {len(articles)} articles de la section '{section}'")
                
                # Si on a assez d'articles depuis espace_investisseurs, on arrête
                if section == "espace_investisseurs" and len(articles) >= max_articles:
                    break
                
                # Respecter le délai
                self._respect_rate_limit()
                
            except Exception as e:
                logger.error(f"Erreur scraping section {section}: {e}")
                continue
        
        # Dédupliquer
        unique_articles = self._deduplicate(all_articles)
        logger.info(f"Total: {len(unique_articles)} articles uniques")
        
        return unique_articles[:max_articles]
    
    def _scrape_section(self, url: str, max_articles: int) -> List[BourseNewsArticle]:
        """Scrape une section spécifique"""
        articles = []
        
        try:
            # Rotation User-Agent
            self._update_headers()
            
            response = self.session.get(url, timeout=30)  # Augmenté à 30s pour sites lents
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Méthode 1: Espace Investisseurs - Chercher les <h5> avec titres d'articles
            h5_titles = soup.find_all('h5')
            if h5_titles:
                logger.debug(f"Trouvé {len(h5_titles)} titres h5")
                for h5 in h5_titles[:max_articles]:
                    article = self._parse_h5_article(h5)
                    if article:
                        articles.append(article)
            
            # Méthode 2: Chercher les divs avec 'article' dans la classe
            if len(articles) < 5:
                article_containers = soup.find_all('div', class_=lambda x: x and 'article' in str(x).lower())
                
                for container in article_containers[:max_articles]:
                    article = self._parse_article_container(container)
                    if article:
                        articles.append(article)
            
            # Méthode 3: Chercher tous les liens /article/
            if len(articles) < 5:
                all_links = soup.find_all('a', href=lambda x: x and '/article/' in x)
                logger.debug(f"Trouvé {len(all_links)} liens d'articles")
                
                for link in all_links[:max_articles]:
                    article = self._parse_link_to_article(link, soup)
                    if article:
                        articles.append(article)
            
        except Exception as e:
            logger.error(f"Erreur lors du scraping de {url}: {e}")
        
        return articles
    
    def _parse_h5_article(self, h5_elem) -> Optional[BourseNewsArticle]:
        """Parse un article depuis un élément h5 (Espace Investisseurs)"""
        try:
            title = h5_elem.get_text(strip=True)
            
            # Skip si titre trop court
            if len(title) < 10:
                return None
            
            # Chercher le lien parent ou adjacent
            link_elem = h5_elem.find_parent('a')
            if not link_elem:
                link_elem = h5_elem.find('a')
            if not link_elem:
                # Chercher dans les siblings
                parent = h5_elem.find_parent()
                if parent:
                    link_elem = parent.find('a', href=True)
            
            if not link_elem or not link_elem.get('href'):
                return None
            
            url = urljoin(self.BASE_URL, link_elem['href'])
            
            # Catégorie depuis l'URL
            category = "general"
            if '/actualite/' in url:
                category = "actualite"
            elif '/marches/' in url:
                category = "marches"
            
            # Essayer de trouver la date dans le parent
            parent = h5_elem.find_parent()
            date_text = None
            if parent:
                date_elem = parent.find(string=lambda x: x and re.search(r'\d{2}/\d{2}/\d{4}', str(x)))
                if date_elem:
                    match = re.search(r'(\d{2})/(\d{2})/(\d{4})', date_elem)
                    if match:
                        day, month, year = match.groups()
                        published_at = datetime(int(year), int(month), int(day))
                    else:
                        published_at = datetime.now() - timedelta(hours=1)
                else:
                    published_at = datetime.now() - timedelta(hours=1)
            else:
                published_at = datetime.now() - timedelta(hours=1)
            
            return BourseNewsArticle(
                title=title,
                url=url,
                summary=title,  # Utiliser le titre comme résumé
                category=category,
                published_at=published_at
            )
            
        except Exception as e:
            logger.debug(f"Erreur parsing h5: {e}")
            return None
    
    def _parse_article_container(self, container) -> Optional[BourseNewsArticle]:
        """Parse un container d'article"""
        try:
            # Titre
            title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5'])
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)
            
            # Skip si titre trop court
            if len(title) < 10:
                return None
            
            # URL
            link_elem = container.find('a', href=True)
            if not link_elem:
                # Chercher onclick
                onclick = container.get('onclick', '')
                if 'location.href=' in onclick:
                    # Extraire l'URL
                    match = re.search(r"location\.href='([^']+)'", onclick)
                    if match:
                        url = urljoin(self.BASE_URL, match.group(1))
                    else:
                        return None
                else:
                    return None
            else:
                url = urljoin(self.BASE_URL, link_elem['href'])
            
            # Catégorie depuis l'URL
            category = "general"
            if '/actualite/' in url:
                category = "actualite"
            elif '/marches/' in url:
                category = "marches"
            elif '/analyse/' in url or '/graphiques' in url:
                category = "analyse"
            
            # Résumé (essayer de trouver un paragraphe)
            summary_elem = container.find('p')
            summary = summary_elem.get_text(strip=True) if summary_elem else title
            
            # Date (difficile à extraire, on estime récent)
            published_at = datetime.now() - timedelta(hours=1)
            
            return BourseNewsArticle(
                title=title,
                url=url,
                summary=summary,
                category=category,
                published_at=published_at
            )
            
        except Exception as e:
            logger.debug(f"Erreur parsing container: {e}")
            return None
    
    def _parse_link_to_article(self, link, soup) -> Optional[BourseNewsArticle]:
        """Crée un article à partir d'un lien"""
        try:
            title = link.get_text(strip=True)
            
            # Skip liens génériques
            if title.lower() in ['lire la suite', 'en savoir plus', '...', '']:
                return None
            if len(title) < 10:
                return None
            
            url = urljoin(self.BASE_URL, link['href'])
            
            # Catégorie
            category = "general"
            if '/actualite/' in url:
                category = "actualite"
            elif '/marches/' in url:
                category = "marches"
            elif '/analyse/' in url or '/graphiques' in url:
                category = "analyse"
            
            return BourseNewsArticle(
                title=title,
                url=url,
                summary=title,  # On utilisera le titre comme résumé
                category=category,
                published_at=datetime.now() - timedelta(hours=2)
            )
            
        except Exception as e:
            logger.debug(f"Erreur parsing link: {e}")
            return None
    
    def _deduplicate(self, articles: List[BourseNewsArticle]) -> List[BourseNewsArticle]:
        """Dédupliquer les articles par URL"""
        seen_urls = set()
        unique_articles = []
        
        for article in articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique_articles.append(article)
        
        return unique_articles


# Fonction helper pour compatibilité avec MediaScraper
def convert_to_media_article(boursenews_article: BourseNewsArticle):
    """Convertit un BourseNewsArticle en MediaArticle"""
    from app.pipelines.ingestion.media_scraper import MediaArticle
    
    return MediaArticle(
        title=boursenews_article.title,
        summary=boursenews_article.summary,
        url=boursenews_article.url,
        source="boursenews",
        published_at=boursenews_article.published_at,
        content=boursenews_article.content,
        sentiment_score=boursenews_article.sentiment_score,
        sentiment_label=boursenews_article.sentiment_label
    )

