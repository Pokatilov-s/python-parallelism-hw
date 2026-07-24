from fastapi import Request

from src.application.job_service import JobService


def get_job_service(request: Request) -> JobService:
    return request.app.state.job_service