This isn't a bug, so I didn't write a repro script, bundle or ledger row.

The diary column is headed "Night of" (`src/nightjar/templates/index.html:70`). It shows the evening a night began, not the calendar date of the bedtime. `Night.night_of` in `src/nightjar/models.py` does this on purpose: it subtracts 12 hours from the local bedtime. Its docstring reads "a 00:15 bedtime on Sunday is Saturday night."

Story S-116 AC1 says the same thing: "a 00:15 bedtime on Sunday counts as Saturday night". Your 00:15 on Sunday 15 November 2026 is therefore correctly listed as Sat 14 Nov. I didn't run the app, since the code and spec answer the question.

If the label confuses people, that's a product and copy question. One option would be showing the bedtime date alongside, or renaming the column. I can raise that with product if you want, but it isn't a defect.