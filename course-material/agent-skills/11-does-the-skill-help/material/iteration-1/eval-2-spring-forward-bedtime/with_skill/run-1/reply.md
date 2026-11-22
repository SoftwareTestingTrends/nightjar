**Not a bug, so I haven't written a repro or touched the ledger.**

8 March 2026 is the spring-forward day in America/Toronto. At 02:00 EST the clocks jump straight to 03:00 EDT, so 02:30 doesn't exist that night.

I ran the app's own conversion, `local_input_to_aware("2026-03-08T02:30", "America/Toronto")`, three times. Each run gave the same result:
- The stored instant is 07:30 UTC, which is 03:30 EDT.
- The diary shows 03:30 because it displays that stored instant in Toronto time.

This matches the design. The `at_local_time` docstring in `src/nightjar/nudge.py:46` says "02:30 on spring-forward day becomes 03:30" so the result is a real instant. The stored times stay correct, and durations are computed in UTC.

The one thing you could fairly call a gap is that nothing tells the user their time was moved. That's a UX question, not a defect against any requirement. If you want a warning or a validation error for skipped local times, it would need a new requirement or story first.

If you actually slept around 02:30 by the clock, the exact instant isn't ambiguous. The skipped hour only affects what you can type. I can write that up as an enhancement idea if you like.