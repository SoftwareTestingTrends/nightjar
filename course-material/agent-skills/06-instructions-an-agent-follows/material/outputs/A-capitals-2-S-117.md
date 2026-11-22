# Test cases: S-117 Export the diary as CSV

Story: [S-117](../stories/S-117.md), traces to [BR-07](../requirements/BR-07.md).
Status: draft for review with Product. Cases are for manual testing before development.

## Test data

**Users and time zones**

| Name | Home time zone | Used for |
|---|---|---|
| Ana | America/Toronto | most cases |
| Lee | Europe/London | London daylight-saving cases |
| Traveller | America/Toronto at home, Europe/London while away | time zone change |

**Clock changes (2026)**

- Toronto: clocks go forward Sun 8 Mar 02:00 (EST -05:00 to EDT -04:00); back Sun 1 Nov 02:00 (EDT to EST).
- London: clocks go forward Sun 29 Mar 01:00 UTC (GMT +00:00 to BST +01:00); back Sun 25 Oct 02:00 BST (to GMT).

**Diaries** (times are local to the night's own time zone)

- **D-standard**: Ana, 3 nights. Sat 28 Feb bed 23:10, wake Sun 1 Mar 06:50. Sun 1 Mar bed 23:40, wake Mon 2 Mar 07:00. Mon 2 Mar bed 23:25, wake Tue 3 Mar 06:55.
- **D-midnight**: Ana, one night: bed 00:25 Sun 1 Mar 2026, wake 07:30. This is the night of Sat 28 Feb.
- **D-empty**: Ana, no nights.
- **D-notes**: Ana, 5 nights, one per note below. 1: `Slept well, woke once`. 2: `Said "no" to coffee`. 3: two lines, `Line one` then a line break then `Line two`. 4: `夜はよく眠れた, café ñ 😴`. 5: empty note.
- **D-1000**: Ana, 1,000 nights with a mix of notes, 100 of them with commas, quotes or line breaks.

**"Now" values**

- N1 = Wed 18 Nov 2026 10:00 Toronto (ordinary day).
- N2 = Thu 19 Nov 2026 23:30 Toronto (still 19 Nov in Toronto, already 20 Nov in UTC).
- N3 = Fri 20 Nov 2026 00:30 Toronto (just after local midnight).
- N4 = Fri 20 Nov 2026 00:30 London (same moment as Thu 19 Nov 19:30 Toronto).

## AC1: Button and file name

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button is on the home page and downloads a file | 1. Sign in as Ana (D-standard). 2. Open the home page. 3. Select "Export CSV". | The button is on the home page. One file downloads, named `nightjar-diary-2026-11-18.csv` when now is N1. |
| TC-117-2 | Date in the name is the user's local date, not UTC (just before local midnight) | 1. Ana, time zone Toronto, now = N2. 2. Select "Export CSV". | File is `nightjar-diary-2026-11-19.csv`, not 20 Nov. |
| TC-117-3 | Date in the name is the local date just after midnight | 1. Ana, time zone Toronto, now = N3. 2. Export. 3. Repeat with Lee in London, now = N4. | Ana's file is `nightjar-diary-2026-11-20.csv`. Lee's file is `nightjar-diary-2026-11-20.csv`. (N3 and N4 are different moments, but both are 20 Nov locally.) |
| TC-117-4 | User changes time zone, then exports | 1. Traveller at now = N2 with zone Toronto: export. 2. Change current time zone to Europe/London (same instant, so London time is Fri 20 Nov 04:30). 3. Export again. | First file is `nightjar-diary-2026-11-19.csv`. Second file is `nightjar-diary-2026-11-20.csv`. |
| TC-117-5 | Single-digit month and day are zero padded | 1. Ana, now = Sun 8 Mar 2026 12:00 Toronto (the day clocks go forward). 2. Export. | File is `nightjar-diary-2026-03-08.csv`. |

## AC2: Header row and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-6 | Header text and order | 1. Export D-standard. 2. Open the file in a plain text editor. | Line 1 is exactly `bedtime,wake_time,timezone,notes`. No spaces, no extra columns, no quotes around the names. |
| TC-117-7 | Header appears once, and every row has 4 fields | 1. Export D-notes. 2. Open in a CSV-aware tool and count fields per record. | One header row only. Header plus 5 records. Each record has exactly 4 fields, including the one with an empty note (it ends with a trailing comma). |
| TC-117-8 | Header matches the import's columns | 1. Compare the header with the first line of the import template or the import's documented columns. | Names and order are identical. |

## AC3: ISO 8601 times with the night's own offset

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-9 | Standard offset in winter | 1. Export D-midnight (Toronto, bed 00:25 on 1 Mar 2026, wake 07:30). | Row starts `2026-03-01T00:25:00-05:00,2026-03-01T07:30:00-05:00,`. Shape and offset match the story's example. |
| TC-117-10 | Night that crosses spring-forward in Toronto | 1. Log Ana: bed Sat 7 Mar 23:30, wake Sun 8 Mar 07:30. 2. Export. | Bedtime ends `-05:00`, wake time ends `-04:00` (the offset that applied at that moment in that zone). The wake time is 7 h real time after bedtime, not 8 h. |
| TC-117-11 | Night that crosses fall-back in Toronto and London | 1. Log Ana: bed Sat 31 Oct 23:30, wake Sun 1 Nov 07:30. 2. Log Lee: bed Sat 24 Oct 23:30, wake Sun 25 Oct 07:30. 3. Export each. | Ana: bedtime `-04:00`, wake `-05:00`. Lee: bedtime `+01:00`, wake `+00:00`. |
| TC-117-12 | Night logged abroad keeps the offset of its own zone | 1. Traveller logs a night in Toronto (Mon 2 Nov, bed 23:00, wake 07:00). 2. Traveller logs a night in London (Tue 3 Nov, bed 23:00, wake 07:00). 3. Set current time zone to Toronto. 4. Export. | Toronto night uses `-05:00` on both times and timezone `America/Toronto`. London night uses `+00:00` and `Europe/London`. The London night is not shifted to Toronto time. |
| TC-117-13 | Time in the repeated hour on fall-back day | 1. Log Ana: bed Sun 1 Nov 01:30 EDT (first pass) and a second night with bed Sun 1 Nov 01:30 EST (second pass). 2. Export. | Offsets are `-04:00` and `-05:00` respectively, so the two times are told apart. (Depends on open question 2.) |

## AC4: "Night of" order, oldest first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-14 | Nights logged out of order | 1. Log Ana's three D-standard nights in the order 2 Mar, 28 Feb, 1 Mar. 2. Export. | Rows run 28 Feb, 1 Mar, 2 Mar (oldest night first). |
| TC-117-15 | Past-midnight bedtime sorts by its "night of" date | 1. Log a night with bed Sat 28 Feb 23:50. 2. Log a night with bed Mon 2 Mar 00:15 (night of Sun 1 Mar). 3. Log a night with bed Mon 2 Mar 23:20. 4. Export. | Order is night of 28 Feb, night of 1 Mar (bed 00:15 on 2 Mar), night of 2 Mar (bed 23:20). The 00:15 night is not placed after the 23:20 night. |
| TC-117-16 | Order follows the night's own time zone, not the instant | 1. Traveller logs night A in London: bed Sat 14 Nov 23:30 GMT (18:30 Toronto). 2. Traveller logs night B in Toronto: bed Sat 14 Nov 19:00 EST (00:00 UTC 15 Nov, after A in real time). 3. Export. | Both are nights of 14 Nov; the order between them follows the rule in open question 3. The test records which order appears and Product confirms it. |
| TC-117-17 | Order across a year boundary | 1. Log nights of 31 Dec 2025 and 1 Jan 2026. 2. Export. | 31 Dec 2025 comes before 1 Jan 2026. |

## AC5: Notes exactly as entered

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-18 | Commas and quotes use standard CSV quoting | 1. Export D-notes. 2. Open the raw text for nights 1 and 2. | Night 1 note is `"Slept well, woke once"`. Night 2 is `"Said ""no"" to coffee"` (quotes doubled, field wrapped). |
| TC-117-19 | Line break inside a note | 1. Export D-notes. 2. Open the raw text and a CSV-aware tool for night 3. | The note is wrapped in quotes and contains the line break. A CSV tool shows one record with two lines in the notes field, not two records. |
| TC-117-20 | Non-English text, accents and emoji | 1. Export D-notes. 2. Open the file in a text editor set to UTF-8, then in a spreadsheet app. | Night 4 reads `夜はよく眠れた, café ñ 😴` with no garbling (it is quoted because of the comma). Spreadsheet behaviour is noted for open question 4. |
| TC-117-21 | Empty note and edge whitespace | 1. Export D-notes plus a night with note `  padded  ` (two spaces each side). | Empty note is an empty field. Padded note keeps both leading and trailing spaces. Nothing is trimmed. |
| TC-117-22 | Note that starts with `=`, `+`, `-` or `@` | 1. Log a note `=1+1`. 2. Export. 3. Open in a spreadsheet app. | The file text holds `=1+1` exactly as entered. What the spreadsheet does with it is open question 5. |

## AC6: Round trip through import

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-23 | Round trip of ordinary nights | 1. Export D-standard. 2. Sign in as a new user with D-empty. 3. Import the file. 4. Compare each night's bedtime, wake time, time zone, "night of" date and note. | Same three nights, same values. |
| TC-117-24 | Round trip of tricky notes | 1. Export D-notes. 2. Import into an empty diary. 3. Compare each note character by character. | All 5 notes are identical, including the quotes, the line break, the non-English text and the empty note. |
| TC-117-25 | Round trip across clock changes and zones | 1. Build a diary with the nights from TC-117-10, 11, 12 and 15. 2. Export, then import into an empty diary. 3. Compare bedtimes, wake times, durations and "night of" dates. | Same instants and durations (7 h on spring-forward night). The 00:15 night is still the night of the previous date. Each night keeps its own time zone. |
| TC-117-26 | Second round trip is stable | 1. Export from the imported diary of TC-117-25. 2. Compare the two files. | Files are identical apart from the date in the name. |

## Edge: Empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-27 | No nights | 1. Sign in as a user with D-empty. 2. Select "Export CSV". 3. Open the file. | A file named `nightjar-diary-<today>.csv` downloads. It holds only `bedtime,wake_time,timezone,notes` and nothing else. |
| TC-117-28 | Minimum data: one night | 1. Log one night with an empty note. 2. Export. | Header plus one row with 4 fields. |
| TC-117-29 | Empty export imports cleanly | 1. Export D-empty. 2. Import it into an empty diary. | Import completes with no error and the diary stays empty (see open question 6). |
| TC-117-30 | Diary becomes empty again | 1. Log a night, delete it, export. | Header row only, same as TC-117-27. |

## Non-functional: 1,000 nights under 2 seconds

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-31 | Exactly 1,000 nights | 1. Load D-1000. 2. Time from selecting "Export CSV" until the download is offered, 5 runs. | Every run is under 2 seconds. The file has 1,001 records (header plus 1,000). |
| TC-117-32 | Over the number in the story | 1. Load 1,001 nights, then 5,000. 2. Time the export. | Both complete without error. Times are recorded; there is no stated limit above 1,000 (open question 7). |
| TC-117-33 | Heavy notes | 1. Load 1,000 nights where every note is 5,000 characters with quotes and line breaks. 2. Time the export. | File is correct; time is recorded against the 2-second limit (open question 7). |

## Open questions

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | What goes in the `timezone` column: IANA name (`America/Toronto`) or an offset? The story names the column but not its format. | TC-117-9, 12, 23, 25 | IANA name, as that is the only form that keeps daylight-saving rules for the import. | Product |
| 2 | In the repeated hour on fall-back day, and for times that do not exist on spring-forward day, what does the diary store and export? | TC-117-13 | Export the real instant with its true offset. Nonexistent local times cannot be logged. | Product |
| 3 | When two nights share a "night of" date (for example logged in two zones), which comes first? | TC-117-16 | Break ties by the real instant of bedtime, earlier first. | Product |
| 4 | Is the file UTF-8, with or without a byte order mark? Spreadsheet apps may garble non-English text without one. | TC-117-20 | UTF-8 with no BOM, as the import expects the same; confirm the import reads a BOM safely. | Product |
| 5 | Should notes starting with `=`, `+`, `-` or `@` be exported unchanged (AC5 says "exactly as entered") even though a spreadsheet may treat them as formulas? | TC-117-22 | Export unchanged to keep the round trip exact, and note the risk to the team. | Product |
| 6 | Does the import accept a header-only file, and what does it show? | TC-117-29 | Yes: it imports zero nights with no error. | Product |
| 7 | Is there a performance target above 1,000 nights or for very long notes, and on what device and network? | TC-117-31, 32, 33 | Keep 2 seconds for 1,000 nights on a mid-range phone; no target above that, but no failure. | Product |
| 8 | Does the line break between records (CRLF or LF) matter, and do notes keep their original line break style? | TC-117-19, 24 | Records end in CRLF as standard CSV; notes keep their original breaks. | Product |
| 9 | Is the "Export CSV" label, and any message shown around the export (such as for an empty diary), covered by the claims check? The button text is user-facing. | TC-117-1, 27 | Yes: run all new wording through the claims check. "Export CSV" is neutral and should pass; the register is owned by Regulatory & Brand, who confirm. | Regulatory & Brand |
