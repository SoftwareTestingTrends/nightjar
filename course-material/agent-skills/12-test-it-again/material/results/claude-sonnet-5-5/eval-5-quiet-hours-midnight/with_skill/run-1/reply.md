I couldn't reproduce this, so I didn't write a `repro.py`.

**What I tried:** I posted 21:00 to 00:00 to `POST /settings` against a throwaway database, three times. It saved every time (303 redirect). The page then showed `00:00` in the "to" field, with no error. I also checked the quiet-hours logic. It treats the window as wrapping past midnight, so it is quiet at 21:00, 23:00 and 00:00 and not quiet at 20:00. At 00:00 itself the check returns not quiet, because the end time is exclusive.

**What does get rejected:** the literal string `24:00` returns 400. A browser time input sends `00:00` for midnight, so the form shouldn't produce `24:00`. If the user's browser or locale lets them type "24:00", that could explain the "invalid" message.

**Questions for the reporter:**
- What exact text did they enter, and in which browser?
- What did the error message say, word for word?
- Did they type into a time field or paste a value?

If they send a `24:00` case, I can re-triage it. Whether `24:00` should be accepted is a product call.

**Files I left behind:**
- I added `bugs/ledger.md` with one row, D-1, status `not reproduced`. There is no bundle folder because there was no repro.
- `bugs/probe.py` is my scratch script. The shell asked for approval before deleting it, so it's still there. It's gitignored and safe to delete.