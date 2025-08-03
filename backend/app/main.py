"""FastAPI application for the AI‑Powered Accessibility Compliance service.

This module defines the primary FastAPI application and exposes
endpoints for kicking off an accessibility scan and retrieving its
results. Scan requests are queued and processed asynchronously to
avoid blocking the HTTP request/response cycle.

The application uses a simple SQLite database to persist scan
metadata and results. Sensitive values (e.g. third‑party API keys)
are encrypted at rest using AES‑256‑GCM via the crypto helpers
defined in :mod:`crypto`.

Note: the actual scanning logic is implemented in `scan.py` and
currently uses stubbed data. You will need to replace the stub with
real headless Chrome + axe‑core/Pa11y integration when you are ready
to support full accessibility reports.
"""

from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from . import database, models, schemas, scan

app = FastAPI(title="AI‑Powered Accessibility Compliance", version="0.1.0")

# Configure CORS for development – adjust allowed origins in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    """Request body schema for creating a new accessibility scan."""

    url: HttpUrl


@app.on_event("startup")
async def on_startup() -> None:
    """Initialise the database tables on application startup."""
    database.Base.metadata.create_all(bind=database.engine)


def get_db() -> Session:
    """Provide a SQLAlchemy session dependency for route handlers."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/scan", response_model=schemas.Scan)
async def create_scan(
    request: ScanRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> models.Scan:
    """Create a new accessibility scan.

    This endpoint persists a new `Scan` row with status `pending` and
    triggers an asynchronous background task to perform the scan.

    Args:
        request: Payload containing the URL to scan.
        background_tasks: FastAPI background task manager.
        db: Database session.

    Returns:
        A `Scan` instance representing the queued job.
    """
    new_scan = models.Scan(
        url=str(request.url),
        status=models.ScanStatus.pending,
        created_at=datetime.utcnow(),
    )
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    # Kick off the asynchronous job
    background_tasks.add_task(scan.run_scan, new_scan.id)
    return new_scan


@app.get("/scan/{scan_id}", response_model=schemas.Scan)
async def get_scan(scan_id: int, db: Session = Depends(get_db)) -> models.Scan:
    """Retrieve a previously requested scan by its ID."""
    scan_obj = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan_obj:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan_obj
