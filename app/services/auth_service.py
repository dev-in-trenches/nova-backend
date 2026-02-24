"""Authentication service with business logic."""

from datetime import timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.db.repositories.user_repository import UserRepository
from app.db.models.user import User, UserRole
import uuid
from app.api.v1.schemas.auth import Token, TokenRefresh, UserCreate, UserResponse
from app.core.exceptions import BadRequestError, UnauthorizedError, ForbiddenError


class AuthService:
    """Service for authentication business logic."""

    def __init__(self, session: AsyncSession):
        """
        Initialize auth service.

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
            is_admin=getattr(user, "is_admin", False),
            skills=getattr(user, "skills", []),
            experience_summary=getattr(user, "experience_summary", ""),
            portfolio_links=getattr(user, "portfolio_links", []),
            preferred_rate=getattr(user, "preferred_rate", 0.0),
            updated_at=getattr(user, "updated_at", user.created_at),
        )

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Register a new user.

        Args:
            user_data: User creation data

        Returns:
            UserResponse schema

        Raises:
            BadRequestError: If email or username already exists
        """
        # Check if email already exists
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise BadRequestError("Email already registered")

        # Check if username already exists
        existing_user = await self.repository.get_by_username(user_data.username)
        if existing_user:
            raise BadRequestError("Username already taken")

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = await self.repository.create(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        role=UserRole.USER,
        is_active=True,
        skills=user_data.skills,
        experience_summary=user_data.experience_summary,
        portfolio_links=[str(link) for link in user_data.portfolio_links],
        preferred_rate=user_data.preferred_rate,
        )

        return self._to_response(new_user)

    async def authenticate_user(
        self, username_or_email: str, password: str
    ) -> Token:
        """
        Authenticate user and return tokens.

        Args:
            username_or_email: Username or email
            password: Plain text password

        Returns:
            Token with access and refresh tokens

        Raises:
            UnauthorizedError: If credentials are invalid
            ForbiddenError: If user is inactive
        """
        # Find user by username or email
        user = await self.repository.get_by_email_or_username(username_or_email)

        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Incorrect username or password")

        if not user.is_active:
            raise ForbiddenError("Inactive user")

        # Create tokens with role information
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user.username,
                "user_id": str(user.id),
                "role": user.role.value if user.role else "user",
                "is_admin": user.is_admin,
            },
            expires_delta=access_token_expires,
        )
        refresh_token = create_refresh_token(
            data={
                "sub": user.username,
                "user_id": str(user.id),
                "role": user.role.value if user.role else "user",
            }
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def refresh_access_token(self, refresh_token: str) -> Token:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: Refresh token string

        Returns:
            Token with new access token

        Raises:
            UnauthorizedError: If token is invalid or user not found
        """
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid token type")

        username = payload.get("sub")
        user_id = payload.get("user_id")

        # convert user_id string from token to UUID
        try:
            user_id = uuid.UUID(user_id) if user_id else None
        except Exception:
            raise UnauthorizedError("Invalid token payload")

        if not username or not user_id:
            raise UnauthorizedError("Invalid token payload")

        # Fetch user from database to get latest role
        user = await self.repository.get_by_id(user_id)

        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")

        # Get role from user
        role = user.role.value if user.role else payload.get("role", "user")

        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": username,
                "user_id": user_id,
                "role": role,
                "is_admin": user.is_admin,
            },
            expires_delta=access_token_expires,
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
