This isn't a bug, so I haven't written a repro script.

Clocks in Toronto went back an hour at 02:00 on Sunday 1 November 2026, when DST ended. Your night from 23:00 Saturday to 07:00 Sunday therefore had 9 real hours. The 02:00–03:00 hour happened twice, and an 8-hour reading would only come from comparing wall-clock times.

I ran `Night.duration` on your night. Bedtime is at UTC-4 (EDT) and wake-up is at UTC-5 (EST), and it returns `9:00:00`. `Night.duration` in `src/nightjar/models.py` converts both times to UTC before subtracting. That is the approach the project notes require for crossing DST.

If you actually slept 8 hours, check whether the bedtime or wake time was entered a different way than you remember. I can look at the stored row if you want.