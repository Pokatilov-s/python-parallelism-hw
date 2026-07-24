import uuid

from fastapi import APIRouter, Depends, status, HTTPException

from src.api.schemas import CreateReportResponse, GetReportJobResponse
from src.api.deps import get_job_service
from src.application.job_service import JobService


router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/{user_id}", response_model=CreateReportResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_report(user_id: int, job_service: JobService = Depends(get_job_service)) -> CreateReportResponse:
    job_id = job_service.start_report_job(user_id)
    job = job_service.get_report_job(job_id)
    return CreateReportResponse(job_id=job_id, status=job.status)


@router.get("/job/{job_id}", response_model=GetReportJobResponse)
async def get_report(job_id: uuid.UUID, job_service: JobService = Depends(get_job_service)) -> GetReportJobResponse:
    job = job_service.get_report_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return GetReportJobResponse(
        job_id=job_id,
        status=job.status,
        result=job.result,
    )
