I couldn't reproduce this, so I don't think it's a bug in NightJar, and I'm not leaving a repro script. I did write one at `bugs/quiet-hours-midnight/repro.py`. It posted 21:00 to 00:00 to `/settings` in a temporary app, and the app accepted it and saved it. Removing the script needs your approval, and the approval prompt didn't go through. Please delete that folder with `rm -r bugs/quiet-hours-midnight`. It currently exits 0, so it would mislead anyone who runs it.

- **Server:** `/settings` in `web.py` parses the times with `time.fromisoformat`, and `00:00` parses fine. `save_user` only checks the time zone. The stored values came back as `21:00:00` and `00:00:00`.
- **Quiet hours logic:** `in_quiet_hours` in `nudge.py` handles a window that wraps past midnight. Midnight as an end time works.
- **Page:** the quiet-hours fields are plain `<input type="time">`, which accept `00:00`.

The "invalid" message probably comes from somewhere else. I'd check these:
- **Time zone:** the form sends the time zone with the quiet hours, and an unknown zone name gives "Unknown time zone: …". That could look like a time error.
- **Browser time picker:** with a 12-hour clock, typing `00:00` or `12:00 AM` can be rejected as invalid.
- **Exact message:** if you send me the exact text and what you typed in each field, I'll look again. If it still fails in a browser, I can walk through the settings page in one.