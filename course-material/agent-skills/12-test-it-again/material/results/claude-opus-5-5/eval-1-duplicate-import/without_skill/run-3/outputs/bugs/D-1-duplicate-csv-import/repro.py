"""D-1: importing the same CSV twice stores every night twice.

Run from the repo root: uv run python bugs/D-1-duplicate-csv-import/repro.py
Exit 1 while the defect is present, 0 once it's fixed.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

CSV = """bedtime,wake_time,timezone,notes
2026-03-01T22:55:00-05:00,2026-03-02T06:50:00-05:00,America/Toronto,
2026-03-02T22:50:00-05:00,2026-03-03T06:45:00-05:00,America/Toronto,
"""

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(CSV))
    diary.add_nights(parse_csv(CSV))
    stored = len(diary.nights())

if stored != 2:
    print(f"BUG: imported the same 2-night CSV twice, diary holds {stored} nights (expected 2)")
    sys.exit(1)
print("OK: importing the same 2-night CSV twice leaves 2 nights")
sys.exit(0)
