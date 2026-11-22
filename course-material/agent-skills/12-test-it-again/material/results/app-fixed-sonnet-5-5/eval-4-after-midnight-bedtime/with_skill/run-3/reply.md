This isn't a bug, so I didn't write a repro, a bundle or a ledger row.

I reproduced what you saw. A night logged with a 00:15 bedtime on Sunday 15 Nov 2026 shows as `Sat 14 Nov` in the "Night of" column.

That column is meant to name the evening the night began, not the calendar date of the bedtime:
- **Code:** `Night.night_of` in `src/nightjar/models.py:43` documents it as "a 00:15 bedtime on Sunday is Saturday night". It subtracts 12 hours from the local bedtime before taking the date.
- **Requirements:** story S-116 AC1 says "a 00:15 bedtime on Sunday counts as Saturday night".
- **Page:** the column header is "Night of", not "Date".

Your bedtime was early Sunday morning, so it belongs to Saturday night. The same rule keeps 23:30 and 00:30 on the same night.

If it still reads as confusing, that is a copy question for product, not a defect. For example, the column could show the bed date as well, or the header could be reworded. I can write that up as a question for product if you'd like.