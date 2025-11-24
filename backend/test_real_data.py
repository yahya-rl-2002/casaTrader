#!/usr/bin/env python3
"""
Script de test pour vérifier la récupération de données réelles
"""
import sys
sys.path.append('.')

from app.pipelines.ingestion.market_scraper import CasablancaMarketScraper
from app.pipelines.ingestion.media_scraper import MediaScraper
from app.services.sentiment_service import SentimentAnalyzer


def test_market_data():
    """Test du scraping des données de marché"""
    print("🔍 Test du scraping de la Bourse de Casablanca...")
    print("=" * 60)
    
    scraper = CasablancaMarketScraper()
    
    # Test 1: Données en direct
    print("\n1️⃣ Récupération des données en direct...")
    try:
        live_data = scraper.fetch_live_data()
        if live_data:
            print(f"✅ {len(live_data)} données récupérées")
            for data in live_data[:3]:  # Afficher les 3 premières
                print(f"   - {data.symbol}: {data.last_price:.2f} MAD ({data.change_percent:+.2f}%)")
                print(f"     Volume: {data.volume:,} | Date: {data.as_of}")
        else:
            print("⚠️ Aucune donnée récupérée (peut-être en fallback)")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 2: Données historiques
    print("\n2️⃣ Récupération des données historiques (30 jours)...")
    try:
        historical_data = scraper.fetch_historical_data(days=30)
        if historical_data:
            print(f"✅ {len(historical_data)} jours de données")
            # Afficher les 3 derniers jours
            for data in historical_data[-3:]:
                print(f"   - {data.date}: Close={data.close_price:.2f}, Volume={data.volume:,}")
        else:
            print("⚠️ Aucune donnée historique")
    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_media_data():
    """Test du scraping des médias"""
    print("\n\n📰 Test du scraping des médias marocains...")
    print("=" * 60)
    
    scraper = MediaScraper()
    
    print("\nRécupération des articles...")
    try:
        articles = scraper.scrape_all_sources(max_articles_per_source=5)
        
        if articles:
            print(f"✅ {len(articles)} articles récupérés")
            for i, article in enumerate(articles[:5], 1):
                print(f"\n   Article {i}:")
                print(f"   📰 Titre: {article.title[:60]}...")
                print(f"   🌐 Source: {article.source}")
                print(f"   📅 Date: {article.published_at}")
                print(f"   🔗 URL: {article.url[:50]}...")
        else:
            print("⚠️ Aucun article récupéré (utilise des données fallback)")
    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_sentiment_analysis():
    """Test de l'analyse de sentiment"""
    print("\n\n🧠 Test de l'analyse de sentiment...")
    print("=" * 60)
    
    analyzer = SentimentAnalyzer()
    
    test_texts = [
        "La bourse de Casablanca affiche une croissance exceptionnelle avec des performances remarquables",
        "Crise économique majeure avec des difficultés importantes sur le marché financier",
        "Le marché reste stable avec des volumes moyens et une volatilité normale"
    ]
    
    for i, text in enumerate(test_texts, 1):
        result = analyzer.analyze_text(text)
        print(f"\n   Test {i}:")
        print(f"   📝 Texte: {text[:60]}...")
        print(f"   📊 Polarité: {result.polarity:.3f} ({analyzer.get_sentiment_label(result.polarity)})")
        print(f"   🎯 Confiance: {result.confidence:.3f}")
        print(f"   ✅ Mots positifs: {', '.join(result.positive_words[:5])}")
        print(f"   ❌ Mots négatifs: {', '.join(result.negative_words[:5])}")


def test_real_scraping():
    """Test du vrai scraping web"""
    print("\n\n🌐 Test du scraping web réel...")
    print("=" * 60)
    
    scraper = CasablancaMarketScraper()
    
    print("\nTentative de connexion à www.casablanca-bourse.com...")
    try:
        import requests
        response = scraper.session.get(scraper.MARKET_URL, timeout=10)
        
        print(f"✅ Connexion réussie!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content Length: {len(response.content)} bytes")
        print(f"   Content Type: {response.headers.get('content-type', 'N/A')}")
        
        # Tenter de parser
        print("\n   Parsing du contenu...")
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Chercher des éléments intéressants
        title = soup.find('title')
        if title:
            print(f"   Titre de la page: {title.get_text()[:100]}")
        
        # Chercher des tables
        tables = soup.find_all('table')
        print(f"   Tables trouvées: {len(tables)}")
        
        # Chercher "MASI"
        masi_mentions = soup.find_all(text=lambda t: t and 'MASI' in t.upper())
        print(f"   Mentions de 'MASI': {len(masi_mentions)}")
        
        if masi_mentions:
            print(f"   Exemples: {[str(m)[:50] for m in masi_mentions[:3]]}")
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print(f"   Type: {type(e).__name__}")


def main():
    """Fonction principale"""
    print("🚀 Test de Récupération de Données Réelles")
    print("=" * 60)
    print("Ce script teste la capacité à récupérer des données réelles")
    print("depuis la Bourse de Casablanca et les médias marocains")
    print("=" * 60)
    
    # Tests
    test_real_scraping()
    test_market_data()
    test_media_data()
    test_sentiment_analysis()
    
    print("\n\n✅ Tests terminés!")
    print("=" * 60)
    print("\n💡 Conseils:")
    print("   - Si le scraping web échoue, vérifiez votre connexion internet")
    print("   - Les données de fallback sont normales en cas d'échec")
    print("   - Pour la production, utilisez une API officielle si disponible")


if __name__ == "__main__":
    main()








