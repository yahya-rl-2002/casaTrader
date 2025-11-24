from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.services.scheduler import SchedulerService
from app.tasks.jobs import run_index_update_job, run_financial_reports_scraping_job_sync
from app.core.logging import get_logger
from app.core.rate_limiter import rate_limiter
from app.core.config import settings
from app.core.monitoring import metrics_middleware


logger = get_logger(__name__)
scheduler_service = SchedulerService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI application.
    Starts the scheduler on startup and stops it on shutdown.
    """
    # Startup
    logger.info("🚀 Starting Fear & Greed Index API")
    
    # Start the scheduler
    scheduler_service.start()
    
    # Schedule the index update job every 10 minutes
    scheduler_service.schedule_interval_job(
        job_callable=run_index_update_job,
        minutes=10,
        job_id="index_update_10min"
    )
    
    # Schedule financial reports scraping job daily at 2:00 AM
    scheduler_service.schedule_daily_job(
        job_callable=run_financial_reports_scraping_job_sync,
        run_time="02:00",
        job_id="financial_reports_scraping_daily"
    )
    
    logger.info("✅ Scheduler started - Index will update every 10 minutes")
    logger.info("✅ Financial reports scraping scheduled daily at 02:00 AM")
    logger.info(f"📊 Active jobs: {len(scheduler_service.list_jobs())}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Fear & Greed Index API")
    scheduler_service.shutdown()
    logger.info("✅ Scheduler stopped")


def create_application() -> FastAPI:
    application = FastAPI(
        title="Casablanca Fear & Greed Index API",
        description="Daily sentiment index tailored for the Casablanca Stock Exchange.",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Store scheduler service in app state for access in endpoints
    application.state.scheduler_service = scheduler_service

    # Configuration CORS pour le frontend (plus sécurisé)
    allowed_origins = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    
    # En production, utiliser les vraies URLs
    if settings.environment == "production":
        # TODO: Ajouter les URLs de production
        pass
    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Plus restrictif
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],  # Plus restrictif
    )
    
    # Metrics middleware (doit être avant rate limiting pour capturer toutes les requêtes)
    application.middleware("http")(metrics_middleware)
    
    # Rate limiting middleware
    @application.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        """Middleware pour le rate limiting"""
        if settings.rate_limit_enabled:
            try:
                is_allowed, rate_limit_info = rate_limiter.check_rate_limit(request)
                if not is_allowed:
                    retry_after = rate_limit_info.get("retry_after", 60)
                    limit = rate_limit_info.get("limit", 0)
                    limit_type = rate_limit_info.get("limit_type", "minute")
                    
                    return JSONResponse(
                        status_code=429,
                        content={
                            "detail": f"Rate limit exceeded: {limit} requests per {limit_type}",
                            "retry_after": retry_after
                        },
                        headers={
                            "Retry-After": str(retry_after),
                            "X-RateLimit-Limit": str(limit),
                            "X-RateLimit-Remaining": "0",
                        }
                    )
            except Exception as e:
                logger.warning(f"Rate limiting error: {e}, allowing request")
        
        response = await call_next(request)
        return response

    application.include_router(api_router, prefix="/api/v1")

    return application


app = create_application()


