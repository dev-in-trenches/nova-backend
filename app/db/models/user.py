"""User model."""

import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, TypeDecorator
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

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(UserRoleEnum(), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)  # Keep for backward compatibility
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
