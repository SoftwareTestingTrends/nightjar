"""D-1: a bedtime typed as 02:30 on 2026-03-08 (Toronto; clocks jump 02:00 -> 03:00,
so 02:30 never happens) is silently saved and shown as 03:30.

Exits 1 while the diary silently stores a different time than the one typed,
0 once it is rejected with an error (or shown as typed)."""

import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    app = create_app(
        diary=diary,
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto")),
        trace_path=Path(tmp) / "coach.jsonl",
    )
    response = TestClient(app).post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T09:00",
            "timezone": "America/Toronto",
        },
    )
    nights = diary.nights()
    if not nights:
        print("OK: bedtime 02:30 rejected (HTTP %s), nothing saved" % response.status_code)
        sys.exit(0)
    shown = nights[0].local_bedtime.strftime("%H:%M")
    if shown == "02:30":
        print("OK: saved and shown as typed, 02:30")
        sys.exit(0)
    print("BUG: typed 02:30 (does not exist in Toronto on 2026-03-08), saved and shown as " + shown)
    sys.exit(1)
