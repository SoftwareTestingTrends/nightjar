"""Importing the same CSV twice stores every night twice.

Exit 1 while the bug is present, 0 once fixed.
Run from the repo root: uv run python bugs/csv-reimport-duplicates/repro.py
"""

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
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    count = len(diary.nights())

if count == 2:
    print("OK: 2 nights after importing a 2-night CSV twice")
    sys.exit(0)
print(f"BUG: expected 2 nights after importing a 2-night CSV twice, found {count}")
sys.exit(1)
