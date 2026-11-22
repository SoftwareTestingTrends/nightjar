I couldn't reproduce this on the current `main`. 21:00 to 00:00 saves fine, so I didn't write a repro script.

**What I ran:**
- **The server:** I posted quiet hours 21:00 to 00:00 to the settings endpoint on an empty test database. It accepted them (status 303), saved 00:00 as the end time, and the page showed `21:00` and `00:00` afterwards. The error handler in `src/nightjar/web.py:110` never fired.
- **A real browser:** I filled in the settings form in headless Chromium and pressed Save. The browser saw no problem with 00:00, the save went through, and no "invalid" text appeared on the page.
- **The quiet-hours check:** a window that ends at midnight works. 21:00, 22:15 and 23:59 count as quiet; 20:59 and 00:00 don't. That matches how other windows treat their end time.
- **The message itself:** the words "Invalid time" don't appear anywhere in the app, templates or tests. The time fields in the form set no limits, so the browser has no reason to reject 00:00.

**There's a tracker ticket for this:** NJ-14, "Quiet hours can't end at midnight", is still **Open**, with the same steps and error message as your report. Either it was fixed without the ticket being updated, or the error only happens somewhere I didn't test. My best guess is a different browser (Safari, Firefox) or a 12-hour clock setting where midnight is typed as "12:00 AM". If you can tell me which browser and system clock format you saw it in, I'll try that next. Otherwise NJ-14 looks ready to close as "can't reproduce on main".

I didn't change anything in the repo. My two test scripts are in `/tmp`, outside the repo.