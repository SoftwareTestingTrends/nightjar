This isn't a bug, so I didn't write a repro script, a bundle or a ledger row.

**What I did:** I built a night with bedtime 00:15 on Sunday 15 Nov 2026 and read `night_of`. It returns `Sat 14 Nov`, which matches what you saw.

**Why it's by design:**
- The diary's "night of" date is the evening the night began. The docstring on `Night.night_of` (`src/nightjar/models.py:44`) says so: "a 00:15 bedtime on Sunday is Saturday night". The code subtracts 12 hours from the local bedtime before taking the date.
- Story S-116 AC1 says the same thing: "a 00:15 bedtime on Sunday counts as Saturday night".
- The coach prompt and the diary page use the same `night_of` value, so they agree with each other.

**If you'd still like Sunday:** the diary column could also show the actual bedtime date, for example "Sat 14 Nov (bed 00:15 Sun)". That would be a product change, not a defect fix. It would also touch S-116 AC1, which relies on the current convention. If you want it, raise it with product as a feature request.