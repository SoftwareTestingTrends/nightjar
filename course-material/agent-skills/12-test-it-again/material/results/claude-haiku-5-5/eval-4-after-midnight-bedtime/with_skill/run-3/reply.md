This isn't a bug, so I didn't write a `repro.py` or touch `bugs/`.

The diary is doing what the spec says. The "Night of" column is the evening the night began, not the calendar date of the bedtime. A bedtime at 00:15 on Sunday 15 November is Saturday night's sleep.

- **Spec:** S-116 AC1 says "a 00:15 bedtime on Sunday counts as Saturday night."
- **Code:** `Night.night_of` in `src/nightjar/models.py:43` subtracts 12 hours from the local bedtime before taking the date, so 00:15 becomes 12:15 the previous day. The diary template (`index.html:75`) displays that value.
- **Test:** `tests/test_diary.py::test_night_of_is_the_evening_the_night_began` covers the same case and passes.
- **Reproduction:** I built a `Night` with a 00:15 bedtime on 15 Nov 2026 in both `America/Toronto` and `Europe/London`. Both give `night_of` = Sat 14 Nov 2026.

If you expected the label to show the calendar date of the bedtime, that's a change to S-116 AC1 and to the `night_of` rule, so it's a product decision rather than a fix. I assumed you meant the "Night of" column, and I didn't run `make test` or `make lint` since nothing changed.