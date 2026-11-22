**Not reproduced.** I couldn't make quiet hours 21:00 to 00:00 fail, so I didn't write `repro.py` or a bundle folder. I added a ledger row instead: `bugs/ledger.md`, D-1, status `not reproduced`.

What I tried, all against throwaway databases:

1. **API:** posted `quiet_start=21:00, quiet_end=00:00` to `/settings`. It returned 303 and stored `00:00:00`. I also tried `21:00`→`23:59`, `23:00`→`00:00` and `00:00`→`07:00`; all saved.
2. **Browser (Chromium, form filled by value):** `21:00`→`00:00` saved, redirected to `/`, and the field showed `00:00`. No error.
3. **Browser (keyboard-typed times):** inconclusive. The typed values didn't land in the inputs; they stayed at the default `07:00`. No error appeared, but this run doesn't really test the report.

The "Invalid time" text doesn't exist anywhere in the app. The only parse on this path is `time.fromisoformat`, and `00:00` parses fine. So the message the user sees may come from somewhere else, such as a different build or a browser or OS input control.

The team tracker already has this report as **NJ-14** (open, in `tools/tracker/seed.json`). I couldn't check its live status because the tracker isn't running on port 8765.

Nothing needs filing for D-1 yet, so there's no `/file-bug` step. To re-triage, I need:
- the exact text on screen and where it appears,
- the browser and OS, and whether the time input was set by typing or the picker,
- the app version or commit they're running.

Housekeeping: I ran a `/tmp/nj-triage/probe.py` that already existed. It used a temp database, so it didn't touch `nightjar.db`. My probe scripts are in `/tmp` (`triage-settings-probe.py`, `triage-ui-probe.py`, `triage-ui-probe2.py`), outside the repo. Nothing in the repo changed except the new, gitignored `bugs/ledger.md`.