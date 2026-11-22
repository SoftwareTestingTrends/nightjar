This isn't a bug, so I haven't written a repro script.

**Why:** 02:30 doesn't exist in America/Toronto on 8 March 2026. At 02:00 EST the clocks jump straight to 03:00 EDT, so the wall times from 02:00 to 02:59 are skipped.

**What the code does:**
- `local_input_to_aware` in `diary.py:151` attaches the zone to the entered 02:30. `zoneinfo` resolves the skipped time using the pre-transition offset, EST (−05:00).
- That gives the instant 07:30 UTC, which I confirmed by running it.
- The diary stores the instant in UTC and shows it in the night's zone. 07:30 UTC is 03:30 EDT, so the diary shows 03:30.

The result is a real instant, one hour after 01:30 EST. This matches the documented design in `nudge.py:46-47`: "02:30 on spring-forward day becomes 03:30".

**What I couldn't check:** I only traced the code. I didn't submit the form in a browser.

If you want a different outcome, that would be a product change rather than a bug fix. For example, the form could reject or warn about a skipped time instead of shifting it silently. The requirements and S-114 docs don't specify that behaviour.