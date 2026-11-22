This isn't a bug. "Night of Saturday 14 November" is the label NightJar is designed to show, so I didn't write a repro script, a bundle or a ledger row.

**What happens:** I logged your night against a throwaway database: bed at 2026-11-15 00:15 in America/Toronto, up at 07:30. The diary stores the bedtime correctly as `2026-11-15 00:15-05:00` and labels the night `2026-11-14 (Saturday)`. So the label you saw is the real behaviour, not a display slip.

**Why that's intended:** the "Night of" column names the evening the night started, not the date you got into bed. Three places say so:
- `src/nightjar/models.py`, the `Night.night_of` docstring: *"The evening this night began: a 00:15 bedtime on Sunday is Saturday night."* It's calculated as the local bedtime minus 12 hours, so any bedtime between midnight and noon belongs to the evening before.
- `docs/stories/S-116.md` AC1 depends on this rule: *"A night belongs to its 'night of' date as shown in the diary (a 00:15 bedtime on Sunday counts as Saturday night)."* That's almost exactly your example.
- `tests/test_diary.py::test_night_of_is_the_evening_the_night_began` checks that a 00:15 bedtime on Sunday 8 March is labelled 7 March.

If people find "Night of Saturday" confusing for an after-midnight bedtime, that's a question for product about wording or design. One option is to show the date you actually went to bed next to the label. Changing the rule itself would also affect S-116's weekly summary window and S-117's ordering, so it shouldn't be done as a bug fix.