I couldn't reproduce this, so I don't think it's a bug in NightJar and I haven't written a repro script.

- **Server:** `POST /settings` with `quiet_start=21:00` and `quiet_end=00:00` returns a 303 redirect, and the values are saved and read back as 21:00 and 00:00. The handler is `src/nightjar/web.py:94`. It uses `time.fromisoformat`, which accepts `00:00`, and the timezone check only looks at the zone name.
- **Nudge logic:** `in_quiet_hours` in `src/nightjar/nudge.py:59` treats 21:00 to 00:00 as a window that wraps past midnight. That's correct: it's quiet from 21:00 up to midnight.
- **Page:** the settings form uses plain `<input type="time">` fields with no custom validation in the template or in `static/`. Any "invalid" message would come from the browser itself or from the server's error banner.

**Cleanup:** I wrote a draft repro at `bugs/quiet-hours-midnight/repro.py` to test this, and it passed (exit 0). I tried to delete it, but the delete needed your approval, so it's still there. It's an untracked file, and `rm -r bugs` removes it.

**What would help:** the exact error text, and whether it appears as a red banner on the page or as a browser tooltip on the field. Which browser you used, and whether the time zone field was filled in, would also help. A browser tooltip would point to the field's own validation, such as a locale that enters midnight as `24:00`. A banner would be the server's message, which could be about the time zone rather than the times.