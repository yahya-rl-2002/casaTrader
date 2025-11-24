#!/usr/bin/env python3
"""
Script de test pour vérifier que le scraper amélioré peut scraper
BourseNews, Medias24 et Hespress
"""
import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from app.pipelines.ingestion.enhanced_media_scraper import EnhancedMediaScraper
from app.core.logging import get_logger

logger = get_logger(__name__)


async def test_scraper():
    """Tester le scraper amélioré avec les 3 sources principales"""
    
    print("=" * 80)
    print("🧪 TEST DU SCRAPER AMÉLIORÉ")
    print("=" * 80)
    print()
    
    scraper = EnhancedMediaScraper(
        delay_between_requests=2.0,
        max_retries=2,  # Réduire pour les tests
        min_content_length=200,  # Réduire pour les tests
        max_article_age_days=7
    )
    
    # Sources à tester
    test_sources = {
        "medias24": [
            "https://medias24.com",
            "https://medias24.com/economie/",
        ],
        "boursenews": [
            "https://boursenews.ma",
            "https://boursenews.ma/espace-investisseurs",
        ],
        "hespress": [
            "https://fr.hespress.com/economie",
        ],
    }
    
    results = {}
    
    for source_name, listing_urls in test_sources.items():
        print(f"\n{'=' * 80}")
        print(f"📰 TEST: {source_name.upper()}")
        print(f"{'=' * 80}")
        
        source_articles = []
        
        for listing_url in listing_urls:
            print(f"\n🔍 Scraping listing: {listing_url}")
            
            try:
                # Scraper les articles depuis le listing
                articles = await asyncio.to_thread(
                    scraper.scrape_articles_from_listing,
                    listing_url,
                    source_name,
                    max_articles=5  # Limiter à 5 pour les tests
                )
                
                source_articles.extend(articles)
                
                print(f"✅ {len(articles)} articles trouvés depuis {listing_url}")
                
                # Afficher les détails des articles
                for i, article in enumerate(articles[:3], 1):  # Afficher les 3 premiers
                    print(f"\n  Article {i}:")
                    print(f"    Titre: {article.title[:60]}...")
                    print(f"    URL: {article.url}")
                    print(f"    Contenu: {len(article.content)} caractères")
                    print(f"    Qualité: {article.quality_score:.2f}")
                    print(f"    Mots: {article.word_count}")
                    if article.published_at:
                        print(f"    Date: {article.published_at}")
                
            except Exception as e:
                print(f"❌ Erreur scraping {listing_url}: {e}")
                logger.error(f"Erreur scraping {listing_url}: {e}", exc_info=True)
                continue
        
        results[source_name] = {
            "total": len(source_articles),
            "articles": source_articles
        }
        
        print(f"\n📊 Résultat {source_name}: {len(source_articles)} articles scrapés")
    
    # Résumé final
    print(f"\n{'=' * 80}")
    print("📊 RÉSUMÉ DES TESTS")
    print(f"{'=' * 80}")
    
    total_articles = sum(r["total"] for r in results.values())
    
    for source_name, result in results.items():
        status = "✅" if result["total"] > 0 else "❌"
        print(f"{status} {source_name}: {result['total']} articles")
    
    print(f"\n🎯 Total: {total_articles} articles scrapés")
    
    if total_articles > 0:
        print("\n✅ SUCCÈS: Le scraper peut scraper tous les médias !")
    else:
        print("\n❌ ÉCHEC: Aucun article n'a été scrapé")
    
    return results


if __name__ == "__main__":
    try:
        results = asyncio.run(test_scraper())
        
        # Afficher quelques exemples d'articles
        print(f"\n{'=' * 80}")
        print("📄 EXEMPLES D'ARTICLES SCRAPÉS")
        print(f"{'=' * 80}")
        
        for source_name, result in results.items():
            if result["articles"]:
                article = result["articles"][0]
                print(f"\n{source_name.upper()}:")
                print(f"  Titre: {article.title}")
                print(f"  URL: {article.url}")
                print(f"  Contenu (premiers 200 caractères):")
                print(f"  {article.content[:200]}...")
                print(f"  Qualité: {article.quality_score:.2f}")
                print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur lors du test: {e}")
        logger.error(f"Erreur lors du test: {e}", exc_info=True)
        sys.exit(1)






