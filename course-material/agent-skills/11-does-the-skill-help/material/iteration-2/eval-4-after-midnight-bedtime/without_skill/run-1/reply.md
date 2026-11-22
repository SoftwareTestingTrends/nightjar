This isn't a bug, so I haven't written a repro script.

The diary labels each entry by the evening the night began. `Night.night_of` in `src/nightjar/models.py:43` does this and says so in its docstring: "a 00:15 bedtime on Sunday is Saturday night". It takes the local bedtime, subtracts 12 hours and uses that date. For 00:15 on Sunday 15 November that gives Saturday 14 November.

The spec says the same. Story S-116 AC1 reads "a 00:15 bedtime on Sunday counts as Saturday night". S-117 AC4 and the weekly summary also rely on that "night of" date.

The label is also the usual convention for sleep diaries. A night that starts at 00:15 Sunday is "Saturday night" to most people. It also keeps a 23:30 bedtime and a 00:30 bedtime in the same "night" instead of splitting them across two dates.

If you'd rather the diary show the calendar date of falling asleep, that would be a product change. It would mean revising S-116 AC1 and S-117 AC4, not fixing a defect.

I didn't run the app or write any files.