I couldn't reproduce this, so I don't think it's a bug in the code, and I haven't written `bugs/<short-name>/repro.py`.

- **Settings endpoint:** `POST /settings` with `quiet_start=21:00` and `quiet_end=00:00` returns a 303 redirect, which is the success response. It doesn't return the 400 "invalid" error. The same goes for 21:00–01:00.
- **Save and read back:** the value saves and reads back as `time(21, 0)` to `time(0, 0)`. On Python 3.12 midnight isn't treated as empty, so `_format_time` doesn't drop it.
- **Quiet-hours check:** `in_quiet_hours` handles the window correctly. It's silent at 21:30 and 23:30 and not silent at 20:30, 00:30 and 01:30. A window that ends at midnight is the same as one that wraps past it.
- **Where the "invalid" message could come from:** `web.py` only returns a 400 for a `ValueError`. That comes from `time.fromisoformat` on a malformed time, or from an unknown time zone in `save_user`. The time inputs on the page are plain `<input type="time">` with no `min`, `max` or `pattern`.

Most likely the error came from the **time zone field**, which is free text. A typo or a non-IANA name there (for example "EST" or "Toronto") would give an invalid error, even though you were editing the quiet hours. A browser that shows a 12-hour picker and submits something odd could also do it.

To narrow it down, I need the exact error text and what is in the time zone box when you save. If it only fails with a particular time zone value, that would be a real validation or usability problem, and I can write a repro for it.

I only added scratch scripts in `/tmp` and changed nothing in the repo.