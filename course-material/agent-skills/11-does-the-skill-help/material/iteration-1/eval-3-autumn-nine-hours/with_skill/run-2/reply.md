This isn't a bug, so I didn't write a `repro.py`, a bug bundle or a ledger row.

Clocks in America/Toronto go back one hour at 02:00 on Sunday 1 November 2026, when 02:00 becomes 01:00. The night of Saturday 31 October therefore had 9 real hours between 23:00 and 07:00, because the 01:00–02:00 hour happened twice.

I checked this against the app's own code. A `Night` from 2026-10-31 23:00 to 2026-11-01 07:00 in `America/Toronto` gives:
- **UTC offsets:** bedtime is at -04:00 (EDT) and wake time is at -05:00 (EST).
- **Duration:** `Night.duration` returns `9:00:00`.

`Night.duration` converts both times to UTC before subtracting, which is the right way to handle a DST change (`src/nightjar/models.py`). Subtracting wall-clock times would have given 8 hours, which is the number you expected.

If you want the diary to show this night differently, for example with a note that the clocks changed, that would be a feature request rather than a defect.