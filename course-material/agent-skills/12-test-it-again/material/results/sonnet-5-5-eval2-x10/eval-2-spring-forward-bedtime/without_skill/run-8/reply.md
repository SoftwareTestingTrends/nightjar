**No, this isn't a bug, so I haven't written a repro.**

Clocks in Toronto jumped from 02:00 straight to 03:00 on 8 March 2026 (spring forward). A local time of 02:30 never happened that night.

I checked what the app does with that input. `local_input_to_aware("2026-03-08T02:30", "America/Toronto")` returns `02:30-05:00`, which is 07:30 UTC. Toronto's wall clock read 03:30 at that instant, so the diary shows 03:30. That is the standard way to resolve a time that doesn't exist, and the stored instant is consistent. Nothing downstream is wrong.

The one rough edge is that the app moves your input forward an hour without telling you. The docs don't say how it should handle a time that doesn't exist. BR-07 only asks that it "works for users who … live through daylight-saving changes". If you want, I can propose a requirement for this, such as rejecting or warning on a nonexistent local time. I'd treat that as an enhancement, not a defect.