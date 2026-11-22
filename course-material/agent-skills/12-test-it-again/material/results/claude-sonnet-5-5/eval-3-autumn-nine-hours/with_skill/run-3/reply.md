This isn't a bug, so I didn't write a repro script or a bundle.

Daylight saving time in Toronto ended at 02:00 on Sunday 1 November 2026, when the clocks went back to 01:00. The night of Saturday 31 October therefore had an extra hour. Here is what I ran:

- Bedtime 23:00 on 31 October is UTC-4 (EDT).
- Wake time 07:00 on 1 November is UTC-5 (EST).
- `Night.duration` gives 9:00:00.

Your clock showed 8 hours from 23:00 to 07:00, but 9 hours really passed. NightJar subtracts the two times in UTC, which is the right way to do it.

I didn't edit any files and added nothing to `bugs/` or the ledger.

One possible follow-up: the page might not make clear that the night crossed a clock change. If you'd like a note shown on those nights, that would be a product decision.