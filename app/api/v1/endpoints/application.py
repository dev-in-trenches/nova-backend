"""Application endpoints."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from app.core.exceptions import AppException
from app.core.security import get_current_user
from app.db.database import get_db
from app.db.models.application import ApplicationStatus
from app.services.application_service import ApplicationService

router = APIRouter()


@router.post("", response_model=ApplicationResponse)
async def create_application(
    payload: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        application_service = ApplicationService(db)
        return await application_service.create_application(
            current_user["user_id"], payload
        )
    except AppException as e:
        raise e


@router.get("", response_model=list[ApplicationResponse])
async def get_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        application_service = ApplicationService(db)
        return await application_service.get_applications(
            current_user["user_id"], skip, limit
        )
    except AppException as e:
        raise e


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        application_service = ApplicationService(db)
        return await application_service.get_application(
            current_user["user_id"], application_id
        )
    except AppException as e:
        raise e


@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: UUID,
    payload: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        application_service = ApplicationService(db)
        return await application_service.update_application(
            current_user["user_id"], application_id, payload
        )
    except AppException as e:
        raise e


@router.delete("/{application_id}", response_model=bool)
async def delete_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        application_service = ApplicationService(db)
        return await application_service.delete_application(
            current_user["user_id"], application_id
        )
    except AppException as e:
        raise e
