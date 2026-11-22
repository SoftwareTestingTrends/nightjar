"""Repro: quiet hours 21:00-00:00 are rejected by the settings form."""

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
    now = datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto"))
    diary = Diary(Path(tmp) / "repro.db")
    app = create_app(
        diary=diary, coach=MockCoach(), clock=lambda: now, trace_path=Path(tmp) / "c.jsonl"
    )
    client = TestClient(app)
    response = client.post(
        "/settings",
        data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
        follow_redirects=False,
    )
    saved = diary.user()
    ok = response.status_code == 303 and saved.quiet_end is not None
    print(
        f"POST /settings 21:00-00:00 -> HTTP {response.status_code}, "
        f"saved quiet_end={saved.quiet_end}"
    )
    sys.exit(0 if ok else 1)
