Yes, it's a real bug. Importing the same CSV twice stores every night twice.

**Cause:** `Diary.add_nights` in `src/nightjar/diary.py` adds a new row for every night in the file. Nothing checks whether that night is already in the diary, and the `nights` table has no rule against duplicates. No requirement says importing twice should be safe, but there's no reason anyone would want duplicate nights.

**Why it matters for the nudge:** the usual bedtime is worked out from the last 14 rows and needs at least 7. With duplicates, those 14 rows are really only 7 different nights. And 4 nights imported twice count as 8, so a nudge appears before the user has the 7 nights that S-114's minimum requires.

**Repro:** `bugs/D-1-csv-reimport-duplicates/repro.py` imports a two-night CSV twice into a temporary, empty diary, the same way `POST /import` does. It exits 1 if the diary holds anything other than 2 nights. I ran it once:

```
BUG: imported the same 2-night CSV twice, diary holds 4 nights   (exit 1)
```

I used the `D-1-…` folder name and also added a `report.md` and a `bugs/ledger.md` row, because `docs/bug-bundles.md` requires those for the `verify-fix` skill to recheck the bug later. The bug isn't filed in the tracker yet.

I haven't fixed it. The likely fix is to treat a night as a duplicate when it has the same bedtime (stored in UTC) and the same wake time, either with a uniqueness rule in the database or a check when importing. Someone needs to decide whether re-importing a night with different notes should skip it or update it.