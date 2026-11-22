"""Repro: a bedtime typed as 02:30 on 2026-03-08 (America/Toronto) is shown as 03:30.

02:30 doesn't exist that night (clocks jump 02:00 -> 03:00). The form silently accepts it
and shifts it an hour. Fixed = the form rejects it (HTTP 400) or keeps the local time as typed.
Run from the repo root: uv run python bugs/dst-gap-bedtime/repro.py
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

TORONTO = ZoneInfo("America/Toronto")

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    app = create_app(
        diary=diary,
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=TORONTO),
        trace_path=Path(tmp) / "coach.jsonl",
    )
    response = TestClient(app).post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T09:00",
            "timezone": "America/Toronto",
        },
        follow_redirects=False,
    )
    nights = diary.nights()

if response.status_code == 400 and not nights:
    print("OK: nonexistent local time 02:30 was rejected")
    sys.exit(0)

shown = nights[0].local_bedtime.strftime("%H:%M") if nights else "nothing stored"
if shown == "02:30":
    print("OK: bedtime kept as typed (02:30)")
    sys.exit(0)

print(f"BUG: typed bedtime 02:30 on 2026-03-08 in America/Toronto; diary shows {shown}")
sys.exit(1)
