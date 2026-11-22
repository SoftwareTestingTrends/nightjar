Yes, it's a real bug. Importing the same CSV twice stores every night twice. I wrote `bugs/csv-reimport-duplicates/repro.py`.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py` calls `add_night` for each row. `add_night` is a plain `INSERT`. The `nights` table has only an auto-increment `id` and no unique constraint, so nothing recognises a repeated night. The `/import` route in `web.py` just passes the parsed rows straight through.

**Why it matters:** duplicated nights skew the median bedtime in `sleep_window.py`, which feeds the nudge and the coach. I found no requirement that says duplicates are allowed. Docs only say that importing an exported file into an empty diary gives the same nights (S-117 AC6).

**Repro:** it imports a 2-night CSV twice into a throwaway database. It exits 1 and prints `BUG: expected 2 nights after importing a 2-night CSV twice, found 4`. It will exit 0 once re-importing no longer duplicates nights. I ran it, and it exited 1 as expected.

- **Not filed:** the local tracker wasn't running, so I couldn't check for an existing issue. I haven't filed one.
- **No fix:** I haven't changed any code. A fix could be a unique index on `(bedtime_utc, wake_time_utc, timezone)` with `INSERT OR IGNORE`. The return value would then need to report how many nights were actually added.
- **Bundle layout:** you asked for `bugs/<short-name>/`, so I used that. `docs/bug-bundles.md` expects `bugs/D-<n>-<short-name>/` plus `report.md` and a ledger row. I didn't create those.