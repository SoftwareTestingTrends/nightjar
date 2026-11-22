"""D-1: export writes UTC (+00:00) instead of the night's own offset (S-117 AC3)."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

SRC = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-01T00:25:00-05:00,2026-03-01T07:30:00-05:00,America/Toronto,\n"
)
with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(SRC))
    row = diary.export_csv().splitlines()[1]
print(f"exported row: {row}")
ok = row.startswith("2026-03-01T00:25:00-05:00,2026-03-01T07:30:00-05:00,")
sys.exit(0 if ok else 1)
