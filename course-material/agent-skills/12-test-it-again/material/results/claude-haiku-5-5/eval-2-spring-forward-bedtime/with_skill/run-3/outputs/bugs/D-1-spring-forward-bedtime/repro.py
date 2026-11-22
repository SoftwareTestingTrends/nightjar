"""D-1: a bedtime logged inside the spring-forward gap is silently moved an hour later.

On 8 March 2026 Toronto clocks jump 02:00 -> 03:00, so 02:30 never happens.
The form accepts "2026-03-08T02:30" and the diary later shows 03:30.

Exit 1: the defect is present (accepted silently, shown as a different time).
Exit 0: fixed (the input is rejected, or the diary shows the time that was entered).
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, local_input_to_aware
from nightjar.models import Night

ZONE = "America/Toronto"
ENTERED = "2026-03-08T02:30"


def main() -> int:
    try:
        bedtime = local_input_to_aware(ENTERED, ZONE)
    except ValueError as error:
        print(f"FIXED: {ENTERED} rejected with {error!r}")
        return 0

    wake = local_input_to_aware("2026-03-08T08:00", ZONE)
    diary = Diary(Path(tempfile.mkdtemp()) / "throwaway.db")
    diary.add_night(Night(bedtime=bedtime, wake_time=wake, timezone=ZONE))
    shown = diary.nights()[0].local_bedtime.strftime("%H:%M")

    if shown == "02:30":
        print(f"FIXED: entered {ENTERED}, diary shows 02:30")
        return 0
    print(f"BUG: entered {ENTERED} (no error), diary shows {shown}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
