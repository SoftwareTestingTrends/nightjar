This isn't a bug, so I didn't write a `repro.py` or a bug bundle.

**Why 9h is correct:** Daylight saving time in Toronto ended at 02:00 on Sunday 1 November 2026, when the clocks went back to 01:00. The night of Saturday 31 October therefore has an extra hour. Bed at 23:00 (UTC-4) and up at 07:00 (UTC-5) is 9 real hours, even though the wall clocks are 8 hours apart.

I ran `Night` for that exact night three times. Each run gave a duration of `9:00:00`, with a UTC offset of -4 at bedtime and -5 at wake time. `Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting, so the extra hour is counted. That is the intended behaviour. `CLAUDE.md` lists naive same-zone subtraction (8h here) as a known mistake.

The 8 hours you expected comes from subtracting the clock times. It undercounts the time you actually slept on a night when the clocks go back.

**Ledger:** `bugs/` doesn't exist yet, and I didn't add a ledger row because the ledger only tracks defects.

**Possible product question:** if the "9h" with no explanation is confusing, that's a UX question, not a calculation bug. One option would be a "clocks changed" note on DST nights. I haven't raised it with product.