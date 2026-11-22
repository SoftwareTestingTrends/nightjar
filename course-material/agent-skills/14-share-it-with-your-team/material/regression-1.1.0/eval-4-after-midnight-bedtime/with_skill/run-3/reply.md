**Not a bug, so I haven't written a `repro.py` or a bundle.**

The diary is working as designed. A night is labelled with the evening it began, not the calendar date of the bedtime.

- **Code:** `Night.night_of` in `src/nightjar/models.py:43` subtracts 12 hours from the local bedtime before taking the date. Its docstring says: "a 00:15 bedtime on Sunday is Saturday night."
- **Spec:** Story S-116 AC1 (`docs/stories/S-116.md:15-18`) states the same rule: "a 00:15 bedtime on Sunday counts as Saturday night."

Your 00:15 bedtime on Sunday 15 November 2026 therefore shows as "Sat 14 Nov", which is the intended behaviour. I read the code and the story but didn't run it, since there was no defect to reproduce.

If the label is confusing, that is a product question, not a defect. For example, the diary could show "Sat night (bed 00:15 Sun)". I haven't added a ledger row.