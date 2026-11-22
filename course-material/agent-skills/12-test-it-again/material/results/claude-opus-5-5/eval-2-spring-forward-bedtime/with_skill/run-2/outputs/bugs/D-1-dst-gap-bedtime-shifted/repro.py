"""D-1: a bedtime inside the spring-forward gap is silently saved an hour later.

02:30 on 2026-03-08 does not exist in America/Toronto (clocks jump 02:00 -> 03:00).
The form accepts it without a word and the diary shows 03:30.

Exit 1 while the defect is present: the night is saved, the diary shows 03:30,
and the page shows no error or notice. Exit 0 once the app either rejects the time
or tells the user it was changed.

Run from the repository root: uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py
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

tmp = Path(tempfile.mkdtemp())
diary = Diary(tmp / "repro.db")  # throwaway, never nightjar.db
app = create_app(
    diary,
    MockCoach(),
    clock=lambda: datetime(2026, 3, 9, 12, tzinfo=UTC),
    trace_path=tmp / "trace.jsonl",
)
client = TestClient(app)

response = client.post(
    "/nights",
    data={
        "bedtime": "2026-03-08T02:30",
        "wake_time": "2026-03-08T09:00",
        "timezone": "America/Toronto",
    },
)
page = response.text
rows = re.findall(r'data-testid="diary-row">\s*<td>[^<]*</td>\s*<td>([^<]*)</td>', page)
told_user = 'role="alert"' in page

if rows == ["03:30"] and not told_user:
    print("DEFECT: entered 02:30 (DST gap), diary silently shows 03:30")
    sys.exit(1)
print(f"OK: diary bed times {rows}, user shown a message: {told_user}")
sys.exit(0)
