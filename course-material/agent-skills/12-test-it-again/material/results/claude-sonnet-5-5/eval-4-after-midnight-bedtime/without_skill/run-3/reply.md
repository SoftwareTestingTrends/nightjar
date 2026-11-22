This is by design, so it isn't a bug and I haven't written a repro script.

`Night.night_of` in `src/nightjar/models.py:43` deliberately labels a night by the evening it began. A 00:15 bedtime on Sunday 15 November is "Saturday night", so the diary shows Sat 14 Nov. That matches the docstring ("a 00:15 bedtime on Sunday is Saturday night"). Story S-116 AC1 states the same rule: "a 00:15 bedtime on Sunday counts as Saturday night". The coach prompt and the diary page both use `night_of`, so they're consistent.

If you'd rather see the actual bedtime date, that would be a requirements change. The diary could show the bedtime timestamp or a label like "Sat night (Sun 00:15)". It would also touch S-116 AC1 and any test that depends on this rule. I can draft that change if you want it.