#!/usr/bin/env python3
"""
Script pour analyser en détail la structure HTML de la Bourse de Casablanca
"""
import sys
sys.path.append('.')

import requests
from bs4 import BeautifulSoup
import json
import re


def analyze_html():
    """Analyser la structure HTML en détail"""
    print("🔍 Analyse Détaillée de la Structure HTML")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    import urllib3
    urllib3.disable_warnings()
    
    url = "https://www.casablanca-bourse.com/fr/live-market/indices/MASI"
    
    try:
        response = session.get(url, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Analyser les tables
        print("\n📊 TABLES TROUVÉES")
        print("-" * 80)
        tables = soup.find_all('table')
        
        for i, table in enumerate(tables):
            print(f"\n🔸 Table #{i}")
            print(f"   Classes: {table.get('class', [])}")
            
            # Headers
            headers = table.find_all('th')
            if headers:
                print(f"   Headers ({len(headers)}): {[h.get_text(strip=True) for h in headers]}")
            
            # Rows
            rows = table.find_all('tr')
            print(f"   Lignes totales: {len(rows)}")
            
            # Analyser les 3 premières lignes de données
            for j, row in enumerate(rows[:3]):
                cols = row.find_all(['td', 'th'])
                if cols:
                    values = [col.get_text(strip=True) for col in cols]
                    print(f"   Ligne {j}: {values}")
        
        # 2. Chercher des divs avec données
        print("\n\n📦 DIVS AVEC DONNÉES")
        print("-" * 80)
        
        # Chercher des patterns de prix
        price_patterns = [
            r'\d+[.,]\d+',  # Prix avec décimales
            r'\d+\s*%',     # Pourcentages
            r'[+-]\d+',     # Variations
        ]
        
        all_divs = soup.find_all('div')
        price_divs = []
        
        for div in all_divs:
            text = div.get_text(strip=True)
            for pattern in price_patterns:
                if re.search(pattern, text) and len(text) < 50:
                    price_divs.append({
                        'text': text,
                        'class': div.get('class', []),
                        'id': div.get('id', '')
                    })
                    break
        
        print(f"Divs avec données numériques: {len(price_divs)}")
        for div_info in price_divs[:10]:
            print(f"   • {div_info['text'][:50]} | Classes: {div_info['class']}")
        
        # 3. Chercher des scripts avec données JSON
        print("\n\n📜 SCRIPTS AVEC DONNÉES")
        print("-" * 80)
        
        scripts = soup.find_all('script')
        for i, script in enumerate(scripts):
            if script.string:
                content = script.string
                
                # Next.js data
                if '__NEXT_DATA__' in content:
                    print(f"\n🎯 Script #{i} - Next.js Data trouvé!")
                    try:
                        # Extraire le JSON
                        match = re.search(r'__NEXT_DATA__\s*=\s*({.*?})\s*</script>', content, re.DOTALL)
                        if match:
                            data = json.loads(match.group(1))
                            print(f"   Structure JSON:")
                            print(f"   Clés principales: {list(data.keys())}")
                            
                            # Explorer pageProps
                            if 'props' in data and 'pageProps' in data['props']:
                                props = data['props']['pageProps']
                                print(f"   PageProps clés: {list(props.keys())}")
                                
                                # Sauvegarder pour inspection
                                with open('nextjs_data.json', 'w', encoding='utf-8') as f:
                                    json.dump(data, f, indent=2, ensure_ascii=False)
                                print(f"   ✅ Données sauvegardées dans nextjs_data.json")
                    except Exception as e:
                        print(f"   ❌ Erreur parsing JSON: {e}")
                
                # Autres données potentielles
                if 'window.' in content and any(keyword in content for keyword in ['data', 'market', 'index', 'quote']):
                    print(f"\n📌 Script #{i} - Variables window détectées")
                    # Extraire les assignations
                    assignments = re.findall(r'window\.(\w+)\s*=\s*({[^;]+}|[^;]+)', content)
                    for var_name, value in assignments[:5]:
                        print(f"   window.{var_name} = {value[:50]}...")
        
        # 4. Chercher des éléments spécifiques MASI
        print("\n\n🎯 ÉLÉMENTS MASI SPÉCIFIQUES")
        print("-" * 80)
        
        # Chercher tous les éléments contenant "MASI"
        masi_elements = soup.find_all(string=lambda text: text and 'MASI' in text.upper())
        print(f"Éléments contenant 'MASI': {len(masi_elements)}")
        
        for elem in masi_elements[:5]:
            parent = elem.parent
            print(f"\n   Texte: {str(elem)[:100]}")
            print(f"   Parent tag: {parent.name}")
            print(f"   Parent classes: {parent.get('class', [])}")
            
            # Chercher des valeurs numériques près de MASI
            siblings = parent.find_next_siblings()
            for sib in siblings[:3]:
                if re.search(r'\d+', sib.get_text()):
                    print(f"   Valeur proche: {sib.get_text(strip=True)}")
        
        # 5. Sauvegarder le HTML complet pour analyse
        with open('page_complete.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"\n✅ HTML complet sauvegardé dans page_complete.html")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    analyze_html()








