"""D-1: a bedtime inside the spring-forward gap is silently shifted by an hour."""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    app = create_app(diary=diary, coach=MockCoach(), trace_path=Path(tmp) / "t.jsonl")
    response = TestClient(app).post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",  # does not exist in Toronto: 02:00 -> 03:00
            "wake_time": "2026-03-08T09:30",
            "timezone": "America/Toronto",
        },
        follow_redirects=False,
    )
    nights = diary.nights()
    shown = nights[0].local_bedtime.strftime("%H:%M") if nights else None

# Fixed = the bad time is rejected, or the diary shows what the user typed.
if response.status_code == 400 or shown == "02:30":
    print(f"OK: status {response.status_code}, diary shows {shown}")
    sys.exit(0)
print(f"BUG: logged 02:30 (nonexistent), accepted with {response.status_code}, diary shows {shown}")
sys.exit(1)
