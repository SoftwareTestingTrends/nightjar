Yes, it's a bug. The repro at `bugs/dst-gap-bedtime/repro.py` prints `BUG: typed bedtime 02:30 on 2026-03-08 in America/Toronto; diary shows 03:30` and exits 1.

**Why it happens.** 8 March 2026 is the spring-forward night in Toronto. Clocks jump from 02:00 to 03:00, so 02:30 never happens that night. `local_input_to_aware` in `src/nightjar/diary.py:151` attaches the zone to the typed time without checking that it exists. The time is stored as UTC (07:30Z). When the diary reads it back, it shows 03:30 EDT. Nothing tells the user their entry changed.

**Why I'm calling it a defect.**
- The form silently rewrites what the user typed. Real elapsed time is still correct, because durations use UTC.
- The shift also moves `night_of` and the usual-bedtime median that the nudge uses.
- S-114 requires correct behaviour across DST transitions.
- I didn't find a requirement that says what should happen for a skipped time. I treated silent alteration as the defect.

**What the repro checks.** It posts the form against a throwaway database. It exits 0 if the form rejects the nonexistent time (HTTP 400) or keeps the local bedtime as typed. It exits 1 if the entry is accepted and shows a different time.

I didn't write a fix. A fix could reject the time with a clear message, or accept it and show a notice. The repro accepts either approach, but a notice alone won't make it exit 0.

I also didn't open a tracker ticket or write a `report.md` and ledger row, since you only asked for the repro script. I can do those if you want.