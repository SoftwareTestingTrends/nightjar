This isn't a bug, so I haven't written a repro script.

**What I found:** `Diary.add_nights` (`src/nightjar/diary.py:70`) already skips nights it has stored. It matches on the UTC bedtime and wake time. The `/import` route in `web.py:85` goes through that method.

**What I ran:** I imported a 2-night CSV into an empty database twice.
- The first import added 2 nights.
- The second import added 0.
- The database ended up with 2 rows.

Because matching is on UTC instants, the same night written with a different UTC offset (for example `-04:00` versus `Z`) is also treated as a duplicate.

**Where duplicates could still come from:** I didn't test these cases.
- **Different times:** if the second CSV has slightly different bedtimes or wake times, such as a re-export that rounds to the minute, those rows count as new nights.
- **Manual entries:** nights logged by hand through `add_night` skip the duplicate check. A CSV containing the same night would be deduped against them, but two manual entries wouldn't be.
- **Page counter:** the `?imported=N` count only includes nights actually added, so a second import should say 0.

If you saw doubled nights, tell me what the CSV looked like and how you imported it (UI or something else). If the times differ between the two files, that would be a different issue, and I can reproduce it.