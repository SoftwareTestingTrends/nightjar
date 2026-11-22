This isn't a bug, so I didn't write a `repro.py`.

**What I checked:** I posted `data/sample_nights.csv` to the real `/import` endpoint twice, using a fresh database each time I ran it.
- First import: `/?imported=21`, with 21 nights stored.
- Second import: `/?imported=0`, still 21 nights stored.

**Why it holds:** `Diary.add_nights` (`src/nightjar/diary.py:70`) compares each row's UTC bedtime and wake time against what's already stored. It skips any night that matches.

**Where you might still see duplicates:**
- **Different times:** A night whose bedtime or wake time differs, even by a minute, counts as a new night. A re-exported CSV with edited times would add a second row for that night.
- **Manual entry:** `add_night` (the log-a-night form) has no duplicate check. That is probably intended.
- **Unfixed rows:** Nights with the same bedtime and wake time but a different timezone or notes are treated as duplicates. The first one stored wins, and I'd expect that.

If you saw doubled nights, tell me what the CSV looked like or how you imported it, and I'll look at that case.

My throwaway probe is still at `bugs/scratch/probe.py`. I couldn't delete it because the `rm` needed your approval. It's safe to remove with `rm -r bugs`, since `bugs/` didn't exist before.