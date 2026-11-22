"""Repro: saving quiet hours 21:00-00:00 in Settings is rejected.

Exit 1 while the bug is present, 0 once fixed.
"""

import sys
import tempfile
from datetime import datetime, time
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
    print("status:", response.status_code)
    saved = diary.user()
    print("saved:", saved.quiet_start, saved.quiet_end)
    if response.status_code != 303 or (saved.quiet_start, saved.quiet_end) != (
        time(21, 0),
        time(0, 0),
    ):
        print("BUG: quiet hours 21:00-00:00 were not saved")
        sys.exit(1)
    print("OK")
