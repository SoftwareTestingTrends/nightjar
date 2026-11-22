**No, this isn't a bug, so I haven't written a repro script.**

8 March 2026 is the spring-forward night in Toronto. At 02:00 EST the clocks jump straight to 03:00 EDT, so no time between 02:00 and 02:59 exists that night. No instant is labelled "02:30" for the diary to store or show.

I traced what the app does with it:
- `local_input_to_aware` (`src/nightjar/diary.py:151`) attaches `America/Toronto` to `02:30`. Python resolves the missing time using the pre-transition offset, `-05:00`.
- `Diary.add_night` stores that as `2026-03-08T07:30Z`.
- On read, `Night.local_bedtime` converts 07:30Z back to Toronto, which gives 03:30 EDT. That is the diary's 03:30.

The shift is the usual way to handle a skipped hour. Calendar apps do the same. The stored instant is consistent, and durations and `night_of` stay correct. That matches the DST requirement in S-114.

One thing is a gap, but it isn't a defect: the app accepts the impossible time and shifts it with no message. If you'd rather it reject the entry or warn the user, that's a new requirement. I can write a repro once the expected behaviour is decided.

If you really went to bed after the clocks changed, 03:30 is the correct local time. If you went to bed before 02:00, the entry should have been something like 01:30.