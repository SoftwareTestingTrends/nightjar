This isn't a bug, so I didn't write a repro, a bundle or a ledger row.

Daylight saving time ended in Toronto at 02:00 on Sunday 1 November 2026, when clocks went back to 01:00. That night had a repeated hour, so 23:00 to 07:00 on the wall clock is 9 real hours.

I confirmed it with `Night` from `src/nightjar/models.py`. Bedtime 23:00 on 31 Oct is UTC-4 and wake time 07:00 on 1 Nov is UTC-5, and `Night.duration` returns `9:00:00`. That is the correct elapsed time. `Night.duration` converts both times to UTC before subtracting, which is what CLAUDE.md prescribes for DST nights. Subtracting the wall-clock times would give the 8 hours you expected, and that would be wrong.

If you want the diary to explain this, for example a "clocks went back, so this night was an hour longer" note, that's a product request. It isn't a defect. I can write it up as a story if you like.