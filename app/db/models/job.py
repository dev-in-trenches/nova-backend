"""JOB LISTING MODEL"""

import enum
import uuid

from sqlalchemy import DECIMAL, JSON, Column, DateTime, Enum, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from app.db.database import Base


class PlatformEnum(str, enum.Enum):
    """Enum for job posting platforms"""

    upwork = "upwork"
    freelancer = "freelancer"


class JobPosting(Base):
    """Model for job postings"""

    __tablename__ = "job_postings"

    id = Column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    platform = Column(Enum(PlatformEnum, name="platform_enum"), nullable=False)
    job_title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    budget = Column(DECIMAL, nullable=True)
    required_skills = Column(JSON, nullable=False)
    url = Column(String, nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    __table_args__ = (
        Index("idx_job_title", "job_title"),
        Index("idx_platform", "platform"),
        Index("idx_created_at", "created_at"),
    )
