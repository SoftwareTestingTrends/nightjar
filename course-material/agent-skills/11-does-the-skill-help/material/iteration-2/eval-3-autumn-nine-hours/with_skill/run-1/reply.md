This isn't a bug, so I didn't write a repro script or a bundle, and I didn't add a ledger row.

**Why 9 hours is correct.** Daylight saving time ends in Toronto on Sunday 1 November 2026, at 02:00 local time. At that point the clocks go back to 01:00. So your night of 31 October, from 23:00 to 07:00 on the wall clock, contained one extra hour:

- You went to bed at 23:00 EDT, which is UTC−4.
- You woke at 07:00 EST, which is UTC−5.
- The real elapsed time is 8 hours plus the repeated 01:00–02:00 hour, so 9 hours.

I ran `Night` with exactly those times. It gave `duration = 9:00:00`, with a bedtime offset of −04:00 and a wake offset of −05:00. `Night.duration` in `src/nightjar/models.py:52` subtracts in UTC on purpose, which is the right way to handle this. `docs/traceability.md` also lists "correct across DST (Toronto, London)" as a requirement, covered by T-114-6.

**What you saw.** 8 hours is what a wall-clock subtraction gives (07:00 − 23:00). The 9h shown is the time you actually spent in bed.

**Possible product question.** Some users might expect the diary to say 8h on a fall-back night. That would be a product decision, and the current behaviour matches the requirement. If you think the page should explain the extra hour, I can raise that as a question for product.