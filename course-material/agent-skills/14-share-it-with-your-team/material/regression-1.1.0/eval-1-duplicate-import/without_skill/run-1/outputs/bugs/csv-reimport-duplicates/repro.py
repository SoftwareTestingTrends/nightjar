"""Importing the same CSV twice must not store every night twice.

Exits 1 while the bug is present, 0 once fixed.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-18T23:00:00-04:00,2026-03-19T07:00:00-04:00,America/Toronto,first\n"
    "2026-03-19T23:30:00-04:00,2026-03-20T07:15:00-04:00,America/Toronto,second\n"
)

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    stored = len(diary.nights())

if stored == 2:
    print("OK: 2 nights stored after importing a 2-night CSV twice")
    sys.exit(0)
print(f"BUG: 2-night CSV imported twice stored {stored} nights (expected 2)")
sys.exit(1)
