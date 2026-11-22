Yes, it's a bug, and I've confirmed it. It reproduced 3 of 3 runs.

**What happens:** 8 March 2026 is the spring-forward night in Toronto, when clocks jump from 02:00 to 03:00. So 02:30 doesn't exist that night. `local_input_to_aware` in `src/nightjar/diary.py` stamps the zone on the typed time, and that resolves to 07:30 UTC, which is 03:30 EDT. The night is accepted with no warning, and its duration comes out an hour short.

**What should happen:** No requirement or story covers this, so the report says "Not specified". I added a question for product: reject the time with a message, or shift it with a visible notice? The same question applies to CSV import and to the repeated 01:30 hour in autumn. The repro treats "not silently changed" as fixed. Either answer makes it exit 0.

**Files:**
- `bugs/D-1-dst-gap-bedtime-shifted/repro.py` exits 1 while the bug is present and 0 once fixed.
- `bugs/D-1-dst-gap-bedtime-shifted/report.md`
- `bugs/ledger.md`, which has the D-1 row with status `confirmed` and tracker `not filed`.

**Next step:** filing changes something the team sees, so I haven't done it. To file it, run:

`/file-bug bugs/D-1-dst-gap-bedtime-shifted`