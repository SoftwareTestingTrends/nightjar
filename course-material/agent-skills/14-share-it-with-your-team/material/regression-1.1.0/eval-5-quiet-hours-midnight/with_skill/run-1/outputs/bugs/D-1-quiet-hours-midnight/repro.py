"""D-1: quiet hours 21:00-00:00 are rejected by Settings. Exit 1 while broken, 0 once fixed."""

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
        diary=Diary(tmp / "throwaway.db"),
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto")),
        trace_path=tmp / "coach.jsonl",
    )
)
response = client.post(
    "/settings",
    data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
    follow_redirects=False,
)
saved = Diary(tmp / "throwaway.db").user()
if response.status_code == 303 and saved.quiet_end is not None:
    print(f"OK: 21:00-00:00 accepted (status {response.status_code}, saved end {saved.quiet_end})")
    sys.exit(0)
print(f"BUG: 21:00-00:00 rejected or not saved (status {response.status_code})")
sys.exit(1)
