# Test cases: S-117 Export the diary as CSV

Source: [S-117](../stories/S-117.md), traces to [BR-07](../requirements/BR-07.md). Cases come from the story only. Where the story is silent, see "Open questions".

## Test data

**Users**

| User | Time zone | Notes |
|---|---|---|
| Aisha | America/Toronto | Main user. Diary below. |
| Ben | Europe/London | Used for London DST and a zone change. |
| Empty | America/Toronto | No nights logged. |

**Reference "now"** (unless a case says otherwise): Sat 21 Nov 2026, 10:00 America/Toronto (15:00 UTC).

**Daylight saving dates in 2026**

| Zone | Spring forward | Fall back |
|---|---|---|
| America/Toronto | Sun 8 Mar, 02:00 -> 03:00 (-05:00 -> -04:00) | Sun 1 Nov, 02:00 -> 01:00 (-04:00 -> -05:00) |
| Europe/London | Sun 29 Mar, 01:00 -> 02:00 (+00:00 -> +01:00) | Sun 25 Oct, 02:00 -> 01:00 (+01:00 -> +00:00) |

**Aisha's standard diary (D1)**: all Toronto time.

| Night of | Bedtime | Wake time | Notes |
|---|---|---|---|
| Sat 28 Feb 2026 | 28 Feb 23:10 | 1 Mar 06:50 | `Slept well` |
| Sun 1 Mar 2026 | 2 Mar 00:25 | 2 Mar 07:30 | (empty) |
| Sat 14 Nov 2026 | 14 Nov 22:45 | 15 Nov 06:30 | `Late coffee, felt "wired"` |

Note: a 00:25 bedtime on 2 Mar belongs to the night of Sun 1 Mar, as in the diary.

**Notes test strings (N)**

| Id | Text |
|---|---|
| N1 | `Tired, but ok` (comma) |
| N2 | `She said "sleep tight"` (double quotes) |
| N3 | `Line one` + line break + `Line two` |
| N4 | `Café, très bien: 夜は良く眠れた 😴` (accents, Japanese, emoji) |
| N5 | `"` (a single quote character) |
| N6 | `,,,` |
| N7 | `  padded  ` (leading and trailing spaces) |
| N8 | Empty |
| N9 | A 5,000-character note mixing commas, quotes and line breaks |

## AC1: "Export CSV" button, file name from today's date in the user's current time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button is on the home page and downloads a file | 1. Log in as Aisha (D1). 2. Open the home page. 3. Click "Export CSV". | An "Export CSV" button is visible on the home page. Clicking it downloads one file. |
| TC-117-2 | File name uses today's date | Now = Sat 21 Nov 2026 10:00 Toronto. Click "Export CSV". | File is named `nightjar-diary-2026-11-21.csv`. |
| TC-117-3 | Just before midnight, same zone | Now = Sat 21 Nov 2026 23:59 Toronto (04:59 UTC on 22 Nov). Export. | File is `nightjar-diary-2026-11-21.csv` (Toronto date, not the UTC date 22 Nov). |
| TC-117-4 | Just after midnight, same zone | Now = Sun 22 Nov 2026 00:01 Toronto (05:01 UTC). Export. | File is `nightjar-diary-2026-11-22.csv`. |
| TC-117-5 | Midnight boundary, 00:00 exactly | Now = Sun 22 Nov 2026 00:00:00 Toronto. Export. | File is `nightjar-diary-2026-11-22.csv`. |
| TC-117-6 | User's zone is ahead of UTC | Ben (London, GMT in Nov). Now = 21 Nov 2026 23:30 UTC = 23:30 London. Export. Then now = 22 Nov 00:30 London. Export. | First file `nightjar-diary-2026-11-21.csv`, second `nightjar-diary-2026-11-22.csv`. |
| TC-117-7 | Zone far ahead of the server/UTC date | Aisha changes her current zone to Pacific/Auckland (+13:00 in Nov). Now = 21 Nov 2026 15:00 UTC = 22 Nov 04:00 Auckland. Export. | File is `nightjar-diary-2026-11-22.csv`. |
| TC-117-8 | Zone change changes the file name date | Aisha in Toronto, now = 21 Nov 2026 22:00 Toronto (22 Nov 03:00 UTC). Change current zone to Europe/London (now 22 Nov 03:00 London). Export. | File is `nightjar-diary-2026-11-22.csv` (the new current zone). |
| TC-117-9 | Zone change, date goes backwards | Aisha in Europe/London, now = 22 Nov 2026 00:30 London (21 Nov 19:30 Toronto). Change current zone to Toronto. Export. | File is `nightjar-diary-2026-11-21.csv`. |
| TC-117-10 | Single-digit month and day are zero-padded | Now = Sun 1 Mar 2026 10:00 Toronto. Export. | File is `nightjar-diary-2026-03-01.csv`. |
| TC-117-11 | Day of Toronto spring forward | Now = Sun 8 Mar 2026 03:30 Toronto (after the jump). Export. | File is `nightjar-diary-2026-03-08.csv`. |
| TC-117-12 | Day of Toronto fall back, in the repeated hour | Now = Sun 1 Nov 2026 01:30 Toronto (first, -04:00 = 05:30 UTC) and again 01:30 (second, -05:00 = 06:30 UTC). Export at each. | Both files are `nightjar-diary-2026-11-01.csv`. |
| TC-117-13 | Day of London spring forward / fall back | Ben. Now = Sun 29 Mar 2026 00:30 London, then 02:30 London. Repeat with Sun 25 Oct 2026 00:30 and 01:30 London. | Files are `...-2026-03-29.csv` for both March times and `...-2026-10-25.csv` for both October times. |
| TC-117-14 | Leap day | Now = Sat 29 Feb 2028 10:00 Toronto. Export. | File is `nightjar-diary-2028-02-29.csv`. |
| TC-117-15 | Two exports on the same day | Export twice on 21 Nov 2026. | Both are named `nightjar-diary-2026-11-21.csv`. How the browser renames the second is browser behaviour (see Open questions 9). |
| TC-117-16 | Button works with an empty diary | Log in as Empty. Click "Export CSV". | A file `nightjar-diary-2026-11-21.csv` downloads (content: see Edge). |

## AC2: Header row and columns `bedtime,wake_time,timezone,notes`

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-17 | Header row is first line, exact text | Export D1. Open the file in a plain text editor. | Line 1 is exactly `bedtime,wake_time,timezone,notes`: four columns, this order, lower case, no spaces. |
| TC-117-18 | Every data row has four fields | Export D1. Parse the file with a standard CSV parser. | Header plus 3 data rows; each row has exactly 4 fields. |
| TC-117-19 | Columns match the import | Compare the header of an exported file with the header the importer accepts (the sample import file). | The two headers are identical in names and order. |
| TC-117-20 | No extra columns or rows | Export D1. | No additional columns (for example no id or "night of" column) and no blank or summary rows. |
| TC-117-21 | `timezone` column holds the night's zone | Export D1 plus a night logged in Europe/London. | The `timezone` field for each night shows the zone that night was logged in. The format of the value is not defined (see Open questions 1). |

## AC3: Times are ISO 8601 with the UTC offset of that night's own time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-22 | Story example, winter offset | Export D1. Find the night of Sun 1 Mar 2026 (bed 00:25 on 2 Mar). | `bedtime` is a value of the form `2026-03-02T00:25:00-05:00`. Format matches the story example `2026-03-01T00:25:00-05:00` (date/time with offset, seconds present). |
| TC-117-23 | Summer offset in the same zone | Log a Toronto night: bed 14 Jul 2026 23:00, wake 15 Jul 07:00. Export. | `bedtime` is `2026-07-14T23:00:00-04:00`, `wake_time` is `2026-07-15T07:00:00-04:00`. |
| TC-117-24 | Night's own zone differs from current zone | Aisha logs a night in Europe/London on 10 Nov (bed 23:30, wake 07:00). She then sets her current zone to Toronto. Export. | The London night shows `2026-11-10T23:30:00+00:00` and `2026-11-11T07:00:00+00:00`. It is not converted to the current zone (-05:00). The Toronto nights keep `-05:00` or `-04:00` as they apply. |
| TC-117-25 | Zone change mid-diary | Ben logs 5 nights in London, changes zone to Toronto, logs 5 more nights. Export. | First 5 rows carry London offsets, last 5 carry Toronto offsets. Each row's `timezone` matches its offsets. |
| TC-117-26 | Zone with a non-whole-hour offset | Log a night in Asia/Kolkata (bed 23:00, wake 06:30). Export. | Times end in `+05:30`. |
| TC-117-27 | Zone with a half-hour offset in the negative direction | Log a night in America/St_Johns on 15 Jan 2026 (bed 22:30). Export. | `bedtime` ends in `-03:30`. |
| TC-117-28 | Toronto spring forward: bed before, wake after the jump | Night of Sat 7 Mar 2026: bed 23:00 on 7 Mar, wake 8 Mar 07:00 (Toronto). Export. | `bedtime` is `2026-03-07T23:00:00-05:00`, `wake_time` is `2026-03-08T07:00:00-04:00`. Each time carries the offset in force at that time. |
| TC-117-29 | Toronto fall back: bed before, wake after the change | Night of Sat 31 Oct 2026: bed 23:00 on 31 Oct, wake 1 Nov 07:00 (Toronto). Export. | `bedtime` is `2026-10-31T23:00:00-04:00`, `wake_time` is `2026-11-01T07:00:00-05:00`. |
| TC-117-30 | Toronto fall back: time inside the repeated hour | Log a night with wake time 1 Nov 2026 01:30 Toronto, first occurrence (-04:00), and another with the second occurrence (-05:00). Export. | The two values are `2026-11-01T01:30:00-04:00` and `2026-11-01T01:30:00-05:00`, so they stay distinguishable. If the app cannot capture which one the user meant, see Open questions 3. |
| TC-117-31 | Toronto spring forward: night that sits on the jump | Log bedtime 8 Mar 2026 01:50 Toronto, wake 8 Mar 06:00. Export. | `bedtime` is `2026-03-08T01:50:00-05:00`; `wake_time` is `2026-03-08T06:00:00-04:00`. Elapsed duration after re-import is 3 h 10 min (real time). |
| TC-117-32 | London spring forward | Ben, night of Sat 28 Mar 2026: bed 23:30, wake 29 Mar 07:30. Export. | `bedtime` `2026-03-28T23:30:00+00:00`, `wake_time` `2026-03-29T07:30:00+01:00`. |
| TC-117-33 | London fall back | Ben, night of Sat 24 Oct 2026: bed 23:30, wake 25 Oct 07:30. Export. | `bedtime` `2026-10-24T23:30:00+01:00`, `wake_time` `2026-10-25T07:30:00+00:00`. |
| TC-117-34 | London in winter uses an explicit offset | Ben logs a night in Jan 2026. Export. | Offset is written as `+00:00` (a numeric UTC offset). Check whether `Z` is acceptable: Open questions 2. |
| TC-117-35 | Bedtime just after midnight | Night of Sat 14 Nov 2026 with bed Sun 15 Nov 00:15, wake 07:45 (Toronto). Export. | `bedtime` is `2026-11-15T00:15:00-05:00` (calendar date of the actual clock time, not the "night of" date). The row sits among the 14 Nov night. |
| TC-117-36 | Bedtime at exactly 00:00 and 23:59 | Log two nights: bed 23:59 and bed 00:00 (next calendar day). Export. | Values `T23:59:00` and `T00:00:00` (not `T24:00:00`), with the correct date for each. |
| TC-117-37 | Wake time crosses midnight | Bed 23:10 on 28 Feb, wake 06:50 on 1 Mar. Export. | `wake_time` date is `2026-03-01`; `bedtime` date is `2026-02-28`. |
| TC-117-38 | Minimum night length | Log a night with 1 minute between bed and wake. Export. | Both times appear exactly, and `wake_time` is 1 minute after `bedtime`. |

## AC4: Nights in "night of" order, oldest first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-39 | Entered in order | Export D1. | Rows are for night of 28 Feb, 1 Mar, 14 Nov (oldest first). |
| TC-117-40 | Entered out of order | Log 14 Nov first, then 28 Feb, then 1 Mar. Export. | Same order as TC-117-39, not the order of entry. |
| TC-117-41 | After-midnight bedtime sorts by "night of" date | Night A: night of Sat 14 Nov, bed Sun 15 Nov 00:15. Night B: night of Sun 15 Nov, bed 22:30 on 15 Nov. Export. | Night A (14 Nov) before night B (15 Nov). |
| TC-117-42 | After-midnight bedtime vs earlier evening bedtime | Night C: night of Sat 14 Nov, bed 14 Nov 23:00. Night D: night of Fri 13 Nov, bed Sat 14 Nov 00:30. Enter C first, then D. Export. | Night D (night of 13 Nov) comes before night C (night of 14 Nov). |
| TC-117-43 | Two nights with the same "night of" date | Log two nights that both belong to Sat 14 Nov (for example bed 14 Nov 23:50 and bed 15 Nov 00:15). Export. | Not defined by the story. See Open questions 5. |
| TC-117-44 | Nights in different zones | Ben logs night of 10 Nov in London, then night of 11 Nov in Toronto (UTC instants about 5 hours apart). Export. | 10 Nov before 11 Nov. Order is by "night of" date, not by UTC instant. |
| TC-117-45 | Year boundary | Nights of Wed 31 Dec 2025 (bed 31 Dec 23:30), Thu 1 Jan 2026 (bed 2 Jan 00:10 would be night of 1 Jan) and Fri 2 Jan 2026. Entered newest first. Export. | Order 31 Dec 2025, 1 Jan 2026, 2 Jan 2026. |
| TC-117-46 | Order around DST change | Nights of Sat 7 Mar, Sun 8 Mar and Mon 9 Mar 2026 (Toronto), entered in reverse. Export. | 7 Mar, 8 Mar, 9 Mar. |
| TC-117-47 | Single night | Diary with one night. Export. | Header plus one data row. |

## AC5: Notes exported exactly as entered, with standard CSV quoting

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-48 | Comma in notes (N1) | Log a night with note N1. Export. Open with a standard CSV parser and in a text editor. | The notes field is enclosed in double quotes (`"Tired, but ok"`). A parser returns `Tired, but ok` in one field; the row has 4 fields. |
| TC-117-49 | Double quotes in notes (N2) | Note N2. Export. | Embedded quotes are doubled: `"She said ""sleep tight"""`. A parser returns `She said "sleep tight"`. |
| TC-117-50 | Line break in notes (N3) | Note N3. Export. | The field is quoted and contains the line break; a parser returns the two lines in one field and the file still has the right number of records. |
| TC-117-51 | Non-English text (N4) | Note N4. Export. Parse. | Parser returns the identical text, with accents, Japanese and emoji intact (no `?` or garbled characters). Encoding to confirm: Open questions 6. |
| TC-117-52 | Note is only a quote character (N5) | Note N5. Export. | Written as `""""`; parser returns `"`. |
| TC-117-53 | Note is only commas (N6) | Note N6. Export. | Written as `",,,"`; parser returns `,,,`; row has 4 fields. |
| TC-117-54 | Leading and trailing spaces (N7) | Note N7. Export. Parse. | Parser returns `  padded  ` with both spaces on each side kept ("exactly as entered"). |
| TC-117-55 | Empty notes (N8) | Night of 1 Mar in D1. Export. | The row still has 4 fields; the notes field is empty. |
| TC-117-56 | Notes that look like a formula | Note `=1+1`, another `@SUM(A1)`, another `-5`. Export. Open in a spreadsheet app. | Text in the file is exactly as entered, per AC5. (How a spreadsheet displays it: Open questions 7.) |
| TC-117-57 | Notes that look like another row | Note `2026-03-02T00:25:00-05:00,2026-03-02T07:30:00-05:00,America/Toronto,hi`. Export. Parse. | Parser sees one record with 4 fields; the note is intact in field 4. |
| TC-117-58 | Notes containing the header text | Note `bedtime,wake_time,timezone,notes`. Export. | Quoted; parser sees header once and the text as the note value. |
| TC-117-59 | Long note (N9) | Note N9. Export. Parse. | Parser returns the 5,000 characters unchanged. (If the app limits note length, the limit is not in the story: Open questions 8.) |
| TC-117-60 | Different line break types | Notes entered with LF, with CRLF, and with a tab. Export. | Each note comes back as entered. See Open questions 6 for how CRLF is handled. |
| TC-117-61 | Notes with HTML or script text | Note `<b>hi</b> & <script>alert(1)</script>`. Export. | Text is in the file exactly as entered, not escaped or stripped. |
| TC-117-62 | Many special characters in one note | Note with comma, quote, line break and emoji together. Export. | One field, quoted, quotes doubled, round-trips unchanged in a parser. |

## AC6: Importing an exported file into an empty diary gives the same nights

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-63 | Basic round trip | 1. Export D1. 2. Create a new user with an empty diary. 3. Import the file. | The new diary has the same 3 nights as D1: same bedtimes and wake times (as instants), same zones, same notes, same "night of" dates and order. |
| TC-117-64 | Round trip with all note types | Log a night per note N1..N9, export, import into an empty diary. | All notes are identical to the originals. |
| TC-117-65 | Round trip, nights from several zones | Ben with London, Toronto and Asia/Kolkata nights (TC-117-24 to 26). Export, import to empty diary. | Each night keeps its own zone and local times; the offsets exported match after re-export. |
| TC-117-66 | Round trip across DST changes | Nights from TC-117-28, 29, 31, 32, 33. Export, import. | Durations (real elapsed time) are unchanged. Local times unchanged. |
| TC-117-67 | Round trip of after-midnight bedtimes | TC-117-35 night. Export, import. | The imported night is the night of Sat 14 Nov, not Sun 15 Nov. |
| TC-117-68 | Re-export after import is identical | Export D1 (file 1). Import into empty diary. Export again (file 2, same day). | The contents of file 1 and file 2 are identical, byte for byte, apart from the file name date if exported on different days. |
| TC-117-69 | Round trip derived outputs | After importing D1-like data with 7+ nights, compare the "usual bedtime" on the home page (and nudge time) before and after. | They are the same, since the nights are the same. |
| TC-117-70 | Large round trip | 1,000 nights with mixed notes. Export, import into empty diary. | 1,000 nights imported, identical to original. |
| TC-117-71 | Round trip of empty diary | Export Empty. Import into an empty diary. | Import succeeds (or is a no-op); the diary is still empty. The importer's behaviour on a header-only file is not in the story: Open questions 4. |
| TC-117-72 | Importing into a diary that already has nights | Export D1. Import into a diary that already has D1. | Not covered by the story (AC6 says "empty diary"). See Open questions 10. |

## Edge: empty diary exports the header row only

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-73 | New user with no nights | Log in as Empty. Click "Export CSV". Open file in a text editor. | The file contains only `bedtime,wake_time,timezone,notes`. No data rows. |
| TC-117-74 | Diary emptied after having nights | Aisha deletes all nights (if the app allows). Export. | Header only, as TC-117-73. |
| TC-117-75 | Minimum data: exactly one night | See TC-117-47. | Header plus one row. |
| TC-117-76 | Header-only file parses | Parse the TC-117-73 file with a standard CSV parser. | One record (the header), zero data records. |

## Non-functional: exporting 1,000 nights takes under 2 seconds

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-77 | 1,000 nights, simple notes | Load a diary with 1,000 nights, empty notes. Click "Export CSV". Time from click (request sent) until the file is delivered. | Under 2 seconds. Repeat 5 times; every run is under 2 seconds. |
| TC-117-78 | 1,000 nights, heavy notes | 1,000 nights, each with a 500-character note containing commas, quotes and line breaks. | Under 2 seconds. |
| TC-117-79 | 1,000 nights, many zones | 1,000 nights spread across 5 time zones including DST nights. | Under 2 seconds. |
| TC-117-80 | Just below and above the size | Time 999, 1,000 and 1,001 nights. | 1,000 is under 2 seconds. 999 is no slower. 1,001 is recorded (the story gives no number above 1,000). |
| TC-117-81 | Output is correct at 1,000 nights | Check the 1,000-night file for row count, order and notes. | Header plus 1,000 rows, in "night of" order, nothing truncated. |

## Claims check

The story adds one piece of user-visible text: the button label "Export CSV". It is neutral and has no medical or treatment wording.

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-82 | Button label passes the claims check | Run `claims.check_text("Export CSV")` and read the button on the home page. | No violations; the label contains none of the banned patterns in `claims/register.yaml`. |
| TC-117-83 | User notes are not run through the claims check | Export a note containing a banned word, for example `Tried to treat my insomnia with tea`. | The note is exported exactly as entered (AC5). It is the user's own text, not NightJar copy. Confirm with Regulatory & Brand: Open questions 11. |

## Open questions

| # | Question | Cases affected | Who should answer |
|---|---|---|---|
| 1 | What exactly goes in the `timezone` column: IANA name (`America/Toronto`), abbreviation, or offset? The story says "same columns as the import" but does not give the value format. | TC-117-19, 21, 24, 65 | Product |
| 2 | In offsets, is UTC written as `+00:00` or `Z`? The story says "the UTC offset" and the example uses `-05:00`. | TC-117-34 | Product |
| 3 | For a time inside the repeated hour on a fall-back night (Toronto 1 Nov 01:30, London 25 Oct 01:30), which offset is expected? And what if the diary cannot record which occurrence the user meant? | TC-117-30 | Product |
| 4 | Must the importer accept a header-only file, and what should it do (succeed with no nights, or show an error)? | TC-117-71 | Product |
| 5 | Can there be two nights with the same "night of" date? If so, what is the order between them? The story gives no tie-break. | TC-117-43 | Product |
| 6 | File encoding (UTF-8? with or without a byte order mark?) and row line endings (LF or CRLF). How are line breaks inside notes written if the user entered CRLF? "Exactly as entered" needs a rule. | TC-117-51, 60 | Product |
| 7 | Notes starting with `=`, `+`, `-` or `@` can run as formulas in spreadsheets (CSV injection). AC5 says "exactly as entered", which conflicts with any protective prefix. Which wins? | TC-117-56 | Product (with security input) |
| 8 | Is there a maximum note length, and what happens to longer notes on export? | TC-117-59 | Product |
| 9 | If a file with the same name already exists, is the download name left to the browser? | TC-117-15 | Product |
| 10 | What should import do for a file whose nights already exist in the diary (duplicates, merge, or reject)? AC6 covers only empty diaries. | TC-117-72 | Product |
| 11 | Confirm user-entered notes are exempt from the claims check on export. | TC-117-83 | Regulatory & Brand |
| 12 | Which "time" does the 2-second limit measure (server response only, or until the browser finishes the download), and on what hardware? | TC-117-77 to 81 | Product |
| 13 | Does the button appear for a user with an empty diary, or should it be disabled? The story says an empty diary exports a header row, which suggests enabled. | TC-117-16, 73 | Product |
