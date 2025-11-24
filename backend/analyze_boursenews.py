#!/usr/bin/env python3
"""
Analyse de BourseNews.ma et ses protections anti-scraping
"""
import sys
sys.path.append('.')

import requests
from bs4 import BeautifulSoup
import time
import json


def test_basic_request():
    """Test requête basique"""
    print("🔍 Test #1 - Requête Basique")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    
    import urllib3
    urllib3.disable_warnings()
    
    url = "https://www.boursenews.ma"
    
    print(f"URL: {url}")
    try:
        response = session.get(url, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"   Content-Length: {len(response.content)} bytes")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        # Vérifier si c'est du JavaScript/Cloudflare/etc
        if 'cf-ray' in response.headers:
            print("   ⚠️  Cloudflare détecté!")
        if 'server' in response.headers:
            print(f"   Server: {response.headers['server']}")
        
        # Analyser le contenu
        if 'javascript' in response.text.lower()[:500]:
            print("   ⚠️  Protection JavaScript détectée dans les premières lignes")
        if 'captcha' in response.text.lower():
            print("   ⚠️  CAPTCHA possible")
        if 'challenge' in response.text.lower()[:1000]:
            print("   ⚠️  Challenge détecté (anti-bot)")
        
        return response
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None


def test_with_headers():
    """Test avec headers avancés"""
    print("\n\n🔍 Test #2 - Requête avec Headers Avancés")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    
    # Headers plus réalistes
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
        'Referer': 'https://www.google.com/'
    }
    session.headers.update(headers)
    
    import urllib3
    urllib3.disable_warnings()
    
    url = "https://www.boursenews.ma"
    
    try:
        response = session.get(url, timeout=15)
        print(f"✅ Status Code: {response.status_code}")
        print(f"   Content-Length: {len(response.content)} bytes")
        
        # Sauvegarder pour inspection
        with open('boursenews_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"   💾 Sauvegardé dans boursenews_response.html")
        
        return response
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None


def test_selenium():
    """Test avec Selenium (navigateur réel)"""
    print("\n\n🔍 Test #3 - Selenium (Navigateur Réel)")
    print("=" * 80)
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        print("✅ Selenium disponible")
        
        # Configuration
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Mode sans interface
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        print("🚀 Lancement du navigateur...")
        driver = webdriver.Chrome(options=chrome_options)
        
        url = "https://www.boursenews.ma"
        print(f"🌐 Navigation vers {url}")
        driver.get(url)
        
        # Attendre le chargement
        time.sleep(3)
        
        print(f"✅ Page chargée")
        print(f"   Titre: {driver.title}")
        
        # Chercher des articles
        articles = driver.find_elements(By.TAG_NAME, 'article')
        print(f"   Articles trouvés: {len(articles)}")
        
        # Sauvegarder le HTML
        with open('boursenews_selenium.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"   💾 HTML sauvegardé dans boursenews_selenium.html")
        
        driver.quit()
        return True
        
    except ImportError:
        print("⚠️  Selenium non installé")
        print("   Installation: pip install selenium")
        return False
    except Exception as e:
        print(f"❌ Erreur Selenium: {e}")
        return False


def analyze_structure(response):
    """Analyser la structure du site"""
    print("\n\n🔍 Test #4 - Analyse Structure HTML")
    print("=" * 80)
    
    if not response:
        print("❌ Pas de réponse à analyser")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Chercher articles
    print("\n📰 Recherche d'articles...")
    
    selectors = [
        ('article', 'Tag article'),
        ('.post', 'Classe .post'),
        ('.entry', 'Classe .entry'),
        ('.article-item', 'Classe .article-item'),
        ('.news-item', 'Classe .news-item'),
        ('[class*="article"]', 'Contient "article"'),
        ('[class*="post"]', 'Contient "post"'),
    ]
    
    for selector, desc in selectors:
        elements = soup.select(selector)
        print(f"   {desc:30} : {len(elements)} éléments")
        
        if elements and len(elements) > 0:
            print(f"      → Premier élément: {str(elements[0])[:100]}...")
    
    # Chercher des liens
    print("\n🔗 Analyse des liens...")
    links = soup.find_all('a', href=True)
    print(f"   Total liens: {len(links)}")
    
    # Filtrer liens articles
    article_links = [
        link for link in links 
        if 'article' in link['href'] or 'post' in link['href'] or len(link['href']) > 30
    ]
    print(f"   Liens articles potentiels: {len(article_links)}")
    
    if article_links:
        print(f"\n   Exemples:")
        for link in article_links[:5]:
            print(f"      • {link.get_text(strip=True)[:50]}...")
            print(f"        {link['href'][:70]}")


def test_api():
    """Chercher une API cachée"""
    print("\n\n🔍 Test #5 - Recherche API")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    
    import urllib3
    urllib3.disable_warnings()
    
    # URLs API possibles
    api_urls = [
        "https://www.boursenews.ma/wp-json/wp/v2/posts",
        "https://www.boursenews.ma/api/articles",
        "https://www.boursenews.ma/feed",
        "https://www.boursenews.ma/feed/rss",
    ]
    
    for url in api_urls:
        print(f"\n🌐 Test: {url}")
        try:
            response = session.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ API trouvée!")
                print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
                
                if 'json' in response.headers.get('Content-Type', ''):
                    try:
                        data = response.json()
                        print(f"   📊 JSON valide: {len(data)} entrées")
                        
                        # Sauvegarder
                        with open('boursenews_api.json', 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        print(f"   💾 Sauvegardé dans boursenews_api.json")
                    except:
                        print(f"   ⚠️  Pas du JSON valide")
                
                elif 'xml' in response.headers.get('Content-Type', ''):
                    print(f"   📰 RSS Feed trouvé!")
                    with open('boursenews_rss.xml', 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"   💾 Sauvegardé dans boursenews_rss.xml")
        
        except Exception as e:
            print(f"   ❌ Erreur: {type(e).__name__}")


def main():
    """Fonction principale"""
    print("\n🕵️  ANALYSE DE BOURSENEWS.MA - PROTECTIONS ANTI-SCRAPING")
    print("=" * 80)
    print("Ce script analyse les protections et trouve les meilleures méthodes")
    print("=" * 80)
    
    # Test 1: Requête basique
    response1 = test_basic_request()
    
    # Test 2: Headers avancés
    response2 = test_with_headers()
    
    # Test 3: Selenium
    test_selenium()
    
    # Test 4: Analyse structure
    if response2:
        analyze_structure(response2)
    
    # Test 5: API
    test_api()
    
    print("\n\n✅ Analyse Terminée!")
    print("=" * 80)
    print("\n💡 Recommandations:")
    print("   1. Vérifier les fichiers sauvegardés (.html, .json, .xml)")
    print("   2. Si Cloudflare: Utiliser cloudscraper ou Selenium")
    print("   3. Si API/RSS: Utiliser directement l'API")
    print("   4. Respecter les délais entre requêtes (2-5 secondes)")
    print("   5. Rotation User-Agent si nécessaire")


if __name__ == "__main__":
    main()








