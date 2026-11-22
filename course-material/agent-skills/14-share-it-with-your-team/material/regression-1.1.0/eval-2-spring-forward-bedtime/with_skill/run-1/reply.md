**Verdict: not a conversion bug, so I haven't written a repro or a bundle.** There is one open question for product, below.

**What happens.** 8 March 2026 is the spring-forward night in America/Toronto. Clocks jump from 02:00 straight to 03:00, so 02:30 never happens that day. I ran `local_input_to_aware` (`src/nightjar/diary.py:151`) with the zone set to Toronto:

| Input (local) | Stored as UTC | Shown as |
|---|---|---|
| 01:30 | 06:30 | 01:30 EST |
| 02:30 | 07:30 | 03:30 EDT |
| 03:30 | 07:30 | 03:30 EDT |

The 02:30 you logged is a time that doesn't exist, and it is stored as the same instant as 03:30. The diary then shows that instant correctly in Toronto time. Nothing is mis-converted. Python's rule for a missing wall time (`fold=0`) puts it one hour forward, which is what most calendar apps do too.

**What I couldn't decide.** The form accepts 02:30 without any warning, and no requirement or story says what should happen in that case. `docs/stories/S-114.md` only says "correct across daylight-saving transitions". The skill says that choosing "this is fine" is product's call, not mine. I also can't write a repro that exits 0 once fixed, because there is no defined fixed behaviour to check against.

**Question for product.** When someone enters a local time that doesn't exist on a DST gap, should NightJar:
- silently shift it forward (today's behaviour),
- reject it with a 400 error and a message, or
- ask the user to pick a time?

If product picks the second or third option, tell me and I'll triage it as a confirmed bug. I'd write `bugs/D-<n>-dst-gap-input/repro.py` and the ledger row at that point. The ambiguous fall-back hour (01:30 happens twice in November) has the same problem and would go in the same question.

I changed no files.