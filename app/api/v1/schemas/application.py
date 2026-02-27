from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.db.models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    job_posting_id: UUID
    proposal_content: str
    bid_amount: Optional[Decimal]
    milestones: Optional[list]
    status: Optional[ApplicationStatus] = ApplicationStatus.drafted
    submitted_at: Optional[datetime]


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus]
    proposal_content: Optional[str]
    bid_amount: Optional[Decimal]
    milestones: Optional[list]
    submitted_at: Optional[datetime]


class ApplicationResponse(ApplicationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)