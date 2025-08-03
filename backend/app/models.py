"""Database models for the accessibility scan service."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime, Enum as PgEnum, Integer, String, Text

from .database import Base


class ScanStatus(str, Enum):
    """Enumeration of possible scan states."""

    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Scan(Base):
    """Represents a single accessibility scan request and result."""

    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    status = Column(PgEnum(ScanStatus), default=ScanStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    report_path = Column(String, nullable=True)  # path in Supabase storage or local FS
    result_json = Column(Text, nullable=True)  # JSON string of the accessibility results

    def __repr__(self) -> str:
        return f"<Scan id={self.id} url={self.url} status={self.status}>"
