"""02:30 on 2026-03-08 in America/Toronto does not exist (clocks jump 02:00 -> 03:00).
Logging it must be rejected (or at least shown back as 02:30), not silently saved
and then displayed as 03:30.
Run from the repo root: uv run python bugs/dst-gap-bedtime/repro.py
Exits 1 while the bug is present, 0 once it is fixed."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, local_input_to_aware
from nightjar.models import Night

TZ = "America/Toronto"

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    try:
        bed = local_input_to_aware("2026-03-08T02:30", TZ)
        wake = local_input_to_aware("2026-03-08T09:30", TZ)
        diary.add_night(Night(bedtime=bed, wake_time=wake, timezone=TZ))
    except ValueError as error:
        print(f"fixed: nonexistent local time rejected ({error})")
        sys.exit(0)
    shown = diary.nights()[0].local_bedtime.strftime("%H:%M")

if shown == "02:30":
    print("fixed: diary shows 02:30")
    sys.exit(0)
print(f"bug: logged 02:30 (a time that doesn't exist), diary shows {shown}")
sys.exit(1)
