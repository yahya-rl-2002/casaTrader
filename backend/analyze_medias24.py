#!/usr/bin/env python3
"""
Analyse détaillée de Medias24.com
"""
import sys
sys.path.append('.')

import requests
from bs4 import BeautifulSoup
import json


def test_medias24_urls():
    """Tester différentes URLs de Medias24"""
    print("🔍 Analyse de Medias24.com")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9',
    })
    
    import urllib3
    urllib3.disable_warnings()
    
    # URLs à tester
    urls = [
        "https://www.medias24.com",
        "https://www.medias24.com/category/economie",
        "https://www.medias24.com/category/finance-marches",
        "https://medias24.com",
        "https://medias24.com/economie",
    ]
    
    for url in urls:
        print(f"\n📍 Test: {url}")
        print("-" * 60)
        try:
            response = session.get(url, timeout=15, allow_redirects=True)
            print(f"   Status: {response.status_code}")
            print(f"   Final URL: {response.url}")
            print(f"   Content-Length: {len(response.content)} bytes")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Titre de la page
                title = soup.find('title')
                if title:
                    print(f"   Page Title: {title.get_text(strip=True)[:60]}...")
                
                # Chercher articles
                articles = soup.find_all('article')
                print(f"   Articles (tag): {len(articles)}")
                
                # Chercher divs/sections
                post_divs = soup.find_all('div', class_=lambda x: x and ('post' in str(x).lower() or 'article' in str(x).lower()))
                print(f"   Post divs: {len(post_divs)}")
                
                # Chercher liens
                links = soup.find_all('a', href=True)
                article_links = [l for l in links if any(kw in l.get('href', '') for kw in ['/article/', '/post/', '/economie/', '/finance/'])]
                print(f"   Article links: {len(article_links)}")
                
                if response.status_code == 200 and len(response.content) > 10000:
                    # Sauvegarder
                    filename = f"medias24_{url.split('/')[-1] or 'home'}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"   💾 Saved: {filename}")
                    
                    # Analyser structure
                    if articles:
                        print(f"\n   📰 Premier article:")
                        art = articles[0]
                        title_elem = art.find(['h1', 'h2', 'h3'])
                        if title_elem:
                            print(f"      Titre: {title_elem.get_text(strip=True)[:60]}...")
                        link_elem = art.find('a', href=True)
                        if link_elem:
                            print(f"      Lien: {link_elem['href'][:60]}...")
                
        except Exception as e:
            print(f"   ❌ Erreur: {type(e).__name__}: {str(e)[:60]}")


def analyze_saved_html():
    """Analyser le HTML sauvegardé"""
    print("\n\n🔍 Analyse Détaillée du HTML")
    print("=" * 80)
    
    try:
        # Essayer de lire les fichiers sauvegardés
        import os
        html_files = [f for f in os.listdir('.') if f.startswith('medias24_') and f.endswith('.html')]
        
        for html_file in html_files:
            print(f"\n📄 Fichier: {html_file}")
            print("-" * 60)
            
            with open(html_file, 'r', encoding='utf-8') as f:
                html = f.read()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Chercher différents sélecteurs
            selectors = {
                'article': soup.find_all('article'),
                '.post': soup.select('.post'),
                '.entry': soup.select('.entry'),
                '[class*="article"]': soup.select('[class*="article"]'),
                '[class*="post"]': soup.select('[class*="post"]'),
                '.wp-block-post': soup.select('.wp-block-post'),
                '.blog-post': soup.select('.blog-post'),
            }
            
            print("   Sélecteurs trouvés:")
            for selector, elements in selectors.items():
                if elements:
                    print(f"      • {selector:30} : {len(elements)} éléments")
            
            # Chercher des classes communes
            all_divs = soup.find_all('div', class_=True)
            classes = {}
            for div in all_divs[:100]:  # Limiter à 100 pour performance
                for cls in div.get('class', []):
                    classes[cls] = classes.get(cls, 0) + 1
            
            # Top 10 classes
            top_classes = sorted(classes.items(), key=lambda x: -x[1])[:10]
            print(f"\n   Top 10 classes CSS:")
            for cls, count in top_classes:
                print(f"      • {cls:30} : {count} occurrences")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")


def main():
    print("\n🕵️  ANALYSE COMPLÈTE DE MEDIAS24.COM")
    print("=" * 80)
    
    test_medias24_urls()
    analyze_saved_html()
    
    print("\n\n✅ Analyse terminée!")
    print("=" * 80)


if __name__ == "__main__":
    main()








