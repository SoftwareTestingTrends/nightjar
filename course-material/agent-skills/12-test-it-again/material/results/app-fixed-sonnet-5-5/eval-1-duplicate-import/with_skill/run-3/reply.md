I couldn't reproduce this, so I didn't write a `repro.py`.

**What I tried:** I posted the same two-night CSV to `/import` twice through the real app, against a throwaway database. I did that 3 times, each with a fresh database. Every time the first import stored 2 nights (`?imported=2`). The second stored 0 (`?imported=0`), and the diary held 2 nights at the end.

**Why it holds:** `Diary.add_nights` (`src/nightjar/diary.py:70`) skips any night whose UTC bedtime and wake time already exist in the diary. It also tracks keys within a single file, so duplicate rows inside one CSV are skipped too.

**Where the report might come from:** I only tested files that are identical row for row. A night that looks like a duplicate in the diary may differ by a minute or two in bedtime or wake time, for example if the file was edited or re-exported. That would be stored as a new night. Whether near-matches should count as duplicates isn't specified anywhere. I haven't tested this, and it would be a product question rather than a bug.

If you can share the CSV, or a screenshot of the doubled rows, I'll try it exactly.

I added a `not reproduced` row (D-1) to `bugs/ledger.md`. Nothing was filed in the tracker.