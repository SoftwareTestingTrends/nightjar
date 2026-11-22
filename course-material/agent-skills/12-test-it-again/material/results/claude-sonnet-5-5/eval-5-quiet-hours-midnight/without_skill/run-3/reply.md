I couldn't reproduce this, so I don't think it's a bug in NightJar, and I haven't written a repro script.

**What I checked**
- I posted `quiet_start=21:00` and `quiet_end=00:00` to `/settings` through the app's test client.
  - The server answered with a 303 redirect, which is a successful save.
  - The saved values read back as 21:00 and 00:00.
  - A normal 21:00–07:00 save behaved the same way.
- The code agrees with this.
  - `web.py` parses the times with `time.fromisoformat`, which accepts `00:00`.
  - `diary.py` stores and reads them back correctly.
  - `in_quiet_hours` in `nudge.py` handles a window that wraps past midnight.
- The settings form uses plain `<input type="time">` fields. It has no custom validation or JavaScript.

**What the "invalid" message probably is**
The app's only error for this form is a 400 response that shows the exception text. I saw no way for these inputs to trigger it. The most likely cause is the browser's own time-field validation. Some browsers reject a time that is partly typed or in the wrong format, for example a 12-hour field where "00:00" has to be entered as "12:00 AM".

**What would help**
- The exact wording of the error.
- Whether it appears in the browser or in the app's error banner.
- Which browser you're using.

If it's the app's banner, send me the text and I'll look again. If you're calling `/settings` directly, send me the request you're using.

My throwaway check script is at `/tmp/nj_check/try_quiet.py`, outside the repo. I changed nothing in the repo.