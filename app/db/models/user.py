"""User model."""

import enum
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, TypeDecorator, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.db.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""

    USER = "user"
    ADMIN = "admin"


class UserRoleEnum(TypeDecorator):
    """Type decorator to ensure enum values are used, not names."""
    
    impl = String
    cache_ok = True
    
    def __init__(self):
        super().__init__()
        self.enum = UserRole
    
    def process_bind_param(self, value, dialect):
        """Convert enum to its value for database storage."""
        if value is None:
            return value
        if isinstance(value, UserRole):
            return value.value  # Return "admin" or "user"
        if isinstance(value, str):
            # If it's already a string, validate it
            try:
                UserRole(value)
                return value
            except ValueError:
                raise ValueError(f"Invalid role value: {value}")
        return value
    
    def process_result_value(self, value, dialect):
        """Convert database value back to enum."""
        if value is None:
            return value
        if isinstance(value, str):
            return UserRole(value)
        return value


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    email = Column(String(320), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    password_hash = Column(String(1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    role = Column(UserRoleEnum(), default=UserRole.USER, nullable=False)
    skills = Column(JSON, server_default='[]', nullable=False)
    experience_summary = Column(String, nullable=True)
    portfolio_links = Column(JSON, server_default='[]', nullable=False)
    preferred_rate = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
