This isn't a bug, so I didn't write a repro script.

The diary labels each night by the evening it began, not by the calendar date of the bedtime. `Night.night_of` in `src/nightjar/models.py:43` does this on purpose. It subtracts 12 hours from the local bedtime and takes the date. A 00:15 bedtime on Sunday 15 Nov becomes Saturday 14 Nov at 12:15, so the night is "Sat 14 Nov". The docstring says so ("a 00:15 bedtime on Sunday is Saturday night"). Story S-116 AC1 also specifies it: "a 00:15 bedtime on Sunday counts as Saturday night".

So the diary is treating "Saturday night" as "the night that started Saturday evening". If you'd rather have the diary show the calendar date of the bedtime, that's a product change. It would also affect the S-116 summary window and the S-117 export order.

I didn't run anything, because the code and the spec agree.