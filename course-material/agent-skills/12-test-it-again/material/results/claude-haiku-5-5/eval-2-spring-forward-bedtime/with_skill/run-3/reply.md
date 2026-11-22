**Yes, it reproduces, and I've logged it as D-1. Whether it's a defect depends on a product decision that no spec makes.**

- **What happens:** 8 March 2026 in Toronto skips 02:00–03:00, so 02:30 never happens. The form turns 02:30 into 07:30 UTC, which the diary shows as 03:30 EDT. The save succeeds with no warning.
- **Why I didn't call it a clear bug:** no requirement or story says what a non-existent time should do. The 02:30 → 03:30 mapping also matches the convention in `nudge.py`, which documents that skipped times normalise to 03:30. That convention was written for computed nudge times, though, not for user input.
- **Why I logged it anyway:** the app silently changes data the user typed, and the skill's rule is that reproduced-but-unspecified behaviour is still `confirmed`, with "Not specified" under Expected.

**Files written**
- `bugs/D-1-spring-forward-bedtime/repro.py`: exits 1 while the bug is present. It exits 0 if the input is rejected or the diary shows 02:30. It ran 3 of 3 with exit 1.
- `bugs/D-1-spring-forward-bedtime/report.md`: status `confirmed`, tracker `not filed`.
- `bugs/ledger.md`: created, with one row for D-1.

I used the `D-<n>-<short-name>` folder layout from `docs/bug-bundles.md`, not the `bugs/<short-name>/` path in your request. The repro uses a throwaway database, and nothing was committed.

**Question for product:** should a bedtime in the spring-forward gap be rejected with a message, or accepted and shown as the normalised time? The repro accepts either outcome as fixed, so it doesn't pick one.

To file it, run `/file-bug bugs/D-1-spring-forward-bedtime`.