This isn't a bug, so I haven't written a repro script.

The diary labels each night by the evening it began, not the calendar date of the bedtime. `Night.night_of` in `src/nightjar/models.py:43` does this on purpose:

```python
"""The evening this night began: a 00:15 bedtime on Sunday is Saturday night."""
return (self.local_bedtime - timedelta(hours=12)).date()
```

Your 00:15 bedtime on Sunday 15 November is "Saturday night", so the diary shows Sat 14 Nov. Story S-116 AC1 (`docs/stories/S-116.md`) says the same thing: "a 00:15 bedtime on Sunday counts as Saturday night".

The column could still be confusing, since it just says "Sat 14 Nov" with no hint that the date is the evening the night started. If you'd like it to say something like "Night of Sat 14 Nov", or to show the actual bedtime date, that's a product change to `index.html` and S-116 rather than a defect. I can draft either one.