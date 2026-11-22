"""D-1: importing the same CSV twice stores every night twice."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-18T23:00:00-04:00,2026-03-19T07:00:00-04:00,America/Toronto,\n"
)

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    count = len(diary.nights())

print(f"1-night CSV imported twice -> {count} nights stored (expected 1)")
sys.exit(1 if count != 1 else 0)
