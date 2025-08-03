"""Accessibility scanning utilities.

This module contains the function executed asynchronously to perform
an accessibility audit of a given URL. In production you should
replace the stubbed logic with a call to a headless browser running
axe‑core or Pa11y. The resulting JSON is stored on disk or in
Supabase storage and referenced via the `report_path` field on the
`Scan` model.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .database import SessionLocal
from .models import Scan, ScanStatus


REPORTS_DIR = Path("data/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)



def _run_a11y_audit(url: str) -> Dict[str, Any]:
    """Placeholder function to perform the accessibility audit.

    For now this function returns a stubbed report containing the URL
    and a dummy violation list. In the future you should implement
    this using headless Chrome + axe‑core or Pa11y.

    Args:
        url: The URL to audit.

    Returns:
        A dictionary representing the accessibility report.
    """
    # TODO: Integrate with real accessibility tools
    return {
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "violations": [
            {
                "id": "image-alt",
                "impact": "moderate",
                "description": "Images should have alt text",
                "help": "Provide alternative text for images",
                "nodes": [],
            }
        ],
    }


def _save_report_json(scan_id: int, report: Dict[str, Any]) -> str:
    """Persist the report JSON to disk and return the path.

    Args:
        scan_id: Identifier of the scan.
        report: Report dictionary to persist.

    Returns:
        The relative path to the JSON file.
    """
    filename = f"scan_{scan_id}.json"
    path = REPORTS_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return str(path)


def run_scan(scan_id: int) -> None:
    """Perform an accessibility scan and persist the results.

    This function is invoked as a background task by the FastAPI
    application. It updates the corresponding `Scan` record in the
    database as the scan progresses.
    """
    db = SessionLocal()
    try:
        scan_record: Scan = db.query(Scan).get(scan_id)
        if not scan_record:
            return
        scan_record.status = ScanStatus.processing
        db.commit()
        # Run the audit (stubbed)
        report = _run_a11y_audit(scan_record.url)
        report_path = _save_report_json(scan_record.id, report)
        # Update the record
        scan_record.status = ScanStatus.completed
        scan_record.completed_at = datetime.utcnow()
        scan_record.report_path = report_path
        scan_record.result_json = json.dumps(report)
        db.commit()
    except Exception as exc:
        # If anything goes wrong, mark the scan as failed
        if scan_record:
            scan_record.status = ScanStatus.failed
            db.commit()
        print(f"Error running scan {scan_id}: {exc}")
    finally:
        db.close()
