I couldn't reproduce this, so I don't think it's a bug in NightJar. I haven't deleted the repro script I wrote, because the shell asked for approval to remove it.

I posted exactly 21:00 to 00:00 to `POST /settings`. The app saved it and returned a 303 redirect, and it read back as `21:00:00` and `00:00:00`. The code agrees:
- **Parsing:** `time.fromisoformat("00:00")` is valid, and `web.py:106-107` has no range check on quiet hours.
- **Midnight-wrapping windows:** `in_quiet_hours` (`nudge.py:59-65`) handles an end time of 00:00, because 21:00 ≤ 00:00 is false, so it takes the wrap branch.
- **Storage:** `_format_time` writes `"00:00"` correctly, because `time(0, 0)` is truthy in Python 3.12.

So this isn't a NightJar bug, and I haven't written a repro that exits 1. The server only returns an "invalid time" error when `time.fromisoformat` raises a `ValueError`. That means the value your form sent wasn't a valid `HH:MM`. I haven't tested that cause in a browser. Likely candidates:
- A browser or locale that submits a 12-hour or localized string such as `12:00 AM` or `24:00`.
- A hand-typed or autofilled value in the time field.
- A timezone field that's blank or invalid. That would give a different message, so check the wording of the error you saw.

If you can send me the exact error text and the browser, I can dig further. If a browser really does submit something other than `HH:MM` for midnight, that would be a bug, and I'd write the repro then.

To clean up, delete `bugs/quiet-hours-midnight/` (it holds only `repro.py`), or approve the `rm` and I'll do it.