"""Application Service for create, get, delete"""

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from app.core.exceptions import NotFoundError
from app.db.models.application import ApplicationStatus
from app.db.repositories.application_repository import ApplicationRepository


class ApplicationService:
    """Application Service"""

    def __init__(self, session: AsyncSession):
        """
        Initialize application service.

        Args:
            session: Database session
        """
        self.repository = ApplicationRepository(session)

    async def create_application(
        self, user_id: UUID, payload: ApplicationCreate
    ) -> ApplicationResponse:
        """Create a new application.

        Args:
            user_id: User ID
            payload: Application create payload

        Returns:
            Application response
        """

        new_app = await self.repository.create(
            user_id=user_id,
            job_posting_id=payload.job_posting_id,
            status=payload.status,
            proposal_content=payload.proposal_content,
            bid_amount=payload.bid_amount,
            milestones=payload.milestones,
            submitted_at=payload.submitted_at,
        )

        return ApplicationResponse.model_validate(new_app)

    async def get_applications(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 20,
        status: Optional[ApplicationStatus] = None,
        sort: Literal["asc", "desc"] = "desc",
    ) -> list[ApplicationResponse]:
        """Get applications by user ID.

        Args:
            user_id: User ID
            skip: Number of applications to skip
            limit: Maximum number of applications to return
            status: Optional application status filter
            sort: Sort order for created_at ("asc" or "desc")

        Returns:
            List of application responses
        """

        applications = await self.repository.get_by_user_id(
            user_id, skip, limit, status, sort
        )

        return [ApplicationResponse.model_validate(app) for app in applications]

    async def get_application(
        self, user_id: UUID, application_id: UUID
    ) -> ApplicationResponse | None:
        """Get application by application ID.

        Args:
            user_id: User ID
            application_id: Application ID

        Returns:
            Application ApplicationResponse
        """

        application = await self.repository.get_by_application_id(
            user_id, application_id
        )

        return ApplicationResponse.model_validate(application) if application else None

    async def update_application(
        self, user_id: UUID, application_id: UUID, payload: ApplicationUpdate
    ) -> ApplicationResponse:
        """Update application by application ID.

        Args:
            user_id: User ID
            application_id: Application ID
            payload: Application update payload

        Returns:
            Application ApplicationResponse
        """

        application = await self.repository.get_by_application_id(
            user_id, application_id
        )

        if not application:
            raise NotFoundError("Application not found")
        submitted_at = (
            datetime.utcnow()
            if payload.status == ApplicationStatus.submitted
            else application.submitted_at
        )

        updated_app = await self.repository.update(
            id=application_id,
            **payload.model_dump(exclude_unset=True),
            submitted_at=submitted_at,
        )

        return ApplicationResponse.model_validate(updated_app)

    async def delete_application(self, user_id: UUID, application_id: UUID) -> bool:
        """Delete application by application ID.

        Args:
            user_id: User ID
            application_id: Application ID

        Returns:
            Application ApplicationResponse
        """

        application = await self.repository.get_by_application_id(
            user_id, application_id
        )

        if not application:
            raise NotFoundError("Application not found")

        return await self.repository.delete(
            id=application_id,
        )
