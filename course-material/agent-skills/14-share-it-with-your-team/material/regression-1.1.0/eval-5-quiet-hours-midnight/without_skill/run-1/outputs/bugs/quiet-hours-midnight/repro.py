"""Repro: saving quiet hours 21:00 -> 00:00 via the settings form is rejected.

Exits 1 while the bug is present, 0 once it is fixed.
Run: uv run python bugs/quiet-hours-midnight/repro.py
"""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "diary.db")
    client = TestClient(
        create_app(diary=diary, trace_path=Path(tmp) / "trace.jsonl"),
        follow_redirects=False,
    )
    response = client.post(
        "/settings",
        data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
    )
    user = diary.user()
    saved = (user.quiet_start and user.quiet_start.strftime("%H:%M"), user.quiet_end and user.quiet_end.strftime("%H:%M"))
    print(f"status={response.status_code} saved={saved}")
    if response.status_code == 303 and saved == ("21:00", "00:00"):
        print("OK: quiet hours 21:00-00:00 saved")
        sys.exit(0)
    print("BUG: quiet hours 21:00-00:00 were not saved")
    sys.exit(1)
