This isn't a bug, so I didn't write a repro script.

The night of Saturday 31 October 2026 runs across the end of daylight saving time in Toronto. Clocks fall back at 02:00 on Sunday 1 November, so that night has two 01:00–02:00 hours. A bed time of 23:00 and a wake time of 07:00 on the wall clock are 9 real hours apart, not 8.

`Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting. That is the correct approach, and CLAUDE.md warns against the wall-clock alternative. I ran your night through it and it returned `9:00:00`.

The 8 hours you expected is the wall-clock difference. If NightJar reported that, it would be the real bug.

If you'd rather the diary show wall-clock time in bed, that would be a product decision. It isn't a defect in the current calculation.