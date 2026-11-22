I couldn't reproduce this, so I don't think it's a bug, and there's no repro script to keep.

I posted `quiet_start=21:00` and `quiet_end=00:00` to `/settings` against a fresh app and diary. It returned a 303 redirect, which is the success path. The code agrees:
- **Parsing:** `web.py:106-107` parses both values with `time.fromisoformat`, and `"00:00"` is valid.
- **Storage:** `time(0, 0)` is truthy in Python 3.5 and later, so the `if value` checks in `diary._format_time` and `_parse_time` don't drop it.
- **Quiet-hours logic:** `nudge.in_quiet_hours` treats a window where start is later than end as wrapping past midnight. 21:00–00:00 therefore covers 21:00 up to midnight, as you'd expect.

The only "invalid" errors in the code are the CSV import errors and an unknown time zone, and neither relates to quiet hours.

I only tested the server side, not a real browser, so I can't say where your message came from. Things worth checking:
- **Browser or OS:** a browser with its own `<input type="time">` validation could be rejecting the value. Which one are you using?
- **Time zone:** an invalid time zone in the same form would also return a 400 with an error. Check the zone field.
- **Exact wording:** the exact text of the error and the entered values would help narrow it down.

I tried to delete my scratch repro file, `bugs/quiet-hours-midnight/repro.py`, but the shell blocked the delete and asked for approval. It passes (exit 0), so it doesn't match what you asked for. Please delete that `bugs/quiet-hours-midnight/` directory, or tell me to retry.