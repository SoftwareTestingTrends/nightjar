"""D-1: importing the same CSV twice stores every night twice.

Run from the repository root:
    uv run python bugs/D-1-reimport-duplicates-nights/repro.py

Exit 1 while the defect is present (second import adds the nights again),
exit 0 once it's fixed (the diary holds each night once after two imports).
"""

import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

CSV = (
    b"bedtime,wake_time,timezone,notes\n"
    b"2026-03-01T23:00:00-05:00,2026-03-02T07:00:00-05:00,America/Toronto,\n"
    b"2026-03-02T23:15:00-05:00,2026-03-03T07:05:00-05:00,America/Toronto,\n"
)
NOW = datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto"))

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(
        create_app(
            diary=diary,
            coach=MockCoach(),
            clock=lambda: NOW,
            trace_path=Path(tmp) / "coach.jsonl",
        )
    )
    for _ in range(2):
        response = client.post("/import", files={"file": ("nights.csv", CSV, "text/csv")})
        assert response.status_code == 200, response.text

    stored = len(diary.nights())

if stored == 2:
    print("OK: imported a 2-night CSV twice, diary holds 2 nights")
    sys.exit(0)
print(f"BUG: imported a 2-night CSV twice, diary holds {stored} nights (expected 2)")
sys.exit(1)
