**This isn't a bug, so I haven't written a repro script or a bundle.**

Clocks in America/Toronto fell back on Sunday 1 November 2026, at 02:00 EDT (UTC-4), when they went back to 01:00 EST (UTC-5). Your night of Saturday 31 October crossed that change:

- Bed at 23:00 EDT is 03:00 UTC.
- Wake at 07:00 EST is 12:00 UTC.
- The real elapsed time is 9 hours, because the 01:00–02:00 hour happened twice.

I ran a `Night` with those times and got `duration` = 9:00:00. The offsets were -4 h at bedtime and -5 h at wake, and `night_of` was 2026-10-31.

The wall clock reads 8 hours (23:00 to 07:00), but you were asleep for 9. `Night.duration` in `src/nightjar/models.py:52` subtracts in UTC on purpose, which is what `CLAUDE.md` asks for, so 9h is correct.

The app doesn't tell the user about the extra hour, which may be why this looked wrong. If you'd like a note such as "includes the extra hour from the clocks going back" next to DST nights, that would be a product decision. I can raise it as a question for product, but I haven't added anything to the ledger.