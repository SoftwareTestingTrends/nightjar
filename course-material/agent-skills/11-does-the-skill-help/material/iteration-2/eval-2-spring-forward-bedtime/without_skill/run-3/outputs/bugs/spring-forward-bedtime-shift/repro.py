"""Repro: a bedtime logged in the skipped spring-forward hour is silently shifted.

Toronto clocks jump 02:00 -> 03:00 on 2026-03-08, so 02:30 does not exist.
POST /nights stores it anyway and the diary then shows 03:30, with no error.
Exit 1 while the bug is present; 0 once the app rejects the time (400) or
otherwise no longer silently saves a different time than the one entered.
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from fastapi.testclient import TestClient  # noqa: E402

from nightjar.diary import Diary  # noqa: E402
from nightjar.web import create_app  # noqa: E402

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(str(Path(tmp) / "repro.db"))
    client = TestClient(create_app(diary=diary, trace_path=Path(tmp) / "trace.jsonl"))
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
    print("status =", response.status_code, "| saved bedtime shown =", shown)
    if nights and shown != "02:30":
        print("BUG: entered 02:30 (does not exist in Toronto on 2026-03-08), saved as", shown)
        sys.exit(1)
print("OK")
