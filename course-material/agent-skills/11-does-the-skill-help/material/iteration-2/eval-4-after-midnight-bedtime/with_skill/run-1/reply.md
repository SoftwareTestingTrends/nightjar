This isn't a bug, so I didn't write a repro script, a bundle or a ledger row.

The diary's "Night of" column shows the evening the night began, not the calendar date of the bedtime. A 00:15 bedtime on Sunday 15 November is Saturday night, so it's listed as Saturday 14 November.

- **Code:** the docstring on `Night.night_of` in `src/nightjar/models.py:43` says "a 00:15 bedtime on Sunday is Saturday night". The column is headed "Night of" in `index.html:70`.
- **Spec:** S-116 AC1 says "a 00:15 bedtime on Sunday counts as Saturday night", and a night belongs to its "night of" date as shown in the diary.
- **Check:** I built a night with bedtime 2026-11-15 00:15 in America/Toronto. `night_of` returned Saturday 14 Nov, as designed.

If the column heading is confusing, you could raise a UX or copy change with product, for example showing the actual bedtime date next to it. That would be a feature request, not a defect.