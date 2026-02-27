"""Job Service for create, get, delete"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.job import (
    JobPostingCreate,
    JobPostingResponse,
    JobPostingUpsert,
)
from app.db.repositories.job_repository import JobPostingRepository


class JobPostingService:
    """Job Service"""

    def __init__(self, session: AsyncSession):
        """
        Initialize Job service.

        Args:
            session: Database session
        """
        self.repository = JobPostingRepository(session)

    async def create_jobposting(self, payload: JobPostingCreate) -> JobPostingResponse:
        """
        Create a new job posting.
        If the job posting already exists, update it.
        Args:
            payload: Job posting data

        Returns:
            JobPostingResponse: Created job posting
        """

        new_job = await self.repository.create(
            platform=payload.platform,
            job_title=payload.job_title,
            description=payload.description,
            budget=payload.budget,
            required_skills=payload.required_skills,
            url=str(payload.url),
        )

        return JobPostingResponse.model_validate(new_job)

    async def update_jobposting(
        self, id: UUID, payload: JobPostingUpsert
    ) -> JobPostingResponse:
        """
        Update a job posting.
        Args:
            id: Job posting ID
            payload: Job posting data

        Returns:
            JobPostingResponse: Updated job posting
        """

        updated_job = await self.repository.update(
            id=id,
            platform=payload.platform,
            job_title=payload.job_title,
            description=payload.description,
            budget=payload.budget,
            required_skills=payload.required_skills,
            url=str(payload.url),
        )

        return JobPostingResponse.model_validate(updated_job)

    async def get_jobpostings(self, skip: int, limit: int) -> list[JobPostingResponse]:
        """
        Get a list of job postings.
        Args:
            skip: Number of job postings to skip
            limit: Maximum number of job postings to return

        Returns:
            list[JobPostingResponse]: List of job postings
        """

        results = await self.repository.get_all(skip=skip, limit=limit)

        return [JobPostingResponse.model_validate(job) for job in results]

    async def get_jobposting(self, id: UUID) -> JobPostingResponse | None:
        """
        Get a job posting.
        Args:
            id: Job posting ID

        Returns:
            JobPostingResponse: Job posting
        """

        job = await self.repository.get_by_id(id)

        return JobPostingResponse.model_validate(job) if job else None
