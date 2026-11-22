"""Repro: importing the same CSV twice stores every night twice."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-01T23:00:00-05:00,2026-03-02T07:00:00-05:00,America/Toronto,a\n"
    "2026-03-02T23:30:00-05:00,2026-03-03T07:30:00-05:00,America/Toronto,b\n"
)

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "throwaway.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    stored = len(diary.nights())

expected = 2
print(f"imported a 2-night CSV twice: {stored} nights stored (expected {expected})")
sys.exit(0 if stored == expected else 1)
