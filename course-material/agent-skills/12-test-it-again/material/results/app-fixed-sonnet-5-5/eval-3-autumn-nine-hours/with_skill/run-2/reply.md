This isn't a bug, so I didn't write a repro script, bundle or ledger row.

DST ended in America/Toronto on Sunday 1 November 2026. At 02:00 the clocks went back to 01:00, so the hour from 01:00 to 02:00 happened twice that night.

- Bedtime at 23:00 on 31 Oct is UTC-4 (EDT).
- Wake at 07:00 on 1 Nov is UTC-5 (EST).
- That makes 9 real hours in bed (03:00 to 12:00 UTC), even though the clock difference is 8.

I checked this by building the night and reading `Night.duration` (`src/nightjar/models.py:52`). It returned `9:00:00`. `duration` subtracts in UTC, which is what the CLAUDE.md DST note requires.

If the app shows "9h", that is correct. The user's "8 hours" is the wall-clock difference. If the product would rather show 8h here, that's a product decision, and nothing in the code is broken.