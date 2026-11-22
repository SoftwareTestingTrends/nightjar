This isn't a bug, so I didn't write `bugs/<short-name>/repro.py`, and I didn't add a ledger row or create a bundle.

The diary is doing what the spec says. The column is headed "Night of", and a night belongs to the evening it began. A 00:15 bedtime on Sunday 15 November is Saturday night's entry, which is why it shows "Sat 14 Nov".

- **Spec:** `docs/stories/S-116.md` AC1 says: "A night belongs to its 'night of' date as shown in the diary (a 00:15 bedtime on Sunday counts as Saturday night)."
- **Code:** `night_of` in `src/nightjar/models.py:43` subtracts 12 hours from the local bedtime before taking the date, and its docstring states the same rule.
- **Test:** `tests/test_diary.py:81` (`test_night_of_is_the_evening_the_night_began`) asserts that a 00:15 bedtime on 8 March 2026 gives night of 7 March.

I reran the report's case against a throwaway database. The bedtime reads "Sun 15 Nov 00:15" and the diary shows "Sat 14 Nov", which matches the spec.

The spec may not match what you expected, though. If you'd rather the diary show the calendar date of the bedtime, that's a product decision, not a code fix. Ask product to change S-116 AC1 and the "Night of" column. I haven't touched either.