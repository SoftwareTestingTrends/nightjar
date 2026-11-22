This isn't a bug, so I haven't written a repro script.

Clocks in America/Toronto go back one hour at 02:00 on Sunday 1 November 2026, so the night of Saturday 31 October has an extra hour. Going to bed at 23:00 and getting up at 07:00 gives 9 hours of real elapsed time, even though the wall clock shows an 8-hour gap. Between 01:00 and 02:00 the clock reads that hour twice.

`Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting. That is the correct approach, and the repo's notes warn about the opposite mistake. I ran your exact night through it and it returned `9:00:00`.

If you actually slept 8 hours, the diary's 9 hours is still right as elapsed time. The 8-hour figure comes from subtracting wall-clock times, which ignores the repeated hour.

If you'd like the UI to flag nights that cross a DST change, say so and I can raise that as a separate improvement. That would be a feature request, not a bug fix.