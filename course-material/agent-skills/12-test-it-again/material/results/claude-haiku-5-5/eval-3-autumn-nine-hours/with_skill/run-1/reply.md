This isn't a bug. The app is right to show 9h, and I didn't write a `repro.py` or a ledger entry.

The night of Saturday 31 October 2026 crosses the end of daylight saving time in Toronto. Clocks go back from 02:00 EDT to 01:00 EST on Sunday 1 November, so the hour from 01:00 to 02:00 happens twice. Your bed-to-wake span is 8 wall-clock hours but 9 real hours:

- 23:00 EDT (UTC−4) on 31 Oct is 03:00 UTC on 1 Nov.
- 07:00 EST (UTC−5) on 1 Nov is 12:00 UTC on 1 Nov.
- That is 9 hours of elapsed time.

I ran the app's own `Night` class with those times, and it gives `duration = 9:00:00`. `Night.duration` subtracts in UTC on purpose, so DST changes are handled. The home page also computes the displayed sleep time from `night.duration` (`src/nightjar/templates/index.html:73`), so the 9h shown is the same value. The night is also correctly attributed to Saturday, as `night_of` returns 2026-10-31.

If your phone or the diary showed something other than 9h for that night, send me what you saw and I'll triage that separately.