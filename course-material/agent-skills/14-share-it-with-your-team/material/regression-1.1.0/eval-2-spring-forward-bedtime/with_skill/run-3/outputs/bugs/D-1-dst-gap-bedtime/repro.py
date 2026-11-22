"""D-1: a bedtime typed as 02:30 on 2026-03-08 (America/Toronto) shows as 03:30.

02:30 doesn't exist that night (clocks jump 02:00 -> 03:00). Exits 1 while the diary
silently shows a different time than was entered; 0 if it is rejected or shown as entered.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, local_input_to_aware
from nightjar.models import Night

ZONE = "America/Toronto"

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")
    try:
        diary.add_night(
            Night(
                bedtime=local_input_to_aware("2026-03-08T02:30", ZONE),
                wake_time=local_input_to_aware("2026-03-08T09:30", ZONE),
                timezone=ZONE,
            )
        )
    except ValueError as error:
        print(f"OK: rejected with a message: {error}")
        sys.exit(0)
    shown = diary.nights()[0].local_bedtime.strftime("%H:%M")

if shown == "02:30":
    print("OK: diary shows 02:30 as entered")
    sys.exit(0)
print(f"BUG: entered 02:30, diary shows {shown}, with no warning")
sys.exit(1)
