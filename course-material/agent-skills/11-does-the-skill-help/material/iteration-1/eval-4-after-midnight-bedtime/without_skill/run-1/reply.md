This isn't a bug, so I didn't write a repro script.

The diary labels each night by the evening it began, and that's deliberate. A 00:15 bedtime on Sunday 15 November is "the night of Saturday 14 November", the same way you'd say "Saturday night" for a late one.

- **Code:** `Night.night_of` in `src/nightjar/models.py:43` subtracts 12 hours from the local bedtime and takes the date. Its docstring says "a 00:15 bedtime on Sunday is Saturday night."
- **Tests:** `tests/test_diary.py:81` (`test_night_of_is_the_evening_the_night_began`) asserts this behaviour. The test builder in `tests/builders.py` also rolls after-midnight bedtimes over to the next calendar day.
- **Docs:** `docs/stories/S-116.md` describes the same "night of" convention, including the 00:15 case. `S-117` AC4 orders nights by it.

If you'd rather the diary showed the calendar date of falling asleep, that's a product change to the convention in S-116 and S-117. It would also affect the coach prompt, since `coach/base.py` uses the same property. It wouldn't fix a defect. I can raise it as a change request if you want one.