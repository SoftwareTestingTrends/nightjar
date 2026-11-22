"""D-1: a bedtime inside the spring-forward gap is silently shifted by an hour.

02:30 on 2026-03-08 does not exist in America/Toronto (clocks jump 02:00 -> 03:00).
The form accepts it without a word and the diary shows 03:30.

Exit 1: the entry is saved and the page shows 03:30 with no mention of 02:30.
Exit 0: the entry is rejected (nothing saved), or the page tells the user about it.
Expected behaviour is not specified yet (question for product). Adjust the pass
condition here if product picks something else.
"""

import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

diary = Diary(Path(tempfile.mkdtemp()) / "repro.db")
app = create_app(diary, MockCoach(), lambda: datetime(2026, 3, 9, 12, tzinfo=UTC))
page = TestClient(app).post(
    "/nights",
    data={
        "bedtime": "2026-03-08T02:30",
        "wake_time": "2026-03-08T09:30",
        "timezone": "America/Toronto",
    },
    follow_redirects=True,
)
nights = diary.nights()

if not nights:
    print(f"OK: nonexistent 02:30 rejected (HTTP {page.status_code}), nothing saved")
    sys.exit(0)
shown = nights[0].local_bedtime.strftime("%H:%M")
if "02:30" in page.text:
    print(f"OK: saved as {shown} and the page mentions 02:30 to the user")
    sys.exit(0)
print(f"DEFECT: entered 02:30, diary silently shows {shown} (no warning, HTTP {page.status_code})")
sys.exit(1)
