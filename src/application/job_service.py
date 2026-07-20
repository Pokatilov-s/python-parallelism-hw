import uuid
import asyncio
import logging

from src.application.report_service import ReportService
from src.infrastructure.job_store import JobStore, Job

log = logging.getLogger(__name__)


class JobService:
    def __init__(self, report_service: ReportService, job_store: JobStore):
        self._report_service = report_service
        self._job_store = job_store

    def get_report_job(self, job_id: uuid.UUID) -> Job | None:
        return self._job_store.get(job_id)

    def start_report_job(self, user_id) -> uuid.UUID:
        job_id = self._job_store.create()
        asyncio.create_task(self._run_report_job(user_id, job_id))
        return job_id

    async def _run_report_job(self, user_id: int, job_id: uuid.UUID) -> None:
        try:
            report = await self._report_service.build_report(user_id)
            self._job_store.mark_done(job_id, report)
        except* Exception as eg:
            log.exception(str(eg.exceptions[0]))
            self._job_store.mark_error(job_id, str(eg.exceptions[0]))
