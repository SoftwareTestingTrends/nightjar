Not a bug. It's intended behavior, so I'm not writing a repro.

`Night.night_of` (`src/nightjar/models.py:43-45`) deliberately labels a night by the evening it began. Its docstring says "a 00:15 bedtime on Sunday is Saturday night". The requirements say the same thing: S-116 AC1 states that "a 00:15 bedtime on Sunday counts as Saturday night". So your 00:15 bedtime on Sunday 15 November shows as Saturday 14 November because the code works that way on purpose.

The code does this by subtracting 12 hours from the local bedtime before taking the date. That puts any bedtime from noon to noon on the same label, so it works across midnight.

If you'd rather the diary label a night by the calendar day you fell asleep, that's a product change. It would mean changing S-116 AC1, `night_of`, and the tests that depend on it. A cheap alternative is to show the bedtime's actual date in the diary row next to the "night of" label. Tell me if you want either.