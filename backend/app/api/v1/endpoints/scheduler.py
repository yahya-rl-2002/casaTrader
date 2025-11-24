from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.logging import get_logger


router = APIRouter()
logger = get_logger(__name__)


def get_scheduler_service(request: Request):
    """Get scheduler service from app state"""
    return request.app.state.scheduler_service


class SchedulerStatusResponse(BaseModel):
    """Response for scheduler status"""
    running: bool
    jobs_count: int
    jobs: list[dict]


class SchedulerConfigRequest(BaseModel):
    """Request to configure scheduler"""
    interval_minutes: int


@router.get("/status", summary="Get scheduler status", response_model=SchedulerStatusResponse)
async def get_scheduler_status(request: Request) -> SchedulerStatusResponse:
    """
    Get the current status of the scheduler.
    
    Returns:
    - running: Whether the scheduler is active
    - jobs_count: Number of scheduled jobs
    - jobs: List of job details
    """
    scheduler_service = get_scheduler_service(request)
    jobs = scheduler_service.list_jobs()
    
    jobs_info = []
    for job in jobs:
        jobs_info.append({
            "id": job.id,
            "name": job.name,
            "next_run_time": str(job.next_run_time) if job.next_run_time else None,
            "trigger": str(job.trigger),
        })
    
    return SchedulerStatusResponse(
        running=scheduler_service.scheduler.running,
        jobs_count=len(jobs),
        jobs=jobs_info
    )


@router.post("/pause/{job_id}", summary="Pause a scheduled job")
async def pause_job(job_id: str, request: Request):
    """
    Pause a specific scheduled job.
    
    Args:
    - job_id: ID of the job to pause
    """
    try:
        scheduler_service = get_scheduler_service(request)
        scheduler_service.scheduler.pause_job(job_id)
        logger.info(f"Job '{job_id}' paused")
        return {"message": f"Job '{job_id}' paused successfully"}
    except Exception as e:
        logger.error(f"Failed to pause job '{job_id}': {e}")
        return {"error": str(e)}


@router.post("/resume/{job_id}", summary="Resume a paused job")
async def resume_job(job_id: str, request: Request):
    """
    Resume a paused scheduled job.
    
    Args:
    - job_id: ID of the job to resume
    """
    try:
        scheduler_service = get_scheduler_service(request)
        scheduler_service.scheduler.resume_job(job_id)
        logger.info(f"Job '{job_id}' resumed")
        return {"message": f"Job '{job_id}' resumed successfully"}
    except Exception as e:
        logger.error(f"Failed to resume job '{job_id}': {e}")
        return {"error": str(e)}


@router.post("/trigger", summary="Trigger pipeline update immediately")
async def trigger_pipeline():
    """
    Manually trigger the Fear & Greed Index pipeline to run immediately.
    This will:
    - Scrape new articles from media sources
    - Analyze sentiment (with LLM if available)
    - Calculate all components
    - Update the index score
    """
    try:
        from app.services.pipeline_service import PipelineService
        from datetime import date
        import asyncio
        
        logger.info("🚀 Pipeline triggered manually from API")
        
        # Create pipeline service and run asynchronously
        async def run_pipeline():
            service = PipelineService(use_llm_sentiment=True)
            result = await service.run_full_pipeline(target_date=date.today())
            logger.info(f"✅ Manual pipeline completed: Score = {result['final_score']:.2f}")
        
        # Run the pipeline in the background
        asyncio.create_task(run_pipeline())
        
        return {
            "message": "Pipeline triggered successfully",
            "status": "running"
        }
    except Exception as e:
        logger.error(f"Failed to trigger pipeline: {e}")
        return {"error": str(e)}


@router.post("/trigger/{job_id}", summary="Trigger a specific job immediately")
async def trigger_job(job_id: str, request: Request):
    """
    Manually trigger a scheduled job to run immediately.
    
    Args:
    - job_id: ID of the job to trigger
    """
    try:
        scheduler_service = get_scheduler_service(request)
        job = scheduler_service.scheduler.get_job(job_id)
        if job:
            job.func()
            logger.info(f"Job '{job_id}' triggered manually")
            return {"message": f"Job '{job_id}' triggered successfully"}
        else:
            return {"error": f"Job '{job_id}' not found"}
    except Exception as e:
        logger.error(f"Failed to trigger job '{job_id}': {e}")
        return {"error": str(e)}


@router.post("/configure", summary="Update scheduler configuration")
async def configure_scheduler(config: SchedulerConfigRequest, request: Request):
    """
    Update the scheduler interval.
    
    Args:
    - interval_minutes: New interval in minutes
    """
    try:
        from app.tasks.jobs import run_index_update_job
        
        scheduler_service = get_scheduler_service(request)
        
        # Remove existing job
        scheduler_service.remove_job("index_update_10min")
        
        # Add new job with updated interval
        scheduler_service.schedule_interval_job(
            job_callable=run_index_update_job,
            minutes=config.interval_minutes,
            job_id="index_update_10min"
        )
        
        logger.info(f"Scheduler reconfigured to run every {config.interval_minutes} minutes")
        
        return {
            "message": f"Scheduler updated successfully",
            "interval_minutes": config.interval_minutes
        }
    except Exception as e:
        logger.error(f"Failed to reconfigure scheduler: {e}")
        return {"error": str(e)}







