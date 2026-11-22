"""D-1: a bedtime typed as 02:30 on 2026-03-08 (America/Toronto, a nonexistent time) is saved as 03:30."""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(create_app(diary=diary), follow_redirects=False)
    response = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T09:30",
            "timezone": "America/Toronto",
        },
    )
    nights = diary.nights()
    if response.status_code >= 400 or not nights:
        print(f"OK: entry rejected (HTTP {response.status_code}), nothing silently changed")
        sys.exit(0)
    shown = nights[0].local_bedtime.strftime("%H:%M")
    if shown != "02:30":
        print(f"BUG: logged 02:30, diary shows {shown} (HTTP {response.status_code}, no warning)")
        sys.exit(1)
    print("OK: diary shows 02:30 as entered")
