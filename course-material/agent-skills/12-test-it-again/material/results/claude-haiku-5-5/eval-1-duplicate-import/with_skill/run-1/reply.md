It's a real bug, reproduced 3 of 3. Importing the same CSV twice stores every night twice: the sample file goes from 21 rows to 42, and each import reports success. The import path inserts every parsed row with no duplicate check (`src/nightjar/diary.py`, `add_nights`).

No requirement or story says what a repeat import should do. The S-117 import criterion only covers importing into an empty diary, so I've marked the bug `confirmed` with Expected set to "Not specified", as the skill directs. Product needs to decide the behaviour, so the repro assumes one copy should remain.

Bundle written to `bugs/D-1-csv-reimport-duplicates/`:
- `repro.py`: imports a one-night CSV twice into a temporary database and exits 1 while two copies are stored. Ran it 3 times, exit 1 each time. I did not run the exit-0 path, since there's no fix yet.
- `report.md`: steps, actual behaviour, the product questions, and an unverified note that duplicates may skew the usual bedtime, which uses the median of the last 14 nights.
- `bugs/ledger.md`: created with the D-1 row (`confirmed`, `not filed`).

I used the `bugs/D-<n>-<short-name>/` folder from `docs/bug-bundles.md` rather than the `bugs/<short-name>/` path in your request, since the contract says to follow that format exactly.

Questions for product before a fix:
- For a night already in the diary, should the import skip it, replace the stored copy, or reject the file?
- What counts as the same night: same bedtime instant, or bedtime plus timezone?
- Should the "Imported N nights" message count only nights actually added?

To hand off to the team, run `/file-bug bugs/D-1-csv-reimport-duplicates`.