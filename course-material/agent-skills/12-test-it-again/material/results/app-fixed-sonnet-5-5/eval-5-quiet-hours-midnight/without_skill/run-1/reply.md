I couldn't reproduce this, so I don't think it's a bug and I haven't left a repro script.

- **21:00 to 00:00 saves fine.** I posted those values to `/settings` with the real app and a temp database. It returned a 303 redirect, and the saved settings read back as 21:00 and 00:00.
- **The window behaves correctly.** With 21:00 to 00:00, `in_quiet_hours` is true at 22:00 and 23:59 and false at 00:00 and 01:00. Midnight is treated as the end of the window.
- **"Invalid" probably comes from a different input.** The only way I found to get a time error is `24:00`, which Python rejects with "hour must be in 0..23". If you typed `24:00` as the end time, that would explain it. Use `00:00` instead.

If it still fails with `00:00`, tell me the exact text of the error and how you entered the time. For example, the browser's time picker might be sending something unexpected. I'd then look at the page itself with `browser-check`.

**Cleanup needed:** my試 script is still at `bugs/quiet-hours-midnight/repro.py`. The sandbox blocked me from deleting it. It exits 0 because the save works, so it isn't a valid repro. Please delete that folder (`rm -r bugs`), or approve the command and I'll run it.