"""D-1: importing the same CSV twice stores every night twice. Exit 1 while present."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-01T23:00:00-05:00,2026-03-02T07:00:00-05:00,America/Toronto,a\n"
    "2026-03-02T23:10:00-05:00,2026-03-03T07:05:00-05:00,America/Toronto,b\n"
)

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "throwaway.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    count = len(diary.nights())

if count == 2:
    print("OK: 2 nights after importing a 2-night file twice")
    sys.exit(0)
print(f"DEFECT: {count} nights after importing a 2-night file twice (expected 2)")
sys.exit(1)
