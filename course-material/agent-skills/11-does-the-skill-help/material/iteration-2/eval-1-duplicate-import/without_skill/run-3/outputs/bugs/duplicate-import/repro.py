"""Importing the same CSV twice stores every night twice.

Run from the repo root: uv run python bugs/duplicate-import/repro.py
Exits 1 while the bug is present, 0 once it's fixed.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = """bedtime,wake_time,timezone,notes
2026-03-18T23:00:00-04:00,2026-03-19T07:00:00-04:00,America/Toronto,
2026-03-19T23:30:00-04:00,2026-03-20T07:15:00-04:00,America/Toronto,late one
"""

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    count = len(diary.nights())

if count == 2:
    print("OK: 2 distinct nights after importing the same 2-night CSV twice")
    sys.exit(0)
print(f"BUG: {count} nights stored after importing the same 2-night CSV twice (expected 2)")
sys.exit(1)
