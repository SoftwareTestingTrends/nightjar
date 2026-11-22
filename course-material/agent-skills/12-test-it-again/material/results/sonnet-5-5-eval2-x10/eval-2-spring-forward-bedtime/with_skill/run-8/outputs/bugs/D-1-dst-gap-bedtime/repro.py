"""D-1: a bedtime in the spring-forward gap (02:30, 8 Mar 2026, Toronto) is silently moved to 03:30."""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(create_app(diary=diary, trace_path=Path(tmp) / "trace.jsonl"))
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
    if response.status_code == 400 and not nights:
        print("OK: nonexistent 02:30 was rejected with a 400")
        sys.exit(0)
    shown = nights[0].local_bedtime.strftime("%H:%M") if nights else "none"
    if shown == "02:30":
        print("OK: stored 02:30")
        sys.exit(0)
    print(f"BUG: entered 02:30 (does not exist), status {response.status_code}, diary shows {shown}")
    sys.exit(1)
