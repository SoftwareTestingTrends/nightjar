The report is right: importing the same CSV twice stores every night twice. I logged it as **D-1, confirmed**. One caveat: no requirement or story says what re-importing should do, so whether it's a bug in the strict sense is product's call.

**What I saw:** in an empty throwaway database, I sent a 2-night CSV to `/import` twice and the diary ended up with 4 nights. This happened in 3 of 3 runs. The import inserts every row with a plain `INSERT` (`Diary.add_nights` → `add_night` in `src/nightjar/diary.py`), and the `nights` table has nothing to stop duplicate rows. The page says "Imported 2 nights." both times.

**What should happen:** I wrote "Not specified" under Expected, because the stories only cover importing into an *empty* diary (S-117 AC6). The question for product is whether a matching row should be skipped, updated or kept, and whether the "Imported N" count should include rows that were skipped.

**Why it matters:** the usual bedtime is the median of the last 14 nights. With duplicates, those 14 rows cover only 7 real nights. Importing `data/sample_nights.csv` twice left the nudge at 22:15, so the sample data shows no visible change, but other diaries could.

**Files** (in `bugs/`, which git ignores):
- `bugs/D-1-reimport-duplicates/repro.py`: exits 1 while duplicates are stored (it prints `BUG: … diary holds 4 nights (expected 2)`) and 0 once importing twice leaves 2 nights. That pass condition assumes the fix is "don't duplicate". If product picks a different behaviour, update the script.
- `bugs/D-1-reimport-duplicates/report.md`
- `bugs/ledger.md`: new row D-1, `confirmed`, `not filed`.

The folder is `D-1-reimport-duplicates` rather than `bugs/<short-name>/` as you asked, because `docs/bug-bundles.md` requires the `D-<n>-` prefix. I didn't change any app code, so I didn't run `make test` or `make lint`.

**Next step:** filing a ticket changes what the team sees, so I didn't do it. To file it, run:

```
/file-bug bugs/D-1-reimport-duplicates
```