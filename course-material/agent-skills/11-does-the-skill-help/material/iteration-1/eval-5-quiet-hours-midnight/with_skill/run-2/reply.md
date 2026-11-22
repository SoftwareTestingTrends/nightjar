I couldn't reproduce this, so I haven't written a `repro.py`. Saving quiet hours 21:00 to 00:00 worked every time I tried it.

**What I tried, each against a throwaway database:**
- **API:** I posted `POST /settings` with start 21:00 and end 00:00 three times. Each time it returned a 303 redirect (success), and the saved end time was `00:00:00`.
- **Real browser:** I filled the Settings form in Chromium with 21:00 to 00:00 and clicked Save, three times. There was no error and the values were saved.
- **Other times:** 21:00 to 07:00 and 00:00 to 06:00 saved fine too.
- **Code:** I read `web.py`, `diary.py` and `nudge.py`. `time(0, 0)` counts as a set value in Python 3.12. `in_quiet_hours` already handles a window that wraps past midnight.

I added a ledger row, `D-1`, with status `not reproduced` in `bugs/ledger.md`. I didn't create a bug bundle folder.

**Why you might see "invalid":**
- **Different build:** you may be running a different build or database than the code I tested.
- **Typed value:** the browser's time field may have received something it couldn't parse, such as a typed `24:00`. I only tried `00:00`.
- **Another field:** the error may come from the time zone field instead, because the app shows the same kind of error for a bad zone name.

If you can send the exact text of the error message and what's in the Time zone field, I'll try again with that.