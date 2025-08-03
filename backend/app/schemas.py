"""Pydantic schemas for data validation and serialization."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl

from .models import ScanStatus


class ScanBase(BaseModel):
    """Base schema representing common scan fields."""

    url: HttpUrl
    status: ScanStatus

    class Config:
        orm_mode = True


class Scan(ScanBase):
    """Schema returned from the API for a scan."""

    id: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    report_path: Optional[str] = None
    result_json: Optional[str] = None
