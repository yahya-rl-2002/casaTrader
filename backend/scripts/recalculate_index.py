#!/usr/bin/env python3
"""
Script pour recalculer l'indice avec les articles réanalysés
"""
import sys
import os
from pathlib import Path
from datetime import date

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.schemas import MediaArticle, IndexScore
from app.services.component_calculator import ComponentCalculator
from app.pipelines.ingestion.market_scraper import CasablancaMarketScraper
from app.core.logging import get_logger

logger = get_logger(__name__)

def recalculate_index():
    """Recalculer l'indice avec les articles réanalysés"""
    db: Session = SessionLocal()
    
    try:
        # Récupérer les articles des 7 derniers jours
        from datetime import timedelta
        cutoff_date = date.today() - timedelta(days=7)
        recent_articles = db.query(MediaArticle).filter(
            MediaArticle.published_at >= cutoff_date
        ).all()
        
        logger.info(f"📰 Récupération de {len(recent_articles)} articles récents...")
        
        # Récupérer les données du marché
        scraper = CasablancaMarketScraper()
        historical_data = scraper.fetch_historical_data(days=252)
        
        logger.info(f"📊 Récupération de {len(historical_data)} points de données du marché...")
        
        # Calculer les composantes
        calculator = ComponentCalculator()
        components = calculator.calculate_all_components(
            historical_data=historical_data,
            media_articles=recent_articles,
            current_date=date.today()
        )
        
        # Calculer le score final
        final_score = calculator.calculate_composite_score(components)
        
        logger.info(f"📈 Nouveau score calculé : {final_score:.2f}")
        logger.info(f"📊 Media Sentiment : {components.media_sentiment:.2f}")
        
        # Sauvegarder le nouveau score
        index_score = IndexScore(
            as_of=date.today(),
            score=final_score,
            momentum=components.momentum,
            price_strength=components.price_strength,
            volume=components.volume,
            volatility=components.volatility,
            equity_vs_bonds=components.equity_vs_bonds,
            media_sentiment=components.media_sentiment
        )
        
        db.add(index_score)
        db.commit()
        
        logger.info("✅ Nouveau score sauvegardé dans la base de données")
        
        return {
            "final_score": final_score,
            "media_sentiment": components.media_sentiment,
            "components": {
                "momentum": components.momentum,
                "price_strength": components.price_strength,
                "volume": components.volume,
                "volatility": components.volatility,
                "equity_vs_bonds": components.equity_vs_bonds,
                "media_sentiment": components.media_sentiment
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du recalcul : {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 80)
    print("🔄 RECALCUL DE L'INDICE AVEC LES ARTICLES RÉANALYSÉS")
    print("=" * 80)
    print()
    
    result = recalculate_index()
    
    print("\n" + "=" * 80)
    print("📊 NOUVEAUX RÉSULTATS")
    print("=" * 80)
    print(f"Score final : {result['final_score']:.2f}")
    print(f"Media Sentiment : {result['media_sentiment']:.2f}")
    print(f"\n📈 COMPOSANTES :")
    comp = result['components']
    print(f"   Momentum : {comp['momentum']:.2f}")
    print(f"   Price Strength : {comp['price_strength']:.2f}")
    print(f"   Volume : {comp['volume']:.2f}")
    print(f"   Volatility : {comp['volatility']:.2f}")
    print(f"   Equity vs Bonds : {comp['equity_vs_bonds']:.2f}")
    print(f"   Media Sentiment : {comp['media_sentiment']:.2f}")
    
    print("\n✅ Recalcul terminé !")
    print(f"\n💡 Le nouveau media_sentiment ({result['media_sentiment']:.2f}) est maintenant dans la base de données !")

