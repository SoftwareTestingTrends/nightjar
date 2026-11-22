No, this isn't a bug, so I haven't written a repro script.

**There was no 02:30 in Toronto on 8 March 2026.** Daylight saving started that night: clocks jumped from 01:59:59 EST straight to 03:00:00 EDT. 02:30 doesn't exist that day, so the app can't store it as a real moment. It has to pick one.

I ran the same conversion the app's add-night form uses (`local_input_to_aware` in `src/nightjar/diary.py:151`):

```
input:  2026-03-08T02:30, America/Toronto
stored: 2026-03-08 02:30-05:00  ==  07:30 UTC
shown:  03:30 EDT (the same instant on the clock that was actually in use)
```

So it reads your 02:30 using the pre-change offset (UTC−5). It saves the instant correctly and shows it on the real clock as 03:30. Nothing is lost:

- **Sleep duration is still right**, because `Night.duration` subtracts in UTC (`src/nightjar/models.py:52`).
- **The behaviour is intended.** `src/nightjar/nudge.py:46` handles the nudge the same way and says so: "02:30 on spring-forward day becomes 03:30". There's also a test for it, `test_T_114_6_nudge_time_skipped_by_dst_moves_forward_an_hour`.
- **No requirement says otherwise.** BR-07, PR-21 and the S-114 DST requirement only ask for correct behaviour across DST changes. None of them says what to do with a skipped time, such as rejecting it or warning.

One gap: the app silently shifts the time without telling you why, which is confusing. If you'd prefer a warning like "02:30 didn't exist on 8 March in Toronto; saved as 03:30", or a rejection asking you to re-enter it, that's a new requirement for Product to decide, not a defect. I can draft it as a story if you want.