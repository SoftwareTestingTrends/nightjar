"""D-1 repro: importing the same CSV twice stores every night twice.

Exit 1 while the defect is present (two imports leave two copies of the night).
Exit 0 once the diary holds one copy after a repeat import, whatever the fix does
(skip the duplicate, replace it, or reject the import).

Run from the repository root:
    uv run python bugs/D-1-csv-reimport-duplicates/repro.py
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

CSV = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-01T23:00:00-05:00,2026-03-02T07:00:00-05:00,America/Toronto,\n"
).encode()
NOW = datetime(2026, 3, 20, 12, tzinfo=ZoneInfo("America/Toronto"))


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:  # throwaway database, never nightjar.db
        diary = Diary(Path(tmp) / "throwaway.db")
        app = create_app(
            diary=diary,
            coach=MockCoach(),
            clock=lambda: NOW,
            trace_path=Path(tmp) / "coach.jsonl",
        )
        client = TestClient(app)
        for _ in range(2):
            client.post("/import", files={"file": ("nights.csv", CSV, "text/csv")})
        stored = len(diary.nights())

    if stored == 1:
        print("OK: importing the same CSV twice left 1 night in the diary")
        return 0
    print(f"BUG: importing the same CSV twice left {stored} nights in the diary (expected 1)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
