It's a real bug. Importing the same CSV twice stores every night twice.

I reproduced it against a throwaway database, not `nightjar.db`. A 2-night CSV imported twice leaves 4 rows instead of 2. `Diary.add_nights` in `src/nightjar/diary.py` inserts every row unconditionally, and the `nights` table has no uniqueness constraint, so nothing rejects a repeat. The `POST /import` route in `web.py` goes through that same code.

I didn't find a requirement that says re-importing should add duplicates. I'm treating "already-imported nights aren't added again" as the expected behaviour. Say so if the team intends something different.

The repro exited 1 on all three runs, with the output `2 distinct nights imported twice -> 4 stored (expected 2)`. It will exit 0 once re-importing leaves 2 nights. I didn't run the repo's tests or lint, since I changed no source code.

I created these files under `bugs/D-1-csv-reimport-duplicates/`:
- `repro.py`
- `report.md`

I also created `bugs/ledger.md` with a row for D-1: status `confirmed`, tracker `not filed`.

I can't file it in the tracker myself, because that changes something the team sees. To file it, run:

`/file-bug bugs/D-1-csv-reimport-duplicates`

The tracker seed data (`tools/tracker/seed.json`) already has a ticket with the same symptom, so `/file-bug`'s duplicate search will probably find it.