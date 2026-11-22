This isn't a bug, so I haven't written a repro script.

Daylight saving time ended in America/Toronto at 02:00 on Sunday 1 November 2026, when clocks went back to 01:00. That made your night one hour longer on the clock:

- Bed at 23:00 on 31 Oct is UTC−4 (EDT).
- Wake at 07:00 on 1 Nov is UTC−5 (EST).
- The real elapsed time is 9 hours, not the 8 you get from subtracting the two wall-clock times.

I ran `Night.duration` (`src/nightjar/models.py:52`) on that night and it returned `9:00:00`. It converts both times to UTC before subtracting, which is what `CLAUDE.md` says to do. The 9h is correct.

If you want the diary to show what the clock said instead, that would be a feature request rather than a bug fix. A short note beside the night, such as "clocks went back; 9h elapsed", might also stop it looking wrong.