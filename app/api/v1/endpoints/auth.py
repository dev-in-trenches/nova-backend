"""Authentication endpoints."""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.db.database import get_db
from app.api.v1.schemas.auth import Token, TokenRefresh, UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate, db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    try:
        auth_service = AuthService(db)
        return await auth_service.register_user(user_data)
    except AppException as e:
        raise e


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Login and get access token."""
    auth_service = AuthService(db)
    return await auth_service.authenticate_user(form_data.username, form_data.password)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token."""
    auth_service = AuthService(db)
    return await auth_service.refresh_access_token(token_data.refresh_token)
