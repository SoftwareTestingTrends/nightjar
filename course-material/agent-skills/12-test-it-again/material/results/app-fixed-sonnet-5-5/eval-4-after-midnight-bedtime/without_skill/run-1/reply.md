This is intended behaviour, not a bug, so I haven't written a repro script.

- **The code does this on purpose.** `Night.night_of` in `src/nightjar/models.py:43` returns the evening a night began. Its docstring says: "a 00:15 bedtime on Sunday is Saturday night."
- **A test covers it.** `test_night_of_is_the_evening_the_night_began` in `tests/test_diary.py` checks that an after-midnight bedtime lands on the previous day's date.
- **The column label fits.** The diary column is headed "Night of", so "Sat 14 Nov" reads as "the night that started on Saturday." That is how people usually talk about a night's sleep.
- **The rollover is correct.** Bedtimes before noon go to the previous date. Your 00:15 on Sunday 15 November therefore shows as Saturday 14 November.

If you'd rather see Sunday, because you want the date you fell asleep, that is a product change and not a defect fix. Options include:
- Show the actual bedtime date alongside "Night of."
- Rename the column.
- Change `night_of`, which would mean changing that test and the coach prompt text in `coach/base.py`, which also uses `night_of`.

I can do any of those if you want.