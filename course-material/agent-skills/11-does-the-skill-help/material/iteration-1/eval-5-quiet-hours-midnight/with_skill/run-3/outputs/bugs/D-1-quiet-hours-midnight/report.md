# D-1: Quiet hours 21:00 to 00:00 rejected as "invalid time"

Status: not reproduced
Tracker: not filed

## Steps to reproduce
1. Open Settings.
2. Set "Quiet from" 21:00 and "to" 00:00, press Save.

## Expected
Settings save; quiet hours wrap to midnight.

## Actual
Reporter sees "the time is invalid". Not seen here: `POST /settings` with
`quiet_start=21:00&quiet_end=00:00` returns 303 and stores 21:00 / 00:00; `GET /` renders (200).
Only strings a `<input type="time">` can't produce are rejected with 400
(`24:00`, `0:00`, `12:00 AM`). `00:00:00` is accepted.

## Reproducibility
0 of 3 runs (throwaway database each time, via FastAPI TestClient). Browser not tried.

## Repro
None written: no defect shown. Ask the reporter for the exact message, browser/locale
(a 12-hour locale or typed "24:00" would explain it) and a screenshot.
