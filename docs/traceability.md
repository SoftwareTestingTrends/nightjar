# Traceability

BR-07 (consistent wind-down routine)
 -> PR-21 (adaptive reminder from the sleep window)
   -> S-114 (bedtime wind-down nudge)

Test ids appear in test names, so `uv run pytest -k T_114_3` runs everything for AC3.

| Criterion | Test id | Tests |
|---|---|---|
| AC1: `lead` min before usual bedtime (default 45), current local time | T-114-1 | `tests/test_nudge.py::test_T_114_1_*`, `tests/test_api.py::test_T_114_1_import_csv_then_see_the_nudge`, `tests/e2e/test_add_night_e2e.py::test_T_114_1_e2e_*` |
| AC2: follows a time zone change from the next day | T-114-2 | `tests/test_nudge.py::test_T_114_2_*`, `tests/test_api.py::test_T_114_2_changing_time_zone_moves_the_nudge` |
| AC3: silent during quiet hours, not skipped | T-114-3 | `tests/test_nudge.py::test_T_114_3_*`, `tests/test_api.py::test_T_114_3_quiet_hours_setting_makes_nudge_silent` |
| AC4: copy only from the claims register | T-114-4 | `tests/test_nudge.py::test_T_114_4_*` |
| Edge: fewer than 7 nights, no nudge | T-114-5 | `tests/test_nudge.py::test_T_114_5_*`, `tests/test_sleep_window.py::test_T_114_5_*` |
| NFR: correct across DST (Toronto, London) | T-114-6 | `tests/test_nudge.py::test_T_114_6_*` |
| Setting: lead time must be 30, 45 or 60 (default 45) | T-114-7 | `tests/test_models.py::test_T_114_7_*` |
| Setting: chosen lead is saved, validated, preserved and reported | T-114-8 | `tests/test_api.py::test_T_114_8_*`, `tests/e2e/test_add_night_e2e.py::test_T_114_8_e2e_*` |
| Setting: databases from before the setting migrate and read as 45 | T-114-9 | `tests/test_diary.py::test_T_114_9_*` |
| Setting: the coach never contradicts the chosen lead | T-114-10 | `tests/test_coach.py::test_T_114_10_*` |

Supporting tests (not tied to one AC): `tests/test_sleep_window.py` (median,
midnight crossing, 14-night window, per-night zones), `tests/test_claims.py`
(including `test_settings_lead_label_and_options_are_claims_clean`),
`tests/test_coach.py`, `tests/test_diary.py`.

## Coach (no story yet)

Safety behaviour of the coach is covered by `evals/cases/E-01..E-08` (run with
`make evals`) and by `tests/test_coach.py` (claims fallback, tracing, journal fencing).
