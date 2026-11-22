It's a real bug. Importing the same CSV twice stores every night a second time, and the repro confirms it.

**Cause:** `POST /import` calls `parse_csv` and then `Diary.add_nights`, which runs a plain `INSERT` for every row. The `nights` table has no unique constraint and nothing checks for an existing night first. The app's manual "log a night" form has the same gap, so a double-submit creates duplicates too.

**Why it matters:** the sleep window uses the last 14 nights, and the nudge needs 7 nights. A 4-night CSV imported twice gives 8 rows, so the nudge can switch on with only 4 real nights. The diary list also shows each night twice.

**Caveat:** the docs don't state that re-importing must be idempotent. S-117 AC6 covers only importing into an empty diary. I treated duplicates as a defect because two nights with the same bedtime and wake time can't both be real. If you'd rather decide that differently, tell me and I'll change the conclusion.

**Repro:** `bugs/csv-import-duplicates/repro.py`, using a throwaway SQLite database. It exits 1 while the bug is present and 0 once it's fixed. Current output:

```
BUG: first import stored 2 nights, second import brought the total to 4
```

Exit code: 1. The script passes `ruff check` and `ruff format --check`. I didn't change any app code or tests.

`bugs/` is gitignored, so the script won't be committed. The bug-bundle contract also expects a `report.md` and a row in `bugs/ledger.md`, which I haven't written. I can add them if you want this tracked for `verify-fix`.