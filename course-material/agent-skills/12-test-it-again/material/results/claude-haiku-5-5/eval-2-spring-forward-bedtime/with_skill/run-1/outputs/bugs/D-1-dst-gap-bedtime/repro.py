"""D-1: a bedtime typed inside the spring-forward gap is silently moved an hour later.

Clocks in America/Toronto jump 02:00 -> 03:00 on 8 March 2026, so 02:30 never happens
that night. Logging 02:30 is stored as 07:30 UTC and shown as 03:30.

Exit 1: defect present (02:30 entered, 03:30 shown).
Exit 0: fixed. Either the entry is rejected with an error, or 02:30 is shown.

Runs against a throwaway database. From the repository root:
    uv run python bugs/D-1-dst-gap-bedtime/repro.py
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

TORONTO = ZoneInfo("America/Toronto")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        app = create_app(
            diary=Diary(folder / "repro.db"),
            coach=MockCoach(),
            clock=lambda: datetime(2026, 3, 20, 12, tzinfo=TORONTO),
            trace_path=folder / "coach.jsonl",
        )
        response = TestClient(app).post(
            "/nights",
            data={
                "bedtime": "2026-03-08T02:30",
                "wake_time": "2026-03-08T08:00",
                "timezone": "America/Toronto",
                "notes": "",
            },
            follow_redirects=False,
        )
        if response.status_code != 303:
            print(f"fixed: entry rejected with HTTP {response.status_code}, nothing stored")
            return 0
        [night] = Diary(folder / "repro.db").nights()

    shown = night.local_bedtime.strftime("%H:%M")
    if shown == "03:30":
        print("defect present: entered 02:30 on 2026-03-08 (Toronto), shown as 03:30")
        return 1
    print(f"fixed: entered 02:30 on 2026-03-08 (Toronto), shown as {shown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
