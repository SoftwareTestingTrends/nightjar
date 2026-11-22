This isn't a bug, so I didn't write a repro script or a bug bundle, and I didn't add a ledger row.

Your clock times are right, but there was a time change that night. Daylight saving ended in Toronto at 02:00 on Sunday 1 November 2026, and clocks went back to 01:00. That means the 01:00–02:00 hour happened twice:

- You went to bed at 23:00 EDT (UTC−4), which is 03:00 UTC.
- You woke at 07:00 EST (UTC−5), which is 12:00 UTC.
- That's **9 hours of real time**, even though the clock only shows an 8-hour gap.

**What the spec says:** story S-116 (`docs/stories/S-116.md:29`) requires that "Durations are real elapsed time, so a night that crosses a daylight-saving change is an hour shorter or longer on the clock." The code does this on purpose: `Night.duration` converts both times to UTC before subtracting them (`src/nightjar/models.py:52`). The project notes also list doing it the other way, with clock times, as a mistake to avoid.

**What I tried:** I logged exactly your night (23:00 on 2026-10-31 to 07:00 on 2026-11-01, America/Toronto) through the app's `/nights` form against a throwaway database, not `nightjar.db`. All 3 runs gave the same result: the bedtime was saved with offset −04:00, the wake time with −05:00, the duration was `9:00:00`, and the diary showed `9h 00m`. Those match the spec.

If you think people would rather see 8 hours, or want a note on nights where the clocks change, that's a question for product, not a defect. The check script I used is outside the repo at `$TMPDIR/nj-triage/check.py`, and you can delete it.