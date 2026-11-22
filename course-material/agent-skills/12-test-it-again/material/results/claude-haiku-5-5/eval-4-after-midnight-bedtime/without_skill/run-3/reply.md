Not a bug, so I didn't write a repro script.

A 00:15 bedtime on Sunday 15 November is listed under **Saturday 14 November**, and that is intended. Your bedtime is the end of Saturday night, not the start of Sunday's. Sleep diaries conventionally file after-midnight bedtimes under the evening they started.

- **The spec says so.** `docs/stories/S-116.md` AC1 reads: "A night belongs to its 'night of' date as shown in the diary (a 00:15 bedtime on Sunday counts as Saturday night)."
- **The code does it.** `Night.night_of` in `src/nightjar/models.py:43-45` takes the local bedtime, subtracts 12 hours, and uses that date. I ran it on a Toronto 00:15 Sunday 15 November bedtime and got `night_of = 2026-11-14 Saturday`.

The rule is anchored at noon, so bedtimes before noon count toward the previous day's night and bedtimes from noon onward count toward that same day's night. If you want the diary to show Sunday, that would change the spec, not the code, and it would also move the S-116 weekly window.