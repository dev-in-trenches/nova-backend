"""Health check endpoints."""

from datetime import datetime

from fastapi import APIRouter

from app.core.redis import redis_client

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    # Add database connectivity check here if needed
    redis = redis_client.redis
    is_redis_connected = False
    if redis:
        is_redis_connected = await redis.ping()
    return {
        "status": "ready",
        "redis": "connected" if is_redis_connected else "disconnected",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/live")
async def liveness_check():
    """Liveness check endpoint."""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
    }
