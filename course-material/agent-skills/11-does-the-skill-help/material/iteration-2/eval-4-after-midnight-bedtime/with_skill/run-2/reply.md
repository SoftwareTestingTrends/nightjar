This isn't a bug, so I didn't write a repro script, a bundle or a ledger row.

The diary column is headed "Night of", and a night is labelled by the evening it began. A bedtime of 00:15 on Sunday 15 November is therefore shown as Sat 14 Nov. I confirmed this by running a night with bedtime 2026-11-15 00:15 in America/Toronto. `night_of` returned 2026-11-14, shown as "Sat 14 Nov".

The code and docs agree on this:
- `src/nightjar/models.py:43-45` documents it: "a 00:15 bedtime on Sunday is Saturday night". It computes the date as local bedtime minus 12 hours.
- `docs/stories/S-116.md` AC1 says the same: "a 00:15 bedtime on Sunday counts as Saturday night".
- `docs/stories/S-117.md` AC4 orders nights by this "night of" date.

If the label is confusing, that is a product question about wording. For example, the header could read "Night starting" or show the actual bed date. It isn't a defect, so I haven't filed anything. Tell me if you want that raised with product.