"""Quiet hours 21:00 -> 00:00 should be accepted by POST /settings."""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(str(Path(tmp) / "repro.db"))
    client = TestClient(create_app(diary=diary), follow_redirects=False)
    r = client.post(
        "/settings",
        data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
    )
    saved = diary.user()
    ok = r.status_code == 303 and str(saved.quiet_end) == "00:00:00"
    print(f"POST /settings 21:00-00:00 -> HTTP {r.status_code}; saved quiet_end={saved.quiet_end}")
    sys.exit(0 if ok else 1)
