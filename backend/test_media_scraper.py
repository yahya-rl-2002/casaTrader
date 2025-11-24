#!/usr/bin/env python3
"""
Test du scraper média amélioré
"""
import sys
sys.path.append('.')

from app.pipelines.ingestion.media_scraper import MediaScraper
from app.services.sentiment_service import SentimentAnalyzer


def main():
    print("🧪 Test du Scraper Média Amélioré")
    print("=" * 80)
    
    # Créer le scraper
    scraper = MediaScraper()
    
    # Tester chaque source séparément
    print("\n📰 Test de L'Économiste")
    print("-" * 80)
    leconomiste_config = scraper.SOURCES['leconomiste']
    articles_eco = scraper._scrape_source('leconomiste', leconomiste_config, max_articles=5)
    
    print(f"✅ {len(articles_eco)} articles récupérés de L'Économiste")
    for i, article in enumerate(articles_eco[:3]):
        print(f"\n   Article #{i+1}:")
        print(f"   📌 Titre: {article.title[:70]}...")
        print(f"   🔗 URL: {article.url[:70]}...")
        print(f"   📝 Résumé: {article.summary[:100]}...")
        print(f"   📅 Date: {article.published_at}")
    
    # Test de toutes les sources
    print("\n\n🌐 Test de Toutes les Sources")
    print("=" * 80)
    all_articles = scraper.scrape_all_sources(max_articles_per_source=5)
    
    print(f"\n✅ Total: {len(all_articles)} articles récupérés")
    
    # Grouper par source
    by_source = {}
    for article in all_articles:
        if article.source not in by_source:
            by_source[article.source] = []
        by_source[article.source].append(article)
    
    print("\n📊 Répartition par source:")
    for source, articles in by_source.items():
        print(f"   • {source}: {len(articles)} articles")
    
    # Afficher quelques exemples
    print("\n\n📰 Exemples d'Articles Récupérés")
    print("=" * 80)
    for i, article in enumerate(all_articles[:5]):
        print(f"\n{i+1}. [{article.source.upper()}]")
        print(f"   📌 {article.title}")
        print(f"   🔗 {article.url}")
        print(f"   📅 {article.published_at}")
        if article.summary:
            print(f"   📝 {article.summary[:150]}...")
    
    # Test de l'analyse de sentiment
    if all_articles:
        print("\n\n🧠 Test de l'Analyse de Sentiment sur Articles Réels")
        print("=" * 80)
        
        analyzer = SentimentAnalyzer()
        # analyze_articles modifie les articles en place
        analyzer.analyze_articles(all_articles[:3])
        
        for article in all_articles[:3]:
            print(f"\n📰 {article.title[:60]}...")
            print(f"   Sentiment: {article.sentiment_label if hasattr(article, 'sentiment_label') else 'N/A'}")
            print(f"   Score: {article.sentiment_score if article.sentiment_score else 0.0:.2f}")
    
    print("\n\n✅ Test Terminé!")
    print("=" * 80)


if __name__ == "__main__":
    main()

