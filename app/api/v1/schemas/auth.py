"""Authentication schemas."""

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List
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

    # These define the fields
    username: str
    email: EmailStr
    password: str
    full_name: str
    skills: List[str]
    experience_summary: str
    portfolio_links: List[HttpUrl]
    preferred_rate: float

    # This updates the "Example Value" in Swagger UI
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "freelancer123",
                    "email": "freelancer@example.com",
                    "password": "securepassword123",
                    "full_name": "Jane Doe",
                    "skills": ["Python", "FastAPI", "React"],
                    "experience_summary": "5 years of full-stack development experience specializing in AI integrations.",
                    "portfolio_links": ["https://github.com/janedoe", "https://janedoe.dev"],
                    "preferred_rate": 75
                }
            ]
        }
    }
