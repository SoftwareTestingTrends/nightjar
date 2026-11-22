I couldn't reproduce this as a bug, so I haven't kept a repro script. I did write a draft one, but deleting it needs your approval and was declined, so `bugs/quiet-hours-midnight/repro.py` is still on disk. Please delete the `bugs/` directory. It was empty before I added it, and the script exits 0 because the bug doesn't reproduce.

**What I checked**
- I posted `quiet_start=21:00` and `quiet_end=00:00` to `/settings` through the real app. It saved both values and redirected with a 303.
- `nudge.py:59-65` already handles windows that wrap past midnight (`start > end`), and midnight is stored and parsed correctly.
- The page has no client-side validation: the inputs in `index.html` are plain `type="time"` with no `min`, `max` or `pattern`.

The only "invalid" message the server can send comes from a `ValueError` in `web.py:110`. That happens when the time string can't be parsed or the timezone is bad.

**What it probably is**
The "time is invalid" message is most likely coming from the timezone field or from how the time was typed. A browser time input that is only partly filled in, such as hours with no AM/PM, sends an empty or invalid value.

**To narrow it down**
- Tell me the exact error text and what is in the timezone field. A typo or a non-IANA value like `EST` would be rejected.
- Tell me which browser you used and whether the end field showed `12:00 AM`.

If you can reproduce it with specific input, send it over and I'll write the repro.