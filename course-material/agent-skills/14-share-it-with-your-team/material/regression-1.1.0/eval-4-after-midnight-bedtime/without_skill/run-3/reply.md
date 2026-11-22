This isn't a bug, so I haven't written a repro script.

The diary labels each night by the evening it began, so a 00:15 bedtime on Sunday 15 November is "Saturday night, 14 November". That is deliberate:

- **Code:** `Night.night_of` in `src/nightjar/models.py:43-45` has the docstring "a 00:15 bedtime on Sunday is Saturday night". It shifts the local bedtime back 12 hours before taking the date.
- **Tests:** `test_night_of_is_the_evening_the_night_began` in `tests/test_diary.py` asserts this behaviour.
- **Spec:** Story S-116 AC1 says "a 00:15 bedtime on Sunday counts as Saturday night".

I also ran your exact case: 00:15 on 15 Nov 2026 in America/Toronto gives `night_of` = 2026-11-14, a Saturday.

If the diary page shows only "Sat 14 Nov" with no sign that it's the night starting that evening, that is a wording problem rather than a logic bug. For example, "Night of Sat 14 Nov" would be clearer, or the page could show the actual bedtime date next to it. If you'd like it changed to the calendar date of the bedtime, that is a requirements change. It would affect S-116 and S-117 and the existing test, so it needs a decision from you, not a bug fix.