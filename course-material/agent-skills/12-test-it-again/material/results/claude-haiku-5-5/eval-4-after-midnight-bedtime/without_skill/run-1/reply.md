It isn't a bug, so I didn't write a repro script.

A "night of" label is the evening the night began, not the calendar day the bedtime falls on. A 00:15 bedtime on Sunday 15 November is Saturday night, and the diary shows it as Saturday 14 November.

- **Spec:** `docs/stories/S-116.md` AC1 says "a 00:15 bedtime on Sunday counts as Saturday night."
- **Code:** `Night.night_of` in `src/nightjar/models.py` subtracts 12 hours from the local bedtime before taking the date.
- **Test:** `tests/test_diary.py::test_night_of_is_the_evening_the_night_began` covers this case and passes.
- **Direct check:** I built your night (00:15 on 15 Nov 2026, America/Toronto) and it gives `night_of` = 2026-11-14.

The noon cutoff is also why the usual-bedtime maths treats 23:30 and 00:30 as one hour apart.

If you want the diary to show the calendar date of the bedtime instead, that is a change to the spec, not a fix. I'd leave it as is unless the team decides otherwise.