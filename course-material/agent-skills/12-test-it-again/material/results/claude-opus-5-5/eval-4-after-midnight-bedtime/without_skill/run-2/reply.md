No, it's not a bug. The diary is doing what it was designed to do, so I didn't write a repro script.

The diary's first column is headed **"Night of"** (`src/nightjar/templates/index.html:70`). It names the evening the night started, not the date you got into bed. If you go to bed after midnight, the night counts as the previous evening's. That's the usual convention in sleep diaries.

- **Code:** `Night.night_of` in `src/nightjar/models.py:43` takes your local bedtime, subtracts 12 hours and uses that date. Its docstring says: *"a 00:15 bedtime on Sunday is Saturday night."*
- **Requirements:** S-116 AC1 (`docs/stories/S-116.md:17`) says the same: *"a 00:15 bedtime on Sunday counts as Saturday night."*
- **Tests:** `tests/test_diary.py:81` (`test_night_of_is_the_evening_the_night_began`) checks this behaviour, and test case TC-116-8 expects your exact example to show as the night of Sat 14 Nov.
- **Your case:** I ran a 00:15 bedtime on Sun 15 Nov 2026 (Toronto time) through the model and got `Sat 14 Nov`, which is correct.

If people keep reading "Night of Sat 14 Nov" as the date they went to bed, that's a wording or UI issue for product to decide on. For example, the bed column could show the full date. The labelling logic itself isn't wrong.