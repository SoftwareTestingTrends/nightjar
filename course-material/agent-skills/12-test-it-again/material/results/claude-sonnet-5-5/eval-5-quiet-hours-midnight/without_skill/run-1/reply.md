This isn't a bug in the app as it stands, so I haven't written `bugs/<short-name>/repro.py`.

I posted a quiet window of 21:00 to 00:00 to `/settings` through the real app. It returned a 303 redirect, which is a success, and it saved `quiet_end` as 00:00. Other windows I tried also saved, including 21:00 to 07:00 and 00:00 to 06:00.

I also read the code path for anything that could reject that window:
- **Parsing:** `web.py` parses the times with `time.fromisoformat`, which accepts `00:00`.
- **Saving:** `Diary.save_user` only validates the timezone. `time(0, 0)` is truthy in Python 3.12, so it isn't dropped on save.
- **Quiet-hours logic:** `in_quiet_hours` treats 21:00 to 00:00 as a window that wraps midnight, which covers 21:00 to 24:00 as intended.
- **Page:** the settings form is plain `<input type="time">` with no `min`, `max`, `pattern` or scripts.

The app also has no "time is invalid" message for this case. The only validation error text on the settings route is the timezone one. So either the message comes from something else, or the input wasn't what it looked like.

Two things I couldn't check:
- **Tracker:** it isn't running, so I couldn't look for an existing report.
- **Real browser:** I didn't run one, so a browser-specific problem with the time input is still possible.

If you can tell me the exact wording of the error, the browser, and whether the timezone field was filled in, I can look again. A blank or oddly formatted timezone is the likeliest source of an "invalid" message. If you'd like, I can also run `/browser-check` on the settings flow.