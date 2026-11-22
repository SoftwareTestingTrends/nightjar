I couldn't reproduce this, so I didn't write a repro script. The app accepts 21:00 to 00:00 and uses it correctly.

**What I checked**
- **Saving the setting:** I sent 21:00 / 00:00 to the settings endpoint the way the form does, using a throwaway database. It saved (`quiet_start=21:00, quiet_end=00:00`) and returned the normal redirect, with no error.
- **How the window behaves:** `in_quiet_hours` (`src/nightjar/nudge.py:59`) handles a window that runs to midnight. 21:00 and 23:30 count as quiet; 20:59, 00:00 and 06:00 don't. That's correct for a window that ends at midnight.
- **Validation:** the settings handler only rejects a bad time zone or a time Python can't read. The time fields in `index.html` have no min/max limits, so nothing on the page would flag 00:00 either.

**The one way I can get an error:** entering **24:00** as the end time. The server rejects it with `hour must be in 0..23` and the settings stay unchanged. Behind the scenes, the time parser in Python's standard library simply doesn't accept 24:00. I wouldn't call that a bug, because the page's time picker can't produce 24:00. The value would have to be typed in some other way, such as through the API.

**What would help pin it down**
- The exact message they saw. "The time is invalid" isn't text this app produces, so it's probably the browser's own warning.
- Their browser and whether it shows 12-hour times. On a 12-hour display, midnight has to be entered as **12:00 AM**. Typing "00:00" there can make the browser call the time invalid before anything reaches the server.

If they can give me those, I can run it in a real browser with the browser-check skill.

I left one scratch file at `/tmp/njcheck/check.py`. Deleting it needed your approval because it's outside the project folder, so you can remove it yourself.