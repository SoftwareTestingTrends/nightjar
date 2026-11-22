It isn't a bug, so I didn't write a repro script. The app's 9 hours is the correct elapsed time.

Clocks in Toronto went back an hour at 02:00 on Sunday 1 November 2026, so that night had 25 hours. Your 23:00 bedtime was EDT (UTC−4), and your 07:00 wake was EST (UTC−5):

- 23:00 EDT on 31 Oct = 03:00 UTC on 1 Nov
- 07:00 EST on 1 Nov = 12:00 UTC on 1 Nov
- Elapsed time: 9 hours

I ran the app's own code (`local_input_to_aware` and `Night.duration` in `src/nightjar/models.py`) on those inputs and got `9:00:00`. `Night.duration` subtracts in UTC, which is the handling the CLAUDE.md warns about for DST nights. The 8 hours you expected is wall-clock arithmetic (07:00 − 23:00), which ignores the repeated 01:00–02:00 hour.

If you want the app to show something other than elapsed time for DST-change nights, that's a product decision rather than a defect. I didn't change any files.