Not a bug. The diary is doing what it was designed to do, so I haven't written a repro script.

The "Night of" column shows the evening the night started, not the calendar date you got into bed. Going to bed at 00:15 on Sunday 15 November means the night started on Saturday evening, so it's listed as the night of Saturday 14 November.

The code and docs all say this on purpose:

- **The code:** `src/nightjar/models.py:42-45`. The comment on `Night.night_of` reads *"a 00:15 bedtime on Sunday is Saturday night"*. It works this out by taking 12 hours off the local bedtime, so any bedtime between midnight and noon counts toward the day before.
- **The spec:** `docs/stories/S-116.md` AC1 says *"A night belongs to its 'night of' date as shown in the diary (a 00:15 bedtime on Sunday counts as Saturday night)."*
- **Tests:** `tests/test_diary.py:81` (`test_night_of_is_the_evening_the_night_began`) checks this behaviour, and test case TC-116-8 uses your exact example: bed at 00:15 on Sun 15 Nov counts as the night of Sat 14 Nov.

There's also a practical reason. If nights were filed by bedtime date, someone who sometimes goes to bed at 23:50 and sometimes at 00:10 would see their nights jump between dates, and some dates would get two nights while others got none.

If the label itself is confusing, that's a fair point about the wording rather than a bug. The column header could say something like "Night of (evening)", or there could be a tooltip. I can raise that as a UX suggestion if you'd like.