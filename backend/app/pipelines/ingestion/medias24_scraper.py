#!/usr/bin/env python3
"""
Scraper optimisé pour Medias24.com
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

# Essayer d'importer cloudscraper pour contourner les protections anti-bot
try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False
    cloudscraper = None

from app.core.logging import get_logger


logger = get_logger(__name__)


@dataclass(slots=True)
class Medias24Article:
    title: str
    url: str
    summary: str
    published_at: Optional[datetime]
    content: str = ""
    sentiment_score: Optional[float] = None
    sentiment_label: str = "neutral"


class Medias24Scraper:
    """
    Scraper optimisé pour Medias24.com
    
    Medias24 est le numéro 1 de l'information économique marocaine
    """
    
    BASE_URL = "https://medias24.com"
    
    # User-Agents à alterner pour éviter la détection
    USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    
    def __init__(self, delay_between_requests: int = 3, use_cloudscraper: bool = True, use_selenium: bool = False):
        """
        Args:
            delay_between_requests: Délai en secondes entre les requêtes (augmenté à 3s par défaut)
            use_cloudscraper: Utiliser cloudscraper pour contourner les protections anti-bot
            use_selenium: Utiliser Selenium (navigateur réel) si cloudscraper échoue
        """
        self.delay = delay_between_requests
        self.last_request_time = 0
        self.current_ua_index = 0
        self.use_cloudscraper = use_cloudscraper and CLOUDSCRAPER_AVAILABLE
        self.use_selenium = use_selenium
        
        # Vérifier si Selenium est disponible
        try:
            from app.pipelines.ingestion.selenium_scraper import SeleniumScraper, SELENIUM_AVAILABLE
            self.selenium_available = SELENIUM_AVAILABLE
        except:
            self.selenium_available = False
        
        # Utiliser cloudscraper si disponible, sinon requests normal
        if self.use_cloudscraper:
            logger.info("Utilisation de cloudscraper pour contourner les protections anti-bot")
            self.session = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'darwin',
                    'desktop': True
                },
                delay=10  # Délai pour éviter la détection
            )
            # Cloudscraper gère déjà la vérification SSL
        else:
            logger.info("Utilisation de requests standard (cloudscraper non disponible)")
            self.session = requests.Session()
            # Configuration SSL pour requests normal
            self.session.verify = False
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Mettre à jour les headers avec rotation User-Agent
        self._update_headers()
        
        # Initialiser la session avec une première requête pour obtenir des cookies
        self._initialize_session()
        
        logger.info("Medias24 scraper initialisé avec délai de %d secondes", self.delay)
    
    def _update_headers(self):
        """Mise à jour des headers avec rotation User-Agent"""
        import random
        
        # Sélectionner un User-Agent aléatoire
        user_agent = random.choice(self.USER_AGENTS)
        
        # Headers réalistes avec plus de détails pour éviter le 403
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',  # Do Not Track
            'Referer': 'https://www.google.com/',
        })
    
    def _initialize_session(self):
        """Initialiser la session avec une première requête pour obtenir des cookies"""
        try:
            logger.info("Initialisation de la session Medias24...")
            
            # Faire une première requête à la page d'accueil pour obtenir des cookies
            # Utiliser un délai plus long pour la première requête
            time.sleep(2)
            
            # Essayer différentes URLs pour voir laquelle fonctionne
            urls_to_try = [
                'https://medias24.com',
                'https://www.medias24.com',
                'https://medias24.com/economie',
            ]
            
            for url in urls_to_try:
                try:
                    # Pour cloudscraper, ne pas désactiver la vérification SSL
                    if self.use_cloudscraper:
                        response = self.session.get(url, timeout=20, allow_redirects=True)
                    else:
                        response = self.session.get(url, timeout=15, allow_redirects=True, verify=False)
                    
                    if response.status_code == 200:
                        logger.info(f"✅ Session initialisée avec succès via {url}")
                        # Attendre un peu avant de continuer
                        time.sleep(1)
                        return True
                    elif response.status_code == 403:
                        logger.warning(f"⚠️  403 pour {url}, on essaie une autre URL...")
                        continue
                except Exception as e:
                    logger.debug(f"Erreur lors de l'initialisation avec {url}: {e}")
                    continue
            
            logger.warning("⚠️  Impossible d'initialiser la session, mais on continue quand même")
            return False
            
        except Exception as e:
            logger.warning(f"Erreur lors de l'initialisation de la session: {e}")
            return False
    
    def _respect_rate_limit(self):
        """Respecter le délai entre les requêtes"""
        now = time.time()
        time_since_last = now - self.last_request_time
        
        if time_since_last < self.delay:
            sleep_time = self.delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def fetch_articles(self, max_articles: int = 20) -> List[Medias24Article]:
        """
        Récupère les articles de Medias24
        
        Args:
            max_articles: Nombre maximum d'articles à récupérer
        
        Returns:
            Liste d'articles
        """
        articles = []
        
        # URLs à essayer dans l'ordre
        urls_to_try = [
            ('https://medias24.com/economie', 'page économie'),
            ('https://medias24.com', 'page d\'accueil'),
            ('https://www.medias24.com', 'page d\'accueil (www)'),
        ]
        
        for url, description in urls_to_try:
            try:
                logger.info(f"Scraping Medias24 {description} ({url}) pour {max_articles} articles")
                
                # Respecter le délai
                self._respect_rate_limit()
                
                # Rotation User-Agent avant chaque requête importante (seulement si pas cloudscraper)
                if not self.use_cloudscraper:
                    self._update_headers()
                
                # Pour cloudscraper, ne pas désactiver la vérification SSL
                if self.use_cloudscraper:
                    response = self.session.get(url, timeout=25, allow_redirects=True)
                else:
                    response = self.session.get(url, timeout=20, allow_redirects=True, verify=False)
                
                # Si 403, essayer Selenium si disponible
                if response.status_code == 403:
                    logger.warning(f"⚠️  403 Forbidden pour {url}")
                    if self.use_selenium and self.selenium_available:
                        logger.info("🔄 Tentative avec Selenium (navigateur réel)...")
                        try:
                            from app.pipelines.ingestion.selenium_scraper import SeleniumScraper
                            with SeleniumScraper(headless=True) as selenium_scraper:
                                html = selenium_scraper.fetch_page(url, wait_for_element='article')
                                if html:
                                    # Utiliser le HTML de Selenium
                                    soup = BeautifulSoup(html, 'html.parser')
                                    logger.info("✅ Page récupérée avec Selenium")
                                    # Continuer avec le parsing normal (sauter le reste de la boucle)
                                    # On traite directement le HTML de Selenium
                                else:
                                    logger.warning("⚠️  Selenium n'a pas réussi non plus")
                                    continue
                        except Exception as e:
                            logger.error(f"❌ Erreur avec Selenium: {e}")
                            continue
                    else:
                        logger.warning(f"⚠️  403 Forbidden pour {url}, on essaie une autre URL...")
                        continue
                
                # Si pas de 403, utiliser le HTML normal
                if response.status_code != 200:
                    response.raise_for_status()
                
                # Parser le HTML (soit de requests, soit de Selenium)
                if 'soup' not in locals():
                    soup = BeautifulSoup(response.content, 'html.parser')
                
                # Méthode 1: Parser les tags <article>
                article_tags = soup.find_all('article', limit=max_articles * 2)  # Prendre plus pour avoir assez après filtrage
                logger.info(f"Found {len(article_tags)} article tags")
                
                # Si pas d'articles trouvés, essayer d'autres méthodes
                if not article_tags:
                    # Chercher dans les divs avec classes communes
                    article_containers = soup.find_all(['div', 'li'], class_=lambda x: x and any(
                        keyword in str(x).lower() for keyword in ['article', 'post', 'news', 'item', 'card']
                    ))
                    logger.info(f"Found {len(article_containers)} article containers")
                    
                    for container in article_containers[:max_articles * 2]:
                        article = self._parse_article_container(container)
                        if article:
                            articles.append(article)
                        if len(articles) >= max_articles:
                            break
                else:
                    for article_tag in article_tags:
                        article = self._parse_article_tag(article_tag)
                        if article:
                            articles.append(article)
                        
                        if len(articles) >= max_articles:
                            break
                
                # Si on a trouvé des articles, on s'arrête
                if articles:
                    break
                    
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    logger.warning(f"⚠️  403 Forbidden pour {url}, on essaie une autre URL...")
                    continue
                else:
                    logger.error(f"Erreur HTTP {e.response.status_code} pour {url}: {e}")
            except Exception as e:
                logger.error(f"Erreur lors du scraping de Medias24 {url}: {e}")
                continue
        
        # Dédupliquer
        unique_articles = self._deduplicate(articles)
        logger.info(f"✅ {len(unique_articles)} articles uniques de Medias24")
        
        return unique_articles[:max_articles]
    
    def _parse_article_container(self, container) -> Optional[Medias24Article]:
        """Parse un conteneur d'article (div, li, etc.)"""
        try:
            # Chercher un lien
            link_elem = container.find('a', href=True)
            if not link_elem:
                return None
            
            url = link_elem['href']
            if not url.startswith('http'):
                url = urljoin(self.BASE_URL, url)
            
            # Chercher un titre
            title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5'])
            if not title_elem:
                title_elem = link_elem
                title = link_elem.get_text(strip=True)
            else:
                title = title_elem.get_text(strip=True)
            
            if not title or len(title) < 15:
                return None
            
            # Résumé
            summary_elem = container.find('p')
            summary = summary_elem.get_text(strip=True) if summary_elem else title
            
            if len(summary) < 20:
                summary = title
            
            # Date
            published_at = self._extract_date(container)
            
            return Medias24Article(
                title=title,
                url=url,
                summary=summary,
                published_at=published_at
            )
            
        except Exception as e:
            logger.debug(f"Erreur parsing container: {e}")
            return None
    
    def _parse_article_tag(self, article_tag) -> Optional[Medias24Article]:
        """Parse un tag <article>"""
        try:
            # Titre
            title_elem = article_tag.find(['h1', 'h2', 'h3', 'h4'])
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            
            # Skip si titre trop court
            if len(title) < 15:
                return None
            
            # URL
            link_elem = article_tag.find('a', href=True)
            if not link_elem:
                return None
            
            url = link_elem['href']
            if not url.startswith('http'):
                url = urljoin(self.BASE_URL, url)
            
            # Résumé
            summary_elem = article_tag.find('p')
            summary = summary_elem.get_text(strip=True) if summary_elem else title
            
            # Si le résumé est trop court, utiliser le titre
            if len(summary) < 20:
                summary = title
            
            # Date (essayer de trouver)
            published_at = self._extract_date(article_tag)
            
            return Medias24Article(
                title=title,
                url=url,
                summary=summary,
                published_at=published_at
            )
            
        except Exception as e:
            logger.debug(f"Erreur parsing article: {e}")
            return None
    
    def _extract_date(self, container) -> Optional[datetime]:
        """Extraire la date de publication"""
        try:
            # Chercher un élément <time>
            time_elem = container.find('time')
            if time_elem:
                datetime_attr = time_elem.get('datetime')
                if datetime_attr:
                    return datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
            
            # Chercher dans le texte
            text = container.get_text()
            
            # Patterns de date français
            date_patterns = [
                r'(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})',
                r'(\d{1,2})/(\d{1,2})/(\d{4})',
                r'(\d{4})-(\d{1,2})-(\d{1,2})',
            ]
            
            months_fr = {
                'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
                'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
                'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
            }
            
            for pattern in date_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        if 'janvier' in pattern or 'février' in pattern:
                            day, month_name, year = match.groups()
                            month = months_fr[month_name.lower()]
                            return datetime(int(year), month, int(day))
                        else:
                            groups = match.groups()
                            if len(groups) == 3:
                                if len(groups[0]) == 4:  # YYYY-MM-DD
                                    return datetime(int(groups[0]), int(groups[1]), int(groups[2]))
                                else:  # DD/MM/YYYY
                                    return datetime(int(groups[2]), int(groups[1]), int(groups[0]))
                    except ValueError:
                        continue
            
            # Par défaut, date récente
            return datetime.now() - timedelta(hours=2)
            
        except Exception:
            return datetime.now() - timedelta(hours=2)
    
    def _deduplicate(self, articles: List[Medias24Article]) -> List[Medias24Article]:
        """Dédupliquer les articles par URL"""
        seen_urls = set()
        unique_articles = []
        
        for article in articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique_articles.append(article)
        
        return unique_articles


# Fonction helper pour compatibilité avec MediaScraper
def convert_to_media_article(medias24_article: Medias24Article):
    """Convertit un Medias24Article en MediaArticle"""
    from app.pipelines.ingestion.media_scraper import MediaArticle
    
    return MediaArticle(
        title=medias24_article.title,
        summary=medias24_article.summary,
        url=medias24_article.url,
        source="medias24",
        published_at=medias24_article.published_at,
        content=medias24_article.content,
        sentiment_score=medias24_article.sentiment_score,
        sentiment_label=medias24_article.sentiment_label
    )








