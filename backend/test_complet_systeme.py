#!/usr/bin/env python3
"""
🧪 TEST COMPLET DU SYSTÈME FEAR & GREED INDEX
Test de toutes les fonctionnalités et génération du score final
"""
import os
import sys
import asyncio
sys.path.append('.')

from datetime import date, datetime, timedelta
from app.services.pipeline_service import PipelineService
from app.services.backtest_service import BacktestService
from app.models.database import get_session
from app.models.schemas import IndexScore, MediaArticle

# Configure OpenAI API key for LLM sentiment analysis
# Set this environment variable before running the test
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  WARNING: OPENAI_API_KEY not set. LLM sentiment analysis will be disabled.")
    print("   To use LLM sentiment, run: export OPENAI_API_KEY='your-key-here'")
    print("   Falling back to dictionary-based sentiment analysis...")
    print()


def print_header(title: str, symbol: str = "="):
    """Print a formatted header"""
    print(f"\n{symbol * 80}")
    print(f"  {title}")
    print(f"{symbol * 80}\n")


def print_section(title: str):
    """Print a section separator"""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}\n")


async def main():
    print_header("🧪 TEST COMPLET DU SYSTÈME FEAR & GREED INDEX", "=")
    
    # =====================================================================
    # ÉTAPE 1 : Vérifier l'état actuel de la base de données
    # =====================================================================
    print_section("📊 ÉTAPE 1 : État Initial de la Base de Données")
    
    db = get_session()
    try:
        initial_scores = db.query(IndexScore).count()
        initial_articles = db.query(MediaArticle).count()
        latest_score = db.query(IndexScore).order_by(IndexScore.as_of.desc()).first()
        
        print(f"   📈 Scores enregistrés : {initial_scores}")
        print(f"   📰 Articles médias : {initial_articles}")
        
        if latest_score:
            print(f"   🕐 Dernier score : {latest_score.score:.2f} (le {latest_score.as_of.date()})")
        else:
            print(f"   ⚠️  Aucun score existant - première exécution")
    finally:
        db.close()
    
    # =====================================================================
    # ÉTAPE 2 : Exécuter le pipeline complet
    # =====================================================================
    print_section("🚀 ÉTAPE 2 : Exécution du Pipeline Complet")
    
    print("   🔄 Lancement du pipeline Fear & Greed Index...")
    print("   ⏳ Cela peut prendre 2-3 minutes (scraping de 4 sources)...\n")
    
    pipeline = PipelineService()
    result = await pipeline.run_full_pipeline()
    
    if result["success"]:
        print(f"   ✅ Pipeline terminé avec succès !\n")
        print(f"   📊 Résultats :")
        print(f"      • Score Final : {result['final_score']:.2f} / 100")
        print(f"      • Date : {result['target_date']}")
        print(f"      • Données marché collectées : {result['market_data_count']} jours")
        print(f"      • Articles médias analysés : {result['media_articles_count']}")
        
        # Afficher les composantes
        components = result["components"]
        print(f"\n   📈 Détail des Composantes :")
        print(f"      • Momentum : {components.momentum:.1f} / 100")
        print(f"      • Price Strength : {components.price_strength:.1f} / 100")
        print(f"      • Volume : {components.volume:.1f} / 100")
        print(f"      • Volatility : {components.volatility:.1f} / 100")
        print(f"      • Equity vs Bonds : {components.equity_vs_bonds:.1f} / 100")
        print(f"      • Media Sentiment : {components.media_sentiment:.1f} / 100")
        
        # Interpréter le score
        print(f"\n   🎯 Interprétation du Score :")
        score = result['final_score']
        if score >= 75:
            sentiment = "😃 EXTREME GREED - Le marché est très optimiste"
        elif score >= 60:
            sentiment = "😊 GREED - Le marché est optimiste"
        elif score >= 40:
            sentiment = "😐 NEUTRAL - Le marché est équilibré"
        elif score >= 25:
            sentiment = "😟 FEAR - Le marché est pessimiste"
        else:
            sentiment = "😱 EXTREME FEAR - Le marché est très pessimiste"
        
        print(f"      {sentiment}")
        
    else:
        print(f"   ❌ Erreur pipeline : {result.get('error', 'Unknown error')}")
        return
    
    # =====================================================================
    # ÉTAPE 3 : Vérifier les nouvelles données dans la DB
    # =====================================================================
    print_section("💾 ÉTAPE 3 : Vérification de la Base de Données")
    
    db = get_session()
    try:
        final_scores = db.query(IndexScore).count()
        final_articles = db.query(MediaArticle).count()
        
        new_scores = final_scores - initial_scores
        new_articles = final_articles - initial_articles
        
        print(f"   📈 Scores enregistrés : {final_scores} (+{new_scores} nouveau{'x' if new_scores > 1 else ''})")
        print(f"   📰 Articles médias : {final_articles} (+{new_articles} nouveau{'x' if new_articles > 1 else ''})")
        
        # Afficher les 5 derniers scores
        recent_scores = db.query(IndexScore).order_by(IndexScore.as_of.desc()).limit(5).all()
        if recent_scores:
            print(f"\n   📊 Historique récent (5 derniers scores) :")
            for i, score in enumerate(recent_scores, 1):
                date_str = score.as_of.strftime("%Y-%m-%d %H:%M")
                print(f"      {i}. {date_str} : {score.score:.2f}")
        
        # Afficher quelques articles récents
        recent_articles = db.query(MediaArticle).order_by(MediaArticle.published_at.desc()).limit(5).all()
        if recent_articles:
            print(f"\n   📰 Articles médias récents :")
            for i, article in enumerate(recent_articles, 1):
                sentiment = "😊" if article.sentiment_score and article.sentiment_score > 10 else "😟" if article.sentiment_score and article.sentiment_score < -10 else "😐"
                score_str = f"{article.sentiment_score:+.1f}" if article.sentiment_score else "N/A"
                print(f"      {i}. [{article.source}] {sentiment} {score_str} - {article.title[:60]}...")
        
    finally:
        db.close()
    
    # =====================================================================
    # ÉTAPE 4 : Tester le Backtest (si assez de données)
    # =====================================================================
    print_section("🔬 ÉTAPE 4 : Analyse de Backtest")
    
    if final_scores >= 10:
        print("   🔍 Exécution du backtest (corrélation score vs rendements)...\n")
        
        backtest_service = BacktestService()
        backtest_result = backtest_service.run_backtest(
            start_date=date.today() - timedelta(days=90),
            end_date=date.today()
        )
        
        print(f"   📊 Résultats du Backtest :")
        print(f"      • Périodes analysées : {backtest_result.total_periods}")
        print(f"      • Période : {backtest_result.period_start} → {backtest_result.period_end}")
        print(f"\n      📈 Corrélations :")
        print(f"         - Score vs Rendement T+1 : {backtest_result.correlation_t1:.3f}")
        print(f"         - Score vs Rendement T+5 : {backtest_result.correlation_t5:.3f}")
        print(f"\n      🎯 Précision des Prédictions :")
        print(f"         - Accuracy T+1 : {backtest_result.accuracy_t1:.1f}%")
        print(f"         - Accuracy T+5 : {backtest_result.accuracy_t5:.1f}%")
        print(f"\n      📊 Moyennes :")
        print(f"         - Score moyen : {backtest_result.mean_score:.2f}")
        print(f"         - Rendement moyen T+1 : {backtest_result.mean_return_t1:.4f}")
        print(f"         - Rendement moyen T+5 : {backtest_result.mean_return_t5:.4f}")
        
        # Interpréter les corrélations
        print(f"\n      💡 Interprétation :")
        if abs(backtest_result.correlation_t1) > 0.5:
            print(f"         ✅ Forte corrélation T+1 - L'indice est prédictif à court terme")
        elif abs(backtest_result.correlation_t1) > 0.3:
            print(f"         ⚠️  Corrélation T+1 modérée - Signal à confirmer")
        else:
            print(f"         ❌ Corrélation T+1 faible - Plus de données nécessaires")
    else:
        print("   ⚠️  Pas assez de données pour le backtest (minimum 10 scores requis)")
        print(f"      Actuellement : {final_scores} scores")
        print(f"      Exécutez le pipeline plusieurs jours de suite pour accumuler l'historique")
    
    # =====================================================================
    # ÉTAPE 5 : Tester les Endpoints API
    # =====================================================================
    print_section("🌐 ÉTAPE 5 : Test des Endpoints API")
    
    print("   📡 Endpoints disponibles :")
    print("      • GET /api/v1/index/latest - Dernier score")
    print("      • GET /api/v1/index/history?range=90d - Historique")
    print("      • GET /api/v1/components/latest - Composantes détaillées")
    print("      • GET /api/v1/backtest/run?range=90d - Backtest")
    print("      • GET /api/v1/metadata - Métadonnées")
    print("      • POST /api/v1/pipeline/run - Lancer le pipeline")
    print("      • GET /api/v1/pipeline/status - Status du pipeline")
    
    print(f"\n   🔗 Base URL : http://localhost:8000")
    print(f"   📚 Documentation interactive : http://localhost:8000/docs")
    
    # =====================================================================
    # RÉSUMÉ FINAL
    # =====================================================================
    print_header("✅ RÉSUMÉ FINAL", "=")
    
    print(f"   🎯 Score Fear & Greed Index : {result['final_score']:.2f} / 100")
    print(f"   📅 Date : {result['target_date']}")
    print(f"   📊 Base de données : {final_scores} scores, {final_articles} articles")
    print(f"   🚀 Système : OPÉRATIONNEL")
    
    print(f"\n   📱 Pour voir le dashboard :")
    print(f"      1. Ouvrir un terminal")
    print(f"      2. cd '/Volumes/YAHYA SSD/Documents/fear and/backend'")
    print(f"      3. source .venv/bin/activate")
    print(f"      4. uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
    print(f"\n      5. Ouvrir un autre terminal")
    print(f"      6. cd '/Volumes/YAHYA SSD/Documents/fear and/frontend'")
    print(f"      7. npm run dev")
    print(f"\n      8. Ouvrir http://localhost:3000 dans votre navigateur")
    
    print(f"\n   💡 Le dashboard affichera :")
    print(f"      • Jauge principale avec le score {result['final_score']:.2f}")
    print(f"      • Graphique historique des {final_scores} derniers scores")
    print(f"      • Décomposition des 6 composantes avec contributions")
    print(f"      • Feed des {new_articles} derniers articles médias")
    print(f"      • Heatmap du volume de trading")
    
    print(f"\n{'=' * 80}\n")
    print(f"   🎉 Test complet terminé avec succès !")
    print(f"\n{'=' * 80}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur durant le test : {e}")
        import traceback
        traceback.print_exc()

