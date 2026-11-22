This isn't a bug, so I didn't write a repro script.

The diary labels each night by the evening it began. `Night.night_of` in `src/nightjar/models.py:43` does this on purpose, and its docstring says: "a 00:15 bedtime on Sunday is Saturday night." Your 00:15 bedtime on Sunday 15 November is therefore listed as Saturday 14 November.

The same rule appears in the S-116 story (AC1): "a 00:15 bedtime on Sunday counts as Saturday night."

The code does what the spec says, so there's no defect. If you'd rather the diary show the calendar date of the bedtime, that's a product change. It would also affect S-116's weekly summary and S-117's export ordering. I can write that up as a change request if you want.