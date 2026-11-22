"""Repro: saving quiet hours 21:00 -> 00:00 in Settings is rejected as invalid.

Exits 1 while the bug is present, 0 once it is fixed.
Run from the repo root: uv run python bugs/quiet-midnight/repro.py
"""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    client = TestClient(
        create_app(diary=diary, coach=MockCoach(), trace_path=Path(tmp) / "coach.jsonl")
    )
    response = client.post(
        "/settings",
        data=dict(timezone="America/Toronto", quiet_start="21:00", quiet_end="00:00"),
        follow_redirects=False,
    )
    saved = diary.user()
    ok = response.status_code == 303 and saved.quiet_end is not None
    print(f"status={response.status_code} saved={saved.quiet_start}->{saved.quiet_end}")
    sys.exit(0 if ok else 1)
