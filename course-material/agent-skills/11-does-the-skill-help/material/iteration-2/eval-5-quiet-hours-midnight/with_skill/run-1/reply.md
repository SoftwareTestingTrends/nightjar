I couldn't reproduce this, so I didn't write a repro script for it.

I submitted `POST /settings` with quiet hours 21:00 to 00:00 three times, each against a fresh temporary database. Every run was accepted with HTTP 303, and the values were saved as 21:00 and 00:00. I also tried `00:00:00` and `21:00:00`, and those were accepted too. Only `24:00` is rejected, and a browser time field doesn't send that. The text "Invalid time" doesn't appear anywhere in `src/`, and I didn't try it in a real browser.

**Ticket NJ-14:** The tracker already has NJ-14, "Quiet hours can't end at midnight", which describes this exact report. It may be stale, or it may come from a different build or browser. I haven't touched it.

**What I wrote:**
- `bugs/ledger.md` has row D-1 with status `not reproduced` and tracker `not filed`.
- `bugs/D-1-quiet-hours-midnight/report.md` records what I tried and asks the reporter for the exact browser, the exact error text and what the field showed.

**Leftover file:** My `rm` of the draft script was blocked, so `bugs/quiet-hours-midnight/repro.py` is still there. Right now it exits 0, so it isn't a real repro, and you can delete that folder. Because I didn't write a repro, there is nothing to file with `/file-bug`.