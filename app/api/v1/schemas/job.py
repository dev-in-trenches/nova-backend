from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl

from app.db.models.job import PlatformEnum


class JobPostingBase(BaseModel):
    platform: PlatformEnum
    job_title: str
    description: str
    budget: Optional[float] = None
    required_skills: List[str]
    url: HttpUrl


class JobPostingUpsert(BaseModel):
    url: HttpUrl

    platform: Optional[PlatformEnum] = None
    job_title: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None
    required_skills: Optional[List[str]] = None


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingResponse(JobPostingBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
