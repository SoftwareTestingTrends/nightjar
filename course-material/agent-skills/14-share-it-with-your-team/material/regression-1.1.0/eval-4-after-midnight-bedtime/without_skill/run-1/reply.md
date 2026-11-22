This isn't a bug, so I haven't written a repro script.

The diary labels each night by the evening it began, so a 00:15 bedtime on Sunday 15 Nov shows as the night of Saturday 14 Nov. That's deliberate:

- `src/nightjar/models.py:43`: `Night.night_of` is documented as "a 00:15 bedtime on Sunday is Saturday night."
- `tests/test_diary.py:81`: `test_night_of_is_the_evening_the_night_began` asserts this behaviour.
- `docs/stories/S-116.md`: a night belongs to its "night of" date as shown in the diary, and the 00:15 bedtime is the example.
- The QA test case TC-116-8 expects the same result for your exact scenario: the 00:15 bedtime on Sun 15 Nov is "the night of Sat 14 Nov".

If you'd rather see the calendar date of the bedtime, that's a product decision. It would change S-116, S-117 and the coach prompt, which reads `night_of` in `coach/base.py`. A smaller option is to relabel the column or show the bedtime date next to it.

I only read the code and didn't run the tests.