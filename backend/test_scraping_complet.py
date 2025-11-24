#!/usr/bin/env python3
"""
Script de test complet du système de scraping amélioré
Teste BourseNews, Medias24 et Hespress
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.enhanced_media_service import EnhancedMediaService
from app.core.logging import get_logger

logger = get_logger(__name__)


async def test_scraping_complet():
    """Tester le scraping complet avec le service amélioré"""
    
    print("=" * 80)
    print("🧪 TEST COMPLET DU SYSTÈME DE SCRAPING AMÉLIORÉ")
    print("=" * 80)
    print()
    
    # Créer le service
    service = EnhancedMediaService(
        max_articles_per_source=10,  # Limiter à 10 pour les tests
        min_quality_score=0.3
    )
    
    print("📋 Configuration:")
    print(f"   - Articles max par source: {service.max_articles_per_source}")
    print(f"   - Score de qualité minimum: {service.min_quality_score}")
    print(f"   - Sources configurées: {', '.join(service.SOURCE_LISTINGS.keys())}")
    print()
    
    # Tester le scraping de toutes les sources
    print("🚀 Démarrage du scraping de toutes les sources...")
    print()
    
    try:
        stats = await service.scrape_all_sources()
        
        print("=" * 80)
        print("📊 RÉSULTATS DU SCRAPING")
        print("=" * 80)
        print()
        
        # Afficher les stats par source
        for source_name, source_stats in stats["sources"].items():
            status = "✅" if source_stats["quality"] > 0 else "❌"
            print(f"{status} {source_name.upper()}:")
            print(f"   - Articles scrapés: {source_stats['scraped']}")
            print(f"   - Articles de qualité: {source_stats['quality']}")
            if source_stats["quality"] > 0:
                print(f"   - Score moyen: {source_stats['avg_quality_score']:.2f}")
            print()
        
        # Résumé global
        print("=" * 80)
        print("📈 RÉSUMÉ GLOBAL")
        print("=" * 80)
        print(f"   - Total scrapé: {stats['total_scraped']} articles")
        print(f"   - Total sauvegardé: {stats['total_saved']} articles")
        print(f"   - Erreurs: {len(stats['errors'])}")
        
        if stats['errors']:
            print("\n⚠️  Erreurs rencontrées:")
            for error in stats['errors']:
                print(f"   - {error.get('source', 'Unknown')}: {error.get('error', 'Unknown error')}")
        
        print()
        
        # Afficher des exemples d'articles
        if stats['total_scraped'] > 0:
            print("=" * 80)
            print("📄 EXEMPLES D'ARTICLES SCRAPÉS")
            print("=" * 80)
            print()
            
            # Récupérer quelques articles depuis la base de données pour afficher
            from app.models.database import get_session
            from app.models.schemas import MediaArticle
            from sqlalchemy import desc
            
            db = get_session()
            
            try:
                recent_articles = (
                    db.query(MediaArticle)
                    .order_by(desc(MediaArticle.scraped_at))
                    .limit(5)
                    .all()
                )
                
                for i, article in enumerate(recent_articles, 1):
                    print(f"Article {i}:")
                    print(f"   Source: {article.source}")
                    print(f"   Titre: {article.title[:70]}...")
                    print(f"   URL: {article.url}")
                    if article.content:
                        print(f"   Contenu: {len(article.content)} caractères")
                    if article.scraped_at:
                        print(f"   Scrapé le: {article.scraped_at.strftime('%Y-%m-%d %H:%M:%S')}")
                    print()
            finally:
                db.close()
        
        # Conclusion
        print("=" * 80)
        if stats['total_saved'] > 0:
            print("✅ SUCCÈS: Le système de scraping fonctionne !")
            print(f"   {stats['total_saved']} articles ont été scrapés et sauvegardés.")
        else:
            print("⚠️  ATTENTION: Aucun article n'a été sauvegardé.")
            print("   Vérifiez les erreurs ci-dessus.")
        print("=" * 80)
        
        return stats
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        logger.error(f"Erreur lors du test: {e}", exc_info=True)
        raise


async def test_source_specifique(source_name: str):
    """Tester le scraping d'une source spécifique"""
    
    print(f"\n{'=' * 80}")
    print(f"🧪 TEST DE LA SOURCE: {source_name.upper()}")
    print(f"{'=' * 80}\n")
    
    service = EnhancedMediaService(
        max_articles_per_source=5,  # Limiter à 5 pour les tests
        min_quality_score=0.3
    )
    
    if source_name not in service.SOURCE_LISTINGS:
        print(f"❌ Source '{source_name}' non trouvée")
        print(f"   Sources disponibles: {', '.join(service.SOURCE_LISTINGS.keys())}")
        return
    
    # Scraper uniquement cette source
    listing_urls = service.SOURCE_LISTINGS[source_name]
    
    print(f"📰 URLs de listing pour {source_name}:")
    for url in listing_urls:
        print(f"   - {url}")
    print()
    
    try:
        # Scraper les articles depuis le listing
        articles = []
        for listing_url in listing_urls:
            print(f"🔍 Scraping: {listing_url}")
            try:
                source_articles = await asyncio.to_thread(
                    service.scraper.scrape_articles_from_listing,
                    listing_url,
                    source_name,
                    5  # Max 5 articles
                )
                articles.extend(source_articles)
                print(f"   ✅ {len(source_articles)} articles trouvés")
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        print(f"\n📊 Total: {len(articles)} articles scrapés")
        
        if articles:
            print(f"\n📄 Détails des articles:")
            for i, article in enumerate(articles[:3], 1):  # Afficher les 3 premiers
                print(f"\n   Article {i}:")
                print(f"      Titre: {article.title[:60]}...")
                print(f"      URL: {article.url}")
                print(f"      Contenu: {len(article.content)} caractères")
                print(f"      Mots: {article.word_count}")
                print(f"      Qualité: {article.quality_score:.2f}")
                if article.published_at:
                    print(f"      Date: {article.published_at.strftime('%Y-%m-%d')}")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        logger.error(f"Erreur lors du test de {source_name}: {e}", exc_info=True)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tester le système de scraping amélioré")
    parser.add_argument(
        "--source",
        type=str,
        help="Tester une source spécifique (medias24, boursenews, hespress, etc.)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Tester toutes les sources (par défaut)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.source:
            # Tester une source spécifique
            asyncio.run(test_source_specifique(args.source))
        else:
            # Tester toutes les sources
            asyncio.run(test_scraping_complet())
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur lors du test: {e}")
        logger.error(f"Erreur lors du test: {e}", exc_info=True)
        sys.exit(1)

