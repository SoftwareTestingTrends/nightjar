This isn't a bug, so I didn't write a repro script.

The diary column is headed "Night of", meaning the evening the night began. A 00:15 bedtime on Sunday 15 November belongs to the night that started on Saturday 14 November, so "Sat 14 Nov" is correct.

This is deliberate and written down in three places:
- `src/nightjar/models.py:44`: `Night.night_of` is documented as "a 00:15 bedtime on Sunday is Saturday night". It works by subtracting 12 hours from the local bedtime and taking the date.
- `docs/stories/S-116.md:17-18`: "a 00:15 bedtime on Sunday counts as Saturday night".
- The test-case example `TC-116-8` uses this exact case: bed 00:15 on Sun 15 Nov gives the night of Sat 14 Nov.

The diary does show the real bedtime time of 00:15 in the "Bed" column. If "Sat 14 Nov" next to 00:15 looks confusing, that's a UX or wording question. You could rename the header to "Evening of" or show the actual calendar date next to it. I can draft that as an improvement suggestion, but it isn't a defect against the current spec.