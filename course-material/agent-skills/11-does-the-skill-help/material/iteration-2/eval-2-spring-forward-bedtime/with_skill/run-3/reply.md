Yes, I'd call it a bug, but the cause isn't what you'd guess. The diary silently changes the time you entered.

**What happens:** 02:30 doesn't exist in Toronto on 8 March 2026, because clocks jump from 02:00 to 03:00. The app accepts it anyway and picks the pre-jump offset (-05:00, which is 07:30 UTC). That displays as 03:30 EDT. Nothing tells you the time was changed, so your 02:30 is lost. The code is `local_input_to_aware` in `src/nightjar/diary.py`.

**Reproduction:** I submitted the entry through the real `POST /nights` route against a throwaway database. It was saved with HTTP 303 and shown as 03:30, and the repro exited 1 on 3 of 3 runs.

**Expected behaviour is not specified.** S-114 only requires the nudge to be correct across DST. No requirement says what to do with a time that doesn't exist. So the bug is confirmed, with "Not specified" under Expected, and product needs to decide:
- reject the entry with a message, or
- shift it and tell the user.

**The repro's exit condition is my guess.** `repro.py` exits 0 if the app rejects the entry (HTTP 400) or shows 02:30. If product picks "shift and warn", that condition needs adjusting.

**Files I wrote:**
- `bugs/D-1-spring-forward-bedtime-shifted/repro.py`
- `bugs/D-1-spring-forward-bedtime-shifted/report.md`
- `bugs/ledger.md` (row D-1: `confirmed`, tracker `not filed`)

**Next step:** filing changes something the team sees, so I haven't done it. To file it, run:

`/file-bug bugs/D-1-spring-forward-bedtime-shifted`