from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Query, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.database import get_session
from app.models.schemas import IndexScore
from app.pipelines.ingestion.market_scraper import CasablancaMarketScraper
from app.core.logging import get_logger
from app.services.cache_service import get_cache_service

router = APIRouter()
logger = get_logger(__name__)

# Service de cache Redis (avec fallback en mémoire)
cache_service = get_cache_service()
CACHE_DURATION_SECONDS = 300  # 5 minutes


@router.get("/latest", summary="Latest volume data for heatmap")
async def get_latest_volume(
    days: int = Query(30, ge=7, le=90, description="Number of days to return"),
    db: Session = Depends(get_session)
) -> dict:
    """
    Récupère les données de volume récentes pour la heatmap.
    
    - **days**: Nombre de jours à retourner (7-90, défaut: 30)
    
    **Optimisation** : Utilise un cache Redis (ou mémoire) de 5 minutes pour éviter les scrapings fréquents.
    """
    cache_key = f"volume:latest:{days}"
    
    # Vérifier le cache
    cached_data = cache_service.get(cache_key)
    if cached_data is not None:
        logger.debug(f"✅ Cache hit: volume data for {days} days")
        return cached_data
    
    try:
        # D'abord essayer de récupérer depuis la DB (historique des index)
        # En utilisant les données de volume des index calculés récemment
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_indexes = (
            db.query(IndexScore)
            .filter(IndexScore.as_of >= cutoff_date)
            .order_by(IndexScore.as_of.asc())
            .all()
        )
        
        if recent_indexes and len(recent_indexes) >= 5:
            # Utiliser les données de volume des index
            logger.debug(f"Using volume data from {len(recent_indexes)} index records")
            
            # Calculer le volume moyen pour la normalisation
            volumes = [idx.volume for idx in recent_indexes if idx.volume is not None]
            if volumes:
                avg_volume = sum(volumes) / len(volumes)
                volume_max = max(volumes)
                volume_min = min(volumes)
                
                volume_data = []
                for idx in recent_indexes:
                    if idx.volume is not None:
                        # Normaliser le volume (0-100)
                        if volume_max > volume_min:
                            normalized = ((idx.volume - volume_min) / (volume_max - volume_min)) * 100
                        else:
                            normalized = 100
                        
                        volume_data.append({
                            "date": idx.as_of.date().isoformat(),
                            "volume": idx.volume,
                            "normalized_volume": round(normalized, 2),
                            "close": None,  # Pas disponible dans IndexScore
                            "change_percent": None,
                        })
                
                result = {
                    "data": volume_data,
                    "count": len(volume_data),
                    "days": days,
                    "average_volume": avg_volume,
                }
                
                # Mettre en cache Redis
                cache_service.set(cache_key, result, ttl_seconds=CACHE_DURATION_SECONDS)
                return result
        
        # Fallback: scraper si pas assez de données en DB
        logger.debug(f"Not enough data in DB, scraping volume data for {days} days")
        scraper = CasablancaMarketScraper()
        historical_data = scraper.fetch_historical_data(days=days)
        
        if not historical_data:
            logger.warning(f"No historical data found for {days} days")
            return {
                "data": [],
                "count": 0,
                "days": days,
                "average_volume": 0,
                "message": "No data available"
            }
        
        # Calculer le volume moyen pour la normalisation
        avg_volume = sum(d.volume for d in historical_data) / len(historical_data)
        
        # Convertir en format API
        volume_data = []
        for data in historical_data:
            change_percent = 0
            if data.open_price > 0:
                change_percent = ((data.close_price - data.open_price) / data.open_price * 100)
            
            volume_data.append({
                "date": data.date.isoformat(),
                "volume": data.volume,
                "normalized_volume": (data.volume / avg_volume) * 100 if avg_volume > 0 else 100,
                "close": data.close_price,
                "change_percent": change_percent,
            })
        
        result = {
            "data": volume_data,
            "count": len(volume_data),
            "days": days,
            "average_volume": avg_volume,
        }
        
        # Mettre en cache Redis
        cache_service.set(cache_key, result, ttl_seconds=CACHE_DURATION_SECONDS)
        return result
    
    except Exception as e:
        logger.error(f"Error fetching volume data: {e}", exc_info=True)
        return {
            "data": [],
            "count": 0,
            "days": days,
            "average_volume": 0,
            "error": str(e)
        }


@router.get("/stats", summary="Volume statistics")
async def get_volume_stats(
    days: int = Query(30, ge=7, le=365, description="Number of days for statistics")
) -> dict:
    """
    Récupère des statistiques sur le volume de trading.
    
    - **days**: Période d'analyse (7-365 jours, défaut: 30)
    """
    try:
        scraper = CasablancaMarketScraper()
        historical_data = scraper.fetch_historical_data(days=days)
        
        if not historical_data:
            return {
                "period_days": days,
                "trading_days": 0,
                "volume_stats": {
                    "average": 0,
                    "min": 0,
                    "max": 0,
                    "total": 0,
                },
                "message": "No data available"
            }
        
        volumes = [d.volume for d in historical_data]
        
        return {
            "period_days": days,
            "trading_days": len(historical_data),
            "volume_stats": {
                "average": sum(volumes) / len(volumes),
                "min": min(volumes),
                "max": max(volumes),
                "total": sum(volumes),
            },
        }
    
    except Exception as e:
        logger.error(f"Error fetching volume stats: {e}")
        return {
            "period_days": days,
            "trading_days": 0,
            "volume_stats": {
                "average": 0,
                "min": 0,
                "max": 0,
                "total": 0,
            },
            "error": str(e)
        }


@router.get("/trend", summary="Volume trend analysis")
async def get_volume_trend() -> dict:
    """
    Analyse la tendance du volume de trading (croissant, décroissant, stable).
    """
    try:
        scraper = CasablancaMarketScraper()
        historical_data = scraper.fetch_historical_data(days=30)
        
        if len(historical_data) < 2:
            return {
                "trend": "insufficient_data",
                "message": "Not enough data to determine trend",
            }
        
        # Comparer première et deuxième moitié
        mid_point = len(historical_data) // 2
        first_half = historical_data[:mid_point]
        second_half = historical_data[mid_point:]
        
        first_half_avg = sum(d.volume for d in first_half) / len(first_half)
        second_half_avg = sum(d.volume for d in second_half) / len(second_half)
        
        change_percent = ((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0
        
        # Déterminer la tendance
        if change_percent > 10:
            trend = "increasing"
            emoji = "📈"
        elif change_percent < -10:
            trend = "decreasing"
            emoji = "📉"
        else:
            trend = "stable"
            emoji = "➡️"
        
        return {
            "trend": trend,
            "emoji": emoji,
            "change_percent": round(change_percent, 2),
            "first_half_avg": round(first_half_avg, 2),
            "second_half_avg": round(second_half_avg, 2),
            "period_days": 30,
            "data_points": len(historical_data),
        }
    
    except Exception as e:
        logger.error(f"Error analyzing volume trend: {e}")
        return {
            "trend": "error",
            "message": str(e),
        }
