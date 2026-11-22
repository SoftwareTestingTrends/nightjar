This isn't a bug, so I didn't write a repro script, a bundle or a ledger row.

The diary is working as designed. "Night of" means the evening a night began, not the calendar day you fell asleep. A 00:15 bedtime on Sunday 15 November counts as Saturday 14 November's night. I ran a 00:15 bedtime on 15 Nov 2026 through `Night.night_of` and it returned 2026-11-14, a Saturday.

The code and the docs both say this:
- **Code:** the docstring on `Night.night_of` (`src/nightjar/models.py:43`) reads "a 00:15 bedtime on Sunday is Saturday night". It works by subtracting 12 hours from the local bedtime.
- **Story S-116, AC1:** "a 00:15 bedtime on Sunday counts as Saturday night". The same rule is used for the diary's "Night of" column, the coach prompt and the weekly summary.

If the label is confusing, that's a copy question for product, not a defect. Examples are changing the column header to "Evening of" or showing the bedtime date next to it. I haven't filed that anywhere.