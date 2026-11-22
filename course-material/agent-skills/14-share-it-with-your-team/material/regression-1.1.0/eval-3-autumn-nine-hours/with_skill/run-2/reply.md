This isn't a bug, so I didn't write a repro script or a bundle.

America/Toronto ended daylight saving time at 02:00 on Sunday 1 November 2026, when the clocks went back to 01:00. Your night of Saturday 31 October therefore had one extra hour:

- You went to bed at 23:00 EDT, which is UTC−4.
- You woke at 07:00 EST, which is UTC−5.
- Between those two moments, 9 hours of real time passed (the 01:00–02:00 hour happened twice).

I checked this by building the night with `Night(...)` and reading `duration`. It returns `9:00:00`, with a UTC−4 offset at bedtime and UTC−5 at wake-up. That matches what the app shows. `Night.duration` in `src/nightjar/models.py:52` subtracts in UTC, which is how CLAUDE.md says to handle DST.

Counting wall-clock times (23:00 to 07:00 is 8 hours) is what gives the wrong answer here.

I made no ledger entry, because the ledger only records confirmed or not-reproduced defects. If product wants the diary to show the clock-time span (8h) on a DST-change night, tell me. That would be a product decision about expected behaviour, and I could record it as a question rather than a bug.