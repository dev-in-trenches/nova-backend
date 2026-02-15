"""User repository with user-specific operations."""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.repositories.base import BaseRepository
from app.db.models.user import User, UserRole


class UserRepository(BaseRepository[User]):
    """Repository for User model with user-specific queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository."""
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            User instance or None
        """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: Username

        Returns:
            User instance or None
        """
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email_or_username(
        self, email_or_username: str
    ) -> Optional[User]:
        """
        Get user by email or username.

        Args:
            email_or_username: Email or username

        Returns:
            User instance or None
        """
        result = await self.session.execute(
            select(User).where(
                (User.email == email_or_username)
                | (User.username == email_or_username)
            )
        )
        return result.scalar_one_or_none()

    async def get_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get users by role.

        Args:
            role: User role
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of users with the specified role
        """
        result = await self.session.execute(
            select(User)
            .where(User.role == role)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get active users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active users
        """
        return await self.get_all(skip=skip, limit=limit, is_active=True)
