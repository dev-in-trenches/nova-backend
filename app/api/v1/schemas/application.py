from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

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


class ApplicationResponse(ApplicationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
