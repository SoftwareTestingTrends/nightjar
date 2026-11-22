# Test cases for S-117: Export the diary as CSV

Story: [S-117](../stories/S-117.md). Traces to [BR-07](../requirements/BR-07.md).
Status: draft for review with Product. No code exists yet.

## Test data

**User:** Test user "Toni", account time zone **America/Toronto** unless a case says otherwise.

**Time zone facts used (2026):**

| Zone | Spring forward | Fall back | Offsets |
|---|---|---|---|
| America/Toronto | Sun 8 Mar, 02:00 to 03:00 | Sun 1 Nov, 02:00 to 01:00 | EST -05:00, EDT -04:00 |
| Europe/London | Sun 29 Mar, 01:00 to 02:00 | Sun 25 Oct, 02:00 to 01:00 | GMT +00:00, BST +01:00 |

**Default "now":** Sat 21 Nov 2026, 10:00 Toronto (15:00 UTC).

**Diary sets** (a night is named by its "night of" date, as in the diary):

| Set | Contents |
|---|---|
| D-empty | No nights. |
| D-one | One night: night of Fri 20 Nov 2026, Toronto, bed 23:00, wake 07:00, note "ok". |
| D-mixed | Toronto nights of 1 Mar (bed Mon 2 Mar 00:25, wake 07:55), 15 Jul (bed 23:10, wake 06:50), 7 Mar (bed 23:30, wake Sun 8 Mar 07:00), 31 Oct (bed 23:30, wake Sun 1 Nov 07:00). London nights of 28 Mar (bed 23:30, wake Sun 29 Mar 07:30), 24 Oct (bed 23:30, wake Sun 25 Oct 07:30), 10 Jan (bed 23:00, wake 07:00). |
| D-notes | Nights whose notes are listed in the AC5 cases. |

---

## AC1: "Export CSV" button downloads `nightjar-diary-YYYY-MM-DD.csv`, today's date in the user's current time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button is on the home page and the file name has the right shape | 1. Use D-one. 2. Now = Sat 21 Nov 2026 10:00 Toronto. 3. Open the home page. 4. Click "Export CSV". | A button labelled "Export CSV" is on the home page. One file downloads, named exactly `nightjar-diary-2026-11-21.csv` (lower case, hyphens, `.csv`). |
| TC-117-2 | Zero-padding of month and day (data variants merged: 5 Mar, 9 Dec, 1 Jan) | 1. Use D-one. 2. Set now to Thu 5 Mar 2026 10:00 Toronto, export. 3. Repeat with Wed 9 Dec 2026 and Fri 1 Jan 2027. | Names are `nightjar-diary-2026-03-05.csv`, `nightjar-diary-2026-12-09.csv`, `nightjar-diary-2027-01-01.csv`. |
| TC-117-3 | Late evening: local date is behind UTC date | 1. Use D-one. 2. Now = Sat 21 Nov 2026 23:30 Toronto (Sun 22 Nov 04:30 UTC). 3. Export. | File is `nightjar-diary-2026-11-21.csv`, not 22 Nov. |
| TC-117-4 | Just after local midnight: local date is ahead of the previous day | 1. Use D-one. 2. Now = Sun 22 Nov 2026 00:05 Toronto (05:05 UTC). 3. Export. | File is `nightjar-diary-2026-11-22.csv`. |
| TC-117-5 | Change of time zone before export uses the new "current" zone | 1. Use D-one. 2. Instant = Sun 22 Nov 2026 03:30 UTC. 3. Time zone is Toronto (Sat 21 Nov 22:30): export. 4. Switch the user's current time zone to Europe/London (Sun 22 Nov 03:30) and export again. | First file is `nightjar-diary-2026-11-21.csv`; second is `nightjar-diary-2026-11-22.csv`. |

## AC2: Header row and columns `bedtime,wake_time,timezone,notes`

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-6 | Header is the exact first line | 1. Use D-mixed. 2. Export. 3. Open the file in a plain-text viewer (not a spreadsheet). | Line 1 is exactly `bedtime,wake_time,timezone,notes`: lower case, underscore, no spaces, no quotes, four columns in this order. Line 2 onward are nights. |
| TC-117-7 | Every row has four fields | 1. Use D-mixed. 2. Export and parse the file with a CSV parser. | The header and each of the 7 data rows parse to exactly 4 fields. There are 7 data rows (one per night, no extra summary or blank rows). |
| TC-117-8 | Header matches the import's columns | 1. Compare the exported header with the header the import expects (see its own story or screen). 2. Import the file (see AC6). | Same names and order. Import accepts the file without any column mapping or warning. |

## AC3: ISO 8601 times with the UTC offset in that night's own time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-9 | Winter and summer offsets in Toronto (data variants merged) | 1. Use D-mixed. 2. Export. 3. Read the rows for the Toronto nights of 1 Mar and 15 Jul. | 1 Mar row: bedtime `2026-03-02T00:25:00-05:00`, wake_time `2026-03-02T07:55:00-05:00`. 15 Jul row: bedtime `2026-07-15T23:10:00-04:00`, wake_time `2026-07-16T06:50:00-04:00`. Format is `YYYY-MM-DDTHH:MM:SS` plus offset, with seconds. |
| TC-117-10 | Night that crosses spring forward, in Toronto (7 to 8 Mar) and London (28 to 29 Mar) | 1. Use D-mixed. 2. Export. 3. Read the Toronto 7 Mar and London 28 Mar rows. | Toronto: bedtime `2026-03-07T23:30:00-05:00`, wake_time `2026-03-08T07:00:00-04:00`. London: bedtime `2026-03-28T23:30:00+00:00` (or `Z`, see question 2), wake_time `2026-03-29T07:30:00+01:00`. Bedtime and wake time in one row have different offsets; each is the offset in force at that moment. |
| TC-117-11 | Night that crosses fall back, in Toronto (31 Oct to 1 Nov) and London (24 to 25 Oct) | 1. Use D-mixed. 2. Export. 3. Read the Toronto 31 Oct and London 24 Oct rows. | Toronto: bedtime `2026-10-31T23:30:00-04:00`, wake_time `2026-11-01T07:00:00-05:00`. London: bedtime `2026-10-24T23:30:00+01:00`, wake_time `2026-10-25T07:30:00+00:00` (or `Z`). The elapsed time is the real duration (9 h 30 min Toronto, 9 h London), not the clock difference. |
| TC-117-12 | Night logged in another zone than the user's current one | 1. Use D-mixed. 2. Set current zone to America/Toronto, export. 3. Set current zone to Asia/Tokyo, export again. 4. Read the London 10 Jan row in both files. | In both files: bedtime `2026-01-10T23:00:00+00:00` (or `Z`), wake_time `2026-01-11T07:00:00+00:00`, timezone `Europe/London` (see question 1). Offsets are not rewritten to Toronto or Tokyo. The rows are identical in the two files. |
| TC-117-13 | Ambiguous clock time on a fall-back night | 1. Create a Toronto night of 31 Oct, bed 23:30, wake Sun 1 Nov 01:30 the first time the clock shows it (EDT, 05:30 UTC). 2. Create a second night with wake at 01:30 the second time (EST, 06:30 UTC). 3. Export. | The two wake_times are `2026-11-01T01:30:00-04:00` and `2026-11-01T01:30:00-05:00`, so they are distinguishable and match the real moment logged. If the app cannot record which 01:30, see question 3. |

## AC4: "Night of" order, oldest first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-14 | Nights entered newest first or out of order | 1. Log nights of 18 Nov, 12 Nov, 20 Nov and 15 Nov, in that order. 2. Export. | Rows are in order 12, 15, 18, 20 Nov (oldest first). |
| TC-117-15 | Bedtime after midnight sorts by its "night of" date | 1. Log night of Fri 13 Nov: bed Fri 23:00. 2. Log night of Sat 14 Nov: bed Sun 15 Nov 00:15. 3. Log night of Sun 15 Nov: bed Sun 23:50. 4. Export. | Order is Fri 13, Sat 14 (its bedtime row starts `2026-11-15T00:15:00-05:00`), Sun 15. The Sat 14 row is not placed after the Sun 15 row, though it starts at 00:15 on the 15th. |
| TC-117-16 | "Night of" order differs from real-time order across zones | 1. Log night of Tue 10 Mar in Pacific/Honolulu, bed 23:30 (Wed 11 Mar 09:30 UTC). 2. Log night of Wed 11 Mar in Pacific/Auckland, bed 20:00 (Wed 11 Mar 07:00 UTC). 3. Export. | Honolulu (night of 10 Mar) first, Auckland (night of 11 Mar) second, even though the Auckland night starts earlier in UTC. See question 4 for the rule behind this. |
| TC-117-17 | Order around a year boundary and a DST night | 1. Log nights of 30 Dec 2025, 31 Dec 2025, 1 Jan 2026, 7 Mar 2026 and 8 Mar 2026 (Toronto). 2. Export. | Rows are in order 30 Dec 2025, 31 Dec, 1 Jan, 7 Mar, 8 Mar. Year change and DST night do not reorder. |

## AC5: Notes exactly as entered, standard CSV quoting

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-18 | Commas and quotes | 1. Log a night with the note `Slept well, then woke at "3am", ok` . 2. Export and open in a plain-text viewer. | Field is `"Slept well, then woke at ""3am"", ok"`: whole field in double quotes, each inner quote doubled, commas untouched. A CSV parser returns the original note. |
| TC-117-19 | Line breaks (LF, CRLF, and a blank line) | 1. Log a note `Line 1`, new line, `Line 2`, blank line, `Line 4`. 2. Export. 3. Parse the file with a CSV parser. | The field is in double quotes with the breaks inside. Parsing gives one row (not several), and the note matches the original, including the blank line and the same type of line break. |
| TC-117-20 | Non-English text, emoji and right-to-left text | 1. Log notes `Dormí mal — café ☕`, `よく眠れた`, `نمت جيدا` and `😴 Zażółć gęślą jaźń`. 2. Export. 3. Open the file as UTF-8. | Each note is identical to the entry, with no `?` or garbled characters. File is UTF-8. A BOM is present or not as decided in question 5. |
| TC-117-21 | Empty note and leading/trailing spaces | 1. Log one night with no note, and another with the note `  padded  ` (two spaces each side). 2. Export. | Empty note gives an empty fourth field (row ends with a comma, still four fields). The padded note keeps both spaces each side (quoted or not, but not trimmed). |
| TC-117-22 | Note that starts with a spreadsheet formula character | 1. Log notes `=1+1`, `+44 20 7946 0000`, `-5 hours`, `@home`. 2. Export. | Notes appear exactly as entered, with no added apostrophe or space, as the story says "exactly as entered". See question 6 for the spreadsheet-safety conflict. |

## AC6: Import into an empty diary gives the same nights

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-23 | Mixed zones and DST nights round-trip | 1. Use D-mixed. 2. Export. 3. Delete all nights so the diary is empty. 4. Import the exported file. | The diary shows 7 nights. For each, "night of" date, bedtime, wake time (same real moment), time zone and duration match the original (for example Toronto 7 Mar is 7 h 30 min; Toronto 31 Oct is 8 h 30 min). |
| TC-117-24 | Tricky notes round-trip | 1. Use D-notes (all notes from TC-117-18 to TC-117-22). 2. Export, empty the diary, import. | Every note is identical to the original, character for character, including line breaks, quotes, emoji and padding. No rows are split or merged. |
| TC-117-25 | After-midnight bedtime keeps its "night of" date | 1. Log a Toronto night with bed Sun 15 Nov 00:15, wake 07:45 (the night of Sat 14 Nov). 2. Export, empty the diary, import. | The imported night is the night of Sat 14 Nov, not Sun 15 Nov. |
| TC-117-26 | Import under a different current zone; second export is unchanged | 1. Use D-mixed. 2. Export file A. 3. Empty the diary. 4. Set current zone to Asia/Tokyo and import A. 5. Set the zone back to Toronto and export file B. | Nights show the same local times in their own zones (not shifted to Tokyo). Files A and B have identical contents (apart from the file name date if "now" differs). |

## Edge: An empty diary exports the header row only

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-27 | Empty diary | 1. Use D-empty (new user, or after deleting every night). 2. Click "Export CSV". | The button is available and a file `nightjar-diary-2026-11-21.csv` downloads. It contains only `bedtime,wake_time,timezone,notes` (with or without a final line break, see question 7). No error, no blank data row. |
| TC-117-28 | Minimum data: one night | 1. Use D-one. 2. Export. | Header plus exactly one row: `2026-11-20T23:00:00-05:00,2026-11-21T07:00:00-05:00,America/Toronto,ok` (timezone format per question 1). |
| TC-117-29 | Empty export imports cleanly | 1. Export D-empty. 2. Import that file into an empty diary. | Import succeeds (or says there is nothing to import, per the import's own wording) and the diary stays empty. No error about a missing or malformed file. |

## Non-functional: Exporting 1,000 nights takes under 2 seconds

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-30 | Exactly 1,000 typical nights | 1. Load 1,000 nights across 3 time zones, with short notes. 2. Start a timer when "Export CSV" is clicked; stop when the file is saved. 3. Repeat 3 times. | Every run takes under 2 seconds (device and network per question 8). File has 1,001 lines (header + 1,000 rows), in "night of" order. |
| TC-117-31 | 1,000 nights with heavy notes | 1. Load 1,000 nights where every note is long (for example 2,000 characters) with commas, quotes, line breaks and non-English text. 2. Time the export as in TC-117-30. | Under 2 seconds, and still 1,000 rows when parsed. The page stays responsive (no frozen button or tab). |
| TC-117-32 | Above the stated limit | 1. Load 5,000 nights. 2. Export. | The story gives no limit for this case: file must still be complete and correct. Record the time. See question 8. |

---

## Open questions

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | What goes in the `timezone` column: IANA name (`America/Toronto`), an offset, or an abbreviation? The story names the column but not its format. | TC-117-12, 28 and AC6 cases | IANA name, since the offset is already in the times and the name is needed for the import to rebuild each night's zone. | Product |
| 2 | For a zero offset, `+00:00` or `Z`? | TC-117-10, 11, 12 | Always `+00:00`, same shape as every other row. | Product |
| 3 | A fall-back wake time of 01:30 happens twice. Can the app record which one, and does the export reflect it? | TC-117-13 | Yes: the export uses the real logged moment, so the offset differs (-04:00 vs -05:00). | Product |
| 4 | When nights in different zones sort differently by "night of" date and by real time, which wins? Also, how are two nights with the same "night of" date ordered? | TC-117-16 | "Night of" date first; ties by bedtime in real time. | Product |
| 5 | Does the file start with a UTF-8 BOM? Excel needs it to show non-English text correctly, but some importers show it as a stray character in the first header. | TC-117-6, 20 | No BOM, since the file must match the import's header exactly; confirm the import's behaviour. | Product |
| 6 | Notes starting with `=`, `+`, `-`, `@` can run as formulas when opened in a spreadsheet. AC5 says "exactly as entered". Should the export add a safety prefix? | TC-117-22, 24 | Keep "exactly as entered" (needed for AC6 round-trip); raise the spreadsheet risk with security. | Product (with security) |
| 7 | Line ending between rows (CRLF or LF) and is there a final line break? | TC-117-19, 27 | CRLF per RFC 4180, with a final line break; parsers must accept either. | Product |
| 8 | On what device and connection is the 2-second limit measured, and does it include the browser's save step? Is there any behaviour expected above 1,000 nights? | TC-117-30, 31, 32 | Measured on a mid-range phone, from click to file saved; larger diaries just have to work, with no stated time limit. | Product |
