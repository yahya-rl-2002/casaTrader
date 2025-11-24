"""
Endpoints de monitoring et observabilité
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.core.monitoring import get_metrics_response
from app.core.logging import get_logger
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter()
logger = get_logger(__name__)


class HealthStatus(BaseModel):
    """Statut de santé du système"""
    status: str
    timestamp: datetime
    version: str
    environment: str
    uptime_seconds: Optional[float] = None


class DatabaseHealth(BaseModel):
    """Statut de la base de données"""
    status: str
    response_time_ms: Optional[float] = None
    error: Optional[str] = None


class SystemHealth(BaseModel):
    """Santé complète du système"""
    overall: HealthStatus
    database: DatabaseHealth
    cache: Optional[dict] = None
    scheduler: Optional[dict] = None


# Timestamp de démarrage pour calculer l'uptime
_start_time = datetime.now()


def get_uptime_seconds() -> float:
    """Calcule l'uptime en secondes"""
    return (datetime.now() - _start_time).total_seconds()


@router.get("/health", summary="Health check complet", response_model=SystemHealth)
async def health_check(
    db: Session = Depends(get_db)
) -> SystemHealth:
    """
    Health check complet du système
    
    Vérifie:
    - Statut général de l'API
    - Connexion à la base de données
    - Statut du cache (si configuré)
    - Statut du scheduler
    """
    from app.core.config import settings
    from app.services.cache_service import get_cache_service
    from app.main import app
    
    # Health général
    overall = HealthStatus(
        status="healthy",
        timestamp=datetime.now(),
        version="0.1.0",
        environment=settings.environment,
        uptime_seconds=get_uptime_seconds()
    )
    
    # Health base de données
    db_health = check_database_health(db)
    
    # Health cache
    cache_health = None
    try:
        cache_service = get_cache_service()
        cache_stats = cache_service.get_stats()
        cache_health = {
            "status": "available" if cache_stats else "unavailable",
            "stats": cache_stats
        }
    except Exception as e:
        logger.warning(f"Cache health check failed: {e}")
        cache_health = {"status": "error", "error": str(e)}
    
    # Health scheduler
    scheduler_health = None
    try:
        scheduler_service = getattr(app.state, 'scheduler_service', None)
        if scheduler_service:
            jobs = scheduler_service.list_jobs()
            scheduler_health = {
                "status": "running",
                "active_jobs": len(jobs),
                "jobs": [{"id": job.id, "next_run": str(job.next_run_time)} for job in jobs]
            }
        else:
            scheduler_health = {"status": "not_available"}
    except Exception as e:
        logger.warning(f"Scheduler health check failed: {e}")
        scheduler_health = {"status": "error", "error": str(e)}
    
    # Déterminer le statut global
    if db_health.status != "healthy":
        overall.status = "degraded"
    
    return SystemHealth(
        overall=overall,
        database=db_health,
        cache=cache_health,
        scheduler=scheduler_health
    )


@router.get("/health/database", summary="Health check base de données", response_model=DatabaseHealth)
async def database_health_check(
    db: Session = Depends(get_db)
) -> DatabaseHealth:
    """Vérifie la santé de la base de données"""
    return check_database_health(db)


def check_database_health(db: Session) -> DatabaseHealth:
    """Vérifie la santé de la base de données"""
    import time
    
    start_time = time.time()
    
    try:
        # Test simple de connexion
        db.execute(text("SELECT 1"))
        db.commit()
        
        response_time = (time.time() - start_time) * 1000  # en ms
        
        return DatabaseHealth(
            status="healthy",
            response_time_ms=round(response_time, 2)
        )
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return DatabaseHealth(
            status="unhealthy",
            error=str(e)
        )


@router.get("/health/ping", summary="Ping simple")
async def ping() -> dict:
    """
    Ping simple pour vérifier que l'API répond
    
    Utilisé par les load balancers et monitoring externes
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/metrics", summary="Métriques Prometheus")
async def metrics():
    """
    Endpoint Prometheus pour les métriques
    
    Retourne les métriques au format Prometheus
    """
    return get_metrics_response()


@router.get("/stats", summary="Statistiques du système")
async def system_stats(
    db: Session = Depends(get_db)
) -> dict:
    """
    Statistiques détaillées du système
    
    Inclut:
    - Statistiques de la base de données
    - Statistiques du cache
    - Statistiques du scheduler
    """
    from app.services.cache_service import get_cache_service
    from app.main import app
    
    stats = {
        "timestamp": datetime.now().isoformat(),
        "database": {},
        "cache": {},
        "scheduler": {}
    }
    
    # Stats base de données
    try:
        # Nombre d'articles
        result = db.execute(text("SELECT COUNT(*) FROM media_articles"))
        stats["database"]["media_articles_count"] = result.scalar()
        
        # Nombre de scores
        result = db.execute(text("SELECT COUNT(*) FROM index_scores"))
        stats["database"]["index_scores_count"] = result.scalar()
        
        # Dernier score
        result = db.execute(
            text("SELECT score, as_of FROM index_scores ORDER BY as_of DESC LIMIT 1")
        )
        row = result.fetchone()
        if row:
            stats["database"]["latest_score"] = {
                "score": row[0],
                "as_of": row[1].isoformat() if row[1] else None
            }
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        stats["database"]["error"] = str(e)
    
    # Stats cache
    try:
        cache_service = get_cache_service()
        cache_stats = cache_service.get_stats()
        stats["cache"] = cache_stats or {}
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        stats["cache"]["error"] = str(e)
    
    # Stats scheduler
    try:
        scheduler_service = getattr(app.state, 'scheduler_service', None)
        if scheduler_service:
            jobs = scheduler_service.list_jobs()
            stats["scheduler"] = {
                "active_jobs": len(jobs),
                "jobs": [
                    {
                        "id": job.id,
                        "next_run": job.next_run_time.isoformat() if job.next_run_time else None
                    }
                    for job in jobs
                ]
            }
    except Exception as e:
        logger.error(f"Error getting scheduler stats: {e}")
        stats["scheduler"]["error"] = str(e)
    
    return stats

