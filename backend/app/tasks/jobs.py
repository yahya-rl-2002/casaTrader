from __future__ import annotations

from datetime import datetime
import asyncio

from app.core.logging import get_logger
from app.services.pipeline_service import PipelineService


logger = get_logger(__name__)


async def run_daily_index_pipeline() -> None:
    """Daily pipeline job (legacy - scheduled once per day)"""
    logger.info("Starting daily index pipeline", extra={"timestamp": datetime.utcnow().isoformat()})

    service = PipelineService()
    result = await service.run_full_pipeline()

    if result.get("success"):
        logger.info(
            "Daily pipeline completed",
            extra={
                "final_score": result.get("final_score"),
                "market_records": result.get("market_data_count"),
                "media_articles": result.get("media_articles_count"),
                "target_date": result.get("target_date"),
            },
        )
    else:
        logger.error(
            "Daily pipeline failed",
            extra={
                "error": result.get("error"),
                "target_date": result.get("target_date"),
            },
        )


def run_index_update_job() -> None:
    """
    Index update job - runs every 10 minutes.
    This is a synchronous wrapper for the async pipeline.
    """
    logger.info("🔄 Starting scheduled index update (every 10 minutes)", extra={
        "timestamp": datetime.utcnow().isoformat()
    })
    
    try:
        # Run the async pipeline in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        service = PipelineService()
        result = loop.run_until_complete(service.run_full_pipeline())
        
        loop.close()
        
        if result.get("success"):
            logger.info(
                "✅ Scheduled update completed successfully",
                extra={
                    "final_score": result.get("final_score"),
                    "market_records": result.get("market_data_count"),
                    "media_articles": result.get("media_articles_count"),
                    "target_date": str(result.get("target_date")),
                },
            )
        else:
            logger.error(
                "❌ Scheduled update failed",
                extra={
                    "error": result.get("error"),
                    "target_date": str(result.get("target_date")),
                },
            )
    except Exception as e:
        logger.error(f"❌ Exception during scheduled update: {e}", exc_info=True)


async def run_financial_reports_scraping_job() -> None:
    """
    Job automatique pour scraper les rapports financiers
    S'exécute quotidiennement pour récupérer les nouveaux rapports
    """
    logger.info("📊 Starting scheduled financial reports scraping", extra={
        "timestamp": datetime.utcnow().isoformat()
    })
    
    try:
        from app.services.financial_reports_scraper import FinancialReportsScraper
        
        scraper = FinancialReportsScraper()
        
        # Scraper toutes les entreprises configurées
        stats = await scraper.scrape_all_companies(
            company_symbols=None,  # Toutes les entreprises
            download_pdfs=True,  # Télécharger et uploader les PDFs
            max_reports_per_company=50  # Max 50 rapports par entreprise
        )
        
        logger.info(
            "✅ Financial reports scraping completed",
            extra={
                "total_companies": stats.get("total_companies", 0),
                "total_scraped": stats.get("total_scraped", 0),
                "total_downloaded": stats.get("total_downloaded", 0),
                "total_saved": stats.get("total_saved", 0),
                "total_errors": stats.get("total_errors", 0),
            },
        )
        
    except Exception as e:
        logger.error(f"❌ Exception during financial reports scraping: {e}", exc_info=True)


def run_financial_reports_scraping_job_sync() -> None:
    """
    Wrapper synchrone pour le job de scraping des rapports financiers
    """
    logger.info("📊 Starting scheduled financial reports scraping (sync wrapper)")
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        loop.run_until_complete(run_financial_reports_scraping_job())
        
        loop.close()
        
    except Exception as e:
        logger.error(f"❌ Exception in financial reports scraping job: {e}", exc_info=True)



