"""
Service amélioré pour le scraping des médias avec contenu complet
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional
import asyncio
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.logging import get_logger
from app.models.database import get_session
from app.models.schemas import MediaArticle
from app.pipelines.ingestion.enhanced_media_scraper import (
    EnhancedMediaScraper,
    EnhancedMediaArticle
)

logger = get_logger(__name__)

# Importer les scrapers spécialisés existants
try:
    from app.pipelines.ingestion.medias24_scraper import Medias24Scraper, convert_to_media_article as convert_medias24
    MEDIAS24_AVAILABLE = True
except ImportError:
    MEDIAS24_AVAILABLE = False
    logger.warning("Medias24 scraper not available")

try:
    from app.pipelines.ingestion.boursenews_scraper import BourseNewsScraper, convert_to_media_article as convert_boursenews
    BOURSENEWS_AVAILABLE = True
except ImportError:
    BOURSENEWS_AVAILABLE = False
    logger.warning("BourseNews scraper not available")


class EnhancedMediaService:
    """
    Service pour scraper les articles avec contenu complet
    et les sauvegarder en base de données
    """
    
    # URLs de listing pour chaque source (seulement Hespress, Medias24 et BourseNews)
    SOURCE_LISTINGS = {
        "hespress": [
            "https://fr.hespress.com/economie",
            "https://fr.hespress.com/economie/",
        ],
        "medias24": [
            "https://medias24.com",
            "https://medias24.com/economie/",
        ],
        "boursenews": [
            "https://boursenews.ma/espace-investisseurs",  # Lien principal pour BourseNews
            "https://boursenews.ma/actualite",
            "https://boursenews.ma",
        ],
    }
    
    def __init__(
        self,
        cache_dir: Optional[str] = None,
        max_articles_per_source: int = 15,
        min_quality_score: float = 0.3
    ):
        """
        Args:
            cache_dir: Répertoire pour le cache (optionnel)
            max_articles_per_source: Nombre maximum d'articles par source
            min_quality_score: Score de qualité minimum (0-1)
        """
        if cache_dir is None:
            cache_dir = str(Path(__file__).parent.parent.parent / "cache" / "scraping")
        
        self.scraper = EnhancedMediaScraper(
            delay_between_requests=2.0,
            max_retries=3,
            cache_dir=cache_dir,
            min_content_length=300,
            max_article_age_days=7
        )
        self.max_articles_per_source = max_articles_per_source
        self.min_quality_score = min_quality_score
        
        logger.info("EnhancedMediaService initialisé")
    
    async def scrape_all_sources(self) -> dict:
        """
        Scraper tous les articles de toutes les sources
        Retourne un dictionnaire avec les statistiques
        """
        logger.info("🚀 Démarrage du scraping amélioré de tous les articles")
        
        all_articles: List[EnhancedMediaArticle] = []
        stats = {
            "sources": {},
            "total_scraped": 0,
            "total_saved": 0,
            "errors": []
        }
        
        # Scraper chaque source
        for source_name, listing_urls in self.SOURCE_LISTINGS.items():
            try:
                logger.info(f"📰 Scraping {source_name}...")
                source_articles = []
                source_success = False
                
                # Utiliser les scrapers spécialisés pour Medias24 et BourseNews
                if source_name == "medias24" and MEDIAS24_AVAILABLE:
                    try:
                        logger.info(f"Utilisation du scraper spécialisé Medias24")
                        medias24_scraper = Medias24Scraper(delay_between_requests=2)
                        medias24_articles = await asyncio.to_thread(
                            medias24_scraper.fetch_articles,
                            max_articles=self.max_articles_per_source
                        )
                        
                        # Convertir et scraper le contenu complet de chaque article
                        for m24_article in medias24_articles:
                            enhanced_article = await asyncio.to_thread(
                                self.scraper.scrape_article,
                                m24_article.url,
                                source_name
                            )
                            if enhanced_article:
                                source_articles.append(enhanced_article)
                            else:
                                # Fallback: utiliser l'article de base
                                from app.pipelines.ingestion.enhanced_media_scraper import EnhancedMediaArticle
                                from datetime import datetime
                                fallback = EnhancedMediaArticle(
                                    title=m24_article.title,
                                    summary=m24_article.summary,
                                    url=m24_article.url,
                                    source=source_name,
                                    published_at=m24_article.published_at,
                                    content=m24_article.summary,  # Utiliser le résumé comme contenu
                                    word_count=len(m24_article.summary.split())
                                )
                                fallback.quality_score = self.scraper._calculate_quality_score(fallback)
                                source_articles.append(fallback)
                        
                        logger.info(f"✅ {len(source_articles)} articles de Medias24")
                        source_success = True
                        
                    except Exception as e:
                        logger.error(f"Erreur scraping Medias24 avec scraper spécialisé: {e}")
                        logger.info(f"Tentative avec scraper générique pour Medias24...")
                        # Fallback: utiliser le scraper générique
                        for listing_url in listing_urls:
                            try:
                                articles = await asyncio.to_thread(
                                    self.scraper.scrape_articles_from_listing,
                                    listing_url,
                                    source_name,
                                    self.max_articles_per_source
                                )
                                source_articles.extend(articles)
                                if len(source_articles) >= self.max_articles_per_source:
                                    break
                            except Exception as e2:
                                logger.error(f"Erreur scraping {listing_url}: {e2}")
                                continue
                        if source_articles:
                            source_success = True
                
                if source_name == "boursenews" and BOURSENEWS_AVAILABLE:
                    try:
                        logger.info(f"Utilisation du scraper spécialisé BourseNews")
                        boursenews_scraper = BourseNewsScraper(delay_between_requests=2)
                        boursenews_articles = await asyncio.to_thread(
                            boursenews_scraper.fetch_articles,
                            max_articles=self.max_articles_per_source,
                            sections=["espace_investisseurs"]
                        )
                        
                        logger.info(f"  📰 {len(boursenews_articles)} articles trouvés par le scraper spécialisé")
                        
                        # Convertir et scraper le contenu complet de chaque article
                        for i, bn_article in enumerate(boursenews_articles, 1):
                            logger.info(f"  Scraping article {i}/{len(boursenews_articles)}: {bn_article.url[:60]}...")
                            enhanced_article = await asyncio.to_thread(
                                self.scraper.scrape_article,
                                bn_article.url,
                                source_name
                            )
                            if enhanced_article:
                                source_articles.append(enhanced_article)
                                logger.info(f"    ✅ Contenu complet scrapé ({len(enhanced_article.content)} caractères)")
                            else:
                                # Fallback: utiliser l'article de base
                                from app.pipelines.ingestion.enhanced_media_scraper import EnhancedMediaArticle
                                fallback = EnhancedMediaArticle(
                                    title=bn_article.title,
                                    summary=bn_article.summary,
                                    url=bn_article.url,
                                    source=source_name,
                                    published_at=bn_article.published_at,
                                    content=bn_article.summary,
                                    word_count=len(bn_article.summary.split())
                                )
                                fallback.quality_score = self.scraper._calculate_quality_score(fallback)
                                source_articles.append(fallback)
                                logger.info(f"    ⚠️  Utilisation du résumé comme contenu (qualité: {fallback.quality_score:.2f})")
                        
                        logger.info(f"✅ {len(source_articles)} articles de BourseNews")
                        source_success = len(source_articles) > 0
                        
                    except Exception as e:
                        logger.error(f"Erreur scraping BourseNews avec scraper spécialisé: {e}")
                        logger.info(f"Tentative avec scraper générique pour BourseNews...")
                        # Fallback: utiliser le scraper générique
                        for listing_url in listing_urls:
                            try:
                                articles = await asyncio.to_thread(
                                    self.scraper.scrape_articles_from_listing,
                                    listing_url,
                                    source_name,
                                    self.max_articles_per_source
                                )
                                source_articles.extend(articles)
                                if len(source_articles) >= self.max_articles_per_source:
                                    break
                            except Exception as e2:
                                logger.error(f"Erreur scraping {listing_url}: {e2}")
                                continue
                        if source_articles:
                            source_success = True
                
                # Scraper générique pour les autres sources (hespress, challenge, lavieeco, leconomiste)
                if not source_success:
                    logger.info(f"Utilisation du scraper générique pour {source_name}")
                    for listing_url in listing_urls:
                        try:
                            logger.info(f"  Scraping {listing_url}...")
                            articles = await asyncio.to_thread(
                                self.scraper.scrape_articles_from_listing,
                                listing_url,
                                source_name,
                                self.max_articles_per_source
                            )
                            if articles:
                                source_articles.extend(articles)
                                source_success = True
                                logger.info(f"  ✅ {len(articles)} articles trouvés")
                            
                            # Limiter le nombre total par source
                            if len(source_articles) >= self.max_articles_per_source:
                                break
                                
                        except Exception as e:
                            logger.error(f"  ❌ Erreur scraping {listing_url}: {e}")
                            stats["errors"].append({
                                "source": source_name,
                                "url": listing_url,
                                "error": str(e)
                            })
                            continue
                    
                    if source_success:
                        logger.info(f"✅ {len(source_articles)} articles de {source_name}")
                    else:
                        logger.warning(f"⚠️  Aucun article trouvé pour {source_name}")
                
                # Filtrer par qualité (mais garder au moins quelques articles même si qualité faible)
                quality_articles = [
                    a for a in source_articles
                    if a.quality_score >= self.min_quality_score
                ]
                
                # Si aucun article de qualité mais qu'on a des articles, prendre les meilleurs
                if not quality_articles and source_articles:
                    # Trier par qualité et prendre les meilleurs
                    sorted_articles = sorted(source_articles, key=lambda x: x.quality_score, reverse=True)
                    quality_articles = sorted_articles[:min(3, len(sorted_articles))]  # Prendre au moins 3 meilleurs
                    logger.info(f"  ⚠️  Aucun article avec qualité >= {self.min_quality_score}, on garde les {len(quality_articles)} meilleurs")
                
                all_articles.extend(quality_articles)
                
                stats["sources"][source_name] = {
                    "scraped": len(source_articles),
                    "quality": len(quality_articles),
                    "avg_quality_score": sum(a.quality_score for a in quality_articles) / len(quality_articles) if quality_articles else 0
                }
                
                logger.info(f"✅ {source_name}: {len(quality_articles)} articles de qualité")
                
            except Exception as e:
                logger.error(f"Erreur scraping source {source_name}: {e}")
                stats["errors"].append({
                    "source": source_name,
                    "error": str(e)
                })
                continue
        
        stats["total_scraped"] = len(all_articles)
        
        # Sauvegarder en base de données
        if all_articles:
            saved_count = await self._save_articles(all_articles)
            stats["total_saved"] = saved_count
            
            # Synchroniser vers Supabase si disponible
            try:
                from app.services.supabase_sync_service import SupabaseSyncService
                sync_service = SupabaseSyncService()
                if sync_service.client:
                    logger.info("🔄 Synchronisation vers Supabase...")
                    sync_stats = sync_service.sync_articles_to_supabase(
                        sources=["hespress", "medias24", "boursenews"],
                        limit=len(all_articles)
                    )
                    if sync_stats.get("success"):
                        logger.info(f"✅ {sync_stats['synced']} articles synchronisés vers Supabase")
                        stats["supabase_synced"] = sync_stats["synced"]
                    else:
                        logger.warning(f"⚠️  Erreur synchronisation Supabase: {sync_stats.get('error')}")
            except Exception as e:
                logger.warning(f"⚠️  Impossible de synchroniser vers Supabase: {e}")
        
        logger.info(f"✅ Scraping terminé: {stats['total_saved']} articles sauvegardés")
        
        return stats
    
    async def _save_articles(self, articles: List[EnhancedMediaArticle]) -> int:
        """
        Sauvegarder les articles en base de données
        Évite les doublons par URL
        """
        saved_count = 0
        
        # Obtenir une session de base de données
        db: Session = get_session()
        
        try:
            for article in articles:
                try:
                    # Vérifier si l'article existe déjà
                    existing = db.query(MediaArticle).filter(
                        MediaArticle.url == article.url
                    ).first()
                    
                    if existing:
                        # Mettre à jour l'article existant si le nouveau est meilleur
                        if article.quality_score > (existing.sentiment_score or 0):
                            existing.title = article.title
                            existing.summary = article.summary
                            existing.content = article.content
                            existing.image_url = article.image_url  # Mettre à jour l'image
                            existing.published_at = article.published_at
                            existing.scraped_at = datetime.now()
                            logger.debug(f"Article mis à jour: {article.url}")
                        else:
                            logger.debug(f"Article déjà existant (meilleur): {article.url}")
                            continue
                    else:
                        # Créer un nouvel article
                        new_article = MediaArticle(
                            title=article.title,
                            summary=article.summary,
                            url=article.url,
                            source=article.source,
                            published_at=article.published_at,
                            content=article.content,
                            image_url=article.image_url,  # Sauvegarder l'image
                            sentiment_score=article.quality_score,  # Utiliser quality_score temporairement
                            sentiment_label=article.sentiment_label,
                            scraped_at=article.scraped_at
                        )
                        db.add(new_article)
                    
                    saved_count += 1
                    
                except Exception as e:
                    logger.error(f"Erreur sauvegarde article {article.url}: {e}")
                    continue
            
            db.commit()
            logger.info(f"✅ {saved_count} articles sauvegardés en base de données")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erreur lors de la sauvegarde: {e}")
            raise
        finally:
            db.close()
        
        return saved_count
    
    async def scrape_recent_articles(self, hours: int = 24) -> dict:
        """
        Scraper uniquement les articles récents (dernières X heures)
        Plus rapide et ciblé
        """
        logger.info(f"🚀 Scraping des articles récents (dernières {hours}h)")
        
        # Réduire le nombre d'articles par source pour un scraping rapide
        original_max = self.max_articles_per_source
        self.max_articles_per_source = 10
        
        try:
            stats = await self.scrape_all_sources()
        finally:
            self.max_articles_per_source = original_max
        
        return stats
    
    async def trigger_scraping_on_access(self) -> dict:
        """
        Déclencher le scraping quand l'utilisateur accède à la page
        Version optimisée pour être rapide
        """
        logger.info("🔄 Déclenchement du scraping en temps réel")
        
        # Vérifier d'abord si on a déjà des articles récents
        db: Session = get_session()
        
        try:
            recent_count = db.query(MediaArticle).filter(
                MediaArticle.scraped_at >= datetime.now() - timedelta(hours=1)
            ).count()
            
            # Si on a déjà des articles récents, on ne scrape pas
            if recent_count >= 10:
                logger.info(f"✅ Déjà {recent_count} articles récents, pas besoin de scraper")
                return {
                    "scraped": False,
                    "reason": "articles_recent",
                    "recent_count": recent_count
                }
            
            # Scraper uniquement les articles récents
            stats = await self.scrape_recent_articles(hours=24)
            
            return {
                "scraped": True,
                "stats": stats
            }
            
        finally:
            db.close()

