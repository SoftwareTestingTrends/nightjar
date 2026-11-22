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
    app = create_app(
        diary=Diary(Path(tmp) / "repro.db"),
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto")),
        trace_path=Path(tmp) / "coach.jsonl",
    )
    client = TestClient(app)
    response = client.post(
        "/settings",
        data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
        follow_redirects=False,
    )

if response.status_code == 303:
    print("OK: quiet hours 21:00-00:00 accepted (HTTP 303)")
    sys.exit(0)
print("BUG: quiet hours 21:00-00:00 rejected, HTTP", response.status_code)
sys.exit(1)
