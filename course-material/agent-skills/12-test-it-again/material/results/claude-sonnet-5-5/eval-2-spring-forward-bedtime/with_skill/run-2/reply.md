It's a bug, but a narrow one. The 03:30 itself is correct. The problem is that NightJar changed your entry and didn't tell you.

On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never happened that night. The form accepted it anyway, with no error or notice. The code in `local_input_to_aware` (`src/nightjar/diary.py`) puts the zone on the typed time without checking that it exists. It stores 02:30 as 07:30 UTC, which reads back as 03:30 EDT.

**Repro:** `uv run python bugs/D-1-dst-gap-bedtime-shifts/repro.py` exited 1 on all 3 runs and printed `BUG: logged 02:30 (nonexistent), accepted with 303, diary shows 03:30`. It uses a throwaway database. It exits 0 if the form rejects the time (HTTP 400) or the diary shows 02:30 as typed.

**What should happen:** no requirement or story covers nonexistent local times, so the report says "Not specified" under Expected. Product needs to choose: reject the entry with a message, or shift it and tell the user. If they pick the second, the repro has to change, because it only counts rejecting or showing 02:30 as fixed.

**Files:** I wrote `bugs/D-1-dst-gap-bedtime-shifts/report.md` (status `confirmed`, tracker `not filed`) and created `bugs/ledger.md` with the D-1 row. Nothing is filed yet.

To file it, run: `/file-bug bugs/D-1-dst-gap-bedtime-shifts`

I didn't run `make test` or `make lint`, since I changed no source or tests.