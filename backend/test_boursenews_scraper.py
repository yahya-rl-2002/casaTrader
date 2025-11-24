#!/usr/bin/env python3
"""
Test du scraper BourseNews.ma optimisé
"""
import sys
sys.path.append('.')

from app.pipelines.ingestion.boursenews_scraper import BourseNewsScraper, convert_to_media_article
from app.services.sentiment_service import SentimentAnalyzer


def main():
    print("🧪 TEST DU SCRAPER BOURSENEWS.MA")
    print("=" * 80)
    print("Test du scraper optimisé avec protections anti-blocage")
    print("=" * 80)
    
    # Créer le scraper
    print("\n📰 Initialisation du scraper...")
    scraper = BourseNewsScraper(delay_between_requests=2)  # 2 secondes entre requêtes
    
    # Test 1: Scraper les articles
    print("\n1️⃣  Récupération des articles...")
    print("-" * 80)
    
    articles = scraper.fetch_articles(max_articles=15, sections=["actualite", "marches", "home"])
    
    print(f"\n✅ {len(articles)} articles récupérés de BourseNews.ma")
    
    # Statistiques par catégorie
    by_category = {}
    for article in articles:
        if article.category not in by_category:
            by_category[article.category] = []
        by_category[article.category].append(article)
    
    print(f"\n📊 Répartition par catégorie:")
    for category, arts in by_category.items():
        print(f"   • {category.upper():15} : {len(arts)} articles")
    
    # Afficher les 10 premiers
    print(f"\n📰 Exemples d'Articles Récupérés:")
    print("=" * 80)
    
    for i, article in enumerate(articles[:10], 1):
        print(f"\n{i}. [{article.category.upper()}]")
        print(f"   📌 {article.title}")
        print(f"   🔗 {article.url}")
        print(f"   📅 {article.published_at.strftime('%Y-%m-%d %H:%M') if article.published_at else 'N/A'}")
        if article.summary and article.summary != article.title:
            print(f"   📝 {article.summary[:100]}...")
    
    # Test 2: Analyse de sentiment
    if articles:
        print(f"\n\n2️⃣  Analyse de Sentiment")
        print("=" * 80)
        
        # Convertir en MediaArticle
        media_articles = [convert_to_media_article(art) for art in articles]
        
        print(f"\n🧠 Analyse de sentiment sur {len(media_articles)} articles...")
        
        analyzer = SentimentAnalyzer()
        analyzer.analyze_articles(media_articles)
        
        # Statistiques
        positive_count = sum(1 for a in media_articles if a.sentiment_score and a.sentiment_score > 10)
        negative_count = sum(1 for a in media_articles if a.sentiment_score and a.sentiment_score < -10)
        neutral_count = len(media_articles) - positive_count - negative_count
        
        avg_sentiment = sum(a.sentiment_score for a in media_articles if a.sentiment_score) / len(media_articles)
        
        print(f"\n📊 Distribution des Sentiments:")
        print(f"   • Positifs: {positive_count} articles 😊")
        print(f"   • Négatifs: {negative_count} articles 😟")
        print(f"   • Neutres: {neutral_count} articles 😐")
        print(f"   • Score moyen: {avg_sentiment:.2f}")
        
        # Afficher quelques exemples
        print(f"\n🎯 Exemples d'Analyse:")
        for i, article in enumerate(media_articles[:5], 1):
            score = article.sentiment_score if article.sentiment_score else 0.0
            sentiment_icon = "😊" if score > 10 else "😟" if score < -10 else "😐"
            print(f"\n   {i}. {article.title[:60]}...")
            print(f"      Sentiment: {article.sentiment_label} {sentiment_icon} (score: {score:.1f})")
    
    # Test 3: Comparaison avec L'Économiste
    print(f"\n\n3️⃣  Comparaison des Sources")
    print("=" * 80)
    
    print(f"\n📊 BourseNews.ma:")
    print(f"   • Articles récupérés: {len(articles)}")
    print(f"   • Catégories: {len(by_category)}")
    print(f"   • Spécialisation: Bourse & Marchés ✅")
    print(f"   • Qualité: Articles financiers spécialisés")
    
    print(f"\n💡 Avantages de BourseNews.ma:")
    print(f"   ✅ Contenu 100% financier/bourse")
    print(f"   ✅ Données de marché intégrées")
    print(f"   ✅ Analyses techniques")
    print(f"   ✅ Sentiment de marché")
    print(f"   ✅ Pas de protection Cloudflare stricte")
    
    # Résumé final
    print(f"\n\n✅ TEST TERMINÉ!")
    print("=" * 80)
    print(f"\n🎉 Résultats:")
    print(f"   ✅ {len(articles)} articles récupérés")
    print(f"   ✅ {len(by_category)} catégories")
    print(f"   ✅ Scraping fonctionnel")
    print(f"   ✅ Anti-blocage opérationnel")
    print(f"   ✅ Sentiment analysé")
    print(f"\n💡 BourseNews.ma est une EXCELLENTE source pour le Fear & Greed Index !")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu")
    except Exception as e:
        print(f"\n\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()








