from __future__ import annotations

from datetime import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings
from app.core.logging import get_logger


logger = get_logger(__name__)


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler(timezone=settings.scheduler_timezone)

    def start(self) -> None:
        if not self.scheduler.running:
            logger.info("Starting scheduler")
            self.scheduler.start()

    def shutdown(self) -> None:
        if self.scheduler.running:
            logger.info("Shutting down scheduler")
            self.scheduler.shutdown()

    def schedule_daily_job(
        self, 
        job_callable, 
        run_time: str | None = None,
        job_id: str = "daily_index_job"
    ) -> None:
        """
        Schedule a job to run daily at a specific time.
        
        Args:
            job_callable: Function to call
            run_time: Time in format "HH:MM" (default: from settings)
            job_id: Unique job identifier
        """
        run_time = run_time or settings.scheduler_daily_run
        hour, minute = map(int, run_time.split(":"))
        trigger = CronTrigger(hour=hour, minute=minute)
        self.scheduler.add_job(job_callable, trigger=trigger, id=job_id, replace_existing=True)
        logger.info(f"Scheduled daily job '{job_id}' at {run_time}")

    def schedule_interval_job(
        self, 
        job_callable, 
        minutes: int = 10,
        job_id: str = "interval_job"
    ) -> None:
        """
        Schedule a job to run at regular intervals.
        
        Args:
            job_callable: Function to call
            minutes: Interval in minutes (default: 10)
            job_id: Unique job identifier
        """
        trigger = IntervalTrigger(minutes=minutes)
        self.scheduler.add_job(
            job_callable, 
            trigger=trigger, 
            id=job_id, 
            replace_existing=True,
            max_instances=1  # Prevent overlapping executions
        )
        logger.info(f"Scheduled interval job '{job_id}' every {minutes} minutes")

    def remove_job(self, job_id: str) -> None:
        """Remove a scheduled job by ID"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed job '{job_id}'")
        except Exception as e:
            logger.warning(f"Failed to remove job '{job_id}': {e}")

    def list_jobs(self) -> list:
        """List all scheduled jobs"""
        return self.scheduler.get_jobs()



