I couldn't reproduce this, so I'm treating it as not a bug and haven't left a `repro.py`. The throwaway script I used to test it is still at `bugs/quiet-midnight/`. The shell asked for approval to delete it, so please remove that folder, or tell me to retry the delete.

**What I checked**
- **Saving 21:00 to 00:00:** I posted those values to `/settings` with a temporary database. The app returned a 303 redirect and saved `21:00 → 00:00`. I didn't run the real browser page.
- **Save path:** In `web.py`, `time.fromisoformat("00:00")` parses fine. `diary.py` stores and reloads midnight without trouble, because `time(0, 0)` counts as set in Python 3.12.
- **Form:** The settings form is two plain `type="time"` inputs with no custom validation or script.
- **Nudge logic:** `in_quiet_hours` treats 21:00 to 00:00 as a window that wraps midnight, which is correct.

**Where the error likely comes from**
- The server only reports an error for a bad time zone (`zone()` raises `ValueError`) or a time it can't parse. The message would say which.
- The time zone box is free text. A typo or an unrecognised name would make the whole save fail, and that may be what you hit.
- A time input left half-filled, or in a browser or locale that submits something other than `HH:MM`, could also be rejected.

If you send me the exact error text and the time zone value, I can check again. I can also fill in the form in a real browser with the `browser-check` skill.