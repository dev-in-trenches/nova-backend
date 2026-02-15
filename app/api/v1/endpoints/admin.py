"""Admin endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_admin_user
from app.core.exceptions import AppException
from app.db.database import get_db
from app.db.models.user import UserRole
from app.api.v1.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
async def list_all_users(
    current_user: dict = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all users (admin only)."""
    user_service = UserService(db)
    return await user_service.get_all_users()


@router.patch("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    role: UserRole,
    current_user: dict = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user role (admin only)."""
    try:
        user_service = UserService(db)
        return await user_service.update_user_role(user_id, role)
    except AppException as e:
        raise e


@router.patch("/users/{user_id}/activate", response_model=UserResponse)
async def toggle_user_activation(
    user_id: int,
    is_active: bool,
    current_user: dict = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Activate or deactivate a user (admin only)."""
    try:
        user_service = UserService(db)
        return await user_service.toggle_user_activation(user_id, is_active)
    except AppException as e:
        raise e
