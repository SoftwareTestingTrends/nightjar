"""D-1: importing the same CSV twice duplicates every night. Exit 1 while present."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-18T23:00:00-04:00,2026-03-19T07:00:00-04:00,America/Toronto,a\n"
    "2026-03-19T23:30:00-04:00,2026-03-20T07:00:00-04:00,America/Toronto,b\n"
)

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "throwaway.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    count = len(diary.nights())

print(f"2 distinct nights imported twice -> {count} rows in diary (expected 2)")
sys.exit(1 if count != 2 else 0)
