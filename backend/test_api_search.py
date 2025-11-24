#!/usr/bin/env python3
"""
Script pour rechercher et tester les APIs disponibles pour la Bourse de Casablanca
"""
import sys
sys.path.append('.')

import requests
from bs4 import BeautifulSoup
import json


def test_casablanca_bourse_api():
    """Tester si la Bourse de Casablanca a une API publique"""
    print("🔍 Recherche d'API - Bourse de Casablanca")
    print("=" * 60)
    
    base_urls = [
        "https://www.casablanca-bourse.com",
        "https://api.casablanca-bourse.com",
        "https://www.casablanca-bourse.com/api",
    ]
    
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    import urllib3
    urllib3.disable_warnings()
    
    for url in base_urls:
        print(f"\n🌐 Test: {url}")
        try:
            response = session.get(url, timeout=10)
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📊 Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            # Chercher des patterns d'API
            if 'application/json' in response.headers.get('content-type', ''):
                print(f"   🎯 Réponse JSON détectée!")
                try:
                    data = response.json()
                    print(f"   📦 Clés: {list(data.keys())[:5]}")
                except:
                    pass
        except Exception as e:
            print(f"   ❌ Erreur: {e}")


def search_for_api_endpoints():
    """Chercher des endpoints API dans le HTML"""
    print("\n\n🔎 Recherche d'endpoints API dans le code source")
    print("=" * 60)
    
    session = requests.Session()
    session.verify = False
    import urllib3
    urllib3.disable_warnings()
    
    try:
        response = session.get("https://www.casablanca-bourse.com/fr/live-market/indices/MASI", timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Chercher des scripts
        scripts = soup.find_all('script')
        print(f"\n📜 {len(scripts)} scripts trouvés")
        
        api_patterns = ['api', 'endpoint', 'fetch', 'ajax', 'data']
        
        for i, script in enumerate(scripts):
            script_content = script.string if script.string else ''
            
            for pattern in api_patterns:
                if pattern in script_content.lower():
                    # Extraire les URLs potentielles
                    import re
                    urls = re.findall(r'https?://[^\s<>"]+|/api/[^\s<>"]+', script_content)
                    if urls:
                        print(f"\n   Script #{i} - Pattern '{pattern}' trouvé:")
                        for url in urls[:3]:
                            print(f"      🔗 {url}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_known_financial_apis():
    """Tester des APIs financières connues"""
    print("\n\n💼 Test d'APIs financières alternatives")
    print("=" * 60)
    
    apis = {
        "Alpha Vantage": "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo",
        "Yahoo Finance": "https://query1.finance.yahoo.com/v8/finance/chart/AAPL",
        "Investing.com": "https://www.investing.com/indices/morocco-all-shares",
    }
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    for name, url in apis.items():
        print(f"\n🌐 {name}")
        print(f"   URL: {url}")
        try:
            response = session.get(url, timeout=10)
            print(f"   ✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    print(f"   🎯 API JSON disponible!")
                    try:
                        data = response.json()
                        print(f"   📦 Structure: {list(data.keys())[:5] if isinstance(data, dict) else 'Array'}")
                    except:
                        pass
                else:
                    print(f"   📄 Type: {content_type}")
        except Exception as e:
            print(f"   ❌ Erreur: {type(e).__name__}")


def analyze_page_structure():
    """Analyser la structure de la page pour mieux comprendre les données"""
    print("\n\n📊 Analyse de la structure de la page")
    print("=" * 60)
    
    session = requests.Session()
    session.verify = False
    import urllib3
    urllib3.disable_warnings()
    
    try:
        response = session.get("https://www.casablanca-bourse.com/fr/live-market/indices/MASI", timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("\n🔍 Éléments clés trouvés:")
        
        # Tables
        tables = soup.find_all('table')
        print(f"\n   📊 Tables: {len(tables)}")
        for i, table in enumerate(tables[:2]):
            print(f"      Table #{i}:")
            print(f"         Classes: {table.get('class', [])}")
            rows = table.find_all('tr')
            print(f"         Lignes: {len(rows)}")
            if rows:
                cols = rows[0].find_all(['th', 'td'])
                print(f"         Colonnes: {len(cols)}")
        
        # Divs avec classes intéressantes
        interesting_classes = ['price', 'value', 'data', 'quote', 'market', 'index']
        print(f"\n   🎯 Divs avec classes intéressantes:")
        for cls in interesting_classes:
            divs = soup.find_all('div', class_=lambda x: x and cls in str(x).lower())
            if divs:
                print(f"      '{cls}': {len(divs)} trouvé(s)")
        
        # Scripts avec données JSON
        print(f"\n   📜 Scripts avec données:")
        scripts = soup.find_all('script')
        for i, script in enumerate(scripts):
            if script.string and ('__NEXT_DATA__' in script.string or 'window.' in script.string):
                print(f"      Script #{i}: Contient des données possibles")
                if '__NEXT_DATA__' in script.string:
                    print(f"         🎯 Next.js data trouvé!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")


def main():
    """Fonction principale"""
    print("🚀 Recherche d'APIs pour la Bourse de Casablanca")
    print("=" * 60)
    
    test_casablanca_bourse_api()
    search_for_api_endpoints()
    analyze_page_structure()
    test_known_financial_apis()
    
    print("\n\n📋 Résumé des Recommandations")
    print("=" * 60)
    print("""
    1️⃣ Bourse de Casablanca:
       - ✅ Connexion SSL résolue
       - ⚠️ Pas d'API publique évidente
       - 💡 Utiliser le scraping web amélioré
    
    2️⃣ APIs Alternatives:
       - Alpha Vantage (nécessite clé API)
       - Yahoo Finance (données limitées)
       - Investing.com (scraping nécessaire)
    
    3️⃣ Solution Recommandée:
       - Scraping web avec fallback intelligent
       - Cache des données pour réduire les requêtes
       - Mise à jour périodique (ex: toutes les heures)
    
    4️⃣ Pour la Production:
       - Contacter la Bourse de Casablanca pour un accès API
       - Utiliser un service de données financières payant
       - Implémenter un système de cache robuste
    """)


if __name__ == "__main__":
    main()








