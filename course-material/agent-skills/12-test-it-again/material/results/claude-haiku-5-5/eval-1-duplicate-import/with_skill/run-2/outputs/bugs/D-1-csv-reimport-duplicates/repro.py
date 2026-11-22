"""D-1 repro: importing the same CSV twice stores every night twice (NJ-12).

Uploads data/sample_nights.csv to /import twice into a throwaway database.
Exits 1 while the defect is present (the second upload adds nights), 0 once fixed.
Run from the repository root: uv run python bugs/D-1-csv-reimport-duplicates/repro.py
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

SAMPLE_CSV = Path(__file__).resolve().parents[2] / "data" / "sample_nights.csv"
NOON = datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto"))


def upload(client: TestClient) -> None:
    with SAMPLE_CSV.open("rb") as csv_file:
        client.post("/import", files={"file": ("nights.csv", csv_file, "text/csv")})


with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    app = create_app(
        diary=diary,
        coach=MockCoach(),
        clock=lambda: NOON,
        trace_path=Path(tmp) / "coach.jsonl",
    )
    client = TestClient(app)
    upload(client)
    after_first = len(diary.nights())
    upload(client)
    after_second = len(diary.nights())

if after_first == 0:
    print("setup: the first import stored no nights, so the check cannot run")
    sys.exit(1)
if after_second == after_first:
    print(f"fixed: re-importing the same file kept {after_second} nights")
    sys.exit(0)
print(
    f"defect: re-importing the same file stored {after_second - after_first} more nights "
    f"({after_second} total, expected {after_first})"
)
sys.exit(1)
