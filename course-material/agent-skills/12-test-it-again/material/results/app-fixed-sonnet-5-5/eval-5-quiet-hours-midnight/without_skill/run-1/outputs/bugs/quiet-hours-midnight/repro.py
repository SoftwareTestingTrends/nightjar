"""Repro: quiet hours 21:00 -> 00:00 should save. Exits 1 while the bug is present, 0 once fixed."""

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
diary = Diary(tmp / "repro.db")
app = create_app(
    diary=diary,
    coach=MockCoach(),
    clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto")),
    trace_path=tmp / "coach.jsonl",
)
client = TestClient(app)
response = client.post(
    "/settings",
    data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
    follow_redirects=False,
)
saved = diary.user()
print(f"status={response.status_code} saved={saved.quiet_start}-{saved.quiet_end}")
ok = response.status_code == 303 and str(saved.quiet_end) == "00:00:00"
sys.exit(0 if ok else 1)
