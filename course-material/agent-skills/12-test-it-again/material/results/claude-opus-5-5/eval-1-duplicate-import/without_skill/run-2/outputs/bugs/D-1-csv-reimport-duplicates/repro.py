"""D-1: importing the same CSV twice stores every night twice.

Run from the repo root: uv run python bugs/D-1-csv-reimport-duplicates/repro.py
Exits 1 while the bug is present, 0 once re-importing leaves one row per night.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = """bedtime,wake_time,timezone,notes
2026-03-01T23:10:00-05:00,2026-03-02T07:05:00-05:00,America/Toronto,first
2026-03-02T23:20:00-05:00,2026-03-03T07:15:00-05:00,America/Toronto,second
"""

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "diary.db")
    # Same calls the POST /import endpoint makes, done twice.
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    stored = len(diary.nights())

expected = 2
if stored != expected:
    print(f"BUG: imported the same 2-night CSV twice, diary holds {stored} nights")
    sys.exit(1)
print(f"OK: imported the same 2-night CSV twice, diary holds {stored} nights")
sys.exit(0)
