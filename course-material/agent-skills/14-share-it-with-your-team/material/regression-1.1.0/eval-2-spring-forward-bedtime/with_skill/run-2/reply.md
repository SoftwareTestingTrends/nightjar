Yes, it's a bug, confirmed 3 of 3 runs. Nothing in the requirements says what should happen, so the expected behavior is "Not specified" and I've left a question for product.

**What happens:** On 8 March 2026 clocks in Toronto jump from 02:00 to 03:00, so 02:30 never exists that night. `local_input_to_aware` (`src/nightjar/diary.py:153`) just attaches the zone to the typed time. The result is read as 02:30 EST, which is 07:30 UTC. After it's saved and read back, that shows as 03:30 EDT. The app accepts the entry and says nothing about the change. The same thing happens to wake times.

**Open question for product:** Should the app reject the input with a message, move it to the nearest valid time and tell the user, or do something else?

**Files** (the repro is in `bugs/D-1-dst-gap-bedtime/` rather than `bugs/<short-name>/`, because `docs/bug-bundles.md` requires the `D-<n>-` prefix):
- `bugs/D-1-dst-gap-bedtime/repro.py` uses a throwaway database. It exits 1 while the diary silently shows a different time than you entered. It exits 0 once the input is rejected with an error or shown as entered. Run it with `uv run python bugs/D-1-dst-gap-bedtime/repro.py`.
- `bugs/D-1-dst-gap-bedtime/report.md`
- `bugs/ledger.md` has a new row for D-1 (confirmed, tracker not filed).

I didn't run `make test` or `make lint`, since I changed no source or tests.

**Next step:** Filing changes something the team sees, so I haven't done it. To file it, run `/nightjar-qa:file-bug bugs/D-1-dst-gap-bedtime`.