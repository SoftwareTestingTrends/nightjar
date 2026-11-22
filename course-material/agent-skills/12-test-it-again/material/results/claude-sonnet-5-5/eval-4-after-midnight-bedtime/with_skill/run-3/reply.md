This isn't a bug, so I didn't write a repro script or a bundle, and there's no ledger row.

The diary does what you describe. I logged a 00:15 bedtime on Sunday 15 Nov 2026 (America/Toronto) and it came back as `night_of` = Sat 14 Nov. But that's the designed behaviour, and two places say so:

- **Code:** the docstring on `Night.night_of` in `src/nightjar/models.py:43` reads "The evening this night began: a 00:15 bedtime on Sunday is Saturday night." The code subtracts 12 hours from the local bedtime and takes the date.
- **Spec:** story S-116 AC1 says "A night belongs to its 'night of' date as shown in the diary (a 00:15 bedtime on Sunday counts as Saturday night)." S-117 AC4 also orders nights by this date.

So the diary labels a night by the evening it began. A sleep that starts at 00:15 on Sunday belongs to Saturday night.

If you'd still like the diary to show the calendar date of the bedtime, that's a product change, not a defect. It would also change the S-116 summary window and the S-117 ordering. I can draft that as a question for product if you want.