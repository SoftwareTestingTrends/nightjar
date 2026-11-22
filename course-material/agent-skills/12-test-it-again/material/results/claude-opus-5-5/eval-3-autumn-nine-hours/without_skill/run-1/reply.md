**This isn't a bug. 9 hours is correct, so I didn't write a repro script.**

Daylight saving time ended in Toronto during that night. At 02:00 on Sunday 1 November 2026 the clocks went back to 01:00, so the hour from 01:00 to 02:00 happened twice. Bed to wake was 8 hours on the clock but 9 hours of real time:

- Bedtime: 31 Oct 23:00 EDT (UTC−4) = 03:00 UTC
- Wake: 1 Nov 07:00 EST (UTC−5) = 12:00 UTC
- Elapsed: **9h 00m**

I checked the calculation in Python with `zoneinfo` and got exactly 9:00:00. The app does the same thing: `Night.duration` (`src/nightjar/models.py:52`) converts both times to UTC before subtracting, as the project's rules require. If it subtracted the wall-clock times instead, it would report the 8 hours you expected, and that would be the actual bug.