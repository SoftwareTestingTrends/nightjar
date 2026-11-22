# D-1: Quiet hours 21:00–00:00 reported as "invalid time" (not reproduced)

Status: not reproduced
Tracker: not filed

## Steps to reproduce
1. Fresh throwaway database, `create_app(diary=Diary(<tmp>/repro.db))`.
2. `POST /settings` with `timezone=America/Toronto`, `quiet_start=21:00`, `quiet_end=00:00`
   (what the `<input type="time">` fields in Settings submit).

## Expected
Settings are saved. Quiet hours 21:00 to 00:00 are a valid window that wraps midnight,
and `in_quiet_hours` handles it correctly (checked by reading `nudge.py:59`).

## Actual
HTTP 303 redirect to `/`; `diary.user().quiet_end` is `00:00:00`. No "invalid time" error.

## Reproducibility
0 of 3 runs showed the error (API level, TestClient). The browser form was not driven.

## Repro
None written, since the defect did not reproduce. Note the tracker already holds NJ-14
("Quiet hours can't end at midnight", Open, says 23:59 works and 00:00 is rejected with
'Invalid time'). That text appears nowhere in `src/`, and the current code accepts 00:00.
