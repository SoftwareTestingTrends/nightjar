"""D-1: a bedtime typed as 02:30 on 2026-03-08 (America/Toronto) is shown as 03:30.

02:30 doesn't exist that night (clocks jump 02:00 -> 03:00). The diary accepts it
silently and shows 03:30. Exits 1 while it does that, 0 once such input is rejected
(ValueError) or otherwise no longer silently changed.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, local_input_to_aware
from nightjar.models import Night

ZONE = "America/Toronto"
TYPED = "02:30"

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")  # throwaway database
    try:
        bedtime = local_input_to_aware("2026-03-08T02:30", ZONE)
        wake = local_input_to_aware("2026-03-08T09:30", ZONE)
        diary.add_night(Night(bedtime=bedtime, wake_time=wake, timezone=ZONE))
    except ValueError as error:
        print(f"OK: input rejected: {error}")
        sys.exit(0)
    shown = diary.nights()[0].local_bedtime.strftime("%H:%M")

if shown == TYPED:
    print(f"OK: diary shows {shown}")
    sys.exit(0)
print(f"BUG: typed {TYPED} on 2026-03-08 ({ZONE}), diary shows {shown} with no warning")
sys.exit(1)
