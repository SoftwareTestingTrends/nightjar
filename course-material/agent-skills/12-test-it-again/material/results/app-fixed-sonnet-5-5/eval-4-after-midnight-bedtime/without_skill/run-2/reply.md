This isn't a bug, so I haven't written a repro script.

The diary labels a night by the evening it began, and that's deliberate. `Night.night_of` (`src/nightjar/models.py:43`) subtracts 12 hours from the local bedtime and takes the date. A 00:15 bedtime on Sunday 15 November becomes 12:15 on Saturday 14 November, so it's listed as "Saturday night". The docstring gives this exact case: "a 00:15 bedtime on Sunday is Saturday night". `docs/stories/S-116.md:18` states the same rule ("on Sunday counts as Saturday night"). `test_night_of_is_the_evening_the_night_began` in `tests/test_diary.py` checks it.

This matches how people usually talk about sleep, since you slept on Saturday night. It also keeps a night together when the bedtime varies. 23:30 on Saturday and 00:30 on Sunday both land on Saturday, so they don't split across two dates.

If you'd rather the diary show the calendar date of the bedtime, that would be a change to the requirement. It would need S-116, the `night_of` docstring and the test updated, and I'd treat it as a feature request rather than a defect.