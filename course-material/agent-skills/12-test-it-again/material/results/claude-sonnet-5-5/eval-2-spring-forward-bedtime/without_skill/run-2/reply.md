**No, this isn't a bug, so I haven't written a repro script.**

8 March 2026 is the day Toronto springs forward. At 02:00 EST the clocks jump straight to 03:00 EDT. The wall-clock time 02:30 never happens that day.

I checked what the app does with that input. `local_input_to_aware` in `src/nightjar/diary.py:151` attaches the zone to `2026-03-08T02:30`, which gives `02:30-05:00`. That is 07:30 UTC. The diary stores UTC and displays it in the night's zone, which is 03:30 EDT. So 03:30 is the real clock time of the instant that 02:30 maps to. It is also the usual behaviour for a nonexistent local time. The stored instant is valid and the duration maths isn't affected.

If you actually went to bed an hour after 01:30 EST, 03:30 EDT is the correct entry.

The app does change what you typed without telling you. A message such as "02:30 doesn't exist on that date; recorded as 03:30" would be a reasonable enhancement. Nothing in the docs requires it, and the app isn't wrong without it, so I'd call it a UX suggestion and not a defect. I can file that as an enhancement if you want.