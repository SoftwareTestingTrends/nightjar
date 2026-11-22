"""Bedtime 02:30 on 2026-03-08 (America/Toronto, a time DST skips) is silently stored as 03:30.

Exit 1 while the bug is present, 0 once fixed (input rejected with a clear error,
or the entry is kept as typed). Run from the repo root.
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
        diary.add_night(night)
    except ValueError as error:
        print(f"OK: nonexistent time rejected: {error}")
        sys.exit(0)
    shown = diary.nights()[0].local_bedtime.strftime("%H:%M")

if shown == "02:30":
    print("OK: bedtime kept as typed (02:30)")
    sys.exit(0)
print(f"BUG: logged 02:30 on 2026-03-08 (skipped by DST), diary shows {shown} with no warning")
sys.exit(1)
