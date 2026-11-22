I've finished reproducing this. I haven't written any files.

**Verdict: not a bug, so there is no `repro.py` and no ledger row.**

8 March 2026 is the spring-forward day in America/Toronto. At 02:00 the clocks jump straight to 03:00, so 02:30 never happens that night. I checked how the app parses the input. `local_input_to_aware` (`src/nightjar/diary.py:151`) gives these results:

| Input (America/Toronto) | Parsed as |
|---|---|
| 01:30 | 01:30 EST, UTC-5 |
| 02:30 | 02:30 at UTC-5, which is 07:30 UTC |
| 03:30 | 03:30 EDT, UTC-4 |

07:30 UTC is 03:30 on the Toronto wall clock. The diary shows 03:30 because that is the real local time for the instant that 02:30 resolves to. That matches the story S-114 requirement to be correct across DST.

**Possible UX gap, not a defect:** the form accepts a time that doesn't exist and silently shifts it by an hour, without telling the user. I found nothing in `docs/` that says how nonexistent times should be handled. If you want a warning or a validation error, that's a product decision and a new requirement. I haven't logged it as a defect.

I didn't create a throwaway database or run the full triage steps, because the cause is clear from the conversion alone. If you'd like the gap logged as an enhancement, tell me and I'll write it up.