Yes, it's a bug. The repro exits 1 now and prints `BUG: entered 02:30 (nonexistent in Toronto), HTTP 303, diary shows 03:30`.

**Cause:** Toronto's clocks jumped from 02:00 to 03:00 on 8 March 2026, so 02:30 never happened that night. `local_input_to_aware` (`src/nightjar/diary.py:151`) attaches the zone to the typed time without checking that it exists. Python reads it with the pre-jump offset (02:30 EST), which is 07:30 UTC. The diary stores that and shows it back in local time as 03:30. The user is never told, and the displayed time is different from what they entered.

I treated this as a defect because the app already rejects other invalid input with a 400. It's still a judgment call, because the requirements don't say what to do with a time that doesn't exist. I defined "fixed" as the form rejecting that time with a 400. If you'd rather shift it to 03:30 and tell the user, the repro's pass condition would need to change.

**Repro:** `bugs/dst-gap-bedtime/repro.py` posts the entry through the real `/nights` form handler. It uses a throwaway database and exits 0 only when the form returns 400 and nothing is saved.

- **Path:** I used the path you asked for, not the `bugs/D-<n>-…` folder and `report.md` layout from `docs/bug-bundles.md`. I also didn't add a ledger entry or file a tracker ticket.
- **Not checked:** I haven't run `make test` or `make lint`.
- **Same bug elsewhere:** The wake-time field and CSV import use the same time conversion, so they probably do the same thing. I didn't test them.