**Not a bug.** I didn't write a repro and didn't add a bundle or ledger row.

- **What happens:** A night with a 00:15 bedtime on Sunday 15 Nov 2026 shows as "Sat 14 Nov". I confirmed this by building that night and checking `night_of`.
- **Why it's intended:** `Night.night_of` in `src/nightjar/models.py:43` documents it: "a 00:15 bedtime on Sunday is Saturday night." The diary labels a night by the evening it began. Story S-116 AC1 says the same thing: "a 00:15 bedtime on Sunday counts as Saturday night."
- **Where the label comes from:** The diary row in `index.html:75` prints `night_of`, so the row reads "Sat 14 Nov" next to a 00:15 bed time.

If the label confuses people, you could ask product whether the column should be renamed ("Night of") or show the actual bedtime date. That's a copy or design question, not a defect, so I haven't raised a ticket.