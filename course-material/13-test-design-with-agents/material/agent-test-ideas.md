I read `nudge.py`, `sleep_window.py`, `docs/stories/S-114.md` and `tests/test_nudge.py`. I didn't read the other test files, so I haven't checked those for overlap. Nothing was run or changed. Existing coverage is AC1–AC4, the cold start at 6 nights, and DST for Toronto and London. The ideas below are gaps, grouped by risk. The first group are places where I think the current code may be wrong.

## Likely bugs

**1. Quiet hours when DST shifts the nudge time**
- Input: Toronto user, quiet hours 03:00–07:00, usual bedtime 02:45, `now` = 7 Mar 2026 12:00.
- Expected: the nudge is at 03:00 EDT, which is inside quiet hours, so `silent is True`.
- Why: `next_nudge` calls `in_quiet_hours(user, nudge_time)` with the nominal 02:00, not the real `at.time()`. The nudge fires at 03:00 but is judged as 02:00, so it is wrongly loud. This is the only place where AC3 and the DST requirement interact, and neither has a test.
- Mirror case: quiet hours 01:00–02:30 would wrongly mark the 03:00 nudge as silent.

**2. Fall-back repeated hour**
- Input: bedtime 02:15, so the nudge is 01:30. Toronto, `now` = 31 Oct 2026 12:00 (the clocks fall back on 1 Nov).
- Expected: `at` is the first 01:30, which is EDT (05:30 UTC), with `fold=0`.
- Why: the existing fall-back test uses 22:15, which is never ambiguous. Neither of the existing "which instant" tests covers a wall time that occurs twice.
- Follow-up: `now` = 06:00 UTC on 1 Nov, which is the second 01:30 (EST). Expected: the next nudge is 2 Nov, not a repeat of 1 Nov.

**3. London nudge time skipped by DST**
- Input: bedtime 01:45, so the nudge is 01:00, which doesn't exist on 29 Mar 2026. `now` = 28 Mar 12:00.
- Expected: 02:00 BST (01:00 UTC).
- Why: the Toronto equivalent exists, but the London spring-forward is only tested at 22:15.

## Midnight and day roll-over (the "things agents get wrong" list)

**4. Bedtime just after midnight**
- Input: usual bedtime 00:10 (nights at 00:10), Toronto, `now` = 20 Mar 12:00.
- Expected: `at` = 20 Mar 23:25. `text` contains "00:10".
- Why: `clock_minus` wrapping appears only in its docstring. Nothing tests the nudge landing on the evening before the bedtime.

**5. Nudge when `now` is already past midnight**
- Input: bedtime 00:30, nudge 23:45, `now` = 21 Mar 00:10.
- Expected: `at` = 21 Mar 23:45. This is the next nudge after `now`, and the 20 Mar 23:45 one has already passed.
- Why: pins the "after midnight, still up" behaviour so a refactor can't silently change it.

**6. Mixed bedtimes across midnight, through the nudge**
- Input: 4 nights at 23:30 and 4 nights at 00:30.
- Expected: the median is 00:00, so the nudge is 23:15.
- Why: `test_sleep_window.py` has midnight crossing, but nothing checks it end to end. A naive median would give about 12:00.

**7. `now` exactly at, and one minute before or after, the nudge time**
- Input: `now` = 20 Mar 22:15:00, then 22:14:59, then 22:15:01 (Toronto, 23:00 bedtime).
- Expected: 21 Mar, 20 Mar 22:15, 21 Mar.
- Why: the `<=` boundary in `next_nudge` is untested. Changing it to `<` would fire the nudge twice.

**8. UTC date differs from the user's local date**
- Input: `now` = 21 Mar 02:00 UTC, which is 20 Mar 22:00 in Toronto.
- Expected: `at` = 20 Mar 22:15 Toronto, which is 15 minutes from now.
- Why: `today` is taken from the user's zone. The existing any-zone test uses midday, where the dates agree, so using the UTC date would still pass.

## Quiet-hours edges (AC3)

**9. Boundaries**
- Input: nudge at 22:15 with quiet hours starting 22:15, then ending 22:15.
- Expected: silent when the nudge equals `quiet_start`. Not silent when it equals `quiet_end`.
- Why: `start <= t < end` is half-open and nothing tests either edge.

**10. Partial or degenerate settings**
- Input: only `quiet_start` set. Separately, `quiet_start == quiet_end`.
- Expected: not silent in both cases, and the nudge is still returned.
- Why: the equal case is ambiguous (never silent, or 24 hours silent?). The story is silent on it, so this test would force the product decision.

**11. Quiet hours follow the current zone**
- Input: quiet hours 22:00–07:00 and nights recorded in London. The user is now in Toronto and `now` is in Toronto.
- Expected: judged against Toronto local time, so `silent=True` for a 22:15 Toronto nudge.
- Why: the wellness-app hazard of reading things in the wrong zone applies to quiet hours too.

## Inputs and data shape

**12. Exactly 7 nights, and the empty list**
- Input: 7 nights, then `[]`.
- Expected: a `Nudge` for 7 nights, `None` for none.
- Why: the existing edge test only checks 6, so a `<=` mistake would pass it.

**13. Nights recorded in another zone, user now elsewhere**
- Input: 7 nights at 23:00 London local, user timezone Toronto.
- Expected: nudge at 22:15 Toronto, not 17:15.
- Why: the per-night-zone logic is tested for `usual_bedtime`, but not that the nudge reapplies the clock time in the new zone (AC2 with real mixed data).

**14. Unsorted and more than 14 nights**
- Input: 20 nights shuffled, with the 6 oldest at 03:00 and the 14 recent at 23:00.
- Expected: 22:15.
- Why: checks that the 14-night window and sorting survive passing through `next_nudge`.

**15. Median rounding on an even count**
- Input: 14 nights, with 7 at 22:00 and 7 at 22:01.
- Expected: a defined result, either 21:15 or 21:16, written into the test.
- Why: `round()` uses banker's rounding, so the result depends on parity and is easy to break unnoticed.

## Copy (AC4)

**16. Copy and bedtime text track the nudge date, not `now`**
- Input: `now` after today's nudge (22:30 on 20 Mar), then compare with `now` = 12:00 on 21 Mar.
- Expected: both give the same `at` and the same `text`. Consecutive days give different templates when the register has 2 or more.
- Why: `nudge_text` uses `at.date()`, so a rollover changes the template. This pins that behaviour and the "varies by day" docstring.

**17. Bedtime formatting in the text**
- Input: bedtime 00:05 and 09:05 (zero padding).
- Expected: "00:05" and "09:05" in `text`, and `check_text` is clean.
- Why: the AC4 test only uses "23:00". The rendered time is the one dynamic part of the text.

**18. Register with one template, or an empty `nudge_copy`**
- Input: monkeypatch `load_register`.
- Expected: one template works on all days. An empty list fails loudly rather than raising an opaque `ZeroDivisionError`.
- Why: the modulo makes an empty register a division by zero. It's low priority but cheap.

## Contract

**19. Returned `at` is aware, in the user's zone, and strictly after `now`**
- Input: a sweep of `now` over the 48 hours around each DST change in both zones.
- Expected: `at.tzinfo == user zone`, `at > now`, and `at - now <= 24h` (25h on fall-back days).
- Why: a property-style check on the main invariants that would catch the DST skips and repeats above without a case per date.

**20. Invalid user timezone**
- Input: `User(timezone="Mars/Olympus")`.
- Expected: a clear error from `zone()`, and no partial `Nudge`.
- Why: the zone field comes from user input via the API.

If you only add some, I'd start with 1, 2, 7, 8 and 9. #1 looks like a real defect, and the rest guard the specific hazards listed in `CLAUDE.md`. New tests would need `T_114_n` names and a row in `docs/traceability.md`. #1 belongs under T-114-3 or T-114-6, and #10 and #11 under T-114-3.
