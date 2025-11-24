"""
Scraper utilisant Selenium pour simuler un navigateur réel
Utile pour contourner les protections anti-bot comme le 403 Forbidden
"""
from __future__ import annotations

from typing import Optional, List
from datetime import datetime
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from app.core.logging import get_logger

logger = get_logger(__name__)

# Essayer d'importer Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger.warning("Selenium not available. Install with: pip install selenium")


class SeleniumScraper:
    """
    Scraper utilisant Selenium pour simuler un navigateur réel
    Utile pour contourner les protections anti-bot
    """
    
    def __init__(self, headless: bool = True, wait_timeout: int = 10):
        """
        Args:
            headless: Mode headless (sans interface graphique)
            wait_timeout: Timeout pour l'attente des éléments (secondes)
        """
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium not available. Install with: pip install selenium")
        
        self.headless = headless
        self.wait_timeout = wait_timeout
        self.driver: Optional[webdriver.Chrome] = None
        
        logger.info("SeleniumScraper initialisé")
    
    def _get_driver(self) -> webdriver.Chrome:
        """Créer et configurer le driver Chrome"""
        if self.driver is None:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Options pour éviter la détection
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # User-Agent réaliste
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Désactiver les logs
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                # Exécuter du JavaScript pour masquer les signes d'automatisation
                self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                    'source': '''
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    '''
                })
                logger.info("✅ Driver Chrome initialisé")
            except WebDriverException as e:
                logger.error(f"❌ Erreur lors de l'initialisation du driver: {e}")
                logger.error("💡 Assurez-vous que ChromeDriver est installé")
                raise
        
        return self.driver
    
    def fetch_page(self, url: str, wait_for_element: Optional[str] = None) -> Optional[str]:
        """
        Récupérer le contenu HTML d'une page avec Selenium
        
        Args:
            url: URL à scraper
            wait_for_element: Sélecteur CSS d'un élément à attendre (optionnel)
        
        Returns:
            HTML de la page ou None en cas d'erreur
        """
        try:
            driver = self._get_driver()
            
            logger.info(f"🌐 Navigation vers {url}")
            driver.get(url)
            
            # Attendre que la page se charge
            if wait_for_element:
                try:
                    WebDriverWait(driver, self.wait_timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element))
                    )
                except TimeoutException:
                    logger.warning(f"⚠️  Élément {wait_for_element} non trouvé, on continue quand même")
            
            # Attendre un peu pour que le JavaScript se charge
            time.sleep(2)
            
            # Récupérer le HTML
            html = driver.page_source
            
            logger.info(f"✅ Page chargée: {len(html)} caractères")
            return html
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du fetch de {url}: {e}")
            return None
    
    def fetch_article_content(self, url: str) -> Optional[dict]:
        """
        Récupérer le contenu complet d'un article
        
        Args:
            url: URL de l'article
        
        Returns:
            Dictionnaire avec title, content, image_url, etc.
        """
        html = self.fetch_page(url, wait_for_element='article, main, .content')
        
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extraire les métadonnées
        result = {
            'title': None,
            'content': None,
            'image_url': None,
            'published_at': None,
        }
        
        # Titre
        title_elem = soup.find('title')
        if title_elem:
            result['title'] = title_elem.get_text(strip=True)
        
        # Contenu
        article_elem = soup.find('article')
        if article_elem:
            # Supprimer les scripts et styles
            for script in article_elem(['script', 'style', 'nav', 'footer', 'aside']):
                script.decompose()
            result['content'] = article_elem.get_text(separator='\n', strip=True)
        else:
            # Fallback: chercher dans main ou content
            main_elem = soup.find('main') or soup.find(['div'], class_=lambda x: x and 'content' in str(x).lower())
            if main_elem:
                for script in main_elem(['script', 'style']):
                    script.decompose()
                result['content'] = main_elem.get_text(separator='\n', strip=True)
        
        # Image
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        if og_image:
            result['image_url'] = og_image.get('content', '').strip()
        else:
            img_elem = soup.find('img')
            if img_elem:
                result['image_url'] = img_elem.get('src') or img_elem.get('data-src', '')
        
        return result
    
    def close(self):
        """Fermer le driver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Driver Chrome fermé")
            except:
                pass
            finally:
                self.driver = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()




