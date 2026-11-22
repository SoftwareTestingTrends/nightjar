This isn't a bug, so I didn't write a bundle or a `repro.py`.

The diary is behaving as specified. A 00:15 bedtime on Sunday 15 November 2026 (Toronto time) is labelled "Sat 14 Nov". I reproduced that directly with the app's own `Night` model:

```
Sun 15 Nov 00:15 -> night_of Sat 14 Nov
```

The rule is intentional and documented in three places:

- `src/nightjar/models.py:44`: "a 00:15 bedtime on Sunday is Saturday night."
- `docs/stories/S-116.md`, AC1: "A night belongs to its 'night of' date as shown in the diary (a 00:15 bedtime on Sunday counts as Saturday night)."
- `tests/test_diary.py::test_night_of_is_the_evening_the_night_began` asserts the same thing.

The label is the evening the night began, so a night that starts at 23:00 Saturday and ends after midnight stays under Saturday. The 00:15 time is the same night, just after midnight. Your bedtime is correct. The "Night of" column is showing the evening the night started, not the calendar day of the bedtime.

If you think the diary should show the calendar day of the bedtime instead, that changes the rule in S-116 and `night_of`. That's a product decision, so I've left it alone. I haven't written anything into `bugs/` and haven't changed any code. `bugs/ledger.md` doesn't exist yet, so nothing there needs updating either.