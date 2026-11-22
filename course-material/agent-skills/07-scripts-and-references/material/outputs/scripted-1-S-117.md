# Test cases for S-117: Export the diary as CSV

Story: [S-117](../stories/S-117.md). Traces to [BR-07](../requirements/BR-07.md).

## Test data

Conventions follow `.claude/skills/write-test-cases/references/test-data.md`.

| Item | Value |
|---|---|
| Default user | Sam, America/Toronto |
| Other users | Lee, Europe/London. Ana, America/Toronto then Europe/London |
| Default "now" | Thu 19 Nov 2026 10:00, America/Toronto (15:00 UTC) |
| Standard night | bed 23:00, wake 06:30 local |
| After-midnight night | bed 00:25, wake 08:00. Night of is the day before |
| Data sets | D-empty, D-week, D-dst, D-notes, D-1000 (see conventions) |
| Notes | N1 to N8 (see conventions) |
| Import | The app's existing CSV import, columns `bedtime,wake_time,timezone,notes` |

Offsets used below: Toronto is -05:00 in winter and -04:00 in summer. London is +00:00 in winter and +01:00 in summer.

## AC1: Export button and file name

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button exists and downloads a correctly named file | 1. Sam has D-week. 2. Now = Thu 19 Nov 2026 10:00 Toronto. 3. Open the home page. 4. Click "Export CSV". | The button is on the home page. A file `nightjar-diary-2026-11-19.csv` is downloaded. |
| TC-117-2 | Date is Sam's local date, not the UTC date | Sam has D-week. Click "Export CSV" at each "now": (a) Thu 19 Nov 20:00 Toronto (01:00 UTC on Fri 20 Nov); (b) Thu 19 Nov 23:59 Toronto; (c) Fri 20 Nov 00:00 Toronto. | (a) `nightjar-diary-2026-11-19.csv`. (b) `nightjar-diary-2026-11-19.csv`. (c) `nightjar-diary-2026-11-20.csv`. |
| TC-117-3 | Date follows the user's current time zone after a change | 1. Ana has nights logged in Toronto. 2. Ana changes her time zone to Europe/London. 3. Now = Fri 20 Nov 00:30 London (Thu 19 Nov 19:30 Toronto). 4. Click "Export CSV". | File name is `nightjar-diary-2026-11-20.csv` (the London date). Before the change, the same instant gives 2026-11-19. |
| TC-117-4 | Export does not change the diary | 1. Sam has D-week. 2. Click "Export CSV" twice. 3. View the diary. | Both files have the same content. The diary still shows the same 7 nights. |

## AC2: Header row and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-5 | Header is the first line and has the exact columns in order | 1. Sam has D-week. 2. Export. 3. Open the file in a plain-text editor. | Line 1 is `bedtime,wake_time,timezone,notes`. No other line repeats it. 7 data lines follow. |
| TC-117-6 | Columns match the import's columns | 1. Compare the exported header with the header the import expects (import help text or sample file). | The two headers are identical, in name and order. |
| TC-117-7 | Every data row has exactly 4 fields | 1. Sam has D-week and D-notes. 2. Export. 3. Parse the file with a CSV reader. | Every row, including those with notes N1 to N4, has exactly 4 fields. |

## AC3: Times in ISO 8601 with the night's own offset

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-8 | Winter night in Toronto uses -05:00 | 1. Sam logs an after-midnight night: bed 00:25 on Sun 1 Mar 2026, wake 08:00. 2. Export. | Bedtime is `2026-03-01T00:25:00-05:00`. Wake time is `2026-03-01T08:00:00-05:00`. |
| TC-117-9 | Toronto night across a daylight-saving change has a different offset at each end | Sam logs standard nights across each change. (a) Spring: bed Sat 7 Mar 23:00, wake Sun 8 Mar 06:30. (b) Fall: bed Sat 31 Oct 23:00, wake Sun 1 Nov 06:30. Export. | (a) Bedtime `2026-03-07T23:00:00-05:00`, wake `2026-03-08T06:30:00-04:00`. (b) Bedtime `2026-10-31T23:00:00-04:00`, wake `2026-11-01T06:30:00-05:00`. |
| TC-117-10 | London night across each change | Lee logs standard nights. (a) Spring: bed Sat 28 Mar 23:00, wake Sun 29 Mar 06:30. (b) Fall: bed Fri 24 Oct 23:00, wake Sat 25 Oct 06:30. Export. | (a) Bedtime `2026-03-28T23:00:00+00:00`, wake `2026-03-29T06:30:00+01:00`. (b) Bedtime `2026-10-24T23:00:00+01:00`, wake `2026-10-25T06:30:00+00:00`. |
| TC-117-11 | Each night keeps its own zone's offset for a traveller | 1. Ana logs a standard night for 12 Nov in Toronto. 2. Ana changes her zone to London and logs a standard night for 17 Nov. 3. Now = Thu 19 Nov 10:00 (London). 4. Export. | The 12 Nov night has offset -05:00 and timezone `America/Toronto`. The 17 Nov night has offset +00:00 and timezone `Europe/London`. The current zone is not applied to the old night. |
| TC-117-12 | Night on a time that does not exist or occurs twice | Sam logs: (a) bed 02:30 on Sun 8 Mar 2026 (skipped hour); (b) bed 01:30 on Sun 1 Nov 2026 (occurs twice). Export. | The app does not export an invalid time. See open question 2 for the exact offsets. |

## AC4: Order, oldest "night of" first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-13 | Nights logged out of order come out oldest first | 1. Sam logs nights for 18, 12, 15, 13 Nov (in that order), then 14, 16, 17 Nov. 2. Export. | Rows are for the nights of 12, 13, 14, 15, 16, 17, 18 Nov, in that order. |
| TC-117-14 | An after-midnight night sorts by its "night of" date | 1. Sam has an empty diary. 2. Log a standard night for Sat 14 Nov (bed 23:00). 3. Log an after-midnight night with bed 00:25 on Sat 14 Nov (the night of Fri 13 Nov), wake 08:00. 4. Export. | The night of Fri 13 Nov (bed `2026-11-14T00:25:00-05:00`) is the first row. The night of Sat 14 Nov (bed `2026-11-14T23:00:00-05:00`) is the second row, even though it was logged first. |
| TC-117-15 | Order across a time zone change | 1. Ana has Toronto nights for 12 to 14 Nov and London nights for 15 to 17 Nov. 2. Export. | Rows run 12 to 17 Nov in order, with the zone changing at the 15 Nov row. |

## AC5: Notes exported exactly as entered

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-16 | Comma, double quotes and line break use standard CSV quoting | 1. Sam has nights with N1, N2, N3. 2. Export. 3. Read the file as text, then with a CSV reader. | N1 is wrapped in quotes. N2 is wrapped in quotes with inner quotes doubled: `"Felt ""rested"" today"`. N3 is wrapped in quotes and keeps the line break. A CSV reader returns the three original notes unchanged. |
| TC-117-17 | Non-English text and emoji | 1. Sam has a night with N4 `Très bien 😴`. 2. Export. 3. Read the file as UTF-8. | The note reads `Très bien 😴` with no garbled characters. |
| TC-117-18 | Leading and trailing spaces, and empty note | 1. Sam has nights with N5 (`  padded  `) and N8 (empty). 2. Export. 3. Read with a CSV reader. | N5 comes back with its two spaces on each side. N8 is an empty field, and the row still has 4 fields. |
| TC-117-19 | Formula-like text is not changed | 1. Sam has a night with N6 `=1+1`. 2. Export. 3. Read the file as text. | The note is exported exactly as `=1+1`. See open question 3 about spreadsheet formulas. |
| TC-117-20 | Very long note | 1. Sam has a night with N7 (2,000 `a`). 2. Export. 3. Read with a CSV reader. | The note comes back as 2,000 `a`, not cut short. |

## AC6: Round trip through the import

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-21 | A plain week round-trips | 1. Sam has D-week. 2. Export. 3. Delete all nights so the diary is empty. 4. Import the file. | The diary has the same 7 nights, with the same bed times, wake times and notes. |
| TC-117-22 | Daylight-saving nights round-trip | 1. Use D-dst (Toronto and London nights across each change). 2. Export. 3. Import into an empty diary. | Every night has the same bed time and wake time as an instant, the same time zone, and the same duration (an hour shorter in spring, an hour longer in fall). |
| TC-117-23 | Tricky notes round-trip | 1. Use D-notes (N1 to N8). 2. Export. 3. Import into an empty diary. | All 8 notes are identical to the originals, including N3's line break, N5's spaces and the empty N8. |
| TC-117-24 | A traveller's nights round-trip | 1. Ana has nights in Toronto and in London (as TC-117-11). 2. Export. 3. Import into an empty diary. | Each night keeps its own time zone and times. The total number of nights is the same. |

## Edge: Empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-25 | Empty diary exports the header only | 1. Sam has D-empty. 2. Click "Export CSV". 3. Open the file in a text editor. | File `nightjar-diary-2026-11-19.csv` downloads. It holds only `bedtime,wake_time,timezone,notes`, with no data rows. |
| TC-117-26 | Diary emptied by deleting nights, and the empty file imports | 1. Sam has D-week. 2. Delete all 7 nights. 3. Export. 4. Import that file into an empty diary. | Export holds the header only. The import gives an empty diary and no error. |

## Non-functional: Performance

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-27 | 1,000 nights export in under 2 seconds | 1. Sam has D-1000. 2. Click "Export CSV". 3. Time from the click until the file is saved. Repeat 3 times. | Each run takes under 2 seconds. See open question 4 for where the timing starts and ends. |
| TC-117-28 | The 1,000-night file is complete | 1. Sam has D-1000. 2. Export. 3. Count rows and compare with the diary. | The file has 1 header row and 1,000 data rows, in order, with notes intact. |

## Open questions

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | What does the `timezone` column hold, and what is its format? The story names the column but not its values. | TC-117-7, TC-117-11, TC-117-22, TC-117-24 | An IANA name such as `America/Toronto`, matching what the import reads. | Product |
| 2 | A bedtime in the skipped hour (02:30 on 8 Mar, Toronto) or the repeated hour (01:30 on 1 Nov, Toronto): which offset is exported? | TC-117-12 | Skipped hour: the app does not accept it, or moves it to 03:30 -04:00. Repeated hour: the first one, `-04:00`. Product to confirm what the diary allows. | Product |
| 3 | Notes starting with `=`, `+`, `-` or `@` can run as formulas in a spreadsheet. The story says "exactly as entered". Do we leave them unchanged? | TC-117-19 | Leave unchanged, as AC5 says. Revisit if a security review asks for it. | Product |
| 4 | Where does the 2-second limit start and end, and on what device and network? | TC-117-27 | From the click to the file being offered for download, on the standard test laptop, with no network delay. | Product |
| 5 | Is a zero offset written as `+00:00` or `Z`? The example only shows non-zero offsets. | TC-117-10 | `+00:00`, so the format is the same for every row. | Product |
| 6 | Is a line break in a note exported as LF or CRLF? And does the file begin with a UTF-8 byte order mark? | TC-117-16, TC-117-17 | Keep the line break as entered (LF). No byte order mark. | Product |
