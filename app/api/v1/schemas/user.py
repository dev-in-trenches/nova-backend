from datetime import datetime
from uuid import UUID
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

# --- Create Schema ---
class UserCreate(BaseModel):
    """
    Schema for User Registration.
    """
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100, pattern="^[a-zA-Z0-9_-]+$")
    password: str = Field(..., min_length=8, description="Plaintext password")
    full_name: Optional[str] = Field(None, max_length=255)
    role: UserRole = UserRole.USER
    skills: List[str] = Field(default_factory=list)
    experience_summary: Optional[str] = None
    portfolio_links: List[HttpUrl] = Field(default_factory=list)
    preferred_rate: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)

# --- Update Schema ---
class UserUpdate(BaseModel):
    """
    Schema for updating User profiles. 
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    skills: Optional[List[str]] = None
    experience_summary: Optional[str] = None
    portfolio_links: Optional[List[HttpUrl]] = None
    preferred_rate: Optional[Decimal] = None

# --- Read/Response Schema ---
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    full_name: Optional[str]
    role: UserRole
    is_active: bool
    is_admin: bool
    skills: List[str]
    experience_summary: Optional[str]
    portfolio_links: List[HttpUrl]
    preferred_rate: Optional[Decimal]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)