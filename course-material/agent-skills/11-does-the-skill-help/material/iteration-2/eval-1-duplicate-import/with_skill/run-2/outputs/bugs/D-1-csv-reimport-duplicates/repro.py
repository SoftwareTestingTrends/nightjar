"""Import the same CSV twice into a throwaway DB; exit 1 if nights are stored twice."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-18T23:00:00-04:00,2026-03-19T07:00:00-04:00,America/Toronto,\n"
    "2026-03-19T23:30:00-04:00,2026-03-20T07:15:00-04:00,America/Toronto,\n"
)

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    count = len(diary.nights())

if count != 2:
    print(f"BUG: importing a 2-night CSV twice stored {count} nights (expected 2)")
    sys.exit(1)
print("OK: re-import stored 2 nights")
