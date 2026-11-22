"""D-1: a bedtime inside the spring-forward gap (02:30, 8 Mar 2026, Toronto) is
silently stored and shown as 03:30. Exits 1 while that happens, 0 once the user is
told (form rejected, or the page shows a DST notice)."""

import re
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

with tempfile.TemporaryDirectory() as tmp:
    app = create_app(Diary(Path(tmp) / "repro.db"), MockCoach(), trace_path=Path(tmp) / "t.jsonl")
    client = TestClient(app)
    response = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T10:00",
            "timezone": "America/Toronto",
        },
        follow_redirects=True,
    )
    page = response.text
    row = re.search(r"<td>Sat 07 Mar</td>\s*<td>(\d\d:\d\d)</td>", page)
    shown = row.group(1) if row else None
    notice = re.search(r"daylight|does not exist|doesn't exist|skipped", page, re.I)
    if not response.history or notice:
        print(f"OK: user was told (status {response.status_code}); row shows {shown}")
        sys.exit(0)
    print(f"BUG: typed 02:30 (nonexistent; clocks jump 02:00->03:00), diary shows {shown}, no notice")
    sys.exit(1)
