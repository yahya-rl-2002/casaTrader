#!/usr/bin/env python3
"""
Parser spécifique pour BourseNews.ma
"""
import sys
sys.path.append('.')

from bs4 import BeautifulSoup


def main():
    print("🔍 Analyse du HTML BourseNews.ma")
    print("=" * 80)
    
    # Lire le fichier sauvegardé
    with open('boursenews_response.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Chercher tous les divs avec "article" dans la classe
    article_divs = soup.find_all('div', class_=lambda x: x and 'article' in str(x).lower())
    print(f"\n📰 Divs avec 'article' dans la classe: {len(article_divs)}")
    
    for i, div in enumerate(article_divs[:5]):
        print(f"\n   Div #{i+1}:")
        print(f"   Classes: {div.get('class', [])}")
        print(f"   Onclick: {div.get('onclick', 'N/A')[:80]}...")
        
        # Chercher titre
        title = div.find(['h1', 'h2', 'h3', 'h4', 'h5'])
        if title:
            print(f"   Titre: {title.get_text(strip=True)[:70]}...")
        
        # Chercher lien
        link = div.find('a', href=True)
        if link:
            print(f"   Lien: {link['href'][:70]}...")
    
    # Chercher les sections spécifiques
    print(f"\n\n🎯 Sections Spécifiques")
    print("=" * 80)
    
    # Section "À la une"
    alaune = soup.find_all('div', class_=lambda x: x and 'la_une' in str(x).lower())
    print(f"\n📌 Section 'À la une': {len(alaune)} éléments")
    
    # Section articles
    all_links = soup.find_all('a', href=True)
    article_links = [l for l in all_links if '/article/' in l.get('href', '')]
    print(f"📌 Liens '/article/': {len(article_links)} éléments")
    
    print(f"\n🔗 Exemples de liens d'articles:")
    for i, link in enumerate(article_links[:10]):
        print(f"   {i+1}. {link.get_text(strip=True)[:60]}...")
        print(f"      URL: {link['href'][:70]}")
    
    # Chercher des patterns JSON/data
    print(f"\n\n💾 Recherche de données structurées")
    print("=" * 80)
    
    scripts = soup.find_all('script')
    for i, script in enumerate(scripts):
        if script.string and 'article' in script.string.lower() and len(script.string) > 100:
            print(f"\n   Script #{i} contient 'article'")
            print(f"   Extrait: {script.string[:200]}...")
    
    # Sauvegarder les liens
    print(f"\n\n💾 Sauvegarde des liens articles")
    with open('boursenews_links.txt', 'w', encoding='utf-8') as f:
        for link in article_links[:20]:
            f.write(f"{link.get_text(strip=True)}\n")
            f.write(f"{link['href']}\n")
            f.write("-" * 40 + "\n")
    print(f"   ✅ Sauvegardé dans boursenews_links.txt")


if __name__ == "__main__":
    main()








