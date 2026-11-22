Not a bug. It's documented, intended behavior, so I haven't written a repro script.

`Night.night_of` in `src/nightjar/models.py:43-45` is deliberately defined as "the evening this night began". Its docstring says: "a 00:15 bedtime on Sunday is Saturday night." Story S-116 AC1 says the same thing: "a 00:15 bedtime on Sunday counts as Saturday night". Your bedtime at 00:15 on Sunday 15 November is therefore correctly listed as the night of Saturday 14 November.

The column is headed "Night of", not "Date", so the label reads as "the night that began on Saturday". If it still looks confusing, that's a UX or copy question. One option is to show the actual bedtime date next to the label. I didn't write a test for it because nothing is broken.