from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class PlatformEnum(str, Enum):
    """Enum for job posting platforms"""

    upwork = "upwork"
    freelancer = "freelancer"


class JobPostingBase(BaseModel):
    platform: PlatformEnum
    job_title: str
    description: str
    budget: Optional[float]
    required_skills: List[str]
    url: HttpUrl
    extracted_at: datetime


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingResponse(JobPostingBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
