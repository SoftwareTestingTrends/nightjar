This isn't a bug, so I haven't written a repro, bundle or ledger row.

Clocks in America/Toronto go back one hour at 02:00 on Sunday 1 November 2026, when daylight saving time ends. Your night crossed that change:

- **Bedtime:** 23:00 on 31 Oct is EDT (UTC−4), which is 03:00 UTC.
- **Wake:** 07:00 on 1 Nov is EST (UTC−5), which is 12:00 UTC.
- **Elapsed time:** 9 hours. The clock repeated the 01:00–02:00 hour, so you spent 9 real hours in bed even though the clock times are 8 hours apart.

I ran this night through `Night.duration` and it returned `9:00:00`. `Night.duration` in `src/nightjar/models.py` subtracts in UTC, which is the approach CLAUDE.md prescribes for DST.

If you'd rather the diary show wall-clock hours (8h) on a DST-change night, that's a product decision, not a defect. I can write up that question for product if you want.