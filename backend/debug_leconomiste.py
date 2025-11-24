#!/usr/bin/env python3
"""
Debug détaillé de L'Économiste
"""
import sys
sys.path.append('.')

import requests
from bs4 import BeautifulSoup


def main():
    print("🔍 Debug Détaillé de L'Économiste")
    print("=" * 80)
    
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    import urllib3
    urllib3.disable_warnings()
    
    url = "https://www.leconomiste.com/economie"
    
    print(f"\n🌐 Connexion à: {url}")
    response = session.get(url, timeout=10)
    print(f"✅ Status: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trouver tous les articles
    articles = soup.find_all('article')
    print(f"\n📰 Total articles trouvés: {len(articles)}")
    
    # Analyser les 10 premiers en détail
    print("\n🔍 Analyse Détaillée des 10 Premiers Articles:")
    print("=" * 80)
    
    finance_keywords = [
        'bourse', 'masi', 'casablanca', 'marché', 'investissement', 'finance',
        'économie', 'titre', 'action', 'obligation', 'trading', 'volatilité',
        'croissance', 'inflation', 'taux', 'devise', 'export', 'import',
        'bancaire', 'crédit', 'capital', 'entreprise', 'secteur', 'performance'
    ]
    
    matching_count = 0
    
    for i, article in enumerate(articles[:10]):
        print(f"\n📌 Article #{i+1}")
        print("-" * 60)
        
        # Titre
        title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
        title = title_elem.get_text(strip=True) if title_elem else "Pas de titre"
        print(f"Titre: {title[:80]}")
        
        # Lien
        link_elem = article.find('a', href=True)
        link = link_elem['href'] if link_elem else "Pas de lien"
        print(f"Lien: {link[:80]}")
        
        # Résumé
        summary_elem = article.find('p')
        summary = summary_elem.get_text(strip=True) if summary_elem else "Pas de résumé"
        print(f"Résumé: {summary[:120]}...")
        
        # Vérifier les keywords
        text_to_check = f"{title} {summary}".lower()
        keywords_found = [kw for kw in finance_keywords if kw in text_to_check]
        
        print(f"Keywords trouvés ({len(keywords_found)}): {', '.join(keywords_found[:5])}")
        
        if len(keywords_found) >= 1:
            print("✅ MATCH - Article financier!")
            matching_count += 1
        else:
            print("❌ Pas assez de keywords financiers")
    
    print(f"\n\n📊 Résumé:")
    print(f"   Total articles: {len(articles)}")
    print(f"   Articles analysés: {min(10, len(articles))}")
    print(f"   Articles financiers: {matching_count}")
    print(f"   Taux de match: {matching_count / min(10, len(articles)) * 100:.1f}%")


if __name__ == "__main__":
    main()








