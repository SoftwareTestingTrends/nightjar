This isn't a bug as reported. I couldn't reproduce it, so I didn't write a `repro.py`.

**What I tried:** I imported the same two-night CSV twice through `POST /import`, using a throwaway SQLite database each time. I ran it three times with three variants:
- the identical file
- the same file with CRLF line endings
- the same nights written as UTC (`Z`) instead of `-04:00` offsets

**What happened:** the first import returned `/?imported=2` and the second returned `/?imported=0`. Each run stored 2 nights, not 4.

**Why:** `Diary.add_nights` (`src/nightjar/diary.py:70`) skips any night whose bedtime and wake time (normalised to UTC) are already stored. That is why the offset variant is also deduplicated.

**What could still look like duplicates:**
- **Different times:** the same night re-exported with different times, such as a changed bedtime or wake time, counts as a new night because the match is exact.
- **Other entry paths:** nights added through the "log a night" form (`add_night`) aren't deduplicated, so logging one by hand and then importing it would store it twice.
- **A different database:** the app's `nightjar.db` may hold rows from before the dedup existed. I didn't touch it.

If you have the CSV and the steps that showed double rows, send them and I'll retry. A same-night match with different times would be a product question.

I added row D-1 to `bugs/ledger.md` with status `not reproduced`. There is no bundle folder and nothing to file.