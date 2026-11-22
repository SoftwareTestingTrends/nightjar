"""Bedtime 02:30 on 2026-03-08 in America/Toronto (a time that doesn't exist: clocks
jump 02:00 -> 03:00) is silently saved and shown as 03:30.

Exit 1 while the diary shows a different time than was logged without rejecting it;
exit 0 once it is either rejected with a ValueError or shown as logged.
Run from the repo root: uv run python bugs/dst-gap-bedtime/repro.py
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, local_input_to_aware
from nightjar.models import Night

TZ = "America/Toronto"

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    try:
        night = Night(
            bedtime=local_input_to_aware("2026-03-08T02:30", TZ),
            wake_time=local_input_to_aware("2026-03-08T09:30", TZ),
            timezone=TZ,
        )
    except ValueError as error:
        print(f"OK: nonexistent time rejected ({error})")
        sys.exit(0)
    diary.add_night(night)
    shown = diary.nights()[0].local_bedtime.strftime("%H:%M")

if shown == "02:30":
    print("OK: diary shows 02:30 as logged")
    sys.exit(0)
print(f"BUG: logged 02:30 on 2026-03-08 ({TZ}), diary shows {shown}, no error")
sys.exit(1)
