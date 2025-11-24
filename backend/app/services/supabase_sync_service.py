"""
Service pour synchroniser les articles de SQLite vers Supabase
"""
from __future__ import annotations

from typing import List, Optional
from datetime import datetime
import os

from app.core.logging import get_logger
from app.models.database import get_session
from app.models.schemas import MediaArticle

logger = get_logger(__name__)

# Essayer d'importer Supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.warning("Supabase client not available. Install with: pip install supabase")


class SupabaseSyncService:
    """
    Service pour synchroniser les articles de SQLite (FastAPI) vers Supabase
    """
    
    def __init__(self):
        """Initialiser le service de synchronisation"""
        if not SUPABASE_AVAILABLE:
            raise ImportError("Supabase client not available. Install with: pip install supabase")
        
        # Récupérer les credentials Supabase depuis les variables d'environnement
        # Essayer d'abord depuis les settings, puis depuis les variables d'environnement
        # PRIORITÉ: Utiliser la clé SERVICE pour contourner RLS (Row Level Security)
        try:
            from app.core.config import settings
            supabase_url = settings.supabase_url or os.getenv("SUPABASE_URL")
            # Priorité: Service Key > Anon Key (Service Key contourne RLS)
            supabase_key = (settings.supabase_service_key or 
                          os.getenv("SUPABASE_SERVICE_KEY") or
                          settings.supabase_anon_key or 
                          os.getenv("SUPABASE_ANON_KEY"))
        except:
            # Priorité: Service Key > Anon Key
            supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
            supabase_url = os.getenv("SUPABASE_URL")
        
        if not supabase_url or not supabase_key:
            logger.warning("⚠️  Variables d'environnement Supabase non configurées")
            logger.warning("   Définissez SUPABASE_URL et SUPABASE_ANON_KEY ou SUPABASE_SERVICE_KEY")
            self.client = None
        else:
            self.client: Optional[Client] = create_client(supabase_url, supabase_key)
            logger.info("✅ Client Supabase initialisé")
    
    def sync_articles_to_supabase(
        self, 
        sources: Optional[List[str]] = None,
        limit: Optional[int] = None
    ) -> dict:
        """
        Synchroniser les articles de SQLite vers Supabase
        
        Args:
            sources: Liste des sources à synchroniser (None = toutes)
            limit: Nombre maximum d'articles à synchroniser (None = tous)
        
        Returns:
            Dictionnaire avec les statistiques de synchronisation
        """
        if not self.client:
            return {
                "success": False,
                "error": "Client Supabase non initialisé",
                "synced": 0
            }
        
        db = get_session()
        stats = {
            "success": True,
            "synced": 0,
            "errors": [],
            "sources": {}
        }
        
        try:
            # Récupérer les articles de SQLite
            query = db.query(MediaArticle)
            
            # Filtrer par sources si spécifié
            if sources:
                query = query.filter(MediaArticle.source.in_(sources))
            
            # Ordonner par date de publication (plus récents en premier)
            query = query.order_by(MediaArticle.published_at.desc())
            
            # Limiter si spécifié
            if limit:
                query = query.limit(limit)
            
            articles = query.all()
            
            logger.info(f"📊 {len(articles)} articles à synchroniser vers Supabase")
            
            # Synchroniser chaque article
            for article in articles:
                try:
                    # Préparer les données pour Supabase
                    article_data = {
                        "title": article.title,
                        "description": article.summary or article.title,
                        "content": article.content or article.summary or "",
                        "source": article.source,
                        "source_url": article.url,
                        "image_url": article.image_url,
                        "published_at": article.published_at.isoformat() if article.published_at else None,
                        "category": None,  # À définir si nécessaire
                        "tags": [],  # À définir si nécessaire
                    }
                    
                    # Vérifier si l'article existe déjà dans Supabase (par URL)
                    existing = self.client.table("articles").select("id").eq("source_url", article.url).execute()
                    
                    if existing.data:
                        # Mettre à jour l'article existant
                        article_id = existing.data[0]["id"]
                        result = self.client.table("articles").update(article_data).eq("id", article_id).execute()
                        logger.debug(f"✅ Article mis à jour dans Supabase: {article.title[:50]}...")
                    else:
                        # Créer un nouvel article
                        result = self.client.table("articles").insert(article_data).execute()
                        logger.debug(f"✅ Article ajouté dans Supabase: {article.title[:50]}...")
                    
                    stats["synced"] += 1
                    
                    # Compter par source
                    source = article.source
                    if source not in stats["sources"]:
                        stats["sources"][source] = 0
                    stats["sources"][source] += 1
                    
                except Exception as e:
                    error_msg = f"Erreur synchronisation article {article.url}: {e}"
                    logger.error(error_msg)
                    stats["errors"].append({
                        "url": article.url,
                        "error": str(e)
                    })
                    continue
            
            logger.info(f"✅ Synchronisation terminée: {stats['synced']} articles synchronisés")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la synchronisation: {e}")
            stats["success"] = False
            stats["error"] = str(e)
        finally:
            db.close()
        
        return stats
    
    def sync_recent_articles(self, hours: int = 24) -> dict:
        """
        Synchroniser uniquement les articles récents
        
        Args:
            hours: Nombre d'heures en arrière pour considérer un article comme récent
        
        Returns:
            Dictionnaire avec les statistiques de synchronisation
        """
        from datetime import timedelta
        
        db = get_session()
        
        try:
            # Récupérer les articles récents
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_articles = db.query(MediaArticle).filter(
                MediaArticle.scraped_at >= cutoff_time
            ).order_by(MediaArticle.published_at.desc()).all()
            
            logger.info(f"📊 {len(recent_articles)} articles récents à synchroniser")
            
            # Synchroniser
            return self.sync_articles_to_supabase(limit=len(recent_articles))
            
        finally:
            db.close()

