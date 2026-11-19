# Spec: user-selectable wind-down lead time

| Field | Value |
|---|---|
| Source | `intent/lead-time.md` (Sam, support; "accepted by the product owner") |
| Refines | [BR-07](../docs/requirements/BR-07.md) -> [PR-21](../docs/requirements/PR-21.md) -> [S-114](../docs/stories/S-114.md) |
| Status | Draft for engineering. **Three decisions in section 7 (D1-D3) should be answered before merge.** |

## 1. Summary

Today the wind-down nudge fires a fixed 45 minutes before the user's usual
bedtime (`WIND_DOWN_LEAD` in `src/nightjar/nudge.py`). The intent lets a user
choose **30, 45 or 60 minutes** on the settings form. Anyone who never chooses
keeps 45, so existing behaviour does not change.

The scheduling change is small. The real work: it **changes an approved
requirement** (PR-21 item 3 and S-114 AC1 both say "45"), it brushes against
Regulatory-owned copy, and 45 is hard-coded in more places than `nudge.py`.

## 2. Requirements

| Id | Requirement |
|---|---|
| LT-1 | The user can choose a lead time of 30, 45 or 60 minutes. No other value is accepted. |
| LT-2 | The default is 45. A user who never chose, and every existing database, behaves exactly as today. |
| LT-3 | The nudge is scheduled `lead` minutes before the usual bedtime, in the user's current local time (S-114 AC1 with 45 replaced by `lead`). |
| LT-4 | AC2 (follows a zone change from the next day), AC3 (quiet hours deliver silently, never skip), AC4 (copy only from the register) and the cold-start edge (fewer than 7 nights, no nudge) hold for every lead value. |
| LT-5 | Correct across DST in America/Toronto and Europe/London for all three values (S-114 NFR). |
| LT-6 | The choice is persisted, survives restarts, and survives saving other settings (zone, quiet hours). |
| LT-7 | Invalid input is rejected with a visible error (HTTP 400 on the form, like a bad zone) and nothing is saved. |
| LT-8 | The settings form shows the current lead; `/api/nudge` reports it. |
| LT-9 | Nothing the app says about timing (nudge, coach, settings copy) contradicts the chosen lead. |

Out of scope: arbitrary minute values, per-weekday leads, real push delivery
(still out of scope per PR-21), any change to how the usual bedtime is computed.

## 3. Design

### 3.1 Data model (`models.py`, `diary.py`)

- Add `User.wind_down_lead_minutes: int = 45`, validated in `__post_init__` against
  `ALLOWED_LEAD_MINUTES = (30, 45, 60)`; raise `ValueError` otherwise. Store plain
  minutes (an `int`, not a `timedelta`) so form, JSON and SQL stay simple.
- `user_settings` gains `wind_down_lead_minutes INTEGER NOT NULL DEFAULT 45`.
  **A migration is required**: `CREATE TABLE IF NOT EXISTS` does not add a column
  to an existing database. On startup, check `PRAGMA table_info(user_settings)` and
  `ALTER TABLE ... ADD COLUMN` if missing.
- `save_user` uses a positional `INSERT OR REPLACE ... VALUES (1, ?, ?, ?, ?)`.
  Rewrite with named columns, otherwise values shift or the insert fails.
- `DEFAULT_USER` picks up the default of 45.

### 3.2 Scheduling (`nudge.py`)

- Remove the module constant `WIND_DOWN_LEAD`. Inside `next_nudge`, use
  `timedelta(minutes=user.wind_down_lead_minutes)` with the existing `clock_minus`.
- Keep the current method: wall-clock subtraction from the usual *local* bedtime,
  then `at_local_time`. Do not subtract from a datetime (see CLAUDE.md DST notes).
  Known edge: C4.
- The lead is a property of the user *now*. It must not enter `sleep_window.py`
  or be applied to past nights.
- `Nudge` and the register-backed `nudge_text` are unchanged (C2).

### 3.3 Web (`web.py`, `templates/index.html`)

- `POST /settings` gains `wind_down_lead: str = Form("")`. **Absent or empty means
  "keep the saved value", not "reset to 45".** Existing API tests post `/settings`
  without the field and must pass unchanged. Parse with `int()`; a `ValueError`
  takes the existing 400 path.
- The handler builds a fresh `User(...)` from the form. It must carry the saved
  lead over from `diary.user()`, or every zone/quiet-hours save would reset it.
- Template: `<select name="wind_down_lead" data-testid="settings-lead">` with the
  three options, preselected from the user. Label "Wind down before bedtime";
  options "30 minutes", "45 minutes", "60 minutes". No "recommended" or efficacy
  wording (C2).
- `/api/nudge` adds `"lead_minutes"` inside `nudge` (additive, non-breaking).
- Optional: the muted line under the nudge shows "30 min before your usual bedtime".

### 3.4 Coach (`coach/mock.py`, `coach/prompts/system.md`)

`MockCoach` says "About 45 minutes before, start to wind down", so a user on 30 or
60 would hear a different number from the coach than from the nudge (LT-9).
Options:

1. **Preferred: make the mock number-free** ("A little before bedtime, start to wind
   down..."). No prompt change, no hash change; the real model is never told 45.
2. Pass the lead in the diary summary built by `build_user_message` and have the
   mock read it. Leaves `system.md` alone but widens the data flow.

Run `make evals` either way; expect `8/8 cases at or above 100% pass rate`.
Editing `system.md` changes the prompt version hash and makes evals mandatory.

### 3.5 Quiet hours (the intent's open question)

Keep the current rule: quiet hours are judged against the **nudge time**
(`in_quiet_hours(user, nudge_time)`). No new code; a longer lead can move the
nudge out of, or into, quiet hours. See D1.

Bedtime 23:00, quiet 22:00-07:00 (start inclusive): 60 -> 22:00 silent, 45 -> 22:15
silent, 30 -> 22:30 silent. Quiet 22:20-07:00: 60 and 45 are not silent, 30 is
silent. The nudge is never skipped (AC3).

## 4. Documents to update (this is a requirement change; say so in the PR)

- `docs/requirements/PR-21.md` item 3: "user-chosen lead time of 30, 45 or 60
  minutes; default 45."
- `docs/stories/S-114.md`: AC1 wording and Notes; add an AC for the setting (or a
  new story if D3 says so).
- `docs/traceability.md`: rows for the new ids.
- `README.md` line 15 ("45 minutes before your usual bedtime").

## 5. Test plan

| Id | Test |
|---|---|
| T-114-1 | Existing `test_T_114_1_*` pass untouched (default 45). Add parametrised 30/45/60 -> 22:30/22:15/22:00 for a 23:00 bedtime. |
| T-114-2 | Zone change with a 60-minute lead: London user gets 22:00 local from the next day. |
| T-114-3 | Quiet-hours matrix per lead (3.5 example); `nudge is not None` every time. |
| T-114-4 | Copy still from the register and `check_text`-clean per lead. |
| T-114-5 | Cold start returns `None` per lead. |
| T-114-6 | The four existing DST transitions for 30 and 60; midnight wrap (bedtime 00:10, 60 -> 23:10); the C4 case. |
| T-114-7 (new) | `User(wind_down_lead_minutes=50)` raises; also 0, -5, 45.0. |
| T-114-8 (new) | API: `wind_down_lead=60` persists; absent field preserves it; `abc` and `50` return 400 and save nothing; a zone-only save keeps the lead. |
| T-114-9 (new) | Diary: a database created with the old schema migrates and reads as 45. |
| T-114-10 (new) | Mock coach answer contains no "45". |
| (new) | Settings label text passes `claims.check_text`. |

`make e2e`: extend the Playwright test (or add one) to pick 60 and see the nudge
time move. If Chromium is missing it is skipped; report that rather than "passed".
Do not edit existing tests to make them pass. Only the "45" wording of AC1 changes,
and only because the requirement did.

## 6. Done means

`make test` (count rises from `66 passed, 1 deselected`), `make lint`, `make e2e`,
`make evals` all clean; paste the summary lines.

## 7. Concerns and unresolved conflicts

### Decisions needed

**D1. Quiet hours.** The intent's open question is unanswered. (a) Judge the nudge
time, as in 3.5: zero new logic, AC3 intact. (b) Make quiet hours independent of
the lead (for example judge the usual bedtime), which needs a new definition and
new tests. **Assumed (a); Product to confirm.** AC3 (silent, never skipped) holds either way.

**D2. Should the nudge text mention the lead?** Assumed no (C2).

**D3. Who approves the PR-21 / S-114 change?** The intent says the product owner
accepted it, but BR-07 and PR-21 name Priya N. (Head of Product) as owner and the
intent author is in support. Confirm that acceptance covers rewriting these documents.

### Contradicting policies

**C1. "Everyone else keeps 45" vs. an approved requirement that says 45.**
PR-21 and S-114 AC1 fix the lead at 45, and CLAUDE.md says to fix code rather than
tests and to change a test only when the requirement changed. The two are
reconcilable only by changing the requirement first (section 4) and keeping the
default at 45, which this spec does. Without that approval the feature would
violate the documented acceptance criteria. Engineering cannot resolve this alone.

**C2. Copy that mentions the lead cannot be shipped by engineering.** CLAUDE.md says
new nudge copy goes in `claims/register.yaml`; `docs/claims.md` says register
changes need Regulatory & Brand review, and CLAUDE.md forbids editing the register to
get around a violation. So "Your wind-down starts in 30 minutes" is blocked pending
Regulatory. This spec avoids the conflict: the three existing templates mention no
minutes and are correct for every lead. The settings label is not nudge copy but is
user-facing, so it is checked with `check_text`. Under the wellness-only rule it must
not imply that any option is better for sleep, which support's "too early or too
late" framing could tempt copywriters to do. If Product wants lead-aware copy, that
is a separate Regulatory request, not part of this work.

**C3. Changing the lead mid-evening can cost a night's nudge.** The next nudge is
recomputed from the injected `now`. If the nudge was 22:15 (45) and the user picks
60 at 22:05, 22:00 has passed, so the next nudge is tomorrow 22:00 and tonight gets
none. Acceptable and consistent with the existing "after the time, roll to tomorrow"
rule, but support should know.

### Technical risks

**C4. DST gaps and a longer lead.** The nudge time is bedtime clock time minus the
lead, then pinned to a real instant. If that wall time lands in the spring-forward
gap (02:00-03:00), `at_local_time` pushes it forward an hour. For a lead of 60 and a
bedtime of 03:00-04:00 that is exactly the bedtime (zero lead); for 30 and 45 the
nudge can land *after* the usual bedtime. It affects one night a year for users with
bedtimes around 02:30-04:00, and the existing test only covers the 45-minute
analogue. On fall-back, ambiguous 01:xx wall times resolve to the first occurrence.
Recommendation: accept, document, and test the behaviour. Subtracting elapsed time
from the bedtime instant would contradict the "usual local bedtime" model used by
AC1/AC2 and their tests. If Product dislikes nudging at or after bedtime, a follow-up
can clamp the nudge to before bedtime.

**C5. Silent regression paths.** (i) positional SQL in `save_user`; (ii) the settings
handler rebuilding `User` and dropping the lead; (iii) no migration for existing
databases; (iv) the coach's hard-coded "45 minutes". Each has a test above.

**C6. Existing tests encode 45.** `test_T_114_1_*`, `test_T_114_6_*` and the Playwright
test rely on the default. They should pass unmodified; if one needs editing, the
default has changed unintentionally.

### Not verified

This spec comes from reading the source, docs and tests. I did not run the suite or
write any code; the 66-test baseline is quoted from CLAUDE.md.
