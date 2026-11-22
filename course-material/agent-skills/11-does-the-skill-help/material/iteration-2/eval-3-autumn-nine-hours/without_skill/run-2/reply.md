This isn't a bug, so I haven't written a repro script.

Clocks in America/Toronto go back one hour at 02:00 on Sunday 1 November 2026. That ends daylight saving time. Your night from 23:00 on Saturday 31 October to 07:00 on Sunday 1 November therefore contained 01:00–02:00 twice. You were in bed for 9 real hours, even though the clock difference is 8.

I ran it to check. `Night.duration` returns `9:00:00` for that night. The UTC offsets are -4h at bedtime and -5h at wake. `Night.duration` in `src/nightjar/models.py` converts both times to UTC before subtracting, which is the approach the project notes require.

If you want the diary to show 8h, that would be a product decision: show wall-clock time instead of elapsed sleep. I wouldn't recommend it, because the 9h figure is the time you actually slept.