This isn't a bug, so I didn't write a repro script.

The diary labels each night by the evening it began, and that's deliberate. In `src/nightjar/models.py:43-45`, `Night.night_of` subtracts 12 hours from the local bedtime and takes the date. Your 00:15 bedtime on Sunday 15 November becomes 12:15 on Saturday 14 November, so the diary shows "Sat 14 Nov".

The docs say the same thing. The docstring reads "a 00:15 bedtime on Sunday is Saturday night." `docs/stories/S-116.md` AC1 repeats it: "a 00:15 bedtime on Sunday counts as Saturday night". It's how people usually talk about sleep, since "Saturday night" ends up in Sunday morning.

If you'd rather see the calendar date of the bedtime, that's a change to the requirements, not a fix. It would affect S-116's summary window and S-117's night ordering. Showing the bedtime time next to the label might also help. I can make either change if you want.