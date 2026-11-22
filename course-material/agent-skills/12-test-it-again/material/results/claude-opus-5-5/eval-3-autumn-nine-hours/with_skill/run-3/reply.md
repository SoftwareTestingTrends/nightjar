This isn't a bug. The 9 hours is correct, so I didn't write a repro script or a bug bundle.

**Why it's 9 hours:** Daylight saving time ended in Toronto at 02:00 on Sunday 1 November 2026. At that moment the clocks went back to 01:00, so the hour from 01:00 to 02:00 happened twice that night. Bed at 23:00 and up at 07:00 looks like 8 hours on the clock, but 9 real hours passed:

- Bedtime 23:00 EDT (UTC−4) is 03:00 UTC
- Wake time 07:00 EST (UTC−5) is 12:00 UTC
- 12:00 − 03:00 = **9 h**

**What I ran:** I saved that exact night to an empty throwaway database (not `nightjar.db`) and read it back, 3 times. Each time it came back as night of 2026-10-31, bed 23:00 −04:00, up 07:00 −05:00, duration `9:00:00`. The diary table shows `night.duration` (`src/nightjar/templates/index.html:73`). That value is worked out in UTC on purpose (`src/nightjar/models.py:53`), so the extra hour is counted.

**What the spec says:** this is the intended behaviour. Story S-116 says durations are real elapsed time, so "a night that crosses a daylight-saving change is an hour shorter or longer on the clock". BR-07 also requires the app to work for people who live through daylight-saving changes.

The skill's steps only cover "confirmed" and "not reproduced", and neither fits this, so I didn't add a row to `bugs/ledger.md`. I can add one with a note if you'd like a record of it.

The "Slept" column gives no hint that a time change happened, which is why the number looked wrong. Adding a hint there would be a product change, not a bug fix.

The cleanup command was blocked because the file is outside the project folder, so my scratch script is still at `/tmp/nj_triage_check.py`. You can delete it.