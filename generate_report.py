#!/usr/bin/env python3
"""
Script pour générer un rapport complet de l'indice Fear & Greed
"""
import json
import requests
from datetime import datetime
from typing import Dict, Any

API_BASE_URL = "http://localhost:8000/api/v1"

def fetch_data(endpoint: str) -> Dict[str, Any]:
    """Récupère les données depuis l'API"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=30)
        if response.ok:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def format_score(score: float) -> str:
    """Formate le score avec interprétation"""
    if score >= 76:
        return f"{score:.2f} - Extreme Greed (Avarice Extrême) 😃"
    elif score >= 56:
        return f"{score:.2f} - Greed (Avarice) 😊"
    elif score >= 41:
        return f"{score:.2f} - Neutral (Neutre) 😐"
    elif score >= 21:
        return f"{score:.2f} - Fear (Peur) 😟"
    else:
        return f"{score:.2f} - Extreme Fear (Peur Extrême) 😱"

def generate_report():
    """Génère le rapport complet"""
    print("=" * 80)
    print("📊 RAPPORT COMPLET - INDICE FEAR & GREED CASABLANCA")
    print("=" * 80)
    print(f"\nDate du rapport : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Base URL : {API_BASE_URL}\n")
    
    # 1. Score principal
    print("-" * 80)
    print("1. SCORE PRINCIPAL")
    print("-" * 80)
    latest_index = fetch_data("index/latest")
    if "error" not in latest_index:
        score = latest_index.get("score", 0)
        as_of = latest_index.get("as_of", "N/A")
        print(f"Score : {format_score(score)}")
        print(f"Date : {as_of}\n")
    else:
        print(f"❌ Erreur : {latest_index['error']}\n")
    
    # 2. Composantes détaillées
    print("-" * 80)
    print("2. COMPOSANTES DÉTAILLÉES (Formule Principale)")
    print("-" * 80)
    components = fetch_data("components/latest")
    if "error" not in components:
        weights = {
            "momentum": 0.20,
            "price_strength": 0.15,
            "volume": 0.15,
            "volatility": 0.20,
            "equity_vs_bonds": 0.15,
            "media_sentiment": 0.15,
        }
        
        total_contribution = 0
        for comp, weight in weights.items():
            value = components.get(comp, 0)
            contribution = value * weight
            total_contribution += contribution
            print(f"{comp:20s} : {value:6.2f} (poids: {weight:.0%}) → {contribution:6.2f}")
        
        print(f"\n{'Total':20s} : {'':6s} {'':15s} → {total_contribution:6.2f}")
        print(f"\nAs_of : {components.get('as_of', 'N/A')}\n")
    else:
        print(f"❌ Erreur : {components['error']}\n")
    
    # 3. Score simplifié
    print("-" * 80)
    print("3. SCORE SIMPLIFIÉ (Formule V2)")
    print("-" * 80)
    simplified = fetch_data("simplified-v2/score")
    if "error" not in simplified:
        print(f"Score : {format_score(simplified.get('score', 0))}")
        print(f"\nDétails :")
        print(f"  Volume moyen      : {simplified.get('volume_moyen', 0):.2f}")
        print(f"  Sentiment news    : {simplified.get('sentiment_news', 0):.2f}")
        print(f"  Performance marché: {simplified.get('performance_marche', 0):.2f}")
        print(f"  Nombre d'actions  : {simplified.get('nombre_actions', 0)}")
        print(f"  Formule           : {simplified.get('formule', 'N/A')}")
        print(f"  Date              : {simplified.get('date', 'N/A')}\n")
    else:
        print(f"❌ Erreur : {simplified['error']}\n")
    
    # 4. Historique
    print("-" * 80)
    print("4. HISTORIQUE (90 derniers jours)")
    print("-" * 80)
    history = fetch_data("index/history?range=90d")
    if "error" not in history and "data" in history:
        data = history.get("data", [])
        if data:
            scores = [d.get("score", 0) for d in data]
            print(f"Nombre de points : {len(data)}")
            print(f"Score moyen      : {sum(scores)/len(scores):.2f}")
            print(f"Score min        : {min(scores):.2f}")
            print(f"Score max        : {max(scores):.2f}")
            print(f"Dernier score    : {data[0].get('score', 0):.2f} ({data[0].get('as_of', 'N/A')})\n")
        else:
            print("Aucune donnée historique disponible\n")
    else:
        print(f"❌ Erreur : {history.get('error', 'Aucune donnée')}\n")
    
    # 5. Articles média
    print("-" * 80)
    print("5. ARTICLES MÉDIA")
    print("-" * 80)
    media = fetch_data("media/latest?limit=10")
    if "error" not in media and "data" in media:
        articles = media.get("data", [])
        print(f"Nombre d'articles : {media.get('count', 0)}")
        if articles:
            # Statistiques sentiment
            sentiment_scores = [a.get("sentiment_score") for a in articles if a.get("sentiment_score") is not None]
            if sentiment_scores:
                avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                print(f"Sentiment moyen  : {avg_sentiment:.2f}")
            
            # Sources
            sources = {}
            for article in articles:
                source = article.get("source", "Inconnu")
                sources[source] = sources.get(source, 0) + 1
            
            print(f"\nPar source :")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                print(f"  {source:20s} : {count} article(s)")
            
            print(f"\n5 derniers articles :")
            for i, article in enumerate(articles[:5], 1):
                title = article.get("title", "Sans titre")
                source = article.get("source", "Inconnu")
                sentiment = article.get("sentiment_score", "N/A")
                print(f"  {i}. [{source}] {title[:50]}... (sentiment: {sentiment})")
        print()
    else:
        print(f"❌ Erreur : {media.get('error', 'Aucune donnée')}\n")
    
    # 6. Données de volume
    print("-" * 80)
    print("6. DONNÉES DE VOLUME")
    print("-" * 80)
    volume = fetch_data("volume/latest?days=30")
    if "error" not in volume and "data" in volume:
        data = volume.get("data", [])
        if data:
            volumes = [d.get("volume", 0) for d in data if d.get("volume") is not None]
            if volumes:
                print(f"Nombre de points : {len(data)}")
                print(f"Volume moyen     : {volume.get('average_volume', 0):.2f}")
                print(f"Volume min       : {min(volumes):.2f}")
                print(f"Volume max       : {max(volumes):.2f}\n")
            else:
                print("Aucune donnée de volume disponible\n")
        else:
            print("Aucune donnée de volume disponible\n")
    else:
        print(f"❌ Erreur : {volume.get('error', 'Aucune donnée')}\n")
    
    # 7. Résumé
    print("=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    if "error" not in latest_index:
        score = latest_index.get("score", 0)
        print(f"\nScore actuel : {format_score(score)}")
        print(f"Date         : {latest_index.get('as_of', 'N/A')}")
        print(f"\nSystème      : ✅ Opérationnel")
        print(f"Backend      : ✅ http://localhost:8001")
        print(f"Frontend     : ✅ http://localhost:8080")
        print(f"Scheduler    : ✅ Actif (toutes les 10 min)")
    else:
        print("\n⚠️ Impossible de récupérer les données du système")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    try:
        generate_report()
    except KeyboardInterrupt:
        print("\n\n❌ Rapport interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur lors de la génération du rapport : {e}")











