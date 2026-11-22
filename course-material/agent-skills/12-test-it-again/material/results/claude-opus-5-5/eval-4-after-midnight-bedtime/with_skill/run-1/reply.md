This isn't a bug. The diary is doing what the spec says, so I didn't write a repro script, a bundle or a ledger row.

**What happens:** I logged a night with a 00:15 bedtime on Sunday 15 November 2026 (America/Toronto). The diary shows it as **Sat 14 Nov 2026**, which matches your report.

**Why that's intended:** the "Night of" column shows the evening the night began, not the date you actually went to bed. A bedtime just after midnight still counts as the night before.
- **Story S-116, AC1** (`docs/stories/S-116.md:17`) says it outright: "A night belongs to its 'night of' date as shown in the diary (a 00:15 bedtime on Sunday counts as Saturday night)." Your report is that exact example.
- **The code** (`src/nightjar/models.py:43`): `night_of` subtracts 12 hours from your local bedtime and takes the date. Any bedtime before noon therefore counts toward the previous evening. Its docstring uses the same 00:15 example.
- **A test covers it:** `test_night_of_is_the_evening_the_night_began` (`tests/test_diary.py:81`).
- **Other features rely on it:** the weekly summary (S-116) and the night ordering in S-117 both group nights by this date.

If you'd rather the diary show the actual bedtime date, that's a change to the requirement, not a defect, so it would go to product. A cheaper option might be to show both dates in the column (e.g. "Sat 14 Nov (bed Sun 00:15)").