I've logged it as a confirmed bug, **D-1**. The behaviour is odd, but the 03:30 itself isn't wrong arithmetic.

On 8 March 2026 Toronto clocks jump from 02:00 to 03:00, so 02:30 never existed that night. The diary accepted it anyway, with a normal redirect and no error. It then showed 03:30, which is the same instant as 02:30 on the old offset. The user gets no warning or note.

No requirement or story says what should happen to a time in that gap. S-114 only covers nudge scheduling across DST. Under the triage-bug rules that makes it `confirmed` with Expected set to "Not specified". Whether the app should reject, shift or flag such a time is product's call, so the report carries a question for them.

**Files created**
- `bugs/D-1-nonexistent-local-time-shifted/repro.py` posts 02:30 for that date and zone to a throwaway database. It exits 1 while the diary accepts the input and shows something other than 02:30. It exits 0 if the input is rejected with HTTP 400 or shown as typed.
- `bugs/D-1-nonexistent-local-time-shifted/report.md`
- `bugs/ledger.md`, with a new D-1 row: confirmed, not filed.

**Verification:** I ran the repro 3 times and got exit 1 each time, printing `typed 02:30, HTTP 303, diary shows 03:30`. I haven't run `make test` or `make lint`, because I changed no source or tests.

The repro's "fixed" condition is my proposal. If product picks "shift forward with a visible note", the repro will need adjusting.

To file it, run `/file-bug bugs/D-1-nonexistent-local-time-shifted`.