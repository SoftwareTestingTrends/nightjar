It's a real behaviour, and I logged it as **D-1, confirmed**. Whether it's a bug in the code is still a decision for product.

**What's going on:** on 8 March 2026, clocks in Toronto went from 02:00 straight to 03:00, so 02:30 never happened that night. The form accepts 02:30 without any message and treats it as standard time (−05:00). That's the same moment as 03:30 daylight time, which is what the diary shows. I got the same result 3 times in a row by submitting the real form against a throwaway database.

The maths is right: the saved time and the 6h duration agree. What's wrong is that you typed one time and the diary quietly saved another. No requirement or story says what should happen when someone enters a time that DST skipped. The triage rules count that as confirmed, with Expected set to "Not specified" and a question for product: reject the entry, save 03:30 and tell the user, or keep doing what it does now.

**Files written (in `bugs/`, which is gitignored):**
- `bugs/D-1-dst-gap-bedtime/repro.py`: I used the `D-<n>-` folder name that `docs/bug-bundles.md` requires, rather than the plain `bugs/<short-name>/` you asked for. It exits 1 while the app saves the time silently, which happened in all 3 runs: `DEFECT: entered 02:30, diary silently shows 03:30 (no warning, HTTP 200)`. It exits 0 if the app either rejects the entry or tells the user. If product decides the silent shift is fine, close the bug as working as intended instead of changing the script.
- `bugs/D-1-dst-gap-bedtime/report.md`: includes the cause, which is `local_input_to_aware` at `src/nightjar/diary.py:151`. CSV import isn't affected because it needs explicit UTC offsets.
- `bugs/ledger.md`: new, with the D-1 row.

**Leftover file:** `bugs/_scratch_probe.py` is a test script I used while reproducing. Deleting it needed your approval, so it's still there; please remove it. `/tmp/nj_probe.py` was already there before I started, and I didn't touch it.

**Next step:** to file it in the tracker, run `/file-bug bugs/D-1-dst-gap-bedtime`.