This isn't a bug, so I didn't write a repro script or add a ledger row.

**What I saw:** I logged a bedtime of 00:15 on Sunday 15 Nov 2026 in America/Toronto. The diary shows it as "Night of Sat 14 Nov". That matches your report.

**Why it's intended:**
- The column is labelled "Night of" (`src/nightjar/templates/index.html:70`). It shows the evening the night began, not the calendar date of the bedtime.
- `Night.night_of` says so in its docstring: "a 00:15 bedtime on Sunday is Saturday night" (`src/nightjar/models.py:42-45`). It subtracts 12 hours from the local bedtime before taking the date.
- Story S-116 AC1 states the same rule: "a 00:15 bedtime on Sunday counts as Saturday night".

So the diary is doing what the spec says. A 00:15 bedtime is the tail end of Saturday night. It also means a 23:30 bedtime on Saturday and a 00:30 bedtime on Sunday both show as Saturday's night.

If you'd still prefer the label to show the bedtime's own date, or to make it clearer (for example "Night of Sat 14 Nov (bed Sun 00:15)"), that's a product change. I'd raise it with product, not file it as a defect.