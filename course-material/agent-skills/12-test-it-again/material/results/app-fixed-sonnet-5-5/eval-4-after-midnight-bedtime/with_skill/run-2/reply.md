This isn't a bug, so I didn't write a repro, a bundle or a ledger row.

The diary's column is headed "Night of", and it gives the evening the night began. Going to bed at 00:15 on Sunday 15 November is Saturday night, so the diary shows Sat 14 Nov.

- **Code:** `Night.night_of` in `src/nightjar/models.py:43` subtracts 12 hours from the local bedtime on purpose. Its docstring says "a 00:15 bedtime on Sunday is Saturday night".
- **Tests:** `tests/test_diary.py:81` checks this behaviour.
- **Requirements:** Story S-116, AC1 says "a 00:15 bedtime on Sunday counts as Saturday night". Test case TC-116-8 covers your exact example, and its expected result is Sat 14 Nov.
- **Check:** I ran your night (bed 00:15, wake 07:45, Sun 15 Nov, Toronto) through the code. It gives `Sat 14 Nov`.

If you'd still like the diary to show the calendar date of the bedtime, that's a product decision. It would change S-116 AC1 and the 7-night window, and it isn't a defect fix. The "Night of" heading could also be made clearer, for example by showing "Sat night". Either is a question for product.