Yes, it's a bug, and I reproduced it. The script is at `bugs/spring-forward-bedtime/repro.py`. It exits 1 now and prints `BUG: typed 02:30, HTTP 303, diary silently saved 03:30`.

**What happens**
- Toronto clocks jump from 02:00 to 03:00 on 8 March 2026, so 02:30 never exists that night.
- `local_input_to_aware` (`src/nightjar/diary.py:153`) attaches the zone to whatever you typed, with no check that the time exists.
- `ZoneInfo` quietly resolves 02:30 to the instant that displays as 03:30.
- `POST /nights` accepts it and redirects with a 303. Nothing tells you the time was changed.

**Why I call it a bug**
- The nudge code does this on purpose, as the docstring on `at_local_time` in `src/nightjar/nudge.py` says. The nudge is computed, so shifting it is fine.
- A diary entry is something you typed, so it shouldn't be changed without telling you. The same normalisation, applied silently, alters your data.
- Which fix is right is a product decision. I'd reject it with a clear "that time doesn't exist on this date" message, which the 400 path through `render(..., error=...)` already supports.

**What the repro checks**
- It posts the bedtime to the real form endpoint against a throwaway database.
- It exits 0 if the entry is rejected or saved as typed. It exits 1 if it's accepted and saved as a different time. That works with whichever fix you choose.

I didn't touch the app code, and I didn't file a tracker issue. The tracker search crashed when I tried it, probably because the tracker isn't running. This isn't covered by the existing DST tests in `tests/test_nudge.py` or `tests/test_diary.py`. I didn't run `make test`, since nothing changed outside `bugs/`.

I used the path you asked for, `bugs/<short-name>/`. `docs/bug-bundles.md` expects `bugs/D-<n>-<name>/` plus a `report.md` and a ledger row. I can convert it to that layout if you want it tracked that way.