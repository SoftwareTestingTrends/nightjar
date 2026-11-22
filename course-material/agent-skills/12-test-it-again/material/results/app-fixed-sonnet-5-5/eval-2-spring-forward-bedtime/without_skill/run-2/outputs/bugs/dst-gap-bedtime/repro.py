"""Repro: a bedtime of 02:30 on 2026-03-08 in America/Toronto doesn't exist (clocks jump
02:00 -> 03:00). The diary silently stores it as 03:30 instead of rejecting it.

Run from the repo root: uv run python bugs/dst-gap-bedtime/repro.py
Exits 1 while the bug is present, 0 once it's fixed.
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

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    app = create_app(
        diary=diary,
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto")),
        trace_path=Path(tmp) / "coach.jsonl",
    )
    response = TestClient(app).post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",  # nonexistent local time
            "wake_time": "2026-03-08T10:30",
            "timezone": "America/Toronto",
        },
        follow_redirects=False,
    )
    nights = diary.nights()

if nights and nights[0].local_bedtime.strftime("%H:%M") != "02:30":
    shown = nights[0].local_bedtime.strftime("%H:%M")
    print("BUG: entered 02:30 (doesn't exist), HTTP", response.status_code, "diary shows", shown)
    sys.exit(1)
print("OK: HTTP", response.status_code, "- nonexistent bedtime not silently shifted")
sys.exit(0)
