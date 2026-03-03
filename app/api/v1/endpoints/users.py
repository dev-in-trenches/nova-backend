"""User endpoints."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.core.exceptions import AppException, UnauthorizedError
from app.db.database import get_db
from app.api.v1.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user information."""
    user_id = current_user.get("user_id")
    
    if not user_id:
        raise UnauthorizedError("Invalid token: user_id missing")

    try:
        user_service = UserService(db)
        return await user_service.get_user_by_id(user_id)
    except AppException as e:
        raise e


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get list of users (paginated)."""
    user_id = current_user.get("user_id")
    
    if not user_id:
        raise UnauthorizedError("User ID not found in token")
    
    user_service = UserService(db)
    return await user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user by ID."""
    
    try:
        user_service = UserService(db)
        return await user_service.get_user_by_id(user_id)
    except AppException as e:
        raise e


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user information."""

    user_id = current_user.get("user_id")
    
    if not user_id:
        raise UnauthorizedError("User ID not found in token")
    
    try:
        user_service = UserService(db)
        return await user_service.update_user(user_id, user_update)
    except AppException as e:
        raise e

@router.put("/me", response_model=UserResponse)
async def replace_current_user_info(
    user_update: UserUpdate, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Replace current user profile.
    """
    user_id = current_user.get("user_id")
    
    if not user_id:
        raise UnauthorizedError("User ID not found in token")

    try:
        user_service = UserService(db)
        return await user_service.update_user(user_id, user_update, partial=False)
    except AppException as e:
        raise e
