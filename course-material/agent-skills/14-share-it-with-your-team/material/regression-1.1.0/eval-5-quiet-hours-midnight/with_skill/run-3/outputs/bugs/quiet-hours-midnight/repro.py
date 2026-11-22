"""Quiet hours 21:00-00:00 via POST /settings. Exit 1 while rejected, 0 once accepted."""

import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

tmp = Path(tempfile.mkdtemp())
client = TestClient(
    create_app(
        diary=Diary(tmp / "repro.db"),
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=UTC),
        trace_path=tmp / "coach.jsonl",
    )
)
response = client.post(
    "/settings",
    data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
    follow_redirects=False,
)
saved = Diary(tmp / "repro.db").user().quiet_end
if response.status_code == 303 and saved is not None:
    print("OK: status", response.status_code, "quiet_end saved as", saved)
    sys.exit(0)
print("BUG: status", response.status_code, "quiet_end saved as", saved)
sys.exit(1)
