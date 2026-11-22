"""Repro: quiet hours 21:00 -> 00:00 are rejected as an invalid time.

Exits 1 while the bug is present, 0 once it is fixed.
Run: uv run python bugs/quiet-hours-midnight/repro.py
"""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

tmp = Path(tempfile.mkdtemp())
app = create_app(diary=Diary(tmp / "repro.db"), coach=MockCoach(), trace_path=tmp / "coach.jsonl")
client = TestClient(app, follow_redirects=False)

response = client.post(
    "/settings",
    data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
)
print(f"POST /settings 21:00-00:00 -> {response.status_code}")
if response.status_code != 303:
    print("BUG: quiet hours 21:00-00:00 were rejected")
    sys.exit(1)
print("OK: saved")
sys.exit(0)
