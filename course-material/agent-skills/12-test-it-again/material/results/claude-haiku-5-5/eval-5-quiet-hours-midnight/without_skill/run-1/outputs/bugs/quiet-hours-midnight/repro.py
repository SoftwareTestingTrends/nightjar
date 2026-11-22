"""Repro: quiet hours cannot end at midnight (00:00) in Settings.

Exits 1 while the defect is present (21:00-00:00 is rejected), 0 once it is fixed.
Uses a throwaway database in a temp directory.
"""

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

NOON = datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto"))


def main() -> int:
    tmp = Path(tempfile.mkdtemp())
    app = create_app(
        diary=Diary(tmp / "repro.db"),
        coach=MockCoach(),
        clock=lambda: NOON,
        trace_path=tmp / "coach.jsonl",
    )
    client = TestClient(app)
    response = client.post(
        "/settings",
        data={"timezone": "America/Toronto", "quiet_start": "21:00", "quiet_end": "00:00"},
        follow_redirects=False,
    )
    if response.status_code == 303:
        print("FIXED: quiet hours 21:00-00:00 saved (HTTP 303)")
        return 0
    message = re.search(r"Invalid[^<\n]*", response.text)
    detail = message.group(0) if message else f"HTTP {response.status_code}"
    print(f"BUG PRESENT: quiet hours 21:00-00:00 rejected ({detail})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
