I couldn't reproduce this, so I didn't write a `repro.py`.

I posted quiet hours 21:00 to 00:00 to `/settings` against a throwaway database, using the same values the page's time inputs send.
- **Three runs:** each one redirected with no error, and the page showed both values saved.
- **Other values:** `23:59` and `00:00:00` are also accepted.
- **What does fail:** only `24:00` and `0:00` return 400. A time input can't produce either.
- **Code:** nothing in `web.py` or `diary.py` rejects midnight.

The team tracker already has **NJ-14**, "Quiet hours can't end at midnight", which makes the same claim. It is still Open, and it may be stale or describe a different input.

I wrote `bugs/D-1-quiet-hours-midnight/report.md` and `bugs/ledger.md`, with D-1 marked `not reproduced` and tracker `not filed`. I didn't run `make test` or the other project checks.

If you can send the exact error text, the browser you used, or a screenshot, I can try again with that. I'd also close or comment on NJ-14 once we know more. I haven't touched the tracker.