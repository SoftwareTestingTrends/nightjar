I couldn't reproduce this on the current code, so I didn't write a `repro.py`. The app saves quiet hours from 21:00 to 00:00 without any error.

**What I tried** (each 3 times, against a new throwaway database, never `nightjar.db`):

1. **Posting the form straight to the server** (`POST /settings` with 21:00 → 00:00): it saved every time with `303`, stored `quiet_end=00:00`, and no "invalid" message appeared. I also tried `21:00:00 → 00:00:00` and the 23:59 workaround from the report, and both saved too.
2. **Using the real page in a browser** (Chromium with Playwright, a real uvicorn server): I typed 21:00 and 00:00 into the Settings form and clicked Save. The browser accepted the form, the page came back with 00:00 in the "to" box, and there was no error text.

**Why it works:**
- Nothing in the code produces an "Invalid time" message. The only check is Python's `time.fromisoformat`, which accepts "00:00".
- A midnight time is saved and read back correctly: `src/nightjar/diary.py:164`.
- The time inputs in the template have no `min` or `max` that would block 00:00.
- The quiet-hours check handles a window that crosses midnight (`src/nightjar/nudge.py:63-65`), so 21:00–00:00 counts 21:00 to 23:59 as quiet, as you'd expect.

**What I recorded:** I created `bugs/ledger.md` with row D-1, status `not reproduced`, tracker `not filed`.

**Things you should know:**
- **There's already a ticket for this:** **NJ-14** ("[Settings] Quiet hours can't end at midnight") is still Open with the same description. It may have been fixed without the ticket being closed, or it may only happen somewhere I didn't test: another browser (Safari and Firefox show time inputs differently), a 12-hour clock where midnight shows as "12:00 AM", or an older deployed build. If the reporter can say which browser and locale they used, I can try again. If it still doesn't reproduce, NJ-14 could probably be closed as can't-reproduce, but that's the team's decision.
- **Leftover scratch files:** my two test scripts are still in `/private/tmp/nightjar-probe/`. Deleting them needed approval because that folder is outside the project, so you can remove it whenever you like.

Since it isn't confirmed, there's nothing to hand on to `/file-bug`.