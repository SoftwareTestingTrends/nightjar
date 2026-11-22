I couldn't reproduce this, so I didn't write a repro script. I found nothing that rejects 21:00 to 00:00.

I tried it against a throwaway database through the real `/settings` endpoint:

- **Save:** `21:00` to `00:00` returns a 303 redirect with no error. The values are stored and read back correctly.
- **Page:** the settings page re-renders with `quiet_start=21:00` and `quiet_end=00:00`.
- **Quiet-hours logic:** `in_quiet_hours` treats it as a window that wraps midnight. 21:00 and 23:59 count as quiet, and 20:59 and 00:00 don't. The end time is exclusive, which is the intended behaviour.
- **Validation code:** the only time parsing is `time.fromisoformat(...)` in `web.py:106-107`. It accepts `00:00`. Python 3.12 treats midnight as a normal time value, so it isn't mistaken for "empty".

The server has no "invalid time" message for these inputs, so the error you saw probably isn't coming from this code. Some possible sources:

- **Browser:** the `<input type="time">` field validates in the browser, for example when the field is only partly filled in. It could also be a locale that shows 12-hour time (`12:00 AM`), or a form that was filled in a different way than my test.
- **Different build:** you may be running a different version or branch than this checkout.

If you can tell me the exact text of the error and where it shows up (a browser tooltip or the red banner at the top of the page), I'll look again. A screenshot would also work. `make e2e` could then drive the real page with those values.