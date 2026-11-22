It isn't a bug. The app is right to show 9 hours.

The night of Saturday 31 October 2026 crosses the fall-back change in Toronto. Clocks went back at 02:00 EDT on Sunday 1 November, so 07:00 that morning is EST (UTC−5), while 23:00 the night before was EDT (UTC−4).

- Bed: 23:00 EDT = 03:00 UTC on 1 Nov
- Wake: 07:00 EST = 12:00 UTC on 1 Nov
- Elapsed time: 9 hours

`Night.duration` in `src/nightjar/models.py:52-54` subtracts in UTC, which is the right approach here. I confirmed by constructing this night directly: it returns `9:00:00` and `night_of` is `2026-10-31`. The 8 hours you're expecting is the wall-clock difference (23:00 to 07:00 on the face of the clock). The extra hour happened because the clock was turned back, and you really were asleep for that hour as well.

I didn't write a repro script because there's no bug to reproduce. I also didn't change any code.

If the diary shows "23:00–07:00 · 9h" and that looks odd to you, that's a display question rather than a calculation error. The app could add a note on DST nights, but that's a design choice for you to make.