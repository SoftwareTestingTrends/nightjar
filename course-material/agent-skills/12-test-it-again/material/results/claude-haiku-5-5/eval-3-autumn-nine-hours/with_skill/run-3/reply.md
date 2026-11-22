This isn't a bug. The 9 hours is correct, and I didn't write a repro script.

The night of Saturday 31 October 2026 crosses the fall-back change in Toronto. Clocks go back from 02:00 EDT to 01:00 EST on Sunday 1 November. So 23:00 EDT to 07:00 EST is 9 real hours, even though the wall clock only moves 8 hours.

Running the app's own code on that night gives:

- `Night.duration` = `9:00:00` (9.0 hours). `models.py:52` subtracts in UTC, which is the intended behaviour and is why the `CLAUDE.md` warning about same-zone subtraction exists.
- Local bedtime is `2026-10-31 23:00-04:00` and local wake is `2026-11-01 07:00-05:00`. The night is correctly filed under Saturday 31 October.
- The diary shows the duration from `night.duration` (`templates/index.html:73`), so it displays 9h.

The "8 hours" figure is the wall-clock difference, which ignores the repeated 01:00–02:00 hour. That hour was actually slept through, so counting it is right.

I didn't create a `bugs/` bundle or touch `bugs/ledger.md`, since the bundle format covers defects and this isn't one. If you saw a different number in the UI, or expected the diary to show 8h, send me the screenshot or the stored bedtime and wake time and I'll triage that.