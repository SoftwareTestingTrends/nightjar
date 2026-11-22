"""D-1: importing the same CSV twice stores every night twice."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-01T23:00:00-05:00,2026-03-02T07:00:00-05:00,America/Toronto,\n"
    "2026-03-02T23:10:00-05:00,2026-03-03T07:05:00-05:00,America/Toronto,\n"
)

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    stored = len(diary.nights())

print(f"2 distinct nights imported twice -> {stored} stored (expected 2)")
sys.exit(0 if stored == 2 else 1)
