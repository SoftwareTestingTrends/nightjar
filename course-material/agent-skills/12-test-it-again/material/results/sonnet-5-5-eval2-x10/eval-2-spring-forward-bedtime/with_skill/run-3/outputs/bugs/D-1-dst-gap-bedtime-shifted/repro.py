"""D-1: a bedtime typed as 02:30 on 2026-03-08 in America/Toronto (a time that does not
exist: clocks jump 02:00 -> 03:00) is silently stored and shown as 03:30."""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, local_input_to_aware
from nightjar.models import Night

ZONE = "America/Toronto"
diary = Diary(Path(tempfile.mkdtemp()) / "repro.db")  # throwaway, never nightjar.db
try:
    night = Night(
        bedtime=local_input_to_aware("2026-03-08T02:30", ZONE),
        wake_time=local_input_to_aware("2026-03-08T09:30", ZONE),
        timezone=ZONE,
        notes="",
    )
    diary.add_night(night)
except ValueError as error:
    print(f"FIXED: nonexistent local time rejected ({error})")
    sys.exit(0)

shown = diary.nights()[0].local_bedtime.strftime("%H:%M")
print(f"typed 02:30, diary shows {shown}, accepted without warning")
sys.exit(1 if shown != "02:30" else 0)
