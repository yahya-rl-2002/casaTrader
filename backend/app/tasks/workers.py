from __future__ import annotations

import asyncio

from app.core.logging import get_logger
from app.services.scheduler import SchedulerService
from app.tasks.jobs import run_daily_index_pipeline


logger = get_logger(__name__)


class Worker:
    def __init__(self) -> None:
        self.scheduler_service = SchedulerService()

    def start(self) -> None:
        logger.info("Starting background worker")
        self.scheduler_service.schedule_daily_job(self._run_pipeline_wrapper)
        self.scheduler_service.start()

    @staticmethod
    def _run_pipeline_wrapper() -> None:
        asyncio.create_task(run_daily_index_pipeline())



