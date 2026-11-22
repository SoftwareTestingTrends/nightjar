This isn't a bug, so I haven't written a repro script.

Clocks in Toronto fall back on Sunday 1 November 2026 at 02:00, when 02:00 EDT becomes 01:00 EST. That repeats the 01:00–02:00 hour, so the night of 31 October into 1 November has 9 real hours between 23:00 and 07:00, not 8. The wall clocks differ by 8 hours, but you were in bed for 9.

I ran that night through `Night.duration` (`src/nightjar/models.py:52`) and it returns `9:00:00`. The code converts both times to UTC before subtracting, which is the correct way to handle a DST change. Your diary entry is right, and you had an extra hour of sleep that night.

If you'd rather the diary showed "8h by the clock" on DST-change nights, that would be a feature request. It's a separate question from this calculation.