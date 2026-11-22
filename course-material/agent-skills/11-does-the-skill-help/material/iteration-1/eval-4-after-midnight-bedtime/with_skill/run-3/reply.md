This isn't a bug, so I didn't write a repro script, a bundle or a ledger row.

- **What happens:** I logged a bed time of 00:15 on Sunday 15 Nov 2026 (America/Toronto). `Night.night_of` returns Saturday 14 Nov, so the diary shows Sat 14 Nov. That is what you saw.
- **It's by design:** the code comment at `src/nightjar/models.py:44` says "a 00:15 bedtime on Sunday is Saturday night". `docs/stories/S-116.md` AC1 says the same: "a 00:15 bedtime on Sunday counts as Saturday night". The diary column is headed "Night of", so it names the evening the night began, not the calendar date you fell asleep.
- **Possible wording problem:** the column header and the stored date are consistent, but "Sat 14 Nov" next to a bed time of 00:15 can read as a mistake. If you want that to change, it's a UX or copy request. It would need a change to S-116 and `night_of`, not a bug fix.

I can draft that as a change request if you want one.