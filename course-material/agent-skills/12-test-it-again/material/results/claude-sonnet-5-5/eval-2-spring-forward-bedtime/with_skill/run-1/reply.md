Yes, it's a bug. I reproduced it 3 of 3 times.

**Cause:** 8 March 2026 is Toronto's spring-forward day, when clocks jump from 02:00 to 03:00. A bedtime of 02:30 doesn't exist that night. `local_input_to_aware` in `src/nightjar/diary.py` attaches the zone to whatever was typed. The nonexistent time resolves to 07:30 UTC, which displays as 03:30. The user gets no warning that their entry changed.

**What should happen:** No requirement says. S-114 only says "correct across daylight-saving transitions". So I wrote "Not specified" under Expected and left a question for product. The question is whether the app should reject a time in the gap, shift it and say so, or do something else. I haven't picked a behaviour, since that's product's call.

**Repro:** `uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py` exits 1 and prints `diary shows 03:30`. It exits 0 once the diary shows 02:30 or rejects the entry with a 400. I ran it three times, and each run printed the same line. The shell only showed me the exit code of the last run, which was 1.

**Files written:**
- `bugs/D-1-dst-gap-bedtime-shifted/repro.py`
- `bugs/D-1-dst-gap-bedtime-shifted/report.md`
- `bugs/ledger.md`, with a new D-1 row (confirmed, not filed)

Filing changes something the team sees, so I haven't done it. To file it, run `/file-bug bugs/D-1-dst-gap-bedtime-shifted`.