This isn't a bug, so I haven't written a repro script.

Daylight saving time ends in Toronto at 02:00 on Sunday 1 November 2026, when clocks go back to 01:00. Your night of 31 October into 1 November therefore had an extra hour. At 23:00 Toronto was on UTC−4. At 07:00 it was on UTC−5. The real time between those two moments is 9 hours, not the 8 you get by subtracting the clock times.

`Night.duration` in `src/nightjar/models.py:52` converts both times to UTC before subtracting, which is the correct approach. I ran your exact times and got `9:00:00`.

If you were in bed from 23:00 to 07:00 on the clock, you really did spend 9 hours in bed that night. If you want to check the sleep figure separately, the 9h is time in bed. It isn't a measure of how much of that time you were asleep.

If you'd like the app to explain this to users, for example with a "this night had a DST change" note, that would be a feature request rather than a bug fix.