This isn't a bug, so I haven't written a repro script.

I posted a 21:00 to 00:00 quiet-hours setting to `/settings` using the app's own test client. It saved and redirected with a 303. Reading the settings back gave `21:00:00` and `00:00:00`. The same happened with `00:00:00` as the end time.

The code agrees with that:
- **Parsing:** `web.py` parses the times with `time.fromisoformat`, which accepts `00:00`.
- **Storage:** `diary.py` formats and parses midnight correctly. Python 3.5 and later treats `time(0, 0)` as truthy, so the `if value` check doesn't drop it.
- **Quiet hours:** `in_quiet_hours` in `nudge.py` treats a start later than the end as a window that wraps past midnight, so 21:00 to 00:00 is a valid window.

The "invalid" message must come from something else. I can only see the server-side error (the 400 response from `/settings`), and 21:00 to 00:00 doesn't trigger it. These are the likely causes:
- **Time zone field:** a bad value (for example a typo or a non-IANA name) fails validation, and the page shows only a generic error.
- **Browser time input:** a locale or 12-hour-clock quirk in the browser's time input.
- **Different build:** a copy of the app other than this checkout.

If you can tell me the exact error text, the time zone value and the browser, I can narrow it down. I can also try it in a real browser with the `browser-check` skill.