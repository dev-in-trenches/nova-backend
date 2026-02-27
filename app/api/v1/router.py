"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import admin, application, auth, health, job_posting, users

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(
    application.router, prefix="/applications", tags=["applications"]
)
api_router.include_router(job_posting.router, prefix="/jobs", tags=["jobs"])
