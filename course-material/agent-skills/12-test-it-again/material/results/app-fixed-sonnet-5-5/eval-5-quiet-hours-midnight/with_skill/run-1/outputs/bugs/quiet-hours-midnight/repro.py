"""Repro: saving quiet hours 21:00-00:00 via POST /settings is rejected."""

import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    app = create_app(
        diary=diary,
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto")),
        trace_path=Path(tmp) / "coach.jsonl",
    )
    response = TestClient(app).post(
        "/settings",
        data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
        follow_redirects=False,
    )
    saved = diary.user()
    ok = response.status_code == 303 and str(saved.quiet_end) == "00:00:00"
    print(f"status={response.status_code} saved quiet_end={saved.quiet_end}")
    sys.exit(0 if ok else 1)
