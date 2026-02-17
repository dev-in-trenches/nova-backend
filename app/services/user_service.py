"""User service with business logic."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user_repository import UserRepository
from app.db.models.user import User, UserRole
from app.api.v1.schemas.user import UserResponse, UserUpdate
from app.core.exceptions import NotFoundError, BadRequestError


class UserService:
    """Service for user business logic."""

    def __init__(self, session: AsyncSession):
        """
        Initialize user service.

        Args:
            session: Database session
        """
        self.repository = UserRepository(session)

    def _to_response(self, user: User) -> UserResponse:
        """
        Convert User model to UserResponse schema.

        Args:
            user: User model instance

        Returns:
            UserResponse schema
        """
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role.value if user.role else "user",
            is_active=user.is_active,
            created_at=user.created_at,
        )

    async def get_user_by_id(self, user_id: UUID) -> UserResponse:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            UserResponse schema

        Raises:
            NotFoundError: If user not found
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return self._to_response(user)

    async def get_users(
        self, skip: int = 0, limit: int = 20
    ) -> List[UserResponse]:
        """
        Get paginated list of users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of UserResponse schemas
        """
        users = await self.repository.get_all(skip=skip, limit=limit)
        return [self._to_response(user) for user in users]

    async def update_user(
        self, user_id: UUID, user_update: UserUpdate
    ) -> UserResponse:
        """
        Update user information.

        Args:
            user_id: User ID
            user_update: User update data

        Returns:
            Updated UserResponse schema

        Raises:
            NotFoundError: If user not found
            BadRequestError: If email already exists
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        update_data = user_update.model_dump(exclude_unset=True)

        # Check if email is being updated and if it already exists
        if "email" in update_data and update_data["email"] != user.email:
            existing_user = await self.repository.get_by_email(update_data["email"])
            if existing_user:
                raise BadRequestError("Email already registered")

        updated_user = await self.repository.update(user_id, **update_data)
        if not updated_user:
            raise NotFoundError("User not found")

        return self._to_response(updated_user)

    async def update_user_role(
        self, user_id: UUID, role: UserRole
    ) -> UserResponse:
        """
        Update user role.

        Args:
            user_id: User ID
            role: New role

        Returns:
            Updated UserResponse schema

        Raises:
            NotFoundError: If user not found
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        is_admin = role == UserRole.ADMIN
        updated_user = await self.repository.update(
            user_id, role=role, is_admin=is_admin
        )
        if not updated_user:
            raise NotFoundError("User not found")

        return self._to_response(updated_user)

    async def toggle_user_activation(
        self, user_id: UUID, is_active: bool
    ) -> UserResponse:
        """
        Activate or deactivate a user.

        Args:
            user_id: User ID
            is_active: Active status

        Returns:
            Updated UserResponse schema

        Raises:
            NotFoundError: If user not found
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        updated_user = await self.repository.update(user_id, is_active=is_active)
        if not updated_user:
            raise NotFoundError("User not found")

        return self._to_response(updated_user)

    async def get_all_users(self) -> List[UserResponse]:
        """
        Get all users (admin only).

        Returns:
            List of UserResponse schemas
        """
        users = await self.repository.get_all(skip=0, limit=1000)
        return [self._to_response(user) for user in users]
