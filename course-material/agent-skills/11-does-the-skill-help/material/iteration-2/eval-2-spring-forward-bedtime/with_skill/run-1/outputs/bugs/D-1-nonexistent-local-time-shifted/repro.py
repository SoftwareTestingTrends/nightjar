"""D-1: a bedtime typed as 02:30 on 2026-03-08 (Toronto) is shown as 03:30.

02:30 does not exist that night (clocks jump 02:00 -> 03:00). The diary accepts it
without a word and shows a different time. Exits 1 while the diary accepts the
input and shows something other than what was typed; 0 once the input is rejected
(HTTP 400) or shown as typed.
"""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "throwaway.db")
    client = TestClient(create_app(diary=diary, coach=object()))
    response = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T09:30",
            "timezone": "America/Toronto",
        },
        follow_redirects=False,
    )
    nights = diary.nights()
    shown = nights[0].local_bedtime.strftime("%H:%M") if nights else None

print(f"typed 02:30, HTTP {response.status_code}, diary shows {shown}")
sys.exit(1 if response.status_code == 303 and shown != "02:30" else 0)
