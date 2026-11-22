Yes, it's a bug. It's a real defect, but what the right behaviour is hasn't been specified.

**What happens:** On 8 March 2026 clocks in Toronto jump from 02:00 to 03:00, so 02:30 doesn't exist that night. The app accepts it anyway (HTTP 303, no warning) and shows 03:30.

**Cause:** `local_input_to_aware` in `src/nightjar/diary.py:153` attaches the zone with `.replace(tzinfo=...)`. For a time in the gap, zoneinfo applies the pre-transition offset (EST), and 02:30 EST is 03:30 EDT. The stored instant is already shifted, so this isn't a display problem. The autumn case, where 01:30 happens twice, is silently resolved the same way.

**Repro:** `uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py` exited 1 in 3 of 3 runs and printed `BUG: logged 02:30, diary shows 03:30`. It exits 0 if the entry is rejected or the diary shows 02:30 as entered. I used a throwaway temp database.

**Question for product:** No requirement or story covers a nonexistent local time. The report says "Not specified" under Expected, with these options:
- reject the entry with a clear message
- accept it and tell the user it was adjusted to 03:30
- something else

If product picks the "adjusted with a notice" option, the repro needs updating to check for that notice.

**Files written** (`bugs/` is gitignored):
- `bugs/D-1-dst-gap-bedtime-shifted/report.md`
- `bugs/D-1-dst-gap-bedtime-shifted/repro.py`
- `bugs/ledger.md`: new row D-1, status `confirmed`, tracker `not filed`

**To file it:** `/file-bug bugs/D-1-dst-gap-bedtime-shifted`. I haven't filed it, since that's visible to the team.