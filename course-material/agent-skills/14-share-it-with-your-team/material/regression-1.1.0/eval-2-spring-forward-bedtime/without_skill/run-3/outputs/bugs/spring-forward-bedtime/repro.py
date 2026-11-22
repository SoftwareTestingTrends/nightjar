"""Repro: a bedtime typed into the skipped spring-forward hour is silently saved an hour later.

Toronto clocks jump 02:00 -> 03:00 on 2026-03-08, so 02:30 never happens. The diary form
accepts it anyway and stores 03:30 with no warning. Exit 1 while a night is saved with a
different local bedtime than the user typed; exit 0 once it is rejected or saved as typed.
Run from the repo root: uv run python bugs/spring-forward-bedtime/repro.py
"""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(
        create_app(diary=diary, coach=MockCoach(), trace_path=Path(tmp) / "coach.jsonl")
    )
    response = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T09:00",
            "timezone": "America/Toronto",
        },
        follow_redirects=False,
    )
    nights = diary.nights()
    saved = nights[0].local_bedtime.strftime("%H:%M") if nights else None

if saved is None or saved == "02:30":
    print(f"OK: typed 02:30, HTTP {response.status_code}, saved {saved}")
    sys.exit(0)
print(f"BUG: typed 02:30, HTTP {response.status_code}, diary silently saved {saved}")
sys.exit(1)
