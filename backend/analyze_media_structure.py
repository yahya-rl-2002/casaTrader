#!/usr/bin/env python3
"""
Script pour analyser la structure des sites média marocains
"""
import sys
sys.path.append('.')

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def analyze_medias24():
    """Analyser Medias24"""
    print("📰 Analyse de Medias24.com")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    import urllib3
    urllib3.disable_warnings()
    
    urls = [
        "https://www.medias24.com/category/economie",
        "https://www.medias24.com/category/finance-marches",
    ]
    
    for url in urls:
        print(f"\n🔍 URL: {url}")
        try:
            response = session.get(url, timeout=10)
            print(f"   ✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher les articles
                articles = soup.find_all('article')
                print(f"   📰 Articles trouvés: {len(articles)}")
                
                # Analyser les 3 premiers
                for i, article in enumerate(articles[:3]):
                    print(f"\n   📌 Article #{i+1}:")
                    
                    # Titre
                    title = article.find(['h1', 'h2', 'h3', 'h4'])
                    if title:
                        print(f"      Titre: {title.get_text(strip=True)[:60]}...")
                    
                    # Lien
                    link = article.find('a', href=True)
                    if link:
                        print(f"      Lien: {link['href'][:60]}...")
                    
                    # Date
                    time_elem = article.find('time')
                    if time_elem:
                        print(f"      Date: {time_elem.get_text(strip=True)}")
                    
                    # Résumé
                    paragraphs = article.find_all('p')
                    if paragraphs:
                        print(f"      Résumé: {paragraphs[0].get_text(strip=True)[:60]}...")
                
                # Chercher des divs d'articles
                if not articles:
                    print("\n   Cherche des divs avec classes 'article'...")
                    article_divs = soup.find_all('div', class_=lambda x: x and 'article' in str(x).lower())
                    print(f"   Divs 'article': {len(article_divs)}")
                    
                    for div in article_divs[:2]:
                        title = div.find(['h1', 'h2', 'h3'])
                        if title:
                            print(f"      • {title.get_text(strip=True)[:60]}")
        
        except Exception as e:
            print(f"   ❌ Erreur: {e}")


def analyze_leconomiste():
    """Analyser L'Économiste"""
    print("\n\n💼 Analyse de L'Économiste.com")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    import urllib3
    urllib3.disable_warnings()
    
    urls = [
        "https://www.leconomiste.com/economie",
        "https://www.leconomiste.com/flash-eco",
    ]
    
    for url in urls:
        print(f"\n🔍 URL: {url}")
        try:
            response = session.get(url, timeout=10)
            print(f"   ✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher les articles
                articles = soup.find_all('article')
                print(f"   📰 Articles trouvés: {len(articles)}")
                
                for i, article in enumerate(articles[:3]):
                    print(f"\n   📌 Article #{i+1}:")
                    title = article.find(['h1', 'h2', 'h3'])
                    if title:
                        print(f"      Titre: {title.get_text(strip=True)[:60]}...")
                    link = article.find('a', href=True)
                    if link:
                        print(f"      Lien: {link['href'][:60]}...")
        
        except Exception as e:
            print(f"   ❌ Erreur: {e}")


def analyze_boursenews():
    """Analyser BourseNews"""
    print("\n\n📊 Analyse de BourseNews.ma")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    import urllib3
    urllib3.disable_warnings()
    
    url = "https://www.boursenews.ma"
    
    print(f"\n🔍 URL: {url}")
    try:
        response = session.get(url, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher les articles
            articles = soup.find_all('article')
            print(f"   📰 Articles trouvés: {len(articles)}")
            
            for i, article in enumerate(articles[:3]):
                print(f"\n   📌 Article #{i+1}:")
                title = article.find(['h1', 'h2', 'h3'])
                if title:
                    print(f"      Titre: {title.get_text(strip=True)[:60]}...")
                link = article.find('a', href=True)
                if link:
                    print(f"      Lien: {link['href'][:60]}...")
    
    except Exception as e:
        print(f"   ❌ Erreur: {e}")


def test_alternative_sources():
    """Tester des sources alternatives"""
    print("\n\n🌐 Test de Sources Alternatives")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    import urllib3
    urllib3.disable_warnings()
    
    sources = {
        "Le Matin": "https://lematin.ma/journal/categorie/economie",
        "Aujourd'hui Le Maroc": "https://aujourdhui.ma/economie",
        "MarocHebdo": "https://www.maroc-hebdo.press.ma/economie",
    }
    
    for name, url in sources.items():
        print(f"\n📰 {name}")
        print(f"   URL: {url}")
        try:
            response = session.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                articles = soup.find_all('article')
                print(f"   Articles: {len(articles)}")
                
                if articles:
                    title = articles[0].find(['h1', 'h2', 'h3'])
                    if title:
                        print(f"   Premier: {title.get_text(strip=True)[:60]}...")
        
        except Exception as e:
            print(f"   ❌ Erreur: {type(e).__name__}")


def main():
    """Fonction principale"""
    print("🔍 Analyse des Sites Média Marocains")
    print("=" * 80)
    print("Ce script analyse la structure des sites d'actualité financière")
    print("=" * 80)
    
    analyze_medias24()
    analyze_leconomiste()
    analyze_boursenews()
    test_alternative_sources()
    
    print("\n\n✅ Analyse terminée!")
    print("=" * 80)
    print("\n💡 Prochaine étape: Créer des scrapers spécifiques pour chaque site")


if __name__ == "__main__":
    main()








