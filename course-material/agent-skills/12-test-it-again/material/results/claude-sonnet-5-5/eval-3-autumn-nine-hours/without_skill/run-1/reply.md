This isn't a bug, so I didn't write a repro script.

DST ended in Toronto at 02:00 on Sunday 1 November 2026, when the clocks went back to 01:00. That night had a repeated hour, so 23:00 to 07:00 on the wall clock is 9 hours of real elapsed time.

I checked this by building your night with `Night` and printing the result:
- The bedtime offset is UTC-4 (EDT) and the wake offset is UTC-5 (EST).
- `Night.duration` computes the gap in UTC, as CLAUDE.md requires, and returned `9:00:00`.

Subtracting the wall-clock times gives 8 hours, which is what you did. That figure ignores the extra hour. Your 9h is correct.

If you want the diary to show this, for example with a note that the night spanned a DST change, that would be a feature request rather than a defect.