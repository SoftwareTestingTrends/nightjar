"""D-1: a bedtime typed inside the spring-forward gap is silently shown as another time.

Exits 1 while the diary silently shows a different time than was entered; 0 if the
input is rejected with an error or shown as entered.
"""

import sys
import tempfile
from datetime import datetime
from pathlib import Path

from nightjar.diary import Diary, local_input_to_aware
from nightjar.models import Night

TZ = "America/Toronto"
try:
    bed = local_input_to_aware("2026-03-08T02:30", TZ)  # 02:30 does not exist this night
    wake = local_input_to_aware("2026-03-08T09:00", TZ)
    with tempfile.TemporaryDirectory() as tmp:  # throwaway database, never nightjar.db
        diary = Diary(Path(tmp) / "repro.db")
        diary.add_night(Night(bedtime=bed, wake_time=wake, timezone=TZ))
        shown = diary.nights()[0].local_bedtime  # what the page renders
except ValueError as error:
    print(f"OK: input rejected with an error: {error}")
    sys.exit(0)

entered = datetime(2026, 3, 8, 2, 30)
if shown.replace(tzinfo=None) == entered:
    print(f"OK: diary shows {shown:%H:%M} as entered")
    sys.exit(0)
print(f"BUG: entered 02:30 on 2026-03-08 ({TZ}), diary shows {shown:%H:%M}, no warning")
sys.exit(1)
