This isn't a bug, so I didn't write a repro script.

I imported the same CSV twice into a fresh database. The first import added 2 nights and the second added 0, leaving 2 stored. When I re-imported with one bedtime written in a different UTC offset (`+00:00` instead of `-04:00`) for the same instant, it still added nothing.

This is because `Diary.add_nights` (`src/nightjar/diary.py:70`) skips any night whose UTC bedtime and wake time already exist. The `/import` route in `src/nightjar/web.py:85` uses it. The page shows the number actually added in `?imported=N`, so a second import should say 0.

I didn't test the browser upload itself, only the diary and parsing code the route calls. The dedup has two limits:
- **Key:** it matches on bedtime and wake time only. If you edit a night's notes or timezone in the CSV and re-import, it counts as already present and the stored row isn't updated.
- **Rows within one file:** two identical rows in a single CSV collapse into one night.

If you saw real doubling, check how it happened:
- **Different values:** the rows may differ slightly, for example a changed bedtime or wake time, or seconds added by a spreadsheet export.
- **Manual logging:** the nights may have been added through the manual "log a night" form. That goes through `add_night`, which doesn't dedupe.

If you can send me the CSV and the steps, I'll test that exact case.