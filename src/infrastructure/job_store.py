import uuid
from dataclasses import dataclass
from enum import StrEnum

from src.domain.report import Report


class JobStatus(StrEnum):
    RUNNING = "running"
    ERROR = "error"
    DONE = "done"


@dataclass
class Job:
    status: JobStatus
    result: Report | None = None
    error: str | None = None


class JobStore:
    def __init__(self) -> None:
        self.jobs: dict[uuid.UUID, Job] = {}

    def create(self) -> uuid.UUID:
        job_id = uuid.uuid4()
        self.jobs[job_id] = Job(status=JobStatus.RUNNING)
        return job_id

    def get(self, job_id: uuid.UUID) -> Job | None:
        return self.jobs.get(job_id, None)

    def mark_done(self, job_id: uuid.UUID, result: Report) -> None:
        self.jobs[job_id] = Job(status=JobStatus.DONE, result=result)

    def mark_error(self, job_id: uuid.UUID, error: str) -> None:
        self.jobs[job_id] = Job(status=JobStatus.ERROR, error=error)
