"""Repro: quiet hours 21:00-00:00 are rejected by POST /settings.

Exit 1 while the bug is present, 0 once it's fixed.
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
    user = diary.user()
    saved = (user.quiet_start, user.quiet_end)
    ok = response.status_code == 303 and saved == (time(21, 0), time(0, 0))
    print("POST /settings 21:00-00:00 -> HTTP", response.status_code, "saved", saved)
    sys.exit(0 if ok else 1)
