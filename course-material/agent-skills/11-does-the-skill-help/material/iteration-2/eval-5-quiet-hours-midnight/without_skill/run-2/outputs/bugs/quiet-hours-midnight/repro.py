"""Repro: saving quiet hours 21:00 -> 00:00 via POST /settings.

Exits 1 while the bug is present (settings rejected or not saved), 0 once fixed.
"""

import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

NOON = datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto"))

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(
        create_app(
            diary=diary,
            coach=MockCoach(),
            clock=lambda: NOON,
            trace_path=Path(tmp) / "trace.jsonl",
        )
    )
    resp = client.post(
        "/settings",
        data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
        follow_redirects=False,
    )
    user = diary.user()
    print("status", resp.status_code, "start", user.quiet_start, "end", user.quiet_end)
    ok = (
        resp.status_code == 303
        and str(user.quiet_start) == "21:00:00"
        and str(user.quiet_end) == "00:00:00"
    )
    sys.exit(0 if ok else 1)
