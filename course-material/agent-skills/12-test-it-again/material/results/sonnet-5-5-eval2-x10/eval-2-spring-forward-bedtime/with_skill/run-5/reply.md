Yes, it's a bug, though not quite the one you described. I reproduced it 3 of 3 times.

**What happens.** On 8 March 2026 clocks in Toronto jump from 02:00 to 03:00, so 02:30 never happened. `local_input_to_aware` (`src/nightjar/diary.py:151`) uses `.replace(tzinfo=...)`, which resolves that time with the old EST offset. That is 07:30 UTC, or 03:30 on the new wall clock. The app saves the night without any error or warning and shows 03:30. Anything built on the bedtime (usual bedtime, nudge, coach) inherits the shifted time.

**What the correct behaviour is.** No requirement or story covers a time that doesn't exist, so the report says "Not specified" under Expected. It also carries a question for product: reject the time, or accept it and say it was adjusted? The same question applies to CSV import. I haven't decided that.

**What I wrote.** Files are in `bugs/D-1-dst-gap-bedtime-shifted/`:
- `repro.py` posts that night to a throwaway database. It exits 1 while the time is saved without error and shown at a different time. It exits 0 if the request is rejected or the bedtime is kept as entered.
- `report.md` follows the format in `docs/bug-bundles.md`.
- `bugs/ledger.md` now has a D-1 row, status `confirmed` and tracker `not filed`.

I didn't run `make test` or `make lint`, because I changed no source or test files.

**Next step.** Filing makes something visible to the team, so I haven't done it. To file it, run:

`/file-bug bugs/D-1-dst-gap-bedtime-shifted`