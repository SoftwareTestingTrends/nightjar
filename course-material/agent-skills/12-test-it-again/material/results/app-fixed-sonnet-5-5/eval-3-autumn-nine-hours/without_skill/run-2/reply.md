This isn't a bug, so I didn't write a repro script.

DST ended in Toronto at 02:00 on Sunday 1 November 2026, when clocks went back to 01:00. Your night of Saturday 31 October ran across that change, so the clock showed 23:00 to 07:00 but 9 hours actually passed. The offset is UTC-4 at bedtime and UTC-5 at wake-up, so 23:00 EDT is 03:00 UTC and 07:00 EST is 12:00 UTC.

`Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting, which is the approach CLAUDE.md recommends. I ran your night through it and it returns `9:00:00`. The 9h shown is correct. You got an extra hour in bed because of the clock change.

If the diary should instead show the 8 hours the wall clock suggests, that would be a product decision. It would go against the app's UTC convention and be wrong for sleep tracking, so I wouldn't recommend it.