#!/usr/bin/env python3
"""
🧪 TEST DE LA FORMULE SIMPLIFIÉE
Test du calcul d'indice basé sur : (Volume + Sentiment + Performance) / Nombre d'actions
"""
import sys
import asyncio
sys.path.append('.')

from app.services.simplified_index_calculator import SimplifiedIndexCalculator


def print_header(title: str, symbol: str = "="):
    """Print a formatted header"""
    print(f"\n{symbol * 80}")
    print(f"  {title}")
    print(f"{symbol * 80}\n")


async def main():
    print_header("🧪 TEST DE LA FORMULE SIMPLIFIÉE", "=")
    
    print("📐 Formule utilisée :")
    print("   Score = (Volume moyen + Sentiment news + Performance marché) / Nombre d'actions")
    print()
    print("   Où :")
    print("   • Volume moyen : Volume journalier MASI sur 20 jours (0-100)")
    print("   • Sentiment news : Degré d'optimisme des news via NLP (0-100)")
    print("   • Performance marché : Jours positifs vs négatifs (0-100)")
    print("   • Nombre d'actions : Total des actions cotées sur MASI (~76)")
    
    print_header("🚀 CALCUL EN COURS...", "-")
    
    calculator = SimplifiedIndexCalculator()
    result = await calculator.calculate_index()
    
    print_header("📊 RÉSULTATS", "=")
    
    print(f"\n   🎯 SCORE FINAL : {result.score:.2f} / 100")
    print(f"   📅 Date : {result.date}")
    print()
    
    print("   📈 DÉTAIL DES COMPOSANTES :")
    print(f"      1️⃣  Volume moyen (20j) : {result.volume_moyen:.2f} / 100")
    print(f"      2️⃣  Sentiment news (NLP) : {result.sentiment_news:.2f} / 100")
    print(f"      3️⃣  Performance marché : {result.performance_marche:.2f} / 100")
    print(f"      ➗  Nombre d'actions MASI : {result.nombre_actions}")
    print()
    
    print("   🔢 CALCUL :")
    print(f"      Numérateur = {result.volume_moyen:.2f} + {result.sentiment_news:.2f} + {result.performance_marche:.2f}")
    print(f"                 = {result.details['numerateur']:.2f}")
    print(f"      Score brut = {result.details['numerateur']:.2f} / {result.nombre_actions}")
    print(f"                 = {result.details['numerateur'] / result.nombre_actions:.2f}")
    print(f"      Score normalisé (x10) = {result.score:.2f} / 100")
    print()
    
    print(f"   💡 INTERPRÉTATION :")
    print(f"      {result.details['interpretation']}")
    
    # Comparaison avec des seuils
    print_header("📊 ANALYSE", "-")
    
    if result.score >= 75:
        emoji = "🤑"
        niveau = "EXTREME GREED"
        conseil = "Le marché est surévalué, prudence recommandée"
    elif result.score >= 60:
        emoji = "😊"
        niveau = "GREED"
        conseil = "Le marché est optimiste, surveiller les excès"
    elif result.score >= 40:
        emoji = "😐"
        niveau = "NEUTRAL"
        conseil = "Le marché est équilibré, bon moment pour analyser"
    elif result.score >= 25:
        emoji = "😟"
        niveau = "FEAR"
        conseil = "Le marché est pessimiste, opportunités possibles"
    else:
        emoji = "😱"
        niveau = "EXTREME FEAR"
        conseil = "Le marché est sous-évalué, occasion d'achat potentielle"
    
    print(f"   {emoji} Niveau : {niveau}")
    print(f"   💭 Conseil : {conseil}")
    
    # Analyse par composante
    print_header("🔍 ANALYSE DÉTAILLÉE", "-")
    
    print("   Volume moyen :")
    if result.volume_moyen > 70:
        print("      ✅ Volume élevé - Forte activité sur le marché")
    elif result.volume_moyen > 40:
        print("      ⚠️  Volume modéré - Activité normale")
    else:
        print("      ❌ Volume faible - Peu d'activité")
    
    print()
    print("   Sentiment des news :")
    if result.sentiment_news > 60:
        print("      ✅ Sentiment positif - Les médias sont optimistes")
    elif result.sentiment_news > 40:
        print("      ⚠️  Sentiment neutre - Médias partagés")
    else:
        print("      ❌ Sentiment négatif - Les médias sont pessimistes")
    
    print()
    print("   Performance marché :")
    if result.performance_marche > 60:
        print("      ✅ Performance positive - Plus d'actions en hausse")
    elif result.performance_marche > 40:
        print("      ⚠️  Performance mixte - Marché équilibré")
    else:
        print("      ❌ Performance négative - Plus d'actions en baisse")
    
    print_header("🌐 API ENDPOINTS", "-")
    
    print("   📡 Nouveaux endpoints disponibles :")
    print("      • GET /api/v1/simplified-v2/score")
    print("        → Score simplifié avec détails")
    print()
    print("      • GET /api/v1/simplified-v2/details")
    print("        → Détails complets du calcul")
    print()
    print("   🔗 Exemples :")
    print("      curl http://localhost:8000/api/v1/simplified-v2/score")
    print("      curl http://localhost:8000/api/v1/simplified-v2/details")
    
    print_header("✅ TEST TERMINÉ", "=")
    
    print(f"\n   🎯 Score calculé : {result.score:.2f} / 100")
    print(f"   📊 Formule : {result.details['formule']}")
    print(f"   💡 {result.details['interpretation']}")
    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu")
    except Exception as e:
        print(f"\n\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()







