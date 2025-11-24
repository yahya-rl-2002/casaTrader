from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel

from app.services.pipeline_service import PipelineService
from app.core.logging import get_logger
from app.core.security import get_current_user_optional, TokenData


logger = get_logger(__name__)
router = APIRouter()

pipeline_service = PipelineService()


class PipelineResponse(BaseModel):
    success: bool
    message: str
    final_score: Optional[float] = None
    target_date: Optional[date] = None
    error: Optional[str] = None


@router.post("/run", summary="Run the Fear & Greed Index pipeline", response_model=PipelineResponse)
async def run_pipeline(
    target_date: Optional[date] = None,
    background_tasks: BackgroundTasks = None,
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
) -> PipelineResponse:
    """Run the complete Fear & Greed Index calculation pipeline"""
    try:
        logger.info(f"Starting pipeline for date: {target_date or 'today'}")
        
        # Run pipeline
        result = await pipeline_service.run_full_pipeline(target_date)
        
        if result["success"]:
            return PipelineResponse(
                success=True,
                message="Pipeline completed successfully",
                final_score=result["final_score"],
                target_date=result["target_date"]
            )
        else:
            return PipelineResponse(
                success=False,
                message="Pipeline failed",
                error=result.get("error", "Unknown error"),
                target_date=result["target_date"]
            )
            
    except Exception as e:
        logger.error(f"Pipeline endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")


@router.post("/run-background", summary="Run pipeline in background")
async def run_pipeline_background(
    target_date: Optional[date] = None,
    background_tasks: BackgroundTasks = None
) -> dict:
    """Run the pipeline in the background"""
    try:
        if background_tasks:
            background_tasks.add_task(
                pipeline_service.run_full_pipeline,
                target_date
            )
            return {
                "message": "Pipeline started in background",
                "target_date": target_date or date.today()
            }
        else:
            # Run synchronously if no background tasks available
            result = await pipeline_service.run_full_pipeline(target_date)
            return result
            
    except Exception as e:
        logger.error(f"Background pipeline error: {e}")
        raise HTTPException(status_code=500, detail=f"Background pipeline failed: {str(e)}")


@router.get("/status", summary="Get pipeline status")
async def get_pipeline_status() -> dict:
    """Get the current status of the pipeline and latest data"""
    try:
        latest_data = await pipeline_service.get_latest_score()
        
        if latest_data:
            return {
                "status": "active",
                "latest_score": latest_data["score"],
                "last_updated": latest_data["as_of"],
                "components": latest_data["components"]
            }
        else:
            return {
                "status": "no_data",
                "message": "No data available. Run the pipeline first."
            }
            
    except Exception as e:
        logger.error(f"Status endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.post("/test", summary="Test pipeline components")
async def test_pipeline() -> dict:
    """Test individual pipeline components"""
    try:
        logger.info("Testing pipeline components")
        
        # Test market scraper
        market_data = pipeline_service.market_scraper.fetch_historical_data(days=30)
        
        # Test media scraper
        media_data = pipeline_service.media_scraper.scrape_all_sources(max_articles_per_source=5)
        
        # Test sentiment analysis
        if media_data:
            sentiment_results = pipeline_service.sentiment_analyzer.analyze_articles(media_data[:3])
        else:
            sentiment_results = []
        
        return {
            "market_data_count": len(market_data),
            "media_articles_count": len(media_data),
            "sentiment_analysis_count": len(sentiment_results),
            "status": "components_working"
        }
        
    except Exception as e:
        logger.error(f"Pipeline test error: {e}")
        raise HTTPException(status_code=500, detail=f"Pipeline test failed: {str(e)}")







