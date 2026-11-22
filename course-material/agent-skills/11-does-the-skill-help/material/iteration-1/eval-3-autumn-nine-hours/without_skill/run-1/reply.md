This isn't a bug, so I haven't written a repro script.

Clocks in America/Toronto go back one hour at 02:00 on Sunday 1 November 2026. Your night from 23:00 on 31 October to 07:00 on 1 November therefore spans the DST change. The clock reads 8 hours between those times, but 9 hours really passed (23:00 EDT is UTC−4 and 07:00 EST is UTC−5). I checked this with `zoneinfo`, and the UTC difference is exactly 9:00:00.

`Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting. That is the right way to do it, and it gives 9h. If you had slept the whole time, 9h would be correct.

Check one thing on your side. If you were in bed for 8 hours by the clock, you may have entered the times as wall-clock values. That would make the app count the repeated 01:00–02:00 hour. If you want the diary to show 8h, enter the real wake time. Otherwise leave it as it is.