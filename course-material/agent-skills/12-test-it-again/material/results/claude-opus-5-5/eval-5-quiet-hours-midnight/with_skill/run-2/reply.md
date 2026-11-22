I couldn't reproduce this on the current code, so I didn't write a `repro.py`.

**What I tried** (each against a fresh throwaway database, never `nightjar.db`):
1. **Through the app's API with a test client:** saving quiet hours from 21:00 to 00:00 went through with no error, and the settings read back as 21:00 and 00:00. Ending at 23:59 or 07:00 also saved fine.
2. **The quiet-hours check:** with 21:00 to 00:00, 22:30 counts as quiet and 20:00 doesn't, which is right.
3. **In a real Chromium browser, 3 runs:** I filled in 21:00 and 00:00 on the Settings form and clicked Save. The browser accepted the form each time, the page reloaded showing 21:00 and 00:00, and no "invalid" text appeared.

**Why it can't happen as reported:** nothing in the current code would reject 00:00. The server just reads the time as given (`src/nightjar/web.py:106-107`). The form's time fields have no minimum or maximum (`src/nightjar/templates/index.html:50-51`). Saving and loading a midnight time works too (`src/nightjar/diary.py:160-165`).

**Tracker:** this matches **NJ-14**, "[Settings] Quiet hours can't end at midnight", which is still marked Open. The problem was probably fixed without the ticket being closed. It's also possible the person reporting it is on an older build, or a browser that handles 00:00 in time fields differently. I only tested Chromium.

**Ledger:** I added row D-1 to `bugs/ledger.md` with status `not reproduced` and a note that it matches NJ-14. Since it isn't a confirmed bug, there's no bug folder and nothing to send to `/file-bug`. Instead, it's worth asking the reporter for their app version and browser, and someone on the team could close or comment on NJ-14.

My test scripts are in `../nightjar_scratch/`, which is outside the repo, and I couldn't delete them without your approval. You can remove them with `rm -rf ../nightjar_scratch`.