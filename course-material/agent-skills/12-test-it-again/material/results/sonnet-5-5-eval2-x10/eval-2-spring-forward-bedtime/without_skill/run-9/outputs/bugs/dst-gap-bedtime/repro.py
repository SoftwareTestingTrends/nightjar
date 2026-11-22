"""Repro: a bedtime inside the spring-forward gap is silently shifted.

02:30 on 2026-03-08 doesn't exist in America/Toronto (clocks jump 02:00 -> 03:00).
The app accepts it and the diary later shows 03:30. Fixed = the form rejects the
time (HTTP 400) instead of silently changing it.

Run from the repo root: uv run python bugs/dst-gap-bedtime/repro.py
Exit 1 while the bug is present, 0 once fixed. Uses a throwaway database.
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

TORONTO = "America/Toronto"

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    app = create_app(
        diary=diary,
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo(TORONTO)),
        trace_path=Path(tmp) / "coach.jsonl",
    )
    response = TestClient(app).post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T09:30",
            "timezone": TORONTO,
        },
        follow_redirects=False,
    )
    nights = diary.nights()
    shown = nights[0].local_bedtime.strftime("%H:%M") if nights else None

if response.status_code == 400 and not nights:
    print("OK: nonexistent bedtime 02:30 was rejected")
    sys.exit(0)
print(f"BUG: entered 02:30 (nonexistent in Toronto), HTTP {response.status_code}, diary shows {shown}")
sys.exit(1)
