Yes, it's a real bug. Importing the same CSV twice stores every night twice.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py:70` calls `add_night` for each row, which does a plain `INSERT`. The `nights` table (lines 23–29) has no uniqueness constraint, and the `/import` handler in `web.py` doesn't check for existing rows either. Nothing in the docs says duplicates are intended.

**Impact:** The usual-bedtime median uses the last 14 nights with a minimum of 7. Doubled rows therefore skew it and can get a user past the 7-night minimum on half the real data.

**Repro:** `bugs/duplicate-csv-import/repro.py` imports a 2-night CSV twice into a throwaway database. It exits 1 while the bug is present and 0 once it's fixed. I ran it and got exit 1 with `BUG: 4 nights stored after importing the same 2-night CSV twice (expected 2)`. I haven't seen it pass, because I haven't fixed anything.

**Not done:**
- **Tracker:** I didn't file it. The tracker at `127.0.0.1:8765` wasn't running.
- **Fix:** I didn't make one. A reasonable one is a `UNIQUE(bedtime_utc, wake_time_utc, timezone)` constraint with `INSERT OR IGNORE`. `add_nights` would then count only the rows actually inserted, so the "imported N" message stays accurate.
- **Path:** You asked for `bugs/<short-name>/`, so the folder doesn't follow the `D-<n>-<short-name>` naming in `docs/bug-bundles.md`. There's also no `report.md` or ledger entry.