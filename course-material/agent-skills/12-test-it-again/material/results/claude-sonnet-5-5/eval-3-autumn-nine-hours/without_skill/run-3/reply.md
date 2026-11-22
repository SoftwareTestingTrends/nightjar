This isn't a bug, so I didn't write a repro script.

DST ends in America/Toronto at 02:00 on Sunday 1 November 2026, when clocks go back an hour. Your bedtime of 23:00 on 31 October was at UTC-4, and your 07:00 wake-up was at UTC-5. The elapsed time between them is 9 hours, because the 01:00–02:00 hour happened twice.

`Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting. That's the approach `CLAUDE.md` calls for, and it gives 9 hours here. A wall-clock subtraction would give the 8 hours you expected, and that would be the wrong answer, since you were in bed for 9 hours.

The 8 hours comes from the clock times, but the diary reports real time slept.

I didn't run `make test` or `make lint`, since I changed no files.