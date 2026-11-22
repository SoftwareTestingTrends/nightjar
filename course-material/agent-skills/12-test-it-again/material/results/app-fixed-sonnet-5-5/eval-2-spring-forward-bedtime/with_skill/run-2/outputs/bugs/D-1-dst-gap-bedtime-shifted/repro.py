"""D-1: a bedtime inside the spring-forward gap is silently shifted an hour."""

import os
import sys
import tempfile

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

diary = Diary(os.path.join(tempfile.mkdtemp(), "repro.db"))
client = TestClient(create_app(diary=diary))
resp = client.post(
    "/nights",
    data={
        "bedtime": "2026-03-08T02:30",  # does not exist in America/Toronto
        "wake_time": "2026-03-08T09:30",
        "timezone": "America/Toronto",
    },
    follow_redirects=False,
)
nights = diary.nights()
if resp.status_code == 303 and nights:
    shown = nights[0].local_bedtime.strftime("%H:%M")
    print("entered 02:30, accepted without warning, diary shows " + shown)
    sys.exit(1 if shown != "02:30" else 0)
print("entered 02:30, not silently changed (HTTP " + str(resp.status_code) + ")")
sys.exit(0)
