Yes, it's a bug, and I reproduced it 3 of 3 times. I haven't run `make lint` or `make test`, because I changed no source or test files, and I haven't linted `repro.py`.

**What happens:** 8 March 2026 is the spring-forward day in Toronto, when clocks jump from 02:00 to 03:00. So 02:30 doesn't exist that day.

The form accepts it anyway. `local_input_to_aware` in `src/nightjar/diary.py` just attaches the zone to the typed time. Python treats the missing 02:30 as 02:30 EST, which is 07:30 UTC, and that displays as 03:30 EDT. The diary never tells you it changed the time, and the night comes out an hour shorter than you think.

**Expected behaviour is not specified.** No requirement or story says what to do with a time that doesn't exist. I recorded that under Expected and put a question to product: reject it with a message, or move it to 03:30 and say so?

The repro assumes the app must not silently change what you typed. It exits 0 if 02:30 is rejected or shown as typed. If product chooses "move to 03:30 and tell the user", the repro needs adjusting.

**Files** (the `bugs/` folder is gitignored, so none of this is committed):
- `bugs/D-1-dst-gap-bedtime-shifted/repro.py` posts to the real `/nights` form against a throwaway database. It exits 1 and prints the 03:30 it saw.
- `bugs/D-1-dst-gap-bedtime-shifted/report.md`
- `bugs/ledger.md` has the new row: D-1, `confirmed`, tracker `not filed`.

**Next step:** filing changes something the team sees, so I haven't done it. To file it, run:

`/file-bug bugs/D-1-dst-gap-bedtime-shifted`