It isn't a bug, so I didn't write a `repro.py` and didn't add a ledger row.

The 9 hours is correct. Toronto's clocks went back from EDT to EST at 02:00 on Sunday 1 November 2026, the night after the one you're reporting. A bedtime of 23:00 on Saturday 31 October and a wake time of 07:00 on Sunday 1 November therefore span 9 real hours, not 8. Your 8 comes from subtracting the wall-clock times (07:00 − 23:00), which ignores that the hour from 01:00 to 02:00 happened twice.

What I ran, against a temporary database rather than `nightjar.db`:

- Bedtime stored as `2026-10-31T23:00-04:00` and wake time as `2026-11-01T07:00-05:00`.
- `Night.duration` returned 9.0 hours, and the value was the same after a round trip through the database.
- The night is attributed to Saturday 31 October, as expected.
- The web template (`src/nightjar/templates/index.html:73`) computes minutes from `night.duration`, so the page shows the same 9 hours.

The code follows the project's rule to subtract in UTC (`Night.duration` in `src/nightjar/models.py:52`), which is why the answer is right across the DST change.

If you expected 8 hours, the thing to check is whether the app should show wall-clock time in place of elapsed time. That's a product decision, not a defect in the current calculation. I haven't written a question for product.