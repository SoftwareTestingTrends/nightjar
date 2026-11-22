This isn't a bug, so I didn't write a `repro.py`, a bundle or a ledger row.

Clocks in America/Toronto go back one hour at 02:00 on Sunday 1 November 2026, when daylight time ends. The night of Saturday 31 October therefore has an extra hour:

- 23:00 on 31 October is EDT (UTC−4), which is 03:00 UTC.
- 07:00 on 1 November is EST (UTC−5), which is 12:00 UTC.
- The gap is 9 hours of real time. A wall clock shows 8 hours between 23:00 and 07:00, but you were in bed for 9.

I checked this three times against `Night.duration`, using a bedtime of 23:00 and a wake time of 07:00 in `America/Toronto`. Each run gave `9:00:00`, with the correct UTC offsets (−4 at bedtime, −5 at wake).

`Night.duration` subtracts in UTC, as the conventions in CLAUDE.md require, so the 9 hours is correct. A wall-clock subtraction would show 8 hours, and that is the mistake to avoid.

If the UI is confusing, a note like "clocks went back that night" next to the duration would help. That would be a feature request, not a defect.