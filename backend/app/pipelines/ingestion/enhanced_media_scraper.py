#!/usr/bin/env python3
"""
Scraper amélioré pour les médias marocains
- Scrape le contenu complet de chaque article individuellement
- Validation de qualité robuste
- Système de retry avec backoff exponentiel
- Cache pour éviter de re-scraper les mêmes articles
- Vérification de fraîcheur des articles
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Set
import re
import time
import hashlib
from urllib.parse import urljoin, urlparse
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class EnhancedMediaArticle:
    """Article avec contenu complet et métadonnées enrichies"""
    title: str
    summary: str
    url: str
    source: str
    published_at: Optional[datetime]
    content: str  # Contenu complet de l'article
    image_url: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = None
    word_count: int = 0
    quality_score: float = 0.0  # Score de qualité (0-1)
    sentiment_score: Optional[float] = None
    sentiment_label: str = "neutral"
    scraped_at: datetime = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.scraped_at is None:
            self.scraped_at = datetime.now()
        if self.word_count == 0:
            self.word_count = len(self.content.split()) if self.content else 0


class EnhancedMediaScraper:
    """
    Scraper amélioré qui récupère le contenu complet de chaque article
    """
    
    # Mots-clés financiers pour valider la pertinence
    FINANCE_KEYWORDS = [
        'bourse', 'masi', 'casablanca', 'marché', 'investissement', 'finance',
        'économie', 'titre', 'action', 'obligation', 'trading', 'volatilité',
        'croissance', 'inflation', 'taux', 'devise', 'export', 'import',
        'bancaire', 'crédit', 'capital', 'entreprise', 'secteur', 'performance',
        'dividende', 'cours', 'indice', 'cotation', 'société', 'entreprise',
        'résultat', 'bénéfice', 'perte', 'chiffre', 'affaires', 'commerce'
    ]
    
    # Patterns pour exclure les pages non-articles
    EXCLUDE_PATTERNS = [
        r'/tag/', r'/category/', r'/auteur/', r'/author/',
        r'/contact', r'/about', r'/mentions-legales',
        r'/video/', r'/podcast/', r'/galerie/', r'/photo/',
        r'/newsletter', r'/abonnement', r'/login', r'/register'
    ]
    
    # User-Agents pour rotation
    USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    ]
    
    def __init__(
        self,
        delay_between_requests: float = 2.0,
        max_retries: int = 3,
        cache_dir: Optional[str] = None,
        min_content_length: int = 300,
        max_article_age_days: int = 7
    ):
        """
        Args:
            delay_between_requests: Délai entre les requêtes (secondes)
            max_retries: Nombre maximum de tentatives pour un article
            cache_dir: Répertoire pour le cache (optionnel)
            min_content_length: Longueur minimale du contenu (caractères)
            max_article_age_days: Âge maximum des articles à scraper (jours)
        """
        self.session = requests.Session()
        self.delay = delay_between_requests
        self.max_retries = max_retries
        self.min_content_length = min_content_length
        self.max_article_age = timedelta(days=max_article_age_days)
        self.last_request_time = 0.0
        self.current_ua_index = 0
        
        # Cache pour éviter de re-scraper
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.scraped_urls: Set[str] = set()
        self._load_cache()
        
        # Configuration SSL
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self._update_headers()
        
        logger.info("EnhancedMediaScraper initialisé")
    
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
        self.current_ua_index = (self.current_ua_index + 1) % len(self.USER_AGENTS)
    
    def _respect_rate_limit(self):
        """Respecter le délai entre les requêtes"""
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.delay:
            sleep_time = self.delay - elapsed
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def _load_cache(self):
        """Charger le cache des URLs déjà scrapées"""
        if self.cache_dir and self.cache_dir.exists():
            cache_file = self.cache_dir / 'scraped_urls.json'
            if cache_file.exists():
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Charger seulement les URLs des dernières 24h
                        cutoff = datetime.now() - timedelta(days=1)
                        for url, timestamp_str in data.items():
                            try:
                                timestamp = datetime.fromisoformat(timestamp_str)
                                if timestamp > cutoff:
                                    self.scraped_urls.add(url)
                            except (ValueError, TypeError):
                                continue
                    logger.info(f"Cache chargé: {len(self.scraped_urls)} URLs")
                except Exception as e:
                    logger.warning(f"Erreur chargement cache: {e}")
    
    def _save_cache(self):
        """Sauvegarder le cache"""
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            cache_file = self.cache_dir / 'scraped_urls.json'
            try:
                data = {url: datetime.now().isoformat() for url in self.scraped_urls}
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                logger.warning(f"Erreur sauvegarde cache: {e}")
    
    def _is_url_excluded(self, url: str) -> bool:
        """Vérifier si l'URL doit être exclue"""
        url_lower = url.lower()
        for pattern in self.EXCLUDE_PATTERNS:
            if re.search(pattern, url_lower):
                return True
        return False
    
    def _is_article_fresh(self, published_at: Optional[datetime]) -> bool:
        """Vérifier si l'article est récent"""
        if not published_at:
            return True  # On accepte les articles sans date
        
        # Normaliser les dates (enlever timezone si nécessaire)
        now = datetime.now()
        if published_at.tzinfo:
            # Si published_at a un timezone, le convertir en naive
            published_at = published_at.replace(tzinfo=None)
        if now.tzinfo:
            now = now.replace(tzinfo=None)
        
        age = now - published_at
        return age <= self.max_article_age
    
    def _fetch_with_retry(self, url: str, retries: int = None) -> Optional[str]:
        """
        Récupérer le HTML d'une URL avec retry et backoff exponentiel
        """
        if retries is None:
            retries = self.max_retries
        
        for attempt in range(retries):
            try:
                self._respect_rate_limit()
                self._update_headers()  # Rotation User-Agent
                
                response = self.session.get(url, timeout=30, allow_redirects=True)
                response.raise_for_status()
                
                # Vérifier que c'est bien du HTML
                content_type = response.headers.get('Content-Type', '').lower()
                if 'text/html' not in content_type:
                    logger.warning(f"URL {url} n'est pas du HTML: {content_type}")
                    return None
                
                return response.text
                
            except requests.exceptions.Timeout:
                wait_time = 2 ** attempt  # Backoff exponentiel
                logger.warning(f"Timeout pour {url} (tentative {attempt + 1}/{retries}), attente {wait_time}s")
                if attempt < retries - 1:
                    time.sleep(wait_time)
                    
            except requests.exceptions.RequestException as e:
                wait_time = 2 ** attempt
                logger.warning(f"Erreur pour {url} (tentative {attempt + 1}/{retries}): {e}, attente {wait_time}s")
                if attempt < retries - 1:
                    time.sleep(wait_time)
                else:
                    logger.error(f"Échec définitif pour {url} après {retries} tentatives")
        
        return None
    
    def _extract_full_content(self, html: str, url: str) -> Optional[str]:
        """
        Extraire le contenu complet de l'article depuis le HTML
        Utilise plusieurs méthodes de fallback
        """
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Méthode 1: Chercher les balises article standard
        article_elem = soup.find('article')
        if article_elem:
            # Supprimer les scripts, styles, etc.
            for script in article_elem(['script', 'style', 'nav', 'footer', 'aside', 'header']):
                script.decompose()
            
            content = article_elem.get_text(separator='\n', strip=True)
            if len(content) >= self.min_content_length:
                return content
        
        # Méthode 2: Chercher les divs avec classes communes
        content_selectors = [
            '.article-content', '.post-content', '.entry-content',
            '.article-body', '.post-body', '.content',
            '[itemprop="articleBody"]', '.article-text'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                for script in content_elem(['script', 'style']):
                    script.decompose()
                content = content_elem.get_text(separator='\n', strip=True)
                if len(content) >= self.min_content_length:
                    return content
        
        # Méthode 3: Chercher le plus grand paragraphe
        paragraphs = soup.find_all('p')
        if paragraphs:
            # Prendre les paragraphes les plus longs (probablement le contenu)
            long_paragraphs = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 100]
            if long_paragraphs:
                content = '\n\n'.join(long_paragraphs)
                if len(content) >= self.min_content_length:
                    return content
        
        # Méthode 4: Extraire tout le texte principal (dernier recours)
        main = soup.find('main') or soup.find('body')
        if main:
            for script in main(['script', 'style', 'nav', 'footer', 'aside', 'header', 'form']):
                script.decompose()
            content = main.get_text(separator='\n', strip=True)
            # Nettoyer les lignes trop courtes (probablement du bruit)
            lines = [line for line in content.split('\n') if len(line.strip()) > 20]
            content = '\n'.join(lines)
            if len(content) >= self.min_content_length:
                return content
        
        return None
    
    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extraire les métadonnées de l'article"""
        metadata = {
            'title': None,
            'description': None,
            'image_url': None,
            'author': None,
            'published_at': None,
            'category': None,
            'tags': []
        }
        
        # Titre
        title_elem = soup.find('title')
        if title_elem:
            metadata['title'] = title_elem.get_text(strip=True)
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc:
            metadata['description'] = meta_desc.get('content', '').strip()
        
        # Image - Méthode améliorée avec plusieurs fallbacks
        image_url = None
        
        # Méthode 1: Open Graph image (priorité)
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        if og_image:
            image_url = og_image.get('content', '').strip()
        
        # Méthode 2: Twitter Card image
        if not image_url:
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image:
                image_url = twitter_image.get('content', '').strip()
        
        # Méthode 3: Image dans l'article (chercher dans article, main, ou content)
        if not image_url:
            # Chercher dans l'article
            article_elem = soup.find('article')
            if article_elem:
                img_elem = article_elem.find('img')
                if img_elem:
                    image_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')
            
            # Si pas trouvé, chercher dans main ou content
            if not image_url:
                main_elem = soup.find('main') or soup.find(['div'], class_=lambda x: x and any(
                    kw in str(x).lower() for kw in ['content', 'article', 'post']
                ))
                if main_elem:
                    img_elem = main_elem.find('img')
                    if img_elem:
                        image_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')
            
            # Dernier recours: première image de la page
            if not image_url:
                img_elem = soup.find('img')
                if img_elem:
                    image_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')
        
        # Normaliser l'URL (convertir en URL absolue si nécessaire)
        if image_url:
            # Ignorer les images trop petites (probablement des icônes)
            if any(skip in image_url.lower() for skip in ['icon', 'logo', 'avatar', 'favicon', 'sprite']):
                image_url = None
            elif image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = urljoin(url, image_url)
            elif not image_url.startswith('http'):
                image_url = urljoin(url, image_url)
        
        metadata['image_url'] = image_url
        
        # Auteur
        author_elem = soup.find('meta', attrs={'name': 'author'})
        if not author_elem:
            author_elem = soup.find('span', class_=re.compile(r'author', re.I))
        if author_elem:
            metadata['author'] = author_elem.get_text(strip=True) if hasattr(author_elem, 'get_text') else author_elem.get('content', '')
        
        # Date de publication
        time_elem = soup.find('time')
        if time_elem:
            datetime_attr = time_elem.get('datetime')
            if datetime_attr:
                try:
                    dt = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                    # Normaliser: enlever le timezone
                    if dt.tzinfo:
                        metadata['published_at'] = dt.replace(tzinfo=None)
                    else:
                        metadata['published_at'] = dt
                except ValueError:
                    pass
        
        # Catégorie
        category_elem = soup.find('meta', attrs={'property': 'article:section'})
        if category_elem:
            metadata['category'] = category_elem.get('content', '').strip()
        
        # Tags
        tags_elems = soup.find_all('meta', attrs={'property': 'article:tag'})
        if tags_elems:
            metadata['tags'] = [tag.get('content', '').strip() for tag in tags_elems if tag.get('content')]
        
        return metadata
    
    def _calculate_quality_score(self, article: EnhancedMediaArticle) -> float:
        """
        Calculer un score de qualité pour l'article (0-1)
        """
        score = 0.0
        
        # Longueur du contenu (40%)
        if article.word_count >= 500:
            score += 0.4
        elif article.word_count >= 300:
            score += 0.3
        elif article.word_count >= 200:
            score += 0.2
        elif article.word_count >= 100:
            score += 0.1
        
        # Présence de mots-clés financiers (30%)
        text_lower = f"{article.title} {article.content}".lower()
        keyword_matches = sum(1 for keyword in self.FINANCE_KEYWORDS if keyword in text_lower)
        if keyword_matches >= 5:
            score += 0.3
        elif keyword_matches >= 3:
            score += 0.2
        elif keyword_matches >= 1:
            score += 0.1
        
        # Métadonnées complètes (20%)
        if article.image_url:
            score += 0.05
        if article.author:
            score += 0.05
        if article.category:
            score += 0.05
        if article.tags:
            score += 0.05
        
        # Fraîcheur (10%)
        if article.published_at:
            age = datetime.now() - article.published_at
            if age.days == 0:
                score += 0.1
            elif age.days <= 1:
                score += 0.08
            elif age.days <= 3:
                score += 0.05
        
        return min(score, 1.0)
    
    def scrape_article(self, url: str, source: str) -> Optional[EnhancedMediaArticle]:
        """
        Scraper un article individuel avec son contenu complet
        """
        # Vérifier le cache
        if url in self.scraped_urls:
            logger.debug(f"URL déjà scrapée (cache): {url}")
            return None
        
        # Vérifier les exclusions
        if self._is_url_excluded(url):
            logger.debug(f"URL exclue: {url}")
            return None
        
        # Récupérer le HTML
        html = self._fetch_with_retry(url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extraire les métadonnées
        metadata = self._extract_metadata(soup, url)
        
        # Extraire le contenu complet
        content = self._extract_full_content(html, url)
        if not content or len(content) < self.min_content_length:
            logger.warning(f"Contenu trop court pour {url}: {len(content) if content else 0} caractères")
            return None
        
        # Créer l'article
        article = EnhancedMediaArticle(
            title=metadata['title'] or "Titre non disponible",
            summary=metadata['description'] or content[:200] + "...",
            url=url,
            source=source,
            published_at=metadata['published_at'],
            content=content,
            image_url=metadata['image_url'],
            author=metadata['author'],
            category=metadata['category'],
            tags=metadata['tags'],
            word_count=len(content.split())
        )
        
        # Calculer le score de qualité
        article.quality_score = self._calculate_quality_score(article)
        
        # Vérifier la fraîcheur
        if not self._is_article_fresh(article.published_at):
            logger.debug(f"Article trop ancien: {url}")
            return None
        
        # Ajouter au cache
        self.scraped_urls.add(url)
        
        logger.info(f"✅ Article scrapé: {article.title[:50]}... (qualité: {article.quality_score:.2f})")
        
        return article
    
    def scrape_articles_from_listing(
        self,
        listing_url: str,
        source: str,
        max_articles: int = 20
    ) -> List[EnhancedMediaArticle]:
        """
        Scraper les articles depuis une page de listing
        1. Récupère les liens depuis la page de listing
        2. Scrape le contenu complet de chaque article individuellement
        """
        articles = []
        
        # Étape 1: Récupérer les liens depuis la page de listing
        logger.info(f"Scraping listing: {listing_url}")
        html = self._fetch_with_retry(listing_url)
        if not html:
            logger.error(f"Impossible de récupérer le listing: {listing_url}")
            return articles
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extraire les liens d'articles
        article_links = self._extract_article_links(soup, listing_url, source)
        logger.info(f"Trouvé {len(article_links)} liens d'articles")
        
        # Étape 2: Scraper chaque article individuellement
        for i, article_url in enumerate(article_links[:max_articles]):
            logger.info(f"Scraping article {i+1}/{min(len(article_links), max_articles)}: {article_url}")
            
            article = self.scrape_article(article_url, source)
            if article and article.quality_score >= 0.3:  # Seuil de qualité minimum
                articles.append(article)
            
            # Délai entre les articles
            if i < len(article_links) - 1:
                time.sleep(self.delay)
        
        # Sauvegarder le cache
        self._save_cache()
        
        logger.info(f"✅ {len(articles)} articles de qualité scrapés depuis {source}")
        
        return articles
    
    def _extract_article_links(self, soup: BeautifulSoup, base_url: str, source: str) -> List[str]:
        """Extraire les liens d'articles depuis la page de listing"""
        links = set()
        
        # Méthode 1: Chercher dans les balises <article>
        article_tags = soup.find_all('article')
        for article in article_tags:
            link_elem = article.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                full_url = urljoin(base_url, href)
                if not self._is_url_excluded(full_url):
                    links.add(full_url)
        
        # Méthode 2: Chercher les liens dans les titres (h1, h2, h3, h4, h5)
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5']):
            link_elem = heading.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                full_url = urljoin(base_url, href)
                if not self._is_url_excluded(full_url):
                    # Vérifier que le texte du titre n'est pas générique
                    title_text = heading.get_text(strip=True).lower()
                    if title_text and len(title_text) >= 10:
                        links.add(full_url)
        
        # Méthode 3: Patterns spécifiques par source
        all_links = soup.find_all('a', href=True)
        
        # Patterns par source (regex patterns doivent être des raw strings)
        source_patterns = {
            'hespress': ['/economie/', '.html', '/article/', '/actualite/', r'/\d{6}-'],  # Hespress: /449321-titre
            'challenge': ['/bourse/', '/actualite-finance-maroc/', '/finance/', r'/\d{4}/\d{2}/\d{2}/'],
            'lavieeco': ['/economie/', '/affaires/', '/article/'],
            'leconomiste': ['/article/', '/economie/', r'/\d{4}-\d{2}-\d{2}/'],
            'boursenews': ['/article/', '/news/', '/actualite/', '/marches/'],
            'medias24': ['/economie/', '/article/', r'/\d{4}/\d{2}/\d{2}/'],
        }
        
        patterns = source_patterns.get(source.lower(), ['/article/', '/news/', '/actualite/', '/economie/', '/bourse/'])
        
        for link in all_links:
            href = link.get('href', '')
            if not href:
                continue
            
            # Vérifier si le lien correspond aux patterns
            matches_pattern = False
            for pattern in patterns:
                if pattern.startswith('/') and pattern in href.lower():
                    matches_pattern = True
                    break
                elif pattern.endswith('/') and pattern in href.lower():
                    matches_pattern = True
                    break
                elif '.' in pattern and pattern in href.lower():
                    matches_pattern = True
                    break
                elif re.search(pattern, href, re.IGNORECASE):
                    matches_pattern = True
                    break
            
            if matches_pattern:
                full_url = urljoin(base_url, href)
                if not self._is_url_excluded(full_url):
                    # Pour Hespress, le texte du lien peut être vide, chercher le titre ailleurs
                    link_text = link.get_text(strip=True).lower()
                    
                    # Si le texte du lien est vide ou générique, chercher dans le parent
                    if not link_text or link_text in ['lire la suite', 'en savoir plus', '...', '', 'lire plus', 'suite', 'plus', '...']:
                        # Chercher un titre dans le parent ou les siblings
                        parent = link.find_parent(['div', 'li', 'article', 'section'])
                        if parent:
                            # Chercher un titre (h1-h5) dans le parent
                            title_elem = parent.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                            if title_elem:
                                link_text = title_elem.get_text(strip=True).lower()
                            else:
                                # Chercher dans les spans ou autres éléments
                                text_elem = parent.find(['span', 'p', 'div'], class_=lambda x: x and any(
                                    kw in str(x).lower() for kw in ['title', 'headline', 'name']
                                ))
                                if text_elem:
                                    link_text = text_elem.get_text(strip=True).lower()
                    
                    # Vérifier que le texte du lien n'est pas générique
                    generic_texts = ['lire la suite', 'en savoir plus', '...', '', 'lire plus', 'suite', 'plus']
                    if link_text and link_text not in generic_texts:
                        # Vérifier que le lien a un titre valide (au moins 8 caractères pour être plus permissif)
                        if len(link_text) >= 8:
                            links.add(full_url)
                    elif source.lower() == 'hespress':
                        # Pour Hespress, accepter les liens même sans texte si l'URL ressemble à un article
                        # Hespress utilise des URLs comme /449321-titre-de-l-article
                        if re.search(r'/\d{6}-', href) or '/economie/' in href.lower():
                            links.add(full_url)
        
        # Méthode 4: Chercher dans les divs avec classes communes (pour toutes les sources)
        article_containers = soup.find_all(['div', 'li', 'section'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['article', 'post', 'news', 'item', 'card', 'entry']
        ))
        for container in article_containers:
            link_elem = container.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                full_url = urljoin(base_url, href)
                if not self._is_url_excluded(full_url):
                    # Vérifier que le lien a un titre valide
                    title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                    if title_elem:
                        title_text = title_elem.get_text(strip=True)
                        if title_text and len(title_text) >= 10:
                            links.add(full_url)
                    else:
                        # Si pas de titre, vérifier le texte du lien
                        link_text = link_elem.get_text(strip=True)
                        if link_text and len(link_text) >= 10:
                            links.add(full_url)
        
        # Méthode 5: Pour les sources spécifiques, chercher des patterns supplémentaires
        if source.lower() == 'challenge':
            # Challenge utilise souvent des URLs avec des slugs
            challenge_links = soup.find_all('a', href=re.compile(r'challenge\.ma/[^/]+/[^/]+'))
            for link in challenge_links:
                href = link.get('href', '')
                if href and not self._is_url_excluded(href):
                    links.add(href)
        
        if source.lower() == 'leconomiste':
            # L'Économiste utilise souvent /article/ ou des dates
            leco_links = soup.find_all('a', href=re.compile(r'leconomiste\.com/(article|economie|actus)'))
            for link in leco_links:
                href = link.get('href', '')
                if href and not self._is_url_excluded(href):
                    links.add(href)
        
        if source.lower() == 'hespress':
            # Hespress utilise des URLs avec des IDs numériques : /449321-titre-article
            hespress_links = soup.find_all('a', href=re.compile(r'hespress\.com/\d{6}-'))
            for link in hespress_links:
                href = link.get('href', '')
                if href and not self._is_url_excluded(href):
                    # Chercher un titre dans le parent
                    parent = link.find_parent(['div', 'li', 'article'])
                    if parent:
                        title_elem = parent.find(['h1', 'h2', 'h3', 'h4', 'h5', 'span', 'p'])
                        if title_elem:
                            title_text = title_elem.get_text(strip=True)
                            if title_text and len(title_text) >= 10:
                                links.add(href)
                        else:
                            # Accepter même sans titre si l'URL est valide
                            links.add(href)
                    else:
                        links.add(href)
        
        logger.debug(f"Trouvé {len(links)} liens d'articles pour {source}")
        return list(links)

