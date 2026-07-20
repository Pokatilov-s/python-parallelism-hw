import uuid

from pydantic import BaseModel

from src.domain.report import Report
from src.infrastructure.job_store import JobStatus


class CreateReportResponse(BaseModel):
    job_id: uuid.UUID
    status: JobStatus


class GetReportJobResponse(BaseModel):
    job_id: uuid.UUID
    status: JobStatus
    result: Report | None = None
