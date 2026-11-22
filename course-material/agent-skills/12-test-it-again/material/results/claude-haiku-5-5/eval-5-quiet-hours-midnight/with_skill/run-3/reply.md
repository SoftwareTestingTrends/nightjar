**Not reproduced.** I couldn't confirm this as a bug, so I did not write a bug bundle or a `repro.py` for it.

**What I ran:** I posted quiet hours 21:00 to 00:00 to the app's `/settings` handler (`src/nightjar/web.py`), using a throwaway database, three times. Each time it was accepted with a 303 redirect, and the script printed `FIXED: 21:00-00:00 accepted`. The app's `quiet_end` parsing (`time.fromisoformat`) handles `00:00` fine, and the `in_quiet_hours` wrap-around logic is correct for this window.

**Why I'm not sure the report is wrong:**
- The string "Invalid time" doesn't appear anywhere in the repo, so the app as it stands doesn't produce that message.
- The same report is open in the local tracker as NJ-14, with the same steps. That suggests the reporter's build or environment differs from this checkout, or the error comes from the browser rather than the server.
- I checked the server handler, not the page in a real browser. If you can reproduce it in the browser, the `browser-check` skill can walk the Settings form and capture a screenshot.

**Files:**
- `bugs/ledger.md` is created with one row: `D-1`, status `not reproduced`, tracker `not filed`, last checked 2026-11-21 (3 of 3 accepted).
- I also created a draft `bugs/quiet-hours-midnight/repro.py`. It should not exist for an unconfirmed bug, and I couldn't delete it because `rm` needs approval. Please delete that folder, or tell me to delete it.

Nothing has been filed. If the browser check confirms the error, I can write the bundle as `D-2`, or update `D-1` to `confirmed`. Then run `/file-bug bugs/D-<n>-<short-name>` to file it.