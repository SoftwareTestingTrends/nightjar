I couldn't reproduce this, so I didn't write a `repro.py`. Importing the same CSV twice does not store the nights twice.

**What I tried:** I used a throwaway SQLite database and posted a 2-night CSV to the real `/import` endpoint twice in a row. I did this in 3 separate runs. Every time, the first import redirected to `/?imported=2` and the second to `/?imported=0`. The diary held 2 nights after both imports.

**Why:** `Diary.add_nights` (`src/nightjar/diary.py:70`) skips any night whose UTC bedtime and wake time are already stored. `POST /import` uses it (`web.py:91`). Because the comparison is on UTC instants, the same night written with a different UTC offset also counts as a duplicate.

**What I didn't check:**
- **Other add paths:** the manual "add night" form (`POST /nights`) calls `add_night` directly and has no dedup. Submitting it twice would store the night twice, but that isn't a CSV import.
- **Edited rows:** a row whose bedtime or wake time was edited between imports is a different night and gets added. That's expected.
- **Where the report came from:** the reporter may have hit one of the cases above. It's worth asking them how they imported and whether the duplicated nights had identical times.

**Files:**
- I added a `not reproduced` row (D-1) to `bugs/ledger.md`, as the triage steps require. No bundle folder was created.
- I left a scratch script at `bugs/_try.py`. It's in the gitignored `bugs/` folder. The sandbox asked for approval to delete it, so you can remove it.

I didn't run `make test` or `make lint`, because I changed no code.