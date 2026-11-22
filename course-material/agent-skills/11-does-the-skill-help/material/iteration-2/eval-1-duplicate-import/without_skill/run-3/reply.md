Yes, this is a real bug. Importing the same CSV twice stores every night twice.

**Cause:** `/import` in `src/nightjar/web.py:85` calls `Diary.add_nights()`. That method (`src/nightjar/diary.py:70`) inserts each row with a plain `INSERT`. The `nights` table has no unique constraint, and nothing compares a row against existing nights. Re-uploading a file therefore doubles the data. The duplicates also skew the usual-bedtime median that the nudge and the coach rely on.

**Caveat:** No requirement or story says whether import should be idempotent. I'm treating it as a bug because nobody wants duplicate nights in a diary. If you'd rather call it a missing requirement, that's your decision.

**Repro:** `bugs/duplicate-import/repro.py` imports the same 2-night CSV twice into a throwaway database. It exits 1 if it finds anything other than 2 nights, and 0 if it finds exactly 2.

I ran it and it exits 1 with `BUG: 4 nights stored after importing the same 2-night CSV twice (expected 2)`. I haven't run it against a fixed build, so the exit-0 path is untested.

I didn't fix the bug. A fix would probably add a unique index on `(bedtime_utc, wake_time_utc, timezone)` and use `INSERT OR IGNORE`. The import message would also need to report skipped duplicates rather than all rows as imported.