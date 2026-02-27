"""Job repository for applications specific"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.db.models.job import JobPosting
from app.db.repositories.base import BaseRepository


class JobPostingRepository(BaseRepository[JobPosting]):
    """Job repository"""

    def __init__(self, session: AsyncSession):
        """Initialize job repository."""

        super().__init__(JobPosting, session)

    async def get_by_url(self, url: str) -> JobPosting | None:
        """Get job posting by URL."""

        results = await self.session.execute(
            select(JobPosting).where(JobPosting.url == url)
        )

        return results.scalar_one_or_none()
