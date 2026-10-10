# Plan: user-selectable wind-down lead time (30/45/60, default 45)

## Context
Intent (`intent/lead-time.md`) and approved spec (`spec/lead-time.md`) let users pick the nudge lead. Today it is the constant `WIND_DOWN_LEAD` (45) in `nudge.py`. This changes an approved requirement (PR-21 item 3, S-114 AC1), so docs change first. Source files checked against the spec: it matches the code (positional INSERT in `diary.py:save_user`, `User` rebuilt in `web.py:save_settings`, "45 minutes" in `coach/mock.py:48`, README:15, PR-21:18, S-114 AC1, traceability row AC1).

## Open decisions (do not block coding, but flag in PR)
- D1 quiet hours: assume (a) judge nudge time, no new logic.
- D2 nudge text: no lead mention (register untouched).
- D3 approval of PR-21/S-114 rewrite by Priya N.: confirm before merge. C1 means docs change lands first.

## Changes from plan review (tester)
- Tests come first, not last: write the tests in "Tests that prove it", run them, and confirm each fails for the right reason before any code. Commit them, then build with the test lock on (`NIGHTJAR_LOCK_TESTS=1`).
- T-114-9 (old-schema migration) is the riskiest step's proof, so it must exist before the `diary.py` change.
- The C4 test must assert the behaviour Product accepted (see decisions), not just "document" it.

## Order of work
1. **Docs (requirement first):** `docs/requirements/PR-21.md` item 3, `docs/stories/S-114.md` (AC1 wording + new AC for the setting), `README.md:15`, `docs/traceability.md` (new rows T-114-7..10 + settings label). State "requirement change" in the PR.
2. **Model:** `src/nightjar/models.py` — `ALLOWED_LEAD_MINUTES = (30, 45, 60)`; `User.wind_down_lead_minutes: int = 45` with `__post_init__` raising `ValueError` for anything else (reject 45.0, bools).
3. **Persistence:** `src/nightjar/diary.py` — add column to `SCHEMA`; migration in `__init__` (check `PRAGMA table_info(user_settings)`, `ALTER TABLE ... ADD COLUMN wind_down_lead_minutes INTEGER NOT NULL DEFAULT 45`); `user()` selects named columns and reads lead; `save_user` uses named-column INSERT. `DEFAULT_USER` gets default.
4. **Scheduling:** `src/nightjar/nudge.py` — delete `WIND_DOWN_LEAD`; use `timedelta(minutes=user.wind_down_lead_minutes)` with existing `clock_minus`; keep `at_local_time`. No change to `sleep_window.py`.
5. **Web:** `src/nightjar/web.py` — `wind_down_lead: str = Form("")`; empty keeps `diary.user().wind_down_lead_minutes`, else `int()` (ValueError -> existing 400 path); carry lead into the rebuilt `User`; add `"lead_minutes"` inside `nudge` in `/api/nudge`. `templates/index.html` — `<select name="wind_down_lead" data-testid="settings-lead">` labelled "Wind down before bedtime", options 30/45/60 minutes, preselected; no efficacy wording. Optional muted line "N min before your usual bedtime".
6. **Coach:** `coach/mock.py:48` make number-free ("A little before bedtime, start to wind down..."). Leave `prompts/system.md` alone (no hash change).
7. **Tests** (below), then verification.

## Tests that prove it
| Id | File | Test |
|---|---|---|
| T-114-1 | `tests/test_nudge.py` | existing tests untouched; add parametrised 30/45/60 -> 22:30/22:15/22:00 (bedtime 23:00) |
| T-114-2 | `test_nudge.py` | London user, lead 60, zone change applies next day at 22:00 local |
| T-114-3 | `test_nudge.py` | quiet-hours matrix per lead (spec 3.5); nudge never None |
| T-114-4 | `test_nudge.py` | register copy and `check_text` clean per lead |
| T-114-5 | `test_nudge.py` / `test_sleep_window.py` | cold start None per lead |
| T-114-6 | `test_nudge.py` | 4 DST transitions for 30 and 60; midnight wrap (00:10, 60 -> 23:10); C4 spring-gap case (document behaviour) |
| T-114-7 | `tests/test_models.py` (new) or `test_diary.py` | `User(wind_down_lead_minutes=...)` raises for 50, 0, -5, 45.0 |
| T-114-8 | `tests/test_api.py` | 60 persists; absent field preserves; `abc` and `50` -> 400 and nothing saved; zone-only save keeps lead; `/api/nudge` reports `lead_minutes` |
| T-114-9 | `tests/test_diary.py` | old-schema DB (create table without column, insert row) migrates and reads 45; reopen persists a chosen lead |
| T-114-10 | `tests/test_coach.py` | mock answer has no "45" |
| new | `tests/test_claims.py` | settings label text passes `claims.check_text` |
| e2e | `tests/e2e/test_add_night_e2e.py` | extend/add: select 60, nudge time moves 15 min earlier; report skipped if Chromium missing |

Never edit existing tests to pass; if one breaks, the default changed by accident (C6).

## Verification
`make test` (count above 66 passed), `make lint`, `make e2e`, `make evals` (`8/8 cases at or above 100% pass rate`). Paste summary lines in the report. Spec's "not verified" caveat: baseline not yet run — run `make test` before starting to confirm 66.

## Known behaviours to document, not fix
C3 mid-evening change can skip tonight's nudge; C4 DST gap can place nudge at/after bedtime for ~02:30-04:00 bedtimes.
