"""Application repository for applications specific"""

from typing import Literal, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.db.models.application import Application, ApplicationStatus
from app.db.repositories.base import BaseRepository


class ApplicationRepository(BaseRepository[Application]):
    """Application repository"""

    def __init__(self, session: AsyncSession):
        """Initialize application repository."""
        super().__init__(Application, session)

    async def get_by_user_id(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 20,
        status: Optional[ApplicationStatus] = None,
        sort: Literal["asc", "desc"] = "desc",
    ) -> list[Application]:
        """Get applications by user id."""

        query = select(Application).where(Application.user_id == user_id)

        if status is not None:
            query = query.where(Application.status == status)

        order_by = (
            Application.created_at.asc()
            if sort == "asc"
            else Application.created_at.desc()
        )

        result = await self.session.execute(
            query.order_by(order_by).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_application_id(
        self, user_id: UUID, application_id: UUID
    ) -> Application:
        """Get application by application id."""

        result = await self.session.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .where(Application.id == application_id)
        )
        return result.scalar_one_or_none()
