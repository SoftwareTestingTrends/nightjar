**Not a bug, so I didn't write a repro script.**

2026-03-08 is the spring-forward date in America/Toronto. At 02:00 EST the clocks jump to 03:00 EDT, so no wall-clock time between 02:00 and 02:59 exists that night. A bedtime of "02:30" can't have happened.

I checked how the app handles it. `local_input_to_aware` in `src/nightjar/diary.py:151` attaches the zone to the entered time. For the nonexistent 02:30 it stores 07:30 UTC. Converted back to Toronto local time, that is 03:30 EDT, which is what the diary shows. This is the standard way to resolve a gap (PEP 495, and most calendar apps do the same). The stored instant is a real moment and the 01:30 case is correct.

The one thing I'd flag is that the app moves the time silently. A user who types 02:30 gets 03:30 with no explanation. If you want that handled, it's a UX improvement, such as a validation message on the form. It isn't a defect in the time conversion, and the project instructions don't specify it. I can write that up as an enhancement if you'd like.