# Test cases for S-117: Export the diary as CSV

Story: [S-117](../stories/S-117.md). Traces to [BR-07](../requirements/BR-07.md).

## Test data

- **Default user:** Sam, America/Toronto. Other users: Lee (Europe/London), Ana (America/Toronto, then Europe/London).
- **Default "now":** Thu 19 Nov 2026 10:00, America/Toronto. Cases that use another "now" say so.
- **Standard night:** bed 23:00, wake 06:30 local. **After-midnight night:** bed 00:25, wake 08:00, "night of" is the day before.
- **Data sets:** D-empty, D-week (Sam, nights of 12 to 18 Nov 2026), D-dst, D-notes, D-1000 (see `references/test-data.md`).
- **Notes N1 to N8:** the exact values in `references/test-data.md`.
- **Daylight saving 2026:** Toronto 8 Mar (forward) and 1 Nov (back). London 29 Mar (forward) and 25 Oct (back).
- "Open the file" means open the downloaded file in a plain text editor, not a spreadsheet, unless a case says otherwise.

## AC1: Export CSV button and file name

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button downloads a correctly named file | 1. Sam with D-week. 2. Now = Thu 19 Nov 2026 10:00 Toronto. 3. Open the home page. 4. Select "Export CSV". | The button is on the home page. A file named `nightjar-diary-2026-11-19.csv` downloads. |
| TC-117-2 | Date rolls over at local midnight | 1. Sam with D-week. 2. Export at Thu 19 Nov 23:59 Toronto. 3. Export again at Fri 20 Nov 00:00 Toronto. | First file is `nightjar-diary-2026-11-19.csv`. Second file is `nightjar-diary-2026-11-20.csv`. |
| TC-117-3 | The name uses the local date, not the UTC date | 1. Sam with D-week. 2. Now = Thu 19 Nov 2026 21:00 Toronto (02:00 UTC on Fri 20 Nov). 3. Export. | File is `nightjar-diary-2026-11-19.csv`, not `...-11-20.csv`. |
| TC-117-4 | The name follows the user's current time zone after a change | 1. Ana switches her time zone from Toronto to London. 2. Now = Fri 20 Nov 2026 03:00 London (Thu 19 Nov 22:00 Toronto). 3. Export. | File is `nightjar-diary-2026-11-20.csv`. |
| TC-117-5 | Single-digit month and day are zero-padded | 1. Sam with D-week. 2. Now = Sun 8 Mar 2026 10:00 Toronto, the day of the spring change. 3. Export. | File is `nightjar-diary-2026-03-08.csv`. |

## AC2: Header row and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-6 | Header row is first and exact | 1. Sam with D-week. 2. Export. 3. Open the file. | Line 1 is exactly `bedtime,wake_time,timezone,notes`: lower case, this order, no spaces, no extra columns. |
| TC-117-7 | One data row per night, four fields each | 1. Sam with D-week. 2. Export. 3. Count rows and fields. | The file has the header plus 7 data rows. Every row has 4 fields. |
| TC-117-8 | The `timezone` column names the night's zone | 1. Lee logs one standard night. 2. Sam logs one standard night. 3. Export each user's diary. | Lee's row has a London time zone value. Sam's row has a Toronto time zone value. See open question 1 for the format. |

## AC3: ISO 8601 times with the night's own UTC offset

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-9 | Offset is the one in force on that date | 1. Sam logs a standard night for Tue 17 Nov 2026 and for Tue 16 Jun 2026. 2. Export. | Nov row: bedtime `2026-11-17T23:00:00-05:00`, wake `2026-11-18T06:30:00-05:00`. Jun row: bedtime `2026-06-16T23:00:00-04:00`, wake `2026-06-17T06:30:00-04:00`. |
| TC-117-10 | Toronto night across a daylight-saving change | 1. Sam logs standard nights for Sat 7 Mar and Sat 31 Oct 2026 (D-dst). 2. Export. | 7 Mar: bedtime `2026-03-07T23:00:00-05:00`, wake `2026-03-08T06:30:00-04:00`. 31 Oct: bedtime `2026-10-31T23:00:00-04:00`, wake `2026-11-01T06:30:00-05:00`. The two offsets in one row differ. |
| TC-117-11 | London night across a change, zero offset | 1. Lee logs standard nights for Sat 28 Mar and Sat 24 Oct 2026 (D-dst). 2. Lee also logs one for Tue 17 Nov. 3. Export. | 28 Mar: bedtime `2026-03-28T23:00:00+00:00`, wake `2026-03-29T06:30:00+01:00`. 24 Oct: bedtime `2026-10-24T23:00:00+01:00`, wake `2026-10-25T06:30:00+00:00`. 17 Nov: both `+00:00`. See open question 2 for `+00:00` or `Z`. |
| TC-117-12 | The repeated hour on fall-back day keeps both offsets | 1. Sam logs a night with bed Sat 31 Oct 23:00 and wake Sun 1 Nov 01:30 EDT. 2. Sam logs a second night, wake Sun 1 Nov 01:30 EST (the second 01:30). 3. Export. | First wake is `2026-11-01T01:30:00-04:00`. Second wake is `2026-11-01T01:30:00-05:00`. Both are valid and not the same instant. See open question 3. |
| TC-117-13 | Each night keeps its own zone after the user travels | 1. Ana logs a standard night for Mon 16 Nov in Toronto. 2. Ana switches to London. 3. Ana logs a standard night for Wed 18 Nov. 4. Export. | 16 Nov row: `-05:00` offsets, Toronto zone. 18 Nov row: `+00:00` offsets, London zone. The Toronto row is not rewritten to London time. |

## AC4: Order, oldest "night of" first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-14 | Nights logged out of order are sorted | 1. Sam logs nights for 15, 12, 18 and 14 Nov (in that order). 2. Export. | Rows are the nights of 12, 14, 15, 18 Nov. |
| TC-117-15 | After-midnight night sorts by its "night of" date | 1. Sam logs a standard night for Sat 14 Nov. 2. Sam logs an after-midnight night, bed Mon 16 Nov 00:25 (night of Sun 15 Nov). 3. Sam logs a standard night for Mon 16 Nov. 4. Export. | Order: night of 14 Nov, night of 15 Nov (bedtime `2026-11-16T00:25:00-05:00`), night of 16 Nov. |
| TC-117-16 | Year boundary | 1. Sam logs a standard night for Wed 30 Dec 2026, an after-midnight night with bed Fri 1 Jan 2027 00:25 (night of Thu 31 Dec), and a standard night for Fri 1 Jan 2027. 2. Export. | Order: night of 30 Dec 2026, night of 31 Dec 2026, night of 1 Jan 2027. |
| TC-117-17 | Order across a daylight-saving change | 1. Sam with D-dst. 2. Export. | Rows run Sat 7 Mar, then later nights, then Sat 31 Oct, with no night repeated or swapped around a change. |

## AC5: Journal notes exactly as entered

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-18 | Commas, quotes and line breaks use standard CSV quoting | 1. Sam with D-notes. 2. Export. 3. Open the file. 4. Check notes N1, N2 and N3. | N1 is `"Slept well, woke once"`. N2 is `"Felt ""rested"" today"`. N3 is quoted with the line break inside the quotes, so the file has one row for that night. |
| TC-117-19 | Non-English text and emoji | 1. Sam with D-notes. 2. Export. 3. Open the file in a plain text editor and in a spreadsheet. | N4 reads `Très bien 😴` in both. No garbled characters. See open question 4 for the byte order mark. |
| TC-117-20 | Spaces and empty notes are kept | 1. Sam with D-notes. 2. Export. 3. Check N5 and N8. | N5 keeps two spaces each side, with no trimming. N8 is an empty fourth field and the row still has 4 fields. |
| TC-117-21 | Text that looks like a formula | 1. Sam with D-notes. 2. Export. 3. Check N6 in a plain text editor. | N6 is `=1+1`, with nothing added in front. See open question 5. |
| TC-117-22 | Very long note | 1. Sam with D-notes. 2. Export. 3. Check N7. | N7 has all 2,000 `a` characters, not cut off. |

## AC6: Round trip through import

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-23 | Plain week | 1. Sam with D-week. 2. Export. 3. Delete all nights so the diary is empty. 4. Import the file. | The diary has the same 7 nights: same bedtime, wake time, time zone and notes. |
| TC-117-24 | Daylight-saving nights | 1. Sam and Lee with D-dst. 2. Export each. 3. Empty each diary. 4. Import each file. | Every night is back with the same instants and the same offsets. No night is an hour shorter or longer. |
| TC-117-25 | Tricky notes | 1. Sam with D-notes. 2. Export. 3. Empty the diary. 4. Import. | All of N1 to N8 match the original text character for character, including the line break in N3 and the spaces in N5. |
| TC-117-26 | Traveller's nights and second export | 1. Ana with a Toronto night and a London night (TC-117-13). 2. Export, empty, import. 3. Export again. | Each night keeps its own zone. The second file has the same rows as the first. Only the file name date may differ. |

## Edge: empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-27 | Empty diary exports the header only | 1. Sam with D-empty. 2. Select "Export CSV". 3. Open the file. | A file named `nightjar-diary-2026-11-19.csv` downloads. It holds only `bedtime,wake_time,timezone,notes`. No data rows. |
| TC-117-28 | Header-only file imports as an empty diary | 1. Import the file from TC-117-27 into an empty diary. | The import succeeds and the diary is still empty. No error. See open question 6. |

## Non-functional: speed

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-29 | 1,000 nights in under 2 seconds | 1. Sam with D-1000. 2. Select "Export CSV". 3. Time from selection to the file being saved. 4. Repeat 5 times. | Every run is under 2 seconds. See open question 7 for how and where to measure. |
| TC-117-30 | Large export is complete | 1. Sam with D-1000. 2. Export. 3. Count rows. | The file has the header plus 1,000 rows, none missing or repeated. |

## Open questions

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | What goes in the `timezone` column: an IANA name such as `America/Toronto`, or an abbreviation? | TC-117-8, TC-117-13 | The IANA name, for example `America/Toronto`, because an abbreviation like EST is ambiguous and the offset alone loses the zone. | Product |
| 2 | For a zero offset, write `+00:00` or `Z`? AC3 says "the UTC offset" and the example uses `-05:00`. | TC-117-11 | Write `+00:00`, so every time has the same shape. | Product |
| 3 | How does a user enter a time in the repeated hour on fall-back day, and which offset applies when they do? | TC-117-12 | The stored instant decides the offset. If entry cannot tell the two apart, drop TC-117-12 and treat the earlier time as `-04:00`. | Product |
| 4 | Should the file start with a UTF-8 byte order mark so spreadsheets show non-English text correctly? | TC-117-19 | No BOM, because AC5 says "exactly as entered" and the importer must read the file back. Product to confirm the spreadsheet behaviour is acceptable. | Product |
| 5 | A note starting with `=` may run as a formula when opened in a spreadsheet. Export as entered, or add a protective prefix? | TC-117-21, TC-117-25 | Export as entered, as AC5 and AC6 require. Product to accept the risk or add a separate story. | Product |
| 6 | Must the importer accept a header-only file? Import is not defined in this story. | TC-117-28 | Yes, it creates zero nights without an error. | Product |
| 7 | Where is the 2-second limit measured: server time, or click to file saved? On what device and connection? | TC-117-29 | Click to file saved, on a mid-range laptop on a normal connection. | Product |
| 8 | Which line ending ends rows and sits inside a note with a line break: `\n` or `\r\n`? | TC-117-18, TC-117-25 | Rows end with `\r\n` as in the CSV standard. A line break in a note is kept as the user entered it. | Product |
| 9 | When two nights in different zones share a "night of" date, or the same night is logged twice, what is their order? AC4 gives no tie-break. | TC-117-13, TC-117-14 | Order by bedtime instant as the tie-break. | Product |
