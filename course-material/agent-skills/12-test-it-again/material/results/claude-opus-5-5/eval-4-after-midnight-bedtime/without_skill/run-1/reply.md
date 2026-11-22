That's not a bug. The diary is working as designed, so I haven't written a repro script.

In the diary, "Night of" means the evening the night began, not the date you got into bed. Going to bed at 00:15 on Sunday 15 November 2026 is the end of Saturday evening, so it shows as the night of Sat 14 Nov.

Where this is stated:

- **Code:** `src/nightjar/models.py:43-45`. `Night.night_of` takes your local bedtime and subtracts 12 hours before reading off the date. Its docstring uses your exact case: *"a 00:15 bedtime on Sunday is Saturday night."* Any bedtime before noon is counted as the night before.
- **Requirements:** `docs/stories/S-116.md` (AC1) says *"a 00:15 bedtime on Sunday counts as Saturday night."*
- **Tests:** `tests/test_diary.py:81` (`test_night_of_is_the_evening_the_night_began`) checks this rule, and the planned test case TC-116-8 uses your scenario: bed 00:15 on Sun 15 Nov, expected night of Sat 14 Nov.

Labelling by the evening also means a 23:45 bedtime and a 00:15 bedtime land on the same night instead of being split across two dates. If you'd rather the column show the date you went to bed, that's a change to the requirement for Product to decide, not a defect.