It isn't a bug, so I didn't write a repro script.

The diary is doing what the spec asks. A night is labelled with the evening it began, so a 00:15 bedtime on Sunday 15 November is listed as the night of Saturday 14 November.

- **Spec:** `docs/stories/S-116.md` AC1 says "a 00:15 bedtime on Sunday counts as Saturday night."
- **Code:** `Night.night_of` in `src/nightjar/models.py` subtracts 12 hours from the local bedtime and takes the date. The docstring states the same rule.
- **Test:** `tests/test_diary.py::test_night_of_is_the_evening_the_night_began` checks this exact case.
- **Run:** I built your night in `America/Toronto`. It gave bedtime `2026-11-15 00:15-05:00` and `night_of` `2026-11-14`, which is Saturday.

The label is the evening you went to bed, not the calendar day of the bedtime. If you want the diary to show Sunday, that is a change to the product rule in S-116 and the model, not a fix to a defect.