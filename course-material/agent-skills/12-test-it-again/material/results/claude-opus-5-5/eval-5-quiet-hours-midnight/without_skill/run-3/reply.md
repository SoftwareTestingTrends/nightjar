I couldn't reproduce this, and nothing in NightJar's code can produce that message, so I didn't write a repro script.

**What I checked:**
- **The server accepts it.** I posted `quiet_start=21:00, quiet_end=00:00` to `/settings` against a temporary database. It returned `303` (success), saved `quiet_start=21:00, quiet_end=00:00`, and the Settings form showed `21:00` and `00:00` when I reloaded it.
- **No "invalid" check exists on the page.** The page loads no JavaScript (the only static file is `style.css`), and the two time fields have no `min`, `max` or `pattern`. Searching `src/nightjar` turns up no "invalid time" message. The only check on this form is `time.fromisoformat`, which accepts `00:00` (`src/nightjar/web.py:106`).
- **The quiet-hours logic handles a midnight end.** In `src/nightjar/nudge.py:59-65`, a window ending at 00:00 is treated as crossing midnight, so 21:00–23:59 counts as quiet. That's what someone setting 21:00 to 00:00 would expect.

**What I couldn't check:**
- I didn't try it in a real browser. The page doesn't validate those fields itself, though, so an error there would most likely come from the browser or its time picker (for example, a 12-hour picker where "12:00 AM" is entered oddly), not from NightJar.
- The bug tracker wasn't running, so I couldn't look for an existing ticket.

If whoever reported it can share the exact error text and which browser they used, or a screenshot, I can look again. I can also walk the Settings form in a real browser with the browser-check skill.

My throwaway test script is still at `/tmp/qh_probe.py`, outside the repo, because deleting it needed permission. Nothing in the repo changed.