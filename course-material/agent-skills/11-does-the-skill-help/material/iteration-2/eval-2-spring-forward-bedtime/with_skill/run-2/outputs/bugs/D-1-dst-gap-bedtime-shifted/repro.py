"""D-1: a bedtime of 02:30 on 2026-03-08 (America/Toronto) is shown as 03:30."""

import re
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
    app = create_app(
        diary=Diary(Path(tmp) / "repro.db"),
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto")),
        trace_path=Path(tmp) / "coach.jsonl",
    )
    client = TestClient(app)
    response = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-08T02:30",
            "wake_time": "2026-03-08T08:00",
            "timezone": "America/Toronto",
            "notes": "",
        },
        follow_redirects=False,
    )
    if response.status_code == 400:
        print("OK: the nonexistent 02:30 was rejected with a message")
        sys.exit(0)
    page = client.get("/").text
    row = re.search(r'data-testid="diary-row">\s*<td>[^<]*</td>\s*<td>(\d\d:\d\d)</td>', page)
    shown = row.group(1) if row else None
    if shown == "02:30":
        print("OK: diary shows the bedtime as entered, 02:30")
        sys.exit(0)
    print(f"BUG: entered 02:30 on 2026-03-08 in America/Toronto, diary shows {shown}")
    sys.exit(1)
