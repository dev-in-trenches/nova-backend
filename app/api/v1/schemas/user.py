"""User schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    email: str
    username: str
    full_name: str | None
    role: str
    is_active: bool
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """User update schema."""

    full_name: str | None = None
    email: str | None = None
