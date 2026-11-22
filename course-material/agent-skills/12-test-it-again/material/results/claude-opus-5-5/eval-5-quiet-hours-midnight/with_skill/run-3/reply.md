I couldn't reproduce this, so it may not be a bug, and I didn't write a `repro.py`. Quiet hours from 21:00 to 00:00 saved fine every time I tried, on a throwaway database each time.

**What I tried**
1. **Sending the form data straight to the server, 3 times.** It saved 21:00 and 00:00 each time, and the Settings form showed 00:00 when I reloaded the page. A 22:15 nudge counted as inside quiet hours, so a window that ends at midnight works.
2. **Filling in the Settings form in a real Chromium browser, 3 times.** Chromium raised no warning on the 00:00 field. After saving, the page showed no error and the form still read 00:00.
3. **Reading the code.** There's no "Invalid time" message anywhere in the app. Nothing in the server, the page, or the time-parsing helpers would reject 00:00.

**Worth knowing**
- **It's already in the tracker as NJ-14** ("[Settings] Quiet hours can't end at midnight"). It's still Open, so either it's been fixed since then or the reporter's setup differs from mine.
- **A likely explanation:** the server rejects `24:00` ("hour must be in 0..23") and `0:00` ("Invalid isoformat string"). Chromium's time picker can't produce either one. But other browsers, older browsers and API clients that send free text can. This is a guess, so it would help to ask the reporter which browser they used and exactly what they typed.

**What I wrote**
- I added a row to `bugs/ledger.md` (the file didn't exist yet, so I created it): D-1, status `not reproduced`, tracker `not filed`. There's no bundle folder, so there's nothing to hand to `/file-bug`.
- My two scratch scripts, `.triage_try.py` and `.triage_browser.py`, are still in the repo root. Deleting them needed your approval, so please remove them or tell me to.

If the reporter confirms it was `24:00` or a particular browser, I can triage again with that input. If it reproduces, I'll write the bundle and `repro.py` then.