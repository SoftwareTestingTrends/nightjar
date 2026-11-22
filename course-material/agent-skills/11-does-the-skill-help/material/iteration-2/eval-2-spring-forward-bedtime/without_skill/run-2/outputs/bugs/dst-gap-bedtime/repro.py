"""02:30 on 2026-03-08 doesn't exist in America/Toronto (clocks jump 02:00 -> 03:00).
NightJar accepts it silently and the diary shows 03:30, an hour off from what was typed.
Exit 1 while a nonexistent local time is silently shifted; 0 once it's rejected (400)
or handled some other way than showing 03:30."""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(create_app(diary=diary, coach=object()))
    resp = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T10:00",
            "timezone": "America/Toronto",
        },
        follow_redirects=False,
    )
    nights = diary.nights()
    if resp.status_code >= 400 or not nights:
        print(f"OK: nonexistent time rejected (HTTP {resp.status_code})")
        sys.exit(0)
    shown = nights[0].local_bedtime.strftime("%H:%M")
    if shown == "03:30":
        print("BUG: typed 02:30 (nonexistent, DST gap), diary shows 03:30, no warning")
        sys.exit(1)
    print(f"OK: diary shows {shown}")
    sys.exit(0)
