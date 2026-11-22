"""Log a bedtime of 02:30 on 2026-03-08 (Toronto spring-forward gap) and read it back."""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(create_app(diary=diary))
    response = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T10:00",
            "timezone": "America/Toronto",
        },
        follow_redirects=False,
    )
    nights = diary.nights()
    shown = nights[0].local_bedtime.strftime("%H:%M") if nights else None

if response.status_code == 400:
    print("rejected 02:30 with an error (gap time handled)")
    sys.exit(0)
if shown == "02:30":
    print("diary shows 02:30 as entered")
    sys.exit(0)
print(f"logged 02:30 on 2026-03-08 in America/Toronto, diary shows {shown}")
sys.exit(1)
