"""D-1: a bedtime typed as 02:30 on 2026-03-08 (America/Toronto, a time that does not
exist: clocks jump 02:00 -> 03:00) is silently saved and shown as 03:30.

Exit 1 while the diary silently changes the entry; exit 0 once it either rejects it
(HTTP 400) or shows the time the user typed. Run from the repo root."""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    app = create_app(diary=diary, coach=MockCoach(), trace_path=Path(tmp) / "trace.jsonl")
    client = TestClient(app)
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

if response.status_code >= 400 and not nights:
    print(f"OK: entry rejected with HTTP {response.status_code}")
    sys.exit(0)
if shown == "02:30":
    print("OK: diary shows 02:30 as typed")
    sys.exit(0)
print(f"BUG: typed 02:30, HTTP {response.status_code}, diary shows {shown} with no warning")
sys.exit(1)
