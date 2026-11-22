This isn't a bug, so I haven't written a repro script.

Daylight saving time ends in America/Toronto at 02:00 on Sunday 1 November 2026, when the clocks go back an hour. The night you logged, 23:00 on Sat 31 Oct to 07:00 on Sun 1 Nov, therefore had 9 real hours on the clock, not 8. The 02:00–03:00 hour happened twice.

`Night.duration` in `src/nightjar/models.py:52` subtracts in UTC, as the project conventions require. I ran that calculation for your night and got `9:00:00`. Subtracting wall-clock times would have given 8 hours, which is the figure that would be wrong.

If you'd rather the diary showed 8 hours, that would be a product decision about how to display DST nights, not a defect fix. I'd keep real elapsed time, because it's what your body actually slept.