"""
Endpoints API pour la gestion des rapports financiers
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from typing import List, Optional
from pydantic import BaseModel

from app.core.logging import get_logger
from app.services.financial_reports_scraper import FinancialReportsScraper

logger = get_logger(__name__)

router = APIRouter()


class ScrapeRequest(BaseModel):
    company_symbols: Optional[List[str]] = None
    download_pdfs: bool = True
    max_reports_per_company: int = 50


class ScrapeResponse(BaseModel):
    success: bool
    message: str
    stats: Optional[dict] = None
    job_id: Optional[str] = None


@router.post("/scrape", response_model=ScrapeResponse, summary="Scraper les rapports financiers")
async def scrape_financial_reports(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks
):
    """
    Scraper automatiquement les rapports financiers des entreprises
    
    - **company_symbols**: Liste des symboles à scraper (None = toutes)
    - **download_pdfs**: Télécharger et uploader les PDFs vers Supabase
    - **max_reports_per_company**: Nombre maximum de rapports par entreprise
    """
    try:
        scraper = FinancialReportsScraper()
        
        # Exécuter en arrière-plan pour ne pas bloquer la requête
        async def run_scraping():
            stats = await scraper.scrape_all_companies(
                company_symbols=request.company_symbols,
                download_pdfs=request.download_pdfs,
                max_reports_per_company=request.max_reports_per_company
            )
            logger.info(f"✅ Scraping terminé: {stats}")
            return stats
        
        # Démarrer le scraping en arrière-plan
        background_tasks.add_task(run_scraping)
        
        return ScrapeResponse(
            success=True,
            message="Scraping démarré en arrière-plan",
            stats=None
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur démarrage scraping: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scrape/company", response_model=ScrapeResponse, summary="Scraper les rapports d'une entreprise")
async def scrape_company_reports(
    company_symbol: str = Query(..., description="Symbole de l'entreprise (ex: CSEMA:ATW)"),
    download_pdfs: bool = Query(True, description="Télécharger et uploader les PDFs"),
    max_reports: int = Query(50, description="Nombre maximum de rapports"),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Scraper les rapports financiers d'une entreprise spécifique
    
    - **company_symbol**: Symbole de l'entreprise (ex: CSEMA:ATW) - en query parameter
    - **download_pdfs**: Télécharger et uploader les PDFs
    - **max_reports**: Nombre maximum de rapports
    """
    try:
        if not company_symbol:
            raise HTTPException(status_code=400, detail="company_symbol est requis")
        
        scraper = FinancialReportsScraper()
        
        async def run_scraping():
            stats = await scraper.scrape_and_save_company(
                company_symbol=company_symbol,
                download_pdfs=download_pdfs,
                max_reports=max_reports
            )
            logger.info(f"✅ Scraping {company_symbol} terminé: {stats}")
            return stats
        
        background_tasks.add_task(run_scraping)
        
        return ScrapeResponse(
            success=True,
            message=f"Scraping démarré pour {company_symbol}",
            stats=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur scraping {company_symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/companies", summary="Liste des entreprises configurées")
async def get_configured_companies():
    """
    Retourner la liste des entreprises pour lesquelles le scraping est configuré
    """
    from app.services.financial_reports_scraper import COMPANY_REPORTS_CONFIG
    
    companies = []
    for symbol, config in COMPANY_REPORTS_CONFIG.items():
        companies.append({
            'symbol': symbol,
            'name': config['name'],
            'urls_count': len(config.get('urls', []))
        })
    
    return {
        'companies': companies,
        'total': len(companies)
    }

