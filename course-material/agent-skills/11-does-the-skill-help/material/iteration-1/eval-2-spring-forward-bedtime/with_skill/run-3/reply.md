**It isn't a bug, so I haven't written a repro or a bundle.**

At 02:00 on 8 March 2026, America/Toronto clocks jump straight to 03:00. The wall time 02:30 doesn't exist that night. The nearest real instant is 07:30 UTC, which is 03:30 EDT.

I checked this against a throwaway database. `local_input_to_aware("2026-03-08T02:30", "America/Toronto")` gives 07:30 UTC. After storing and reloading the night, `local_bedtime` is 03:30-04:00. The same result came out on 3 of 3 runs.

The code deliberately treats this as correct. `src/nightjar/nudge.py:46` says "DST skips (02:30 on spring-forward day becomes 03:30) so the result is a real instant". Story S-114 also requires correct handling across spring-forward. Stored instants and durations come out right.

**Possible product gap, not a defect:** the form accepts the nonexistent time without telling you. A cleaner design would reject it or warn "02:30 doesn't exist that night; saved as 03:30". Nothing in the requirements asks for that, so I'd raise it as an improvement request to the team.

**Before the first shift:** when you build a `Night` in memory, `local_bedtime` still reads 02:30-05:00, a time that never existed. The page only shows saved nights, so you won't see this there.

I didn't touch `bugs/` or the ledger, since you said not to write a repro for a non-bug. If you want the missing validation tracked anyway, say so and I'll draft it as a feature request instead of a defect.