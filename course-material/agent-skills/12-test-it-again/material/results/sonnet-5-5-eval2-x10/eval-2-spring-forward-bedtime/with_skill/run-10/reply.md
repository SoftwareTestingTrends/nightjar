Yes, it's a bug, though what the app should do instead isn't specified. I confirmed it and wrote a repro that exits 1 now and should exit 0 once it's fixed.

**What happens:** Toronto clocks jump from 02:00 straight to 03:00 on 8 March 2026, so 02:30 never existed that night. The app accepts it anyway and shows 03:30, with no warning. The cause is `local_input_to_aware` in `src/nightjar/diary.py`, which uses `.replace(tzinfo=…)` and never checks that the time exists.

**Expected behaviour:** no requirement or story says what should happen to a time that was skipped. S-114 only asks for the nudge to be correct across DST. I wrote "Not specified" in the report and left a question for product. The options I listed are to reject it with a clear message, or to accept it and say it was moved to 03:30. Either is better than silently changing what the user typed.

**Repro:** it posts the night through `/nights` against a throwaway database. It exits 0 if the app rejects the time (HTTP 400) or shows 02:30. It ran 3 times and exited 1 each time, printing `BUG: entered 02:30, status 303, diary shows 03:30`. If product picks "accept and tell the user it moved to 03:30", the pass condition in `repro.py` will need updating to match.

**Files**, all under `bugs/` (which is gitignored):
- `bugs/D-1-spring-forward-bedtime-shifted/repro.py`
- `bugs/D-1-spring-forward-bedtime-shifted/report.md`
- `bugs/ledger.md`, with a new row for D-1 (confirmed, not filed)

Filing it in the tracker changes something the team sees, so I haven't done it. To file it, run:

`/file-bug bugs/D-1-spring-forward-bedtime-shifted`