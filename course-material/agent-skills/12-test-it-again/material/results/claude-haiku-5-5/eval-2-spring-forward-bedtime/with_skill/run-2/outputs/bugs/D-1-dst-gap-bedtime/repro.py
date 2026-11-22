"""D-1: a bedtime inside the spring-forward gap is silently shown an hour later.

On 8 March 2026 Toronto clocks jump 02:00 -> 03:00, so 02:30 never happens.
The diary accepts a 02:30 entry and shows it as 03:30 EDT, with no message.

Exit 1 while the defect is present (the entry is accepted and shown as 03:30).
Exit 0 once it is fixed (the impossible time is refused with a ValueError).

The fixed behaviour is an assumption for product to confirm: the report does
not say what the diary should do with a non-existent time.
"""

import sys
import tempfile
from pathlib import Path

from nightjar.diary import Diary, local_input_to_aware
from nightjar.models import Night

ZONE = "America/Toronto"


def main() -> int:
    db = Path(tempfile.mkdtemp()) / "throwaway.db"  # never nightjar.db
    diary = Diary(db)
    try:
        bedtime = local_input_to_aware("2026-03-08T02:30", ZONE)
        wake_time = local_input_to_aware("2026-03-08T09:00", ZONE)
        diary.add_night(Night(bedtime=bedtime, wake_time=wake_time, timezone=ZONE))
    except ValueError as error:
        print(f"FIXED: impossible 02:30 entry refused ({error})")
        return 0

    shown = diary.nights()[0].local_bedtime.strftime("%H:%M %Z")
    if shown == "03:30 EDT":
        print("BUG PRESENT: entered 02:30 on 2026-03-08, diary shows 03:30 EDT")
        return 1
    print(f"FIXED: entered 02:30 on 2026-03-08, diary shows {shown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
