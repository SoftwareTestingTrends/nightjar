# Test cases for S-117: Export the diary as CSV

Story: [S-117](../stories/S-117.md) · Traces to [BR-07](../requirements/BR-07.md)
Status: draft for review by Product and Test. Written from the story only, before any code.

## Test data

**User:** Sam. Time zone setting is `America/Toronto` unless a case says otherwise.
**Now:** Thu 19 Nov 2026, 10:00 Toronto (EST, UTC-5) unless a case says otherwise.

Offsets used below (2026):

| Zone | Rule | Offsets |
|---|---|---|
| America/Toronto | DST starts Sun 8 Mar 02:00, ends Sun 1 Nov 02:00 | EST -05:00, EDT -04:00 |
| Europe/London | BST starts Sun 29 Mar 01:00 UTC, ends Sun 25 Oct 01:00 UTC | GMT +00:00, BST +01:00 |

**Diary D1, "standard five" (Toronto, all EST -05:00):**

| Night of | Bedtime | Wake time | Notes |
|---|---|---|---|
| Mon 9 Nov | Mon 9 Nov 23:15 | Tue 10 Nov 07:00 | `Read before bed` |
| Tue 10 Nov | Tue 10 Nov 23:30 | Wed 11 Nov 07:10 | (empty) |
| Wed 11 Nov | Thu 12 Nov 00:20 | Thu 12 Nov 07:45 | `Late call` |
| Thu 12 Nov | Thu 12 Nov 23:00 | Fri 13 Nov 07:00 | `Tea` |
| Fri 13 Nov | Fri 13 Nov 22:50 | Sat 14 Nov 06:50 | `Early night` |

The Wed 11 Nov night (bed 00:20 on Thu) is the "night of" Wed 11 Nov, following the rule in the S-116 example. See open question 1.

**Diary D2, DST and travel nights:**

| Night of | Zone | Bedtime | Wake time |
|---|---|---|---|
| Sat 28 Feb 2026 | Toronto | Sun 1 Mar 00:25 -05:00 | Sun 1 Mar 07:30 -05:00 |
| Sat 7 Mar 2026 | Toronto | Sat 7 Mar 23:00 -05:00 | Sun 8 Mar 07:00 -04:00 (7 h elapsed) |
| Sat 31 Oct 2026 | Toronto | Sat 31 Oct 23:00 -04:00 | Sun 1 Nov 07:00 -05:00 (9 h elapsed) |
| Sat 28 Mar 2026 | London | Sat 28 Mar 23:30 +00:00 | Sun 29 Mar 08:00 +01:00 |
| Sat 24 Oct 2026 | London | Sat 24 Oct 23:30 +01:00 | Sun 25 Oct 07:30 +00:00 |
| Mon 16 Nov 2026 | Asia/Kolkata | Mon 16 Nov 22:30 +05:30 | Tue 17 Nov 06:30 +05:30 |

**Note texts (N-series), used in AC5:**

| ID | Text as entered |
|---|---|
| N-a | `Tired, but calm` (comma) |
| N-b | `He said "go to bed"` (double quotes) |
| N-c | two lines: `Line one` / `Line two` (line break) |
| N-d | `Dormi mal 😴 — café, 夜` (accents, emoji, CJK) |
| N-e | `مرحبا بالعالم` (right-to-left) |
| N-f | `"` (a single quote character) |
| N-g | `,,,` |
| N-h | `  padded  ` (leading and trailing spaces) |
| N-i | `0123` |
| N-j | `=1+1` |
| N-k | `Couldn't treat my insomnia` (words the claims register bans) |
| N-l | a note of 5,000 characters including commas, quotes and 20 line breaks |

---

## AC1: "Export CSV" button downloads `nightjar-diary-YYYY-MM-DD.csv` using today's date in the user's current time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button is on the home page | 1. Log in as Sam with D1. 2. Open the home page. | An "Export CSV" button is visible. |
| TC-117-2 | Click downloads one file with the right name | 1. D1, now = Thu 19 Nov 2026 10:00 Toronto. 2. Click "Export CSV". | One file is downloaded, named `nightjar-diary-2026-11-19.csv`. |
| TC-117-3 | Last minute of the day in Toronto, UTC is already tomorrow | 1. D1, zone Toronto. 2. Now = Thu 19 Nov 23:59 Toronto (04:59 UTC on 20 Nov). 3. Click "Export CSV". | File is named `nightjar-diary-2026-11-19.csv`, not 2026-11-20. |
| TC-117-4 | First minute of the next day | 1. As TC-117-3 but now = Fri 20 Nov 00:01 Toronto. | File is named `nightjar-diary-2026-11-20.csv`. |
| TC-117-5 | Time zone change moves the date | 1. D1. 2. Now = Thu 19 Nov 23:30 Toronto (= Fri 20 Nov 04:30 London). 3. Change the time zone setting to `Europe/London`. 4. Click "Export CSV". | File is named `nightjar-diary-2026-11-20.csv` (London date). Changing the setting back to Toronto and exporting again gives `2026-11-19`. |
| TC-117-6 | Day with a spring-forward change in Toronto | 1. D1. 2. Now = Sun 8 Mar 2026 23:30 EDT (-04:00). 3. Export. | `nightjar-diary-2026-03-08.csv`. |
| TC-117-7 | Day with a fall-back change in Toronto, both 01:30s | 1. D1. 2. Export at Sun 1 Nov 2026 01:30 EDT, then again at 01:30 EST. | Both files are named `nightjar-diary-2026-11-01.csv`. |
| TC-117-8 | London day where UTC is the day before | 1. D1, zone `Europe/London`. 2. Now = Sun 25 Oct 2026 00:30 BST (Sat 24 Oct 23:30 UTC). 3. Export. | `nightjar-diary-2026-10-25.csv`. |
| TC-117-9 | Single-digit month and day are zero-padded | 1. Now = Sun 1 Mar 2026 09:00 Toronto. 2. Export. | `nightjar-diary-2026-03-01.csv`. |
| TC-117-10 | Button works with an empty diary | 1. New user with no nights. 2. Open home page and click "Export CSV". | Button is visible and a file is downloaded (content: see Edge section). |
| TC-117-11 | Button label passes the claims check | 1. Run `docs/claims.md` check on the button text "Export CSV" and any other text this feature shows (tooltips, confirmation or error messages). | No violations from the banned list. Any text beyond "Export CSV" is listed in open question 9. |

## AC2: Header row and the same columns as the import: `bedtime,wake_time,timezone,notes`

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-12 | Header row is exactly the required text | 1. Export D1. 2. Read the first line. | First line is exactly `bedtime,wake_time,timezone,notes`: lowercase, this order, no spaces, no extra columns. |
| TC-117-13 | Header appears once and only first | 1. Export D1 (5 nights). | The file has one header line and 5 data rows. No header text appears in any other row. |
| TC-117-14 | Header matches the import's columns | 1. Compare the export header with the header of the file the import accepts (import documentation or sample file). | The columns are identical in name and order. |
| TC-117-15 | Every data row has 4 fields | 1. Export D1 and D2 together. 2. Parse as CSV. | Every parsed record has exactly 4 fields, including the night with empty notes. |

## AC3: Times are ISO 8601 with the UTC offset that applied in that night's own time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-16 | Story example, winter Toronto | 1. Log a night in Toronto, bed Sun 1 Mar 2026 00:25, wake 07:30. 2. Export. | Row starts `2026-03-01T00:25:00-05:00,2026-03-01T07:30:00-05:00,`. |
| TC-117-17 | Summer Toronto uses -04:00 | 1. Log a Toronto night, bed Tue 14 Jul 2026 23:10, wake Wed 15 Jul 07:00. 2. Export. | Bedtime `2026-07-14T23:10:00-04:00`, wake `2026-07-15T07:00:00-04:00`. |
| TC-117-18 | Night spans the spring-forward change (Toronto) | 1. Use the Sat 7 Mar 2026 night from D2. 2. Export. | Bedtime `2026-03-07T23:00:00-05:00`, wake `2026-03-08T07:00:00-04:00`. Offsets differ in the same row, because each time uses the offset in force at that time. |
| TC-117-19 | Night spans the fall-back change (Toronto) | 1. Use the Sat 31 Oct 2026 night from D2. 2. Export. | Bedtime `2026-10-31T23:00:00-04:00`, wake `2026-11-01T07:00:00-05:00`. |
| TC-117-20 | Night spans spring-forward in London | 1. Use the Sat 28 Mar 2026 London night. 2. Export. | Bedtime `2026-03-28T23:30:00` + the GMT offset (`+00:00`, see open question 4), wake `2026-03-29T08:00:00+01:00`. |
| TC-117-21 | Night spans fall-back in London | 1. Use the Sat 24 Oct 2026 London night. 2. Export. | Bedtime `2026-10-24T23:30:00+01:00`, wake `2026-10-25T07:30:00` + the GMT offset (see open question 4). |
| TC-117-22 | Bedtime in the repeated hour on fall-back day | 1. Toronto, Sun 1 Nov 2026. 2. Log a bedtime of 01:30 EDT (-04:00) on one night and, in a separate diary, a bedtime of 01:30 EST (-05:00) (if the app can record the two). 3. Export each. | `2026-11-01T01:30:00-04:00` for the first and `2026-11-01T01:30:00-05:00` for the second. The two exports are distinguishable. See open question 5. |
| TC-117-23 | A night in a different zone from the current setting | 1. Zone setting = Toronto. 2. Diary has the Asia/Kolkata night from D2. 3. Export. | That row is `2026-11-16T22:30:00+05:30,2026-11-17T06:30:00+05:30,`, using the night's own offset, not -05:00. |
| TC-117-24 | Time zone change between nights | 1. Log a Toronto night of Mon 9 Nov (bed 23:15 -05:00). 2. Change setting to `Europe/London`. 3. Log a night of Tue 10 Nov, bed 23:30. 4. Export. | Row 1 keeps `-05:00`. Row 2 shows London's offset for that date. Offsets are not rewritten to the current zone. |
| TC-117-25 | Current zone changed after logging | 1. Log D1 in Toronto. 2. Change the setting to London. 3. Export. | All D1 rows still show `-05:00`, and the times are unchanged. |
| TC-117-26 | The `timezone` column agrees with the offset | 1. Export D2. | For each row, the `timezone` value (see open question 3 for its format) is the zone whose offset on that date matches the bedtime offset. |
| TC-117-27 | Format of times | 1. Export D1. | Each time matches the pattern `YYYY-MM-DDTHH:MM:SS±HH:MM` (see open question 4 on seconds and `Z`). |

## AC4: Nights are in "night of" order, oldest first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-28 | Standard order | 1. Export D1. | Rows are in order of night of: 9, 10, 11, 12, 13 Nov. |
| TC-117-29 | Entered out of order | 1. Log nights in this order: Fri 13 Nov, Mon 9 Nov, Thu 12 Nov, Tue 10 Nov, Wed 11 Nov. 2. Export. | Rows are Mon 9, Tue 10, Wed 11, Thu 12, Fri 13 (not entry order). |
| TC-117-30 | Past midnight bedtime sorts under the previous date | 1. Log Fri 13 Nov night with bed 22:50 and Wed 11 Nov night with bed Thu 12 Nov 00:20. 2. Also log Thu 12 Nov night, bed 23:00. 3. Export. | Order: Wed 11 (bed 00:20 on 12th), Thu 12 (bed 23:00 on 12th), Fri 13. The 00:20 night comes before the 23:00 night even though both bedtimes fall on 12 Nov. |
| TC-117-31 | Order across a month and a year boundary | 1. Log nights of Wed 31 Dec 2025, Thu 1 Jan 2026, Sat 28 Feb 2026, Sun 1 Mar 2026. 2. Export. | Oldest first in that order. |
| TC-117-32 | Order across DST changes | 1. Export D2. | The rows are in "night of" order: 28 Feb, 7 Mar, 28 Mar, 24 Oct, 31 Oct, 16 Nov 2026. |
| TC-117-33 | Mixed time zones, order follows night of | 1. Log Toronto night of Fri 13 Nov and London night of Thu 12 Nov. 2. Export. | Thu 12 (London) before Fri 13 (Toronto). Behaviour for two nights with the same night-of date in different zones is open question 6. |
| TC-117-34 | One night | 1. Diary with only the Fri 13 Nov night. 2. Export. | Header and exactly one data row. |
| TC-117-35 | Newest night is included | 1. D1 + night of Wed 18 Nov (last night, bed 23:05, wake Thu 19 Nov 07:00). 2. Export at now = Thu 19 Nov 10:00. | The last row is the night of Wed 18 Nov. Nothing is dropped for being recent. |

## AC5: Notes exported exactly as entered, with standard CSV quoting

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-36 | Comma | 1. Log a night with N-a. 2. Export. | The field is `"Tired, but calm"`, quoted. Parsed as CSV, the notes value is `Tired, but calm` and the row still has 4 fields. |
| TC-117-37 | Double quotes | 1. N-b. | Field is `"He said ""go to bed"""` (quotes doubled, field quoted). Parsed value equals N-b. |
| TC-117-38 | Line break | 1. N-c. | Field is quoted and contains the line break. Parsed as CSV, the file has the same number of records as nights and the value equals N-c. A viewer that is not a CSV parser may show two lines. That is fine. |
| TC-117-39 | Non-English text | 1. N-d. 2. Export. 3. Open in a UTF-8 aware tool. | Accents, emoji and CJK appear unchanged, with no `?` or garbled characters. Encoding: open question 7. |
| TC-117-40 | Right-to-left text | 1. N-e. | Value equals N-e, character for character. |
| TC-117-41 | Only a quote character | 1. N-f. | Field is `""""` and parses back to `"`. |
| TC-117-42 | Only commas | 1. N-g. | Field is `",,,"` and parses back to `,,,`. |
| TC-117-43 | Spaces at the start and end | 1. N-h. | Parsed value is `  padded  ` with both spaces on each side kept (not trimmed). |
| TC-117-44 | Text that looks like a number | 1. N-i. | Parsed value is `0123` (leading zero kept). |
| TC-117-45 | Text that starts with `=` | 1. N-j. | Parsed value is `=1+1`, as the story requires "exactly as entered". Whether the export must guard against spreadsheet formulas is open question 8. |
| TC-117-46 | Notes with words the claims register bans | 1. N-k. 2. Export. | Value is exactly N-k. The claims check applies to NightJar's own text, not to the user's own notes. Confirm in open question 9. |
| TC-117-47 | Empty note | 1. Night with no notes (Tue 10 Nov in D1). 2. Export. | The row has 4 fields and the last is empty. |
| TC-117-48 | Very long note with every special character | 1. N-l. 2. Export. | Value is exactly N-l, with nothing cut off. The row count equals the night count. |
| TC-117-49 | Several nights with tricky notes together | 1. Log N-a, N-b, N-c, N-d on four consecutive nights. 2. Export. 3. Parse as CSV. | 4 records, each with 4 fields, and each notes value equal to what was entered. A line break or quote in one night does not affect the next row. |
| TC-117-50 | Unicode that has two forms (é as one character vs `e` + accent) | 1. Enter a note using `e` followed by a combining accent U+0301. 2. Export. | The exported bytes are the same characters as entered, with no normalisation to the other form. |

## AC6: Importing an exported file into an empty diary gives the same nights

"Same nights" is read as: same count, same bedtime and wake time as moments in time, same time zone, same notes, same "night of" date. See open question 10.

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-51 | Round trip of D1 | 1. Export D1. 2. Create a new user with an empty diary. 3. Import the file. | The new diary has 5 nights matching D1 in every field, in the same order. |
| TC-117-52 | Round trip of D2 (DST, London, Kolkata) | 1. Export D2. 2. Import into an empty diary. | 6 nights with identical times, offsets and zones. The 7 h and 9 h nights keep their real elapsed time. |
| TC-117-53 | Round trip of all note texts N-a to N-l | 1. Log one night per note. 2. Export and import into an empty diary. | Each imported note equals the original. |
| TC-117-54 | Round trip when the current zone differs from the nights' zone | 1. Export D1 (logged in Toronto). 2. Set the importing user's zone to `Europe/London`. 3. Import. | The nights are still the same nights: bedtime offsets `-05:00`, night-of dates unchanged, not shifted to London time. |
| TC-117-55 | Round trip twice | 1. Export D1, import into diary B. 2. Export diary B. | The file from B has the same rows as the file from D1. Only the file name may differ if the date differs. |
| TC-117-56 | Round trip of an empty diary | 1. Export an empty diary (header only). 2. Import into an empty diary. | Import succeeds (or reports "nothing to import", see open question 11) and the diary remains empty. No error about a missing row. |
| TC-117-57 | Round trip of 1,000 nights | 1. Export the 1,000-night diary. 2. Import into an empty diary. | 1,000 nights, matching. |
| TC-117-58 | Import into a non-empty diary is outside this story | Not tested here. | See open question 12. |

## Edge: An empty diary exports the header row only

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-59 | Empty diary | 1. New user with 0 nights. 2. Click "Export CSV". | A file `nightjar-diary-<today>.csv` is downloaded. It contains `bedtime,wake_time,timezone,notes` and no data rows. Line ending: open question 7. |
| TC-117-60 | Minimum data: one night | 1. One night (Fri 13 Nov). 2. Export. | Header plus exactly one row. No blank rows. |
| TC-117-61 | Diary emptied after having nights | 1. Log D1. 2. Delete all 5 nights (if deletion exists). 3. Export. | Header row only, with none of the deleted nights. |
| TC-117-62 | A night that was edited | 1. Log Fri 13 Nov. 2. Change the note to N-a. 3. Export. | The row has the edited note and times, and there is only one row for that night. |

## Non-functional: Exporting 1,000 nights takes under 2 seconds

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-63 | 1,000 nights, typical notes | 1. Prepare a diary with 1,000 nights across mixed zones (Toronto, London, Kolkata) and DST changes, notes about 50 characters. 2. Time from clicking "Export CSV" to the file being available. Repeat 5 times. | Every run is under 2 seconds. Environment: open question 13. |
| TC-117-64 | 1,000 nights, heavy notes | 1. As TC-117-63 but every note is N-l (5,000 characters with quotes and line breaks). 2. Time it. | Under 2 seconds, and every note matches. |
| TC-117-65 | Just over the number in the story | 1. 1,001 nights. 2. Export. | All 1,001 nights are exported (the diary is not capped at 1,000). Time is reported. The story sets the limit only for 1,000. |
| TC-117-66 | Fewer than 1,000 nights | 1. 999 nights. 2. Export. | Under 2 seconds. Not slower than the 1,000-night run. |
| TC-117-67 | Row count matches | 1. Export the 1,000-night diary. 2. Count the records. | 1,001 records (header + 1,000), no duplicates, no gaps. |

---

## Open questions

| # | Question | Cases affected | Who should answer |
|---|---|---|---|
| 1 | What is the cut-off for the "night of" date? S-116 says a 00:15 bedtime on Sunday counts as Saturday night, but does not give the hour at which the date flips (for example, is a 04:00 or 11:00 bedtime still the previous night?). S-117 AC4 uses "night of" without defining it. Please confirm the S-116 rule applies to S-117 and give the cut-off. | D1 data, TC-117-28 to TC-117-35 | Product |
| 2 | Does the filename date come from the user's time zone setting at the moment of the click (as assumed), and is that setting always a named zone (not a fixed offset)? | TC-117-3 to TC-117-9 | Product |
| 3 | What does the `timezone` column contain? IANA names such as `America/Toronto` (assumed), or offsets? Does it have to match the import's format exactly? The import's format is not described in any linked document. | TC-117-26, TC-117-51 to TC-117-57 | Product |
| 4 | Is the format always `±HH:MM`? When the offset is zero (London in winter), is it `+00:00` or `Z`? Are seconds always written (`:00`)? Are fractional seconds ever used? | TC-117-16 to TC-117-21, TC-117-27 | Product |
| 5 | Can the app record a time in the repeated hour on fall-back day, and which instant is stored? Can a user pick a time that does not exist (02:30 on Sun 8 Mar in Toronto)? What does the export show? | TC-117-22 | Product |
| 6 | When two nights have the same night-of date in different zones (a user who travels, or two logs for one night), what is the order? Is a duplicate night-of date even allowed? | TC-117-33 | Product |
| 7 | File details: character encoding (UTF-8 assumed), whether to include a byte-order mark (affects Excel), the row separator (CRLF or LF), and whether the last row ends with a line break. How are line breaks in notes written: as entered (CRLF vs LF) or normalised? | TC-117-38, TC-117-39, TC-117-59 | Product |
| 8 | AC5 says notes are exported exactly as entered, but text beginning with `=`, `+`, `-` or `@` can run as a formula when the file is opened in a spreadsheet. Should the export leave it unchanged (as AC5 reads), or add a safeguard? A safeguard would change what AC5 and AC6 expect. | TC-117-45 | Product (and security, if involved) |
| 9 | Does the claims check apply to anything beyond the button label "Export CSV"? For example: a download confirmation, an error message, an empty-diary message. Are the user's exported notes exempt, as assumed here? The claims register is not in the docs, only the policy. | TC-117-11, TC-117-46 | Regulatory & Brand (claims); Product (list of texts) |
| 10 | What does "the same nights" mean in AC6? We assume the same bedtime and wake moments, zone, notes, and night-of date. Are there fields (such as a creation date or an id) that may differ? | TC-117-51 to TC-117-57 | Product |
| 11 | What should import do with a header-only file: succeed with nothing, or show an error? | TC-117-56 | Product |
| 12 | Importing the exported file into a diary that already has nights (duplicates) is not covered by S-117. Is it covered by another story? | TC-117-58 | Product |
| 13 | For the 2-second limit: on which environment and data size is it measured (device, network, server vs browser export), and does the time include the browser download? | TC-117-63 to TC-117-67 | Product |
| 14 | Is there any access control for the button, such as logged-out users or users without data consent? The story says "a NightJar user" only. | TC-117-1, TC-117-10 | Product |
