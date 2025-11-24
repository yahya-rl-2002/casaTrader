from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.database import get_session
from app.models.schemas import IndexScore
from app.services.simplified_index_calculator import SimplifiedIndexCalculator
from app.core.logging import get_logger
from app.services.cache_service import get_cache_service

router = APIRouter()
logger = get_logger(__name__)

# Service de cache Redis (avec fallback en mémoire)
cache_service = get_cache_service()
CACHE_DURATION_SECONDS = 300  # 5 minutes


class SimplifiedScoreResponse(BaseModel):
    """Réponse du score simplifié"""
    score: float
    volume_moyen: float
    sentiment_news: float
    performance_marche: float
    nombre_actions: int
    date: str
    formule: str
    interpretation: str


@router.get("/score", summary="Calculate simplified Fear & Greed score", response_model=SimplifiedScoreResponse)
async def get_simplified_score(db: Session = Depends(get_session)) -> SimplifiedScoreResponse:
    """
    Calcule le score Fear & Greed selon la formule simplifiée :
    
    **Score = (Volume moyen + Sentiment news + Performance marché) / Nombre d'actions**
    
    Où :
    - **Volume moyen** : Volume journalier moyen MASI sur 20 jours (0-100)
    - **Sentiment news** : Degré d'optimisme des news via NLP (0-100)
    - **Performance marché** : Actions positives vs négatives (0-100)
    - **Nombre d'actions** : Nombre total d'actions cotées sur MASI (~76)
    
    Retourne un score entre 0 (Extreme Fear) et 100 (Extreme Greed).
    
    **Optimisation** : Utilise un cache Redis (ou mémoire) de 5 minutes pour éviter les recalculs fréquents.
    Si une donnée récente existe en DB, utilise les composants du dernier index.
    """
    cache_key = "simplified:score:v2"
    
    # Vérifier le cache
    cached_data = cache_service.get(cache_key)
    if cached_data is not None:
        logger.debug("✅ Cache hit: simplified score")
        return cached_data
    
    try:
        # D'abord, essayer d'utiliser les données de la DB (plus rapide)
        latest_index = db.query(IndexScore).order_by(desc(IndexScore.as_of)).first()
        
        if latest_index and latest_index.as_of and \
           (datetime.now() - latest_index.as_of.replace(tzinfo=None)).total_seconds() < 600:  # Moins de 10 minutes
            # Utiliser les composants de la DB pour calculer un score simplifié
            logger.debug("Using latest index data from DB for simplified score")
            
            # Estimation basée sur les composants existants
            volume_score = latest_index.volume or 50.0
            sentiment_score = latest_index.media_sentiment or 50.0
            # Performance marché estimée à partir du price_strength
            performance_score = latest_index.price_strength or 50.0
            
            # Calcul simplifié basé sur les composants
            nombre_actions = 76  # Valeur fixe pour MASI
            score = (volume_score + sentiment_score + performance_score) / nombre_actions * 100
            
            result = SimplifiedScoreResponse(
                score=round(score, 2),
                volume_moyen=round(volume_score, 2),
                sentiment_news=round(sentiment_score, 2),
                performance_marche=round(performance_score, 2),
                nombre_actions=nombre_actions,
                date=latest_index.as_of.date().isoformat(),
                formule=f"({volume_score:.2f} + {sentiment_score:.2f} + {performance_score:.2f}) / {nombre_actions}",
                interpretation="Calculé à partir des composants de l'indice principal"
            )
            
            # Mettre en cache Redis
            cache_service.set(cache_key, result, ttl_seconds=CACHE_DURATION_SECONDS)
            return result
    except Exception as e:
        logger.warning(f"Error using DB data for simplified score: {e}, falling back to calculation")
    
    # Si pas de données récentes en DB, calculer (mais avec cache)
    logger.debug("Calculating simplified score from scratch")
    calculator = SimplifiedIndexCalculator()
    result_data = await calculator.calculate_index()
    
    result = SimplifiedScoreResponse(
        score=result_data.score,
        volume_moyen=result_data.volume_moyen,
        sentiment_news=result_data.sentiment_news,
        performance_marche=result_data.performance_marche,
        nombre_actions=result_data.nombre_actions,
        date=result_data.date.isoformat(),
        formule=result_data.details["formule"],
        interpretation=result_data.details["interpretation"],
    )
    
    # Mettre en cache Redis
    cache_service.set(cache_key, result, ttl_seconds=CACHE_DURATION_SECONDS)
    return result


@router.get("/details", summary="Get detailed breakdown of simplified calculation")
async def get_simplified_details():
    """
    Retourne le détail complet du calcul simplifié avec toutes les métriques.
    """
    calculator = SimplifiedIndexCalculator()
    result = await calculator.calculate_index()
    
    return {
        "score_final": result.score,
        "date": result.date.isoformat(),
        "composantes": {
            "volume_moyen": {
                "valeur": result.volume_moyen,
                "description": "Volume journalier moyen MASI sur 20 jours",
                "echelle": "0-100",
            },
            "sentiment_news": {
                "valeur": result.sentiment_news,
                "description": "Degré d'optimisme des news (analyse NLP)",
                "echelle": "0-100",
            },
            "performance_marche": {
                "valeur": result.performance_marche,
                "description": "Performance marché (jours positifs vs négatifs)",
                "echelle": "0-100",
            },
        },
        "denominateur": {
            "nombre_actions": result.nombre_actions,
            "description": "Nombre total d'actions cotées sur MASI",
        },
        "calcul": {
            "formule": result.details["formule"],
            "numerateur": result.details["numerateur"],
            "score_final": result.score,
        },
        "interpretation": result.details["interpretation"],
    }







