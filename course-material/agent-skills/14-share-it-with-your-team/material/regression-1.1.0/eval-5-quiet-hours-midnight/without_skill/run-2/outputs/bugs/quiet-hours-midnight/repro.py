"""Repro: saving quiet hours 21:00-00:00 via /settings is rejected."""

import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

tmp = Path(tempfile.mkdtemp())
client = TestClient(
    create_app(
        diary=Diary(tmp / "t.db"),
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, tzinfo=ZoneInfo("America/Toronto")),
        trace_path=tmp / "coach.jsonl",
    )
)
r = client.post(
    "/settings",
    data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
    follow_redirects=False,
)
print("status", r.status_code)
sys.exit(0 if r.status_code == 303 else 1)
