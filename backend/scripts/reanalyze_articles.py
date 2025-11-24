#!/usr/bin/env python3
"""
Script pour réanalyser les articles existants avec le nouveau système d'analyse amélioré
"""
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.models.database import get_session, engine
from app.models.schemas import MediaArticle
from app.services.sentiment_service import SentimentAnalyzer
from app.services.llm_sentiment_service import LLMSentimentAnalyzer
from app.core.logging import get_logger

logger = get_logger(__name__)

def reanalyze_articles(use_llm: bool = False):
    """Réanalyser tous les articles existants avec le nouveau système"""
    from app.models.database import SessionLocal
    db: Session = SessionLocal()
    
    try:
        # Récupérer tous les articles
        articles = db.query(MediaArticle).all()
        
        logger.info(f"📰 Réanalyse de {len(articles)} articles avec le nouveau système amélioré...")
        
        # Initialiser les analyseurs
        sentiment_analyzer = SentimentAnalyzer()
        llm_analyzer = LLMSentimentAnalyzer() if use_llm else None
        
        updated_count = 0
        errors = 0
        
        for article in articles:
            try:
                # Préparer le texte à analyser
                text = f"{article.title} {article.summary or ''}"
                
                if use_llm and llm_analyzer and llm_analyzer.enabled:
                    # Utiliser LLM si disponible
                    result = llm_analyzer.analyze_article(
                        title=article.title,
                        summary=article.summary or '',
                        article_id=article.id
                    )
                    new_sentiment_score = result.sentiment_score
                    new_sentiment_label = result.sentiment_label
                else:
                    # Utiliser NLP amélioré
                    result = sentiment_analyzer.analyze_text(text)
                    new_sentiment_score = result.polarity
                    new_sentiment_label = sentiment_analyzer.get_sentiment_label(result.polarity)
                
                # Vérifier si le score a changé
                old_score = article.sentiment_score
                
                # Mettre à jour les scores
                article.sentiment_score = new_sentiment_score
                article.sentiment_label = new_sentiment_label
                
                if old_score != new_sentiment_score:
                    logger.info(
                        f"✅ Article {article.id}: {old_score:.3f} → {new_sentiment_score:.3f} "
                        f"({article.title[:50]}...)"
                    )
                    updated_count += 1
                else:
                    logger.debug(f"➡️  Article {article.id}: Score inchangé ({new_sentiment_score:.3f})")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors de l'analyse de l'article {article.id}: {e}")
                errors += 1
                continue
        
        # Sauvegarder les modifications
        db.commit()
        
        logger.info(
            f"✅ Réanalyse terminée : {updated_count} articles mis à jour, "
            f"{len(articles) - updated_count} inchangés, {errors} erreurs"
        )
        
        return {
            "total_articles": len(articles),
            "updated": updated_count,
            "unchanged": len(articles) - updated_count,
            "errors": errors
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la réanalyse : {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()

def recalculate_media_sentiment():
    """Recalculer le media_sentiment avec les nouveaux scores"""
    from app.services.component_calculator import ComponentCalculator
    from app.models.database import SessionLocal
    from app.models.schemas import MediaArticle
    from datetime import date, timedelta
    
    db: Session = SessionLocal()
    
    try:
        # Récupérer les articles des 7 derniers jours
        cutoff_date = date.today() - timedelta(days=7)
        recent_articles = db.query(MediaArticle).filter(
            MediaArticle.published_at >= cutoff_date
        ).all()
        
        # Calculer le nouveau media_sentiment
        calculator = ComponentCalculator()
        new_sentiment = calculator._calculate_media_sentiment(recent_articles, date.today())
        
        logger.info(f"📊 Nouveau media_sentiment calculé : {new_sentiment:.2f}")
        
        return new_sentiment
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du recalcul : {e}", exc_info=True)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Réanalyser les articles existants")
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Utiliser LLM (GPT) pour l'analyse au lieu du NLP amélioré"
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("🔄 RÉANALYSE DES ARTICLES EXISTANTS")
    print("=" * 80)
    print(f"\nMode : {'LLM (GPT)' if args.use_llm else 'NLP amélioré (contexte marocain)'}")
    print()
    
    # Réanalyser les articles
    result = reanalyze_articles(use_llm=args.use_llm)
    
    print("\n" + "=" * 80)
    print("📊 RÉSULTATS")
    print("=" * 80)
    print(f"Total articles : {result['total_articles']}")
    print(f"Articles mis à jour : {result['updated']}")
    print(f"Articles inchangés : {result['unchanged']}")
    print(f"Erreurs : {result['errors']}")
    
    # Recalculer le media_sentiment
    print("\n" + "=" * 80)
    print("📈 RECALCUL DU MEDIA_SENTIMENT")
    print("=" * 80)
    
    new_sentiment = recalculate_media_sentiment()
    print(f"\nNouveau media_sentiment : {new_sentiment:.2f}")
    
    print("\n✅ Réanalyse terminée !")
    print("\n💡 Conseil : Le media_sentiment sera mis à jour lors du prochain calcul de l'indice.")

