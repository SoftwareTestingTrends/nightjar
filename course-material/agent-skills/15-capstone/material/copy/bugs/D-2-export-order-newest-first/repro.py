"""D-2: export lists nights newest first instead of oldest first (S-117 AC4)."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, parse_csv

SRC = (
    "bedtime,wake_time,timezone,notes\n"
    "2026-03-01T23:00:00-05:00,2026-03-02T07:00:00-05:00,America/Toronto,first\n"
    "2026-03-02T23:00:00-05:00,2026-03-03T07:00:00-05:00,America/Toronto,second\n"
    "2026-03-03T23:00:00-05:00,2026-03-04T07:00:00-05:00,America/Toronto,third\n"
)
with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    diary.add_nights(parse_csv(SRC))
    lines = diary.export_csv().splitlines()[1:]
notes = [line.rsplit(",", 1)[1] for line in lines]
print(f"export order: {notes}")
sys.exit(0 if notes == ["first", "second", "third"] else 1)
