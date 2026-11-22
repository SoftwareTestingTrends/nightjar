"""D-1: a bedtime typed as 02:30 on 2026-03-08 (America/Toronto, a time that doesn't
exist: clocks jump 02:00 -> 03:00) is silently saved and shown as 03:30."""

import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
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

if response.status_code >= 400 or not nights:
    print(f"OK: nonexistent time rejected (HTTP {response.status_code})")
    sys.exit(0)
shown = f"{nights[0].local_bedtime:%H:%M}"
if shown != "02:30":
    print(f"BUG: entered 02:30 (nonexistent in Toronto), saved without error as {shown}")
    sys.exit(1)
print("OK: bedtime kept as entered")
