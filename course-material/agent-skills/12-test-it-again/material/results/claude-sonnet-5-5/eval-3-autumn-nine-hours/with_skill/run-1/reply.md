This isn't a bug, so I haven't written a repro, a bundle, or a ledger row.

DST ended in America/Toronto at 02:00 on Sunday 1 November 2026, when clocks fell back to 01:00. That night had an extra hour. Bed at 23:00 EDT (UTC−4) and up at 07:00 EST (UTC−5) is 03:00 UTC to 12:00 UTC, so 9 real hours elapsed.

I confirmed this by running the calculation in Python. `Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting, so it returns 9:00:00. That is correct, and it is the approach CLAUDE.md prescribes. The wall clock shows 8 hours, but you were asleep for 9.

**Possible follow-up for product:** the diary shows only the 23:00 and 07:00 times, so the 9h looks like an error. If you'd like a "clocks changed overnight" note on the night, that is a feature request, not a defect. I can write it up that way if you want.