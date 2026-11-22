This isn't a bug, so I haven't written a repro script.

The diary's "night of" label is the evening the night began. A bedtime of 00:15 on Sunday 15 November belongs to Saturday night, so the diary correctly shows Sat 14 Nov. Two places say this is deliberate:

- **Code:** `Night.night_of` in `src/nightjar/models.py:43-45` has the docstring "The evening this night began: a 00:15 bedtime on Sunday is Saturday night." It subtracts 12 hours from the local bedtime and takes the date.
- **Spec:** S-116 AC1 in `docs/stories/S-116.md` says "a 00:15 bedtime on Sunday counts as Saturday night".

The label also matches how people talk about sleep. "Saturday night" means the night you go to bed on Saturday evening, even if you fall asleep after midnight.

If you'd still like the diary to show the calendar date of the bedtime, that would be a product change, not a bug fix. It would also touch S-116's windowing, the coach prompt (`coach/base.py` also uses `night_of`), and S-117's "night of" ordering. A clearer column header, such as "Night of (evening started)", might fix the confusion with less change.