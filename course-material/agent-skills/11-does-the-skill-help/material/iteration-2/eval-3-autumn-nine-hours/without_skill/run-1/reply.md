This isn't a bug, so I haven't written a repro script.

Clocks in America/Toronto go back one hour at 02:00 on Sunday 1 November 2026. Your night of Saturday 31 October therefore had an extra hour:

- 23:00 on 31 Oct is EDT (UTC−4), which is 03:00 UTC.
- 07:00 on 1 Nov is EST (UTC−5), which is 12:00 UTC.
- The elapsed time is 9 hours of real time.

I confirmed this with `zoneinfo`. `Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting, which is the right way to handle a DST change. The 8 hours you counted is the wall-clock difference between 23:00 and 07:00, and it ignores the repeated 01:00–02:00 hour.

If you want the app to show something different for DST-change nights, such as a note that the night was 9 hours because the clocks changed, that would be a feature request.