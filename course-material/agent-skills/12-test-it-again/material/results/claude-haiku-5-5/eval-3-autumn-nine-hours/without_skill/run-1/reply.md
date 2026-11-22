It isn't a bug, so I didn't write `bugs/<short-name>/repro.py`.

The clocks go back at 02:00 on Sunday 1 November 2026 in Toronto. Your night runs from 23:00 EDT on Saturday to 07:00 EST on Sunday, so it contains an extra hour. The real elapsed time is 9 hours, and wall-clock subtraction gives 8.

I checked the project's own `Night` class with that exact night. `duration` is 9:00:00. `Night.duration` in `src/nightjar/models.py:52` subtracts in UTC, which is the fix the CLAUDE.md warns about, and the diary template in `index.html` displays that value directly.

The tracker's seed entry for this ticket (`tools/tracker/seed.json`) already describes this exact case and says the UTC fix is in. I didn't touch the tracker.