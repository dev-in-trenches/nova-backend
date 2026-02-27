"""Jobs endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.job import (
    JobPostingCreate,
    JobPostingResponse,
    JobPostingUpsert,
)
from app.core.exceptions import AppException
from app.db.database import get_db
from app.services.job_service import JobPostingService

router = APIRouter()


@router.post("", response_model=JobPostingResponse)
async def create_jobposting(
    payload: JobPostingUpsert,
    db: AsyncSession = Depends(get_db),
):
    try:
        jobposting_service = JobPostingService(db)
        jobposting = await jobposting_service.repository.get_by_url(str(payload.url))
        print(jobposting, payload)

        if jobposting is not None:
            return await jobposting_service.update_jobposting(
                UUID(str(jobposting.id)), payload
            )
        else:
            job_data = JobPostingCreate(**payload.model_dump())
            return await jobposting_service.create_jobposting(job_data)
    except AppException as e:
        raise e


@router.get("", response_model=list[JobPostingResponse])
async def get_jobpostings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    try:
        jobposting_service = JobPostingService(db)
        return await jobposting_service.get_jobpostings(skip=skip, limit=limit)
    except AppException as e:
        raise e


@router.get("/{job_id}", response_model=JobPostingResponse)
async def get_jobposting(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        jobposting_service = JobPostingService(db)
        jobposting = await jobposting_service.get_jobposting(job_id)
        return jobposting
    except AppException as e:
        raise e
