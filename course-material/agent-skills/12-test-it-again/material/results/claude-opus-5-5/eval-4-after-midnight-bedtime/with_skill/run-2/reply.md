This isn't a bug. The diary is working as designed, so I didn't write a repro script or a bug bundle.

**What happens:** A night that starts at 00:15 on Sunday 15 Nov 2026 shows as "Night of Sat 14 Nov". I checked this directly against `Night.night_of`, with nothing written to the real database.

**Why that's intended:** "Night of" means the evening the night began, not the date on the clock when you got into bed. The spec says so explicitly:

- **Story S-116, AC1** (`docs/stories/S-116.md:17`): "a 00:15 bedtime on Sunday counts as Saturday night."
- **The code** (`src/nightjar/models.py:43-46`) works out the date by taking the local bedtime minus 12 hours, and its comment uses the same example: "a 00:15 bedtime on Sunday is Saturday night."

So any bedtime between noon Saturday and 11:59 Sunday morning counts as Saturday night. That keeps 23:30 and 00:30 bedtimes under the same night instead of splitting them across two dates. The weekly summary and the sorting (S-116, S-117) both depend on this.

If you think the label is confusing for users, that's a question about the wording or design for product (Priya N. owns S-116), not a defect. For example, the column could read "Sat 14 → Sun 15 Nov". I haven't added anything to the ledger, since it only tracks real or suspected defects.