import enum
import uuid

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Index, Numeric, Text, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.db.database import Base


class ApplicationStatus(str, enum.Enum):
    drafted = "drafted"
    approved = "approved"
    submitted = "submitted"
    interviewed = "interviewed"
    won = "won"
    lost = "lost"


class Application(Base):
    __tablename__ = "applications"

    id = Column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_posting_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("job_postings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status = Column(
        Enum(ApplicationStatus, name="application_status_enum", create_type=True),
        server_default="drafted",
        nullable=False,
    )
    proposal_content = Column(Text, nullable=False)
    bid_amount = Column(Numeric(10, 2), nullable=True)
    milestones = Column(JSON, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    submitted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_applications_status", "status"),
        Index("idx_applications_user_status", "user_id", "status"),
    )
