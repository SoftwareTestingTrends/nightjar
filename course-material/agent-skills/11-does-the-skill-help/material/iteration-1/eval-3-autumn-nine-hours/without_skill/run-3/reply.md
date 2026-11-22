This isn't a bug, so I haven't written a repro script.

Your night ran across the end of daylight saving time in Toronto. Clocks went back from 02:00 to 01:00 early on Sunday 1 November 2026, so the 01:00–02:00 hour happened twice. From 23:00 on Saturday to 07:00 on Sunday, 9 hours actually elapsed. The wall clocks differ by 8 hours, but the real elapsed time is 9.

`Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting. That is the right way to handle a DST change, and it's what `CLAUDE.md` asks for. I ran your night through it (23:00 → 07:00, `America/Toronto`) and got `9:00:00`.

If you slept the whole time, 9h is correct. If the app shows 9h but you'd rather see wall-clock time, that would be a product decision, not a defect. Say so and I can look at it as a change request.