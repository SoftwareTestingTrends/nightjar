**It isn't a bug, so I haven't written a repro or a bundle.**

On 8 March 2026 Toronto clocks jump from 01:59 EST straight to 03:00 EDT, so 02:30 never happened that night. I ran it through the same code path the app uses, and this is what it does:

- `local_input_to_aware("2026-03-08T02:30", "America/Toronto")` gives `02:30-05:00`. Nothing is wrong yet, but that wall time doesn't exist.
- The diary stores it as `07:30Z`.
- Read back in Toronto, `07:30Z` is `03:30-04:00`. That is the real instant the nonexistent time resolves to.
- `01:30` on that night is stored and shown unchanged, and so is any time outside the gap.

`src/nightjar/nudge.py:46` says the same thing: DST-skipped wall times are normalised, so 02:30 becomes 03:30. The 03:30 is correct. The most likely real cause is that the user typed a time their clock never showed. Or they were still thinking in the pre-change offset.

**Product question:** the form accepts an impossible time without telling the user and then displays a different one. No story or requirement covers this. S-114 only asks for correct handling across DST, and that handling is correct here. Whether the form should warn ("02:30 doesn't exist on that date; saved as 03:30") or reject the entry is product's decision. If product wants that, it's a feature request. If you'd like, I can write it up that way.

I didn't touch `bugs/` or the ledger.