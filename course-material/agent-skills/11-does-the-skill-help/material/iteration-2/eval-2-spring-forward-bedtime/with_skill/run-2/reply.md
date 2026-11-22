Yes, I reproduced it, so I'm treating it as a bug. I've logged it as **D-1**, status `confirmed`.

**What happens:** 02:30 on 8 March 2026 doesn't exist in Toronto. Clocks jump from 02:00 to 03:00 that night. The app saves the time anyway and shows 03:30. `local_input_to_aware` (`src/nightjar/diary.py:151`) attaches the time zone to the typed time without checking that the time exists. The entry is saved as 07:30 UTC, which is 03:30 Toronto time, and the user is never told. Sleep duration is calculated from the shifted time.

**Not specified:** No requirement or story says what should happen here. S-114 only covers the nudge across DST. I've recorded Expected as "Not specified" with a question for product. They need to decide whether to reject the time with a message, snap it to a valid time with a notice, or keep accepting it silently.

**Repro:** `uv run python bugs/D-1-dst-gap-bedtime-shifted/repro.py`
- It posts the night through `POST /nights` to a throwaway database.
- It exits 1 while the diary shows a time other than 02:30, and 0 if the input is rejected with a 400 or shown as entered. It prints one line saying what it saw.
- It exited 1 on 3 of 3 runs. I ran each run as a separate command because the shell blocked a loop.
- If product picks a different fix, such as snapping with a notice, the exit condition in the script will need updating.

**Files**
- `bugs/D-1-dst-gap-bedtime-shifted/report.md`
- `bugs/D-1-dst-gap-bedtime-shifted/repro.py`
- `bugs/ledger.md` — new file, one row, tracker `not filed`

I didn't run `make test` or `make lint`, since I changed no source or tests.

**Next step:** filing makes something visible to the team, so you need to start it: `/file-bug bugs/D-1-dst-gap-bedtime-shifted`