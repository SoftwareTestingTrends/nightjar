"""Repro: a bedtime typed as 02:30 on 2026-03-08 (America/Toronto) is shown as 03:30.

That wall-clock time doesn't exist (clocks jump 02:00 -> 03:00). The app should
reject it with a message (the web form already shows ValueError text as a 400),
not silently store and show a different time. Exits 1 while the bug is present,
0 once fixed.

Run from the repo root: uv run python bugs/dst-gap-bedtime/repro.py
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, local_input_to_aware
from nightjar.models import Night

ZONE = "America/Toronto"
TYPED = "2026-03-08T02:30"

with tempfile.TemporaryDirectory() as tmp:
    diary = Diary(Path(tmp) / "repro.db")  # empty, throwaway database
    try:
        diary.add_night(
            Night(
                bedtime=local_input_to_aware(TYPED, ZONE),
                wake_time=local_input_to_aware("2026-03-08T08:20", ZONE),
                timezone=ZONE,
            )
        )
    except ValueError as error:
        print(f"OK: nonexistent local time rejected: {error}")
        sys.exit(0)
    shown = diary.nights()[0].local_bedtime  # what the diary page displays

if shown.strftime("%Y-%m-%dT%H:%M") == TYPED:
    print("OK: diary shows the time as typed")
    sys.exit(0)

print(f"BUG: typed {TYPED} {ZONE}, diary shows {shown:%H:%M} (accepted silently)")
sys.exit(1)
