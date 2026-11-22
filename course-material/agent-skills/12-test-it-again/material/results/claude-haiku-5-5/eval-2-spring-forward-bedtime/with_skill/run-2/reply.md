It reproduces, but I'm not sure it's a defect. The requirements don't say what should happen to a time that doesn't exist, so I've recorded it as confirmed with an open question for product, per the triage procedure.

**What happens:** 8 March 2026 is the spring-forward date in Toronto. Clocks went from 02:00 straight to 03:00, so 02:30 never occurred. The app accepts a 02:30 entry without a message and shows it as 03:30 EDT. That's because `local_input_to_aware` uses `replace(tzinfo=...)` with `fold=0`, which picks the pre-transition offset (-05:00). The instant stored is 07:30 UTC, which displays as 03:30 EDT.

**Why I lean towards "not a bug":** `nudge.at_local_time` deliberately maps a skipped wall time forward to the next real instant (02:30 becomes 03:30), and `test_T_114_6_nudge_time_skipped_by_dst_moves_forward_an_hour` locks that in. The diary is consistent with that convention. The open question is whether the diary should refuse the impossible time instead. That's product's call, so I haven't decided it.

**What I wrote:**
- `bugs/D-1-dst-gap-bedtime/repro.py`: exits 1 while the entry is accepted and shown as 03:30 EDT, and 0 once it's refused with a `ValueError`. The "refuse" fix is my assumption. If product wants a different outcome, the exit-0 condition needs changing.
- `bugs/D-1-dst-gap-bedtime/report.md`: "Expected" is "Not specified", with three questions for product. The third asks whether the reporter meant 01:30 EST, which may make this a data-entry mistake.
- `bugs/ledger.md`: a new file with one row, D-1, status `confirmed`, tracker `not filed`.

**Verification:** `repro.py` run three times gave exit 1 each time, printing `BUG PRESENT: entered 02:30 on 2026-03-08, diary shows 03:30 EDT`. I used a temporary database, not `nightjar.db`. I didn't run `make test` or `make lint` because I changed nothing in `src/` or `tests/`. `bugs/` is gitignored.

If product decides this is intended behaviour, the ledger row can be updated and the bundle closed. If you want it tracked, run `/file-bug bugs/D-1-dst-gap-bedtime`. I haven't filed anything.