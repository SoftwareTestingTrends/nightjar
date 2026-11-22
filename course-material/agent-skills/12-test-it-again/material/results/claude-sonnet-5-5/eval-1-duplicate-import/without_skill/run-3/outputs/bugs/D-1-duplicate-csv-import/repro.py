"""Importing the same CSV twice should not store every night twice."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-18T23:00:00-04:00,2026-03-19T07:00:00-04:00,America/Toronto,\n"
    "2026-03-19T23:30:00-04:00,2026-03-20T07:15:00-04:00,America/Toronto,late\n"
)

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    stored = len(diary.nights())

expected = 2
print(f"imported a {expected}-night CSV twice; diary holds {stored} nights (expected {expected})")
sys.exit(0 if stored == expected else 1)
