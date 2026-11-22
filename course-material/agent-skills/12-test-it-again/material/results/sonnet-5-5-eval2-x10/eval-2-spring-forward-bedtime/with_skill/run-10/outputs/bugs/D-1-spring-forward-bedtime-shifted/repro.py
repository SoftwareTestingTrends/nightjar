"""D-1: logging 02:30 on 2026-03-08 (a time that doesn't exist in Toronto) is silently stored as 03:30."""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(create_app(diary=diary, coach=MockCoach(), trace_path=Path(tmp) / "t.jsonl"))
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
    shown = nights[0].local_bedtime.strftime("%H:%M") if nights else None

# Fixed = the app either rejects the nonexistent time or shows what was typed.
if response.status_code == 400 or shown == "02:30":
    print(f"OK: status {response.status_code}, diary shows {shown}")
    sys.exit(0)
print(f"BUG: entered 02:30, status {response.status_code}, diary shows {shown}")
sys.exit(1)
