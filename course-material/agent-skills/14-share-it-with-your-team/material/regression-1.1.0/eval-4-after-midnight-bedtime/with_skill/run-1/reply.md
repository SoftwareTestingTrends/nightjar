This isn't a bug, so I didn't write a repro script or a ledger row.

The diary labels each night by the evening it began, the "night of" date. A 00:15 bedtime on Sunday 15 November is Saturday night, so the row says Sat 14 Nov. Three places say this is intended:

- **Code:** `Night.night_of` at `src/nightjar/models.py:43-45` subtracts 12 hours from the local bedtime before taking the date. Its docstring says "a 00:15 bedtime on Sunday is Saturday night."
- **Requirements:** `docs/stories/S-116.md` AC1 says "A night belongs to its 'night of' date as shown in the diary (a 00:15 bedtime on Sunday counts as Saturday night)."
- **Other uses:** the same date drives the diary table (`index.html:75`), the coach prompt and the CSV export order (S-117 AC4).

I didn't run the app to check this. I read the code and docs only. The diary row also shows the actual bedtime (00:15), so the real time is still visible.

If the label confuses you, the fix would be to change how the diary presents it, for example "Sat night" instead of "Sat 14 Nov". That's a product decision and would affect S-116 and S-117, so it needs product's input.