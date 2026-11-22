"""Importing the same CSV twice must not store every night twice. Exit 1 = bug present."""

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

print(f"2 nights imported twice -> {count} stored (expected 2)")
sys.exit(0 if count == 2 else 1)
