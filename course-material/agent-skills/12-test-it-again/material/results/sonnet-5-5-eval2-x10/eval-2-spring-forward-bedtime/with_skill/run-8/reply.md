Yes, this is a real defect, though the expected behaviour isn't specified anywhere.

On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never happened that night. The app accepts the entry without a warning and shows 03:30. The cause is in `local_input_to_aware` (`src/nightjar/diary.py:151`). It attaches the zone with `.replace(tzinfo=...)`, and Python resolves the nonexistent time using the old UTC offset, which lands on 03:30. Nobody decided that, and the user isn't told. The wake time field has the same problem.

I ran the repro 3 times, and it exited 1 each time with: `BUG: entered 02:30 (does not exist), status 303, diary shows 03:30`.

No requirement or story covers a local time that doesn't exist, so the report says "Not specified" under Expected. There is a question for product: should the app reject it with a message, or move it forward and tell the user? The repro exits 0 if the entry is rejected with a 400 or stored as typed. If product picks "move forward and tell the user", that check needs adjusting.

Files are in `bugs/D-1-dst-gap-bedtime/`:
- `repro.py`
- `report.md`
- `bugs/ledger.md` (row D-1, status `confirmed`, tracker `not filed`)

I haven't filed it, because filing is visible to the team. To file it, run:

`/file-bug bugs/D-1-dst-gap-bedtime`