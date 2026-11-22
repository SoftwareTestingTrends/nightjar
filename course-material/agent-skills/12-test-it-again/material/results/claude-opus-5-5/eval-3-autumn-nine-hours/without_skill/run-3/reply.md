This isn't a bug, so I haven't written a repro script.

Daylight saving time ended in Toronto at 02:00 on Sunday 1 November 2026, and the clocks went back to 01:00. That means the hour from 01:00 to 02:00 happened twice that night.

- 23:00 on 31 October was EDT (UTC−4), which is 03:00 UTC.
- 07:00 on 1 November was EST (UTC−5), which is 12:00 UTC.
- From 03:00 to 12:00 UTC is **9 hours** of real time.

The clock times say 8 hours, but you were actually in bed for 9. `Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting them, which is the right way to handle this. I ran the same calculation with `zoneinfo` and it also gave 9:00:00.

If the app had shown 8 hours, that would have been the bug: subtracting the clock times directly gives the wrong answer on DST nights.