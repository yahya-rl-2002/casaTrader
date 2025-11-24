from fastapi import APIRouter

from .endpoints import (
    components, health, index, metadata, pipeline, simplified, backtest,
    simplified_v2, scheduler, media, volume, auth, monitoring, financial_reports
)


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["Monitoring"])
api_router.include_router(index.router, prefix="/index", tags=["Index"])
api_router.include_router(components.router, prefix="/components", tags=["Components"])
api_router.include_router(metadata.router, prefix="/metadata", tags=["Metadata"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])
api_router.include_router(simplified.router, prefix="/simplified", tags=["Simplified"])
api_router.include_router(simplified_v2.router, prefix="/simplified-v2", tags=["Simplified V2"])
api_router.include_router(backtest.router, prefix="/backtest", tags=["Backtest"])
api_router.include_router(scheduler.router, prefix="/scheduler", tags=["Scheduler"])
api_router.include_router(media.router, prefix="/media", tags=["Media"])
api_router.include_router(volume.router, prefix="/volume", tags=["Volume"])
api_router.include_router(financial_reports.router, prefix="/financial-reports", tags=["Financial Reports"])


