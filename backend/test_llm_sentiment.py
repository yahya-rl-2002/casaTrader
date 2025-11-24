#!/usr/bin/env python3
"""
🤖 Test du LLM Sentiment Analyzer
Test unitaire pour vérifier que l'analyse de sentiment avec GPT fonctionne correctement
"""
import os
import sys
import asyncio
sys.path.append('.')

from app.services.llm_sentiment_service import LLMSentimentAnalyzer


# Articles de test en français (Bourse de Casablanca)
TEST_ARTICLES = [
    {
        'id': 1,
        'title': "La BMCI affiche une croissance record au T3 2025",
        'summary': "La Banque Marocaine du Commerce et de l'Industrie a publié ses résultats trimestriels avec une hausse de 28% du bénéfice net. Les analystes sont optimistes pour l'avenir."
    },
    {
        'id': 2,
        'title': "Craintes de récession sur le marché marocain",
        'summary': "Les investisseurs s'inquiètent de la volatilité croissante du MASI. Les volumes de transaction ont chuté de 15% cette semaine, reflétant une prudence accrue."
    },
    {
        'id': 3,
        'title': "Le secteur bancaire marocain maintient sa stabilité",
        'summary': "Malgré un contexte international incertain, les banques marocaines continuent d'afficher des performances solides. Les provisions pour risques restent maîtrisées."
    },
]


async def test_llm_sentiment():
    """Test de l'analyseur LLM avec des articles de test"""
    
    print("=" * 80)
    print("🤖 Test du LLM Sentiment Analyzer")
    print("=" * 80)
    print()
    
    # Vérifier si la clé API est configurée
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERREUR : La variable d'environnement OPENAI_API_KEY n'est pas définie !")
        print()
        print("Pour configurer la clé API :")
        print("   export OPENAI_API_KEY='sk-proj-...'")
        print()
        print("Pour obtenir une clé API :")
        print("   https://platform.openai.com/api-keys")
        print()
        return False
    
    print("✅ Clé API OpenAI configurée")
    print(f"   Clé : {os.getenv('OPENAI_API_KEY')[:20]}...")
    print()
    
    # Initialiser l'analyseur
    try:
        analyzer = LLMSentimentAnalyzer()
        print(f"✅ LLM Sentiment Analyzer initialisé")
        print(f"   Modèle : {analyzer.model}")
        print(f"   Activé : {analyzer.enabled}")
        print()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        return False
    
    # Tester l'analyse par lot
    print("-" * 80)
    print("📝 Analyse des articles de test...")
    print("-" * 80)
    print()
    
    try:
        results = analyzer.analyze_articles_batch(TEST_ARTICLES)
        
        for i, (article, result) in enumerate(zip(TEST_ARTICLES, results), 1):
            print(f"📰 Article {i}/{len(TEST_ARTICLES)}")
            print(f"   Titre : {article['title']}")
            print(f"   Score : {result.sentiment_score:+.3f} ({result.sentiment_label})")
            print(f"   Explication : {result.reasoning}")
            print()
        
        # Calculer la moyenne
        avg_sentiment = sum(r.sentiment_score for r in results) / len(results)
        normalized_avg = (avg_sentiment + 1.0) * 50.0
        
        print("-" * 80)
        print(f"📊 Résumé de l'analyse")
        print("-" * 80)
        print(f"   Articles analysés : {len(results)}")
        print(f"   Score moyen (LLM) : {avg_sentiment:+.3f}")
        print(f"   Score normalisé   : {normalized_avg:.2f}/100")
        
        # Répartition
        positive = sum(1 for r in results if r.sentiment_score > 0.2)
        neutral = sum(1 for r in results if -0.2 <= r.sentiment_score <= 0.2)
        negative = sum(1 for r in results if r.sentiment_score < -0.2)
        
        print(f"   Répartition :")
        print(f"      Positifs : {positive} ({positive/len(results)*100:.0f}%)")
        print(f"      Neutres  : {neutral} ({neutral/len(results)*100:.0f}%)")
        print(f"      Négatifs : {negative} ({negative/len(results)*100:.0f}%)")
        print()
        
        print("=" * 80)
        print("✅ Test réussi ! Le LLM fonctionne correctement.")
        print("=" * 80)
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse : {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_single_article():
    """Test avec un seul article pour debug"""
    print("=" * 80)
    print("🧪 Test d'un article unique")
    print("=" * 80)
    print()
    
    analyzer = LLMSentimentAnalyzer()
    
    test_article = {
        'title': "Test : La bourse de Casablanca en hausse",
        'summary': "Le MASI a gagné 2% aujourd'hui grâce aux bonnes performances du secteur bancaire."
    }
    
    print(f"📰 Article : {test_article['title']}")
    print()
    
    results = analyzer.analyze_articles_batch([test_article])
    result = results[0]
    
    print(f"✅ Résultat :")
    print(f"   Score : {result.sentiment_score:+.3f}")
    print(f"   Label : {result.sentiment_label}")
    print(f"   Explication : {result.reasoning}")
    print()


async def main():
    """Fonction principale"""
    
    # Test complet
    success = await test_llm_sentiment()
    
    if success:
        # Test unitaire optionnel
        print()
        response = input("Voulez-vous tester un article unique ? (o/n) : ")
        if response.lower() == 'o':
            print()
            await test_single_article()
    
    return success


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur fatale : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
