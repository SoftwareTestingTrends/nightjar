I couldn't reproduce this, so I haven't written a repro script. I don't think it's a bug in NightJar.

I posted to `/settings` with a throwaway database and quiet hours of 21:00 to 00:00. It returned a 303 redirect, which is a successful save. After saving, `diary.user()` gave back `quiet_start=21:00` and `quiet_end=00:00`, and the home page loaded fine (200). 21:00 to 23:59 and 21:00 to 07:00 also saved without error.

The code agrees:
- **Validation:** `web.py:106-107` only calls `time.fromisoformat`, which accepts `00:00`. The only other check is on the time zone. NightJar has no check that rejects a quiet window, and no "invalid time" message for one.
- **Midnight handling:** `in_quiet_hours` in `nudge.py:63-65` treats a window with `end <= start` as wrapping past midnight. So 21:00 to 00:00 correctly covers 21:00 to midnight.
- **Storage:** `_format_time` and `_parse_time` in `diary.py` round-trip `00:00` correctly.

That means the "invalid" message probably isn't coming from NightJar's server. The time fields are plain `<input type="time">`, so it may be your browser's own validation. It could also be a different field, such as the time zone, or a stale or different build of the app. If you can tell me one of these, I can look again:
- the exact wording of the message and where it appears
- your browser and locale (a 12-hour locale can make `00:00` entry awkward, for example `12:00 AM`)
- whether the failure shows as a 400 response in the page's error area or as a browser tooltip

If it's a 400 from the app, send me the response text and I'll try again.