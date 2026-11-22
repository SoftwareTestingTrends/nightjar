**This isn't a bug, so I haven't written a repro script.**

8 March 2026 is the spring-forward night in Toronto. At 02:00 EST the clocks jump straight to 03:00 EDT, so 02:30 never happened that night.

I ran the app's own input conversion (`local_input_to_aware`) to check:

| Input (America/Toronto) | Stored as UTC | Shown as |
|---|---|---|
| 01:30 | 06:30 | 01:30 EST |
| 02:30 | 07:30 | 03:30 EDT |
| 03:30 | 07:30 | 03:30 EDT |

The 02:30 you typed is a time that doesn't exist. Python's `zoneinfo` reads it using the pre-jump offset (EST, UTC−5), which gives 07:30 UTC, and that is 03:30 EDT. The app stores the instant in UTC and displays it in the night's zone, as `CLAUDE.md` requires. There's no time-zone or offset error in the conversion.

There is a small usability gap. The form accepts a time that doesn't exist and shifts it by an hour without telling the user. That is a possible enhancement, for example a validation message like "02:30 doesn't exist on 8 March in America/Toronto". Nothing in S-114 or the requirements asks for it, so I wouldn't call it a defect. If you want it, I can file it as an enhancement. Don't write a repro that "fails" on it, since the current behaviour is the standard handling of a DST gap.