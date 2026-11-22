"""D-1: a bedtime inside the spring-forward gap is silently saved as a different time.

02:30 on 2026-03-08 does not exist in America/Toronto (clocks jump 02:00 -> 03:00).
The "Log a night" form accepts it without a word and the diary shows 03:30.

Exit 1 while the defect is present (night saved silently, diary shows a bedtime other
than the one entered); exit 0 once it's fixed (the form refuses the time, or the diary
shows what was entered). If product chooses a different behaviour, update this check.
"""

import re
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach.mock import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

ENTERED = "02:30"

tmp = Path(tempfile.mkdtemp())
diary = Diary(tmp / "repro.db")  # throwaway database, never nightjar.db
client = TestClient(
    create_app(
        diary,
        MockCoach(),
        clock=lambda: datetime(2026, 3, 9, 12, 0, tzinfo=UTC),
        trace_path=tmp / "trace.jsonl",
    )
)

response = client.post(
    "/nights",
    data={
        "bedtime": f"2026-03-08T{ENTERED}",
        "wake_time": "2026-03-08T09:00",
        "timezone": "America/Toronto",
    },
    follow_redirects=False,
)

if response.status_code != 303 or not diary.nights():
    print(f"OK: form refused the non-existent time (HTTP {response.status_code})")
    sys.exit(0)

row = re.search(r'data-testid="diary-row">\s*<td>[^<]*</td>\s*<td>([^<]*)</td>', client.get("/").text)
shown = row.group(1).strip() if row else "?"
if shown == ENTERED:
    print(f"OK: diary shows the bedtime as entered ({shown})")
    sys.exit(0)

print(f"BUG: entered {ENTERED}, form saved it silently (HTTP 303), diary shows {shown}")
sys.exit(1)
