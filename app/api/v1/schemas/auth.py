"""Authentication schemas."""

from pydantic import BaseModel, EmailStr
from app.api.v1.schemas.user import UserResponse


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str


class TokenRefresh(BaseModel):
    """Token refresh request schema."""

    refresh_token: str


class UserCreate(BaseModel):
    """User creation schema."""

    email: EmailStr
    username: str
    password: str
    full_name: str | None = None
