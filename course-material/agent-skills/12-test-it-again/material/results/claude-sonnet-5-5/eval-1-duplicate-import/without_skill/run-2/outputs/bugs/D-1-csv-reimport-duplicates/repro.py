"""Importing the same CSV twice should not store every night twice."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = """bedtime,wake_time,timezone,notes
2026-03-01T23:00:00-05:00,2026-03-02T07:00:00-05:00,America/Toronto,a
2026-03-02T23:30:00-05:00,2026-03-03T07:15:00-05:00,America/Toronto,b
"""

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    stored = len(diary.nights())

if stored == 2:
    print("OK: 2 nights stored after importing a 2-night CSV twice")
    sys.exit(0)
print(f"BUG: {stored} nights stored after importing a 2-night CSV twice (expected 2)")
sys.exit(1)
