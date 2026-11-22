I couldn't reproduce this, so I'm treating it as not a bug. I added a ledger row, and the `repro.py` I wrote earlier is still on disk.

**What I tried:** I posted `/settings` with quiet hours 21:00 to 00:00 against a throwaway database, three times. Each time it was accepted with a 303 redirect, and the end time was saved as `00:00`. I also read the code:
- `web.py` parses the times with `time.fromisoformat`, and `00:00` is valid.
- `nudge.py` treats 21:00 to 00:00 as a window that wraps midnight, so it behaves correctly.
- The text "Invalid time" doesn't appear anywhere in `src/`.

**Ticket and browser:** `tools/tracker/seed.json` has a ticket, "[Settings] Quiet hours can't end at midnight", which describes the same report. I couldn't search the tracker, because `tracker.py search` crashed with a JSON decode error. I haven't checked the page in a real browser either. The message may come from the browser's own `<input type="time">` validation, which would depend on the browser and locale. If you still see it, tell me the browser and exactly what you typed, and I'll check it with `/nightjar-qa:browser-check`.

**Cleanup still needed:** you asked for no repro script if this isn't a bug. The shell asked for approval before it would remove files, so `bugs/D-1-quiet-hours-midnight/repro.py` is still there. It currently exits 0, which means the bug isn't present. Please delete it with `rm -r bugs/D-1-quiet-hours-midnight`, or approve the removal and I'll do it.

**Ledger:** `bugs/ledger.md` now has D-1 with status `not reproduced` and tracker `not filed`. Nothing was filed.