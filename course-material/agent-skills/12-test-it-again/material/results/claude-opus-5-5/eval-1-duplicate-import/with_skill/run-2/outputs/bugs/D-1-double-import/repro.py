"""D-1: importing the same CSV twice stores every night twice.

Exits 1 while the defect is present, 0 once it's fixed.
Run from the repo root: uv run python bugs/D-1-double-import/repro.py
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
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-18T23:10:00-04:00,2026-03-19T07:00:00-04:00,America/Toronto,\n"
    "2026-03-19T23:20:00-04:00,2026-03-20T07:05:00-04:00,America/Toronto,\n"
)
NOON = datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto"))

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(
        create_app(diary, MockCoach(), lambda: NOON, Path(tmp) / "coach.jsonl")
    )
    for _ in range(2):
        response = client.post(
            "/import",
            files={"file": ("nights.csv", CSV.encode(), "text/csv")},
            follow_redirects=False,
        )
        assert response.status_code == 303, response.status_code
    stored = len(diary.nights())

if stored != 2:
    print(f"BUG: imported a 2-night CSV twice, diary now holds {stored} nights (want 2)")
    sys.exit(1)
print("OK: importing the same 2-night CSV twice leaves 2 nights")
sys.exit(0)
