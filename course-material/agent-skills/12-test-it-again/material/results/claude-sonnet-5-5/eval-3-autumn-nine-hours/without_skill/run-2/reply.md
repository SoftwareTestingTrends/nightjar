This isn't a bug, so I haven't written a repro script.

Daylight saving time ended in America/Toronto at 02:00 on Sunday 1 November 2026, when clocks went back to 01:00. Your night of Saturday 31 October therefore had an extra hour:

- Bedtime was 23:00 EDT (UTC−4).
- Wake time was 07:00 EST (UTC−5).
- The real elapsed time is 8 hours on the wall clock plus the repeated 01:00–02:00 hour, which makes 9 hours.

`Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting, which is the approach CLAUDE.md prescribes for DST. I ran your night through it and it returned `9:00:00`, with offsets of −4h at bedtime and −5h at wake.

If your in-bed time really was 23:00 to 07:00 by the clock, then 9 hours is the correct elapsed time. The diary is showing the real duration, not the wall-clock difference.

If something else looks off, such as a different date or a night with no DST change, send me the stored bedtime, wake time and zone. I'll check that case.