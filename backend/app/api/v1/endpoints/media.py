from datetime import datetime
from typing import List, Optional
import asyncio

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.schemas import MediaArticle
from app.core.logging import get_logger
from app.api.dependencies import get_db
from app.services.cache_service import get_cache_service

router = APIRouter()
logger = get_logger(__name__)

# Service de cache Redis (avec fallback en mémoire)
cache_service = get_cache_service()


@router.get("/latest", summary="Latest media articles with sentiment")
async def get_latest_media(
    limit: int = Query(20, ge=1, le=500, description="Number of articles to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    cursor: Optional[str] = Query(None, description="Cursor for cursor-based pagination (article ID)"),
    auto_scrape: bool = Query(False, description="Auto-scrape if articles are old"),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> dict:
    """
    Récupère les derniers articles médias avec leur analyse de sentiment.
    Déclenche automatiquement le scraping si les articles sont anciens.
    
    - **limit**: Nombre d'articles à retourner (1-500, défaut: 20)
    - **offset**: Offset pour pagination classique (défaut: 0)
    - **cursor**: ID de l'article pour pagination cursor-based (plus performant)
    - **auto_scrape**: Déclencher automatiquement le scraping si nécessaire (défaut: False)
    
    **Optimisation** : Utilise cursor-based pagination si `cursor` est fourni (plus performant pour grandes listes).
    Sinon, utilise offset-based pagination classique.
    """
    try:
        # Vérifier le cache pour les requêtes fréquentes
        cache_key = f"media:latest:{limit}:{offset}:{cursor or 'none'}"
        cached_result = cache_service.get(cache_key)
        if cached_result is not None:
            logger.debug(f"✅ Cache hit: media articles (limit={limit}, offset={offset})")
            return cached_result
        # Vérifier si la table existe, sinon la créer
        from app.models.schemas import Base
        from app.models.database import engine
        Base.metadata.create_all(bind=engine, checkfirst=True)
        
        # Vérifier si on a besoin de scraper
        if auto_scrape:
            from datetime import timedelta
            recent_count = db.query(MediaArticle).filter(
                MediaArticle.scraped_at >= datetime.now() - timedelta(hours=1)
            ).count()
            
            # Si moins de 10 articles récents, déclencher le scraping en arrière-plan
            if recent_count < 10:
                logger.info(f"🔄 Déclenchement automatique du scraping (seulement {recent_count} articles récents)")
                if background_tasks:
                    background_tasks.add_task(trigger_enhanced_scraping)
                else:
                    # Si pas de background_tasks, lancer en arrière-plan
                    asyncio.create_task(trigger_enhanced_scraping())
        
        # Pagination optimisée : cursor-based si cursor fourni, sinon offset-based
        if cursor:
            # Cursor-based pagination (plus performant)
            try:
                cursor_id = int(cursor)
                query = (
                    db.query(MediaArticle)
                    .filter(MediaArticle.id < cursor_id)  # Articles plus anciens que le cursor
                    .order_by(desc(MediaArticle.published_at))
                    .limit(limit + 1)  # +1 pour savoir s'il y a une page suivante
                )
            except ValueError:
                # Cursor invalide, fallback sur offset
                query = (
                    db.query(MediaArticle)
                    .order_by(desc(MediaArticle.published_at))
                    .offset(offset)
                    .limit(limit)
                )
                cursor = None
        else:
            # Offset-based pagination classique
            query = (
                db.query(MediaArticle)
                .order_by(desc(MediaArticle.published_at))
                .offset(offset)
                .limit(limit)
            )
        
        articles = query.all()
        
        # Pour cursor-based, vérifier s'il y a une page suivante
        has_next = False
        next_cursor = None
        if cursor and len(articles) > limit:
            has_next = True
            articles = articles[:limit]
            next_cursor = str(articles[-1].id) if articles else None
        
        result = {
            "data": [
                {
                    "id": article.id,
                    "source": article.source or "Source inconnue",
                    "title": article.title or "Titre non disponible",
                    "url": article.url or "#",
                    "summary": getattr(article, 'summary', None),
                    "content": getattr(article, 'content', None),  # Contenu complet
                    "image_url": getattr(article, 'image_url', None),  # URL de l'image principale
                    "published_at": article.published_at.isoformat() if article.published_at else None,
                    "sentiment_score": article.sentiment_score,
                    "sentiment_label": article.sentiment_label,
                    "scraped_at": article.scraped_at.isoformat() if article.scraped_at else None,
                }
                for article in articles
            ],
            "count": len(articles),
            "limit": limit,
        }
        
        # Ajouter les métadonnées de pagination
        if cursor:
            result["pagination"] = {
                "type": "cursor",
                "has_next": has_next,
                "next_cursor": next_cursor,
            }
        else:
            result["pagination"] = {
                "type": "offset",
                "offset": offset,
                "has_next": len(articles) == limit,  # Probablement plus de résultats
            }
        
        # Mettre en cache (TTL court pour les données dynamiques)
        cache_service.set(cache_key, result, ttl_seconds=60)  # 1 minute pour les articles
        
        return result
    except Exception as e:
        logger.error(f"Error fetching media articles: {e}", exc_info=True)
        
        # Retourner une structure vide en cas d'erreur
        return {
            "data": [],
            "count": 0,
            "limit": limit,
            "error": str(e)
        }


@router.get("/sources", summary="List of media sources")
async def get_media_sources(db: Session = Depends(get_db)) -> dict:
    """
    Récupère la liste des sources médias avec le nombre d'articles par source.
    """
    from sqlalchemy import func
    
    sources = (
        db.query(
            MediaArticle.source,
            func.count(MediaArticle.id).label("count")
        )
        .group_by(MediaArticle.source)
        .all()
    )
    
    return {
        "sources": [
            {"name": source, "article_count": count}
            for source, count in sources
        ],
        "total_sources": len(sources),
    }


@router.get("/sentiment-stats", summary="Sentiment statistics")
async def get_sentiment_stats(db: Session = Depends(get_db)) -> dict:
    """
    Récupère des statistiques sur le sentiment des articles.
    """
    from sqlalchemy import func
    
    # Compter par label de sentiment
    sentiment_counts = (
        db.query(
            MediaArticle.sentiment_label,
            func.count(MediaArticle.id).label("count")
        )
        .filter(MediaArticle.sentiment_label.isnot(None))
        .group_by(MediaArticle.sentiment_label)
        .all()
    )
    
    # Statistiques sur les scores
    sentiment_stats = db.query(
        func.avg(MediaArticle.sentiment_score).label("avg"),
        func.min(MediaArticle.sentiment_score).label("min"),
        func.max(MediaArticle.sentiment_score).label("max"),
    ).filter(MediaArticle.sentiment_score.isnot(None)).first()
    
    total_articles = db.query(func.count(MediaArticle.id)).scalar()
    
    return {
        "total_articles": total_articles,
        "sentiment_distribution": {
            label: count for label, count in sentiment_counts
        },
        "sentiment_scores": {
            "average": float(sentiment_stats.avg) if sentiment_stats.avg else None,
            "min": float(sentiment_stats.min) if sentiment_stats.min else None,
            "max": float(sentiment_stats.max) if sentiment_stats.max else None,
        },
    }


@router.post("/trigger-scraping", summary="Trigger enhanced scraping")
async def trigger_scraping_endpoint(background_tasks: BackgroundTasks = BackgroundTasks()) -> dict:
    """
    Déclencher manuellement le scraping amélioré des articles.
    Le scraping s'exécute en arrière-plan pour ne pas bloquer la requête.
    """
    try:
        if background_tasks:
            background_tasks.add_task(trigger_enhanced_scraping)
        else:
            asyncio.create_task(trigger_enhanced_scraping())
        
        return {
            "message": "Scraping déclenché en arrière-plan",
            "status": "running"
        }
    except Exception as e:
        logger.error(f"Erreur déclenchement scraping: {e}")
        return {
            "error": str(e),
            "status": "error"
        }


@router.post("/sync-to-supabase", summary="Sync articles to Supabase")
async def sync_to_supabase_endpoint(
    sources: List[str] = Query(None, description="Sources to sync (default: all configured sources)"),
    limit: int = Query(None, description="Limit number of articles to sync (default: all)")
) -> dict:
    """
    Synchroniser les articles de SQLite vers Supabase.
    Utile pour synchroniser immédiatement tous les articles existants.
    
    - **sources**: Liste des sources à synchroniser (ex: ["hespress", "medias24", "boursenews"])
    - **limit**: Nombre maximum d'articles à synchroniser (None = tous)
    """
    try:
        from app.services.supabase_sync_service import SupabaseSyncService
        
        sync_service = SupabaseSyncService()
        
        if not sync_service.client:
            return {
                "success": False,
                "error": "Client Supabase non initialisé. Vérifiez SUPABASE_URL et SUPABASE_ANON_KEY",
                "synced": 0
            }
        
        # Utiliser les sources configurées si non spécifiées
        if not sources:
            sources = ["hespress", "medias24", "boursenews"]
        
        logger.info(f"🔄 Synchronisation vers Supabase: {sources}")
        
        stats = sync_service.sync_articles_to_supabase(
            sources=sources,
            limit=limit
        )
        
        return {
            "success": stats.get("success", False),
            "synced": stats.get("synced", 0),
            "sources": stats.get("sources", {}),
            "errors": stats.get("errors", []),
            "message": f"{stats.get('synced', 0)} articles synchronisés vers Supabase"
        }
        
    except ImportError as e:
        logger.error(f"Erreur import SupabaseSyncService: {e}")
        return {
            "success": False,
            "error": "Service de synchronisation non disponible. Installez supabase: pip install supabase",
            "synced": 0
        }
    except Exception as e:
        logger.error(f"Erreur synchronisation Supabase: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "synced": 0
        }


@router.get("/cache/stats", summary="Get cache statistics")
async def get_cache_stats() -> dict:
    """
    Retourne les statistiques du cache (Redis ou mémoire).
    Utile pour le monitoring et le debugging.
    """
    stats = cache_service.get_stats()
    return {
        "cache": stats,
        "message": "Cache statistics retrieved successfully"
    }


@router.delete("/cache/clear", summary="Clear cache")
async def clear_cache(pattern: Optional[str] = Query(None, description="Pattern to clear (ex: 'volume:*')")) -> dict:
    """
    Vide le cache. Si un pattern est fourni, supprime seulement les clés correspondantes.
    
    - **pattern**: Pattern Redis (ex: "volume:*", "simplified:*")
    """
    if pattern:
        count = cache_service.delete_pattern(pattern)
        return {
            "success": True,
            "message": f"Cleared {count} cache keys matching pattern '{pattern}'"
        }
    else:
        success = cache_service.clear()
        return {
            "success": success,
            "message": "Cache cleared successfully" if success else "Failed to clear cache"
        }


async def trigger_enhanced_scraping():
    """
    Fonction pour déclencher le scraping amélioré en arrière-plan
    """
    try:
        from app.services.enhanced_media_service import EnhancedMediaService
        
        logger.info("🚀 Démarrage du scraping amélioré en arrière-plan")
        service = EnhancedMediaService()
        result = await service.trigger_scraping_on_access()
        
        logger.info(f"✅ Scraping terminé: {result}")
        
        # Synchroniser vers Supabase après le scraping
        try:
            from app.services.supabase_sync_service import SupabaseSyncService
            sync_service = SupabaseSyncService()
            if sync_service.client:
                logger.info("🔄 Synchronisation vers Supabase...")
                sync_stats = sync_service.sync_recent_articles(hours=24)
                if sync_stats.get("success"):
                    logger.info(f"✅ {sync_stats['synced']} articles synchronisés vers Supabase")
                else:
                    logger.warning(f"⚠️  Erreur synchronisation Supabase: {sync_stats.get('error')}")
        except Exception as e:
            logger.warning(f"⚠️  Impossible de synchroniser vers Supabase: {e}")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du scraping amélioré: {e}", exc_info=True)

