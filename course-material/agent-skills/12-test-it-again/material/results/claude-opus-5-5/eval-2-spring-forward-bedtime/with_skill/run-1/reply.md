The 03:30 itself is the correct instant. What I've logged as a defect is that the app changes your entry without telling you.

**What's happening:** 8 March 2026 is spring-forward night in Toronto. Clocks jump from 02:00 straight to 03:00, so 02:30 never existed that night. The form accepts the time anyway, stores it as 07:30 UTC, and the diary shows 03:30 EDT with no message. I reproduced this through the real form with a throwaway database, on the first try.

**Why I logged it rather than calling it fine:** none of the requirements (BR-07, PR-21) or stories (S-114, S-116, S-117) say what to do when someone enters a time that doesn't exist. The triage rules say that still counts as `confirmed`, with "Not specified" under Expected, because deciding the behaviour is acceptable is product's call. So I wrote the script instead of calling it not a bug.

**Cause:** `local_input_to_aware()` in `src/nightjar/diary.py` attaches the zone to the time without checking that the time exists. `zoneinfo` then reads 02:30 with the winter offset, which comes back out as 03:30. `nudge.py` makes the same shift on purpose for scheduling, but nothing says that's right for what users type in.

**The bundle:** it's at `bugs/D-1-dst-gap-bedtime-shifted/`, not `bugs/<short-name>/`, because the team's bundle format requires the `D-<n>-` prefix.
- `repro.py` exited 1 in all 3 runs: `BUG: entered 02:30, form saved it silently (HTTP 303), diary shows 03:30`. It exits 0 once the form refuses a time that doesn't exist, or once the diary shows 02:30.
- `report.md` asks product to pick one of three options:
  - (a) refuse the time
  - (b) save it as 03:30 and tell the user
  - (c) keep the current silent behaviour
- The script assumes (a). If product picks (b), the check needs to also look for the notice. If they pick (c), this isn't a defect and the row should be closed.
- `bugs/ledger.md` has the row: D-1, `confirmed`, tracker `not filed`.

I didn't change any app code, so I didn't run `make test` or `make lint`.

Filing it changes what the team sees, so I haven't. To file it, run:

```
/file-bug bugs/D-1-dst-gap-bedtime-shifted
```