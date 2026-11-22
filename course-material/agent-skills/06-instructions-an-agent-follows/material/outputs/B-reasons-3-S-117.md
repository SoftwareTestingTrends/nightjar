# Test cases: S-117 Export the diary as CSV

Story: [S-117](../stories/S-117.md). Traces to [BR-07](../requirements/BR-07.md).
Expected results come from the story. Where the story is silent, the case points to an open question at the end.

## Test data

**User A** has the time zone America/Toronto. Unless a case says otherwise, "now" is **Sat 21 Nov 2026, 10:00 Toronto** (EST, UTC-5).

**Daylight-saving dates in 2026**

| Zone | Clocks go forward | Clocks go back |
|---|---|---|
| America/Toronto | Sun 8 Mar, 02:00 to 03:00 (-05:00 to -04:00) | Sun 1 Nov, 02:00 to 01:00 (-04:00 to -05:00) |
| Europe/London | Sun 29 Mar, 01:00 to 02:00 (+00:00 to +01:00) | Sun 25 Oct, 02:00 to 01:00 (+01:00 to +00:00) |

**Diary D1 (reused)**: seven nights for User A, all Toronto unless stated.

| Night of | Bedtime | Wake time | Time zone | Notes |
|---|---|---|---|---|
| Sat 28 Feb | 28 Feb 23:40 | 1 Mar 07:10 | America/Toronto | (empty) |
| Sun 1 Mar | 2 Mar 00:25 | 2 Mar 07:30 | America/Toronto | Late film |
| Sat 7 Mar | 7 Mar 23:30 | 8 Mar 07:00 | America/Toronto | Clocks go forward overnight |
| Sat 31 Oct | 31 Oct 23:30 | 1 Nov 07:00 | America/Toronto | Clocks go back overnight |
| Sat 28 Mar | 28 Mar 23:30 | 29 Mar 07:00 | Europe/London | Trip: clocks go forward overnight |
| Sat 24 Oct | 24 Oct 23:15 | 25 Oct 07:00 | Europe/London | Trip: clocks go back overnight |
| Tue 10 Nov | 10 Nov 23:00 | 11 Nov 06:45 | Asia/Kolkata | Trip, +05:30 |

All exports below are made from the home page with the "Export CSV" button, and the file is opened in a plain-text editor, not a spreadsheet app.

---

## AC1: Button and file name

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button exists and downloads one file | 1. Open the home page as User A with D1. 2. Click "Export CSV". | The button is on the home page and labelled "Export CSV". One file downloads. Its name is `nightjar-diary-2026-11-21.csv`. |
| TC-117-2 | Midnight in the user's zone decides the date (not UTC) | 1. Now = Sat 21 Nov 23:30 Toronto (04:30 UTC on 22 Nov). Export. 2. Now = Sun 22 Nov 00:10 Toronto (05:10 UTC). Export. | 1. `nightjar-diary-2026-11-21.csv`. 2. `nightjar-diary-2026-11-22.csv`. |
| TC-117-3 | Changing time zone changes the date | 1. Instant = 19:30 Toronto on Sat 21 Nov, which is 00:30 Sun 22 Nov in London. 2. With the zone set to Toronto, export. 3. Change the user's zone to Europe/London and export again at the same instant. | 2. `nightjar-diary-2026-11-21.csv`. 3. `nightjar-diary-2026-11-22.csv`. |
| TC-117-4 | Dates at daylight-saving changes, including the repeated hour | Export with these "now" values: (a) Toronto Sun 1 Nov 01:30 EDT; (b) Toronto Sun 1 Nov 01:30 EST (the repeated hour); (c) Toronto Sun 8 Mar 03:00 EDT; (d) London Sun 25 Oct 01:30 (both occurrences); (e) London Sun 29 Mar 00:59 and 02:00. | Each date in the file name is the local calendar date: (a) and (b) 2026-11-01; (c) 2026-03-08; (d) 2026-10-25; (e) 2026-03-29. |
| TC-117-5 | Month and year boundaries use zero-padded `YYYY-MM-DD` | Export with now = Thu 31 Dec 2026 23:59 Toronto, Fri 1 Jan 2027 00:00 Toronto, Mon 2 Feb 2026 09:00 Toronto. | `nightjar-diary-2026-12-31.csv`, `nightjar-diary-2027-01-01.csv`, `nightjar-diary-2026-02-02.csv`. Month and day always have 2 digits. |

## AC2: Header row and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-6 | Header is exact, and is the first line | 1. Export D1. 2. Read line 1. | Line 1 is exactly `bedtime,wake_time,timezone,notes`: lower case, underscore, no spaces, no extra columns. See open question 4 for line endings and encoding. |
| TC-117-7 | Every data row has 4 fields in column order | 1. Export D1. 2. Check each of the 7 data rows. | There are 7 data rows after the header. Each has bedtime, wake time, time zone and notes in that order, with 4 fields. A night with empty notes ends with a trailing comma, and its last field is empty. |
| TC-117-8 | The time zone column is filled for every night | 1. Export D1. 2. Read the `timezone` field of each row. | Each row's `timezone` is the zone of that night (Toronto, London or Kolkata), not the user's current zone. Format: see open question 1. |

## AC3: ISO 8601 times with the night's own UTC offset

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-9 | Story example, winter offset | 1. Export D1. 2. Read the row for the night of Sun 1 Mar. | Bedtime is `2026-03-02T00:25:00-05:00`. Wake time is `2026-03-02T07:30:00-05:00`. Format is `YYYY-MM-DDTHH:MM:SS±HH:MM`. |
| TC-117-10 | Summer offset | 1. Log a Toronto night: bed 15 Jul 23:10, wake 16 Jul 07:00. 2. Export. | Bedtime `2026-07-15T23:10:00-04:00`, wake time `2026-07-16T07:00:00-04:00`. |
| TC-117-11 | Offset follows the night's zone, not the user's current zone | 1. User A is in Toronto "now". 2. Export D1. 3. Read the Kolkata night of Tue 10 Nov and the London night of Sat 24 Oct. | Kolkata night: `2026-11-10T23:00:00+05:30` and `2026-11-11T06:45:00+05:30`. London night of 24 Oct: bedtime `2026-10-24T23:15:00+01:00`. None use -05:00. |
| TC-117-12 | Night spans a spring-forward change | 1. Export D1. 2. Read the Toronto night of Sat 7 Mar and the London night of Sat 28 Mar. | Toronto: bedtime `2026-03-07T23:30:00-05:00`, wake time `2026-03-08T07:00:00-04:00`. London: bedtime `2026-03-28T23:30:00+00:00`, wake time `2026-03-29T07:00:00+01:00`. Each time gets the offset in force at that moment. See open question 3. |
| TC-117-13 | Night spans a fall-back change | 1. Export D1. 2. Read the Toronto night of Sat 31 Oct and the London night of Sat 24 Oct. | Toronto: bedtime `2026-10-31T23:30:00-04:00`, wake time `2026-11-01T07:00:00-05:00`. London: bedtime `2026-10-24T23:15:00+01:00`, wake time `2026-10-25T07:00:00+00:00`. |
| TC-117-14 | A time inside the repeated hour keeps its true offset | 1. Log a Toronto night with wake time at the first 01:30 on Sun 1 Nov (EDT) and another with wake time at the second 01:30 (EST). 2. Export. | One row has `2026-11-01T01:30:00-04:00` and the other has `2026-11-01T01:30:00-05:00`. They are not both written with the same offset. See open question 8. |

## AC4: Order, oldest "night of" first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-15 | Nights logged out of order come out sorted | 1. Log the 7 nights of D1 in this order: 31 Oct, 10 Nov, 1 Mar, 28 Mar, 7 Mar, 24 Oct, 28 Feb. 2. Export. | Rows run by night of: 28 Feb, 1 Mar, 7 Mar, 28 Mar, 24 Oct, 31 Oct, 10 Nov. The oldest is first and the newest is last. |
| TC-117-16 | Night of date differs from the bedtime date | 1. Log night of Sat 14 Nov with bed 15 Nov 00:15, wake 07:45. 2. Log night of Sun 15 Nov with bed 15 Nov 22:50. 3. Export. | The night of Sat 14 Nov (bedtime `2026-11-15T00:15:00-05:00`) comes before the night of Sun 15 Nov (bedtime `2026-11-15T22:50:00-05:00`). See open question 2. |
| TC-117-17 | "Night of" order beats absolute-time order across zones | 1. Log night of Tue 10 Nov in Pacific/Honolulu: bed 23:30 (-10:00) = 09:30 UTC on 11 Nov. 2. Log night of Wed 11 Nov in Asia/Tokyo: bed 18:00 (+09:00) = 09:00 UTC on 11 Nov. 3. Export. | The Honolulu night of 10 Nov is first, then the Tokyo night of 11 Nov, even though the Tokyo bedtime is the earlier instant. See open question 2. |
| TC-117-18 | Order at year end and across a daylight-saving change | 1. Log nights of Wed 30 Dec 2026, Thu 31 Dec 2026, Fri 1 Jan 2027, Sat 7 Mar 2026 and Sun 8 Mar 2026. 2. Export. | Order is 7 Mar, 8 Mar, 30 Dec, 31 Dec, 1 Jan 2027. Nights either side of the clock change are not swapped or dropped. |

## AC5: Notes exported exactly as entered

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-19 | Commas and double quotes | 1. Log notes: `Tea, then read` ; `She said "sleep well"` ; `"` (a single quote mark); `a,"b",c`. 2. Export. | Each note is wrapped in double quotes, with inner quotes doubled: `"Tea, then read"`, `"She said ""sleep well"""`, `""""`, `"a,""b"",c"`. A plain parser returns each original string. |
| TC-117-20 | Line breaks inside a note | 1. Log a note of 3 lines: `Line 1`, blank line, `Line 3`. 2. Log a second note with Windows-style `\r\n` breaks. 3. Export. | Each note is quoted and the breaks stay inside the quotes. A parser reads 1 record per night, and the notes match what was typed, including the blank line. See open question 4 for line-ending conversion. |
| TC-117-21 | Non-English text and symbols | 1. Log notes: `昨夜はよく眠れた` ; `Café, très calme` ; `نوم هادئ` ; `Привет 🌙` ; `ñ ü ß`. 2. Export. 3. Read the file as UTF-8. | All characters are identical to the original, with no `?` or garbled characters. Each row stays one record. |
| TC-117-22 | Whitespace, empty and long notes | 1. Log notes: `  leading and trailing  ` ; empty ; only a space ; a note of 5,000 characters ; `x` (1 character). 2. Export. | Spaces are kept. An empty note is an empty last field. The long note is complete and is not cut. |
| TC-117-23 | Notes that look like spreadsheet formulas | 1. Log notes: `=1+1` ; `+44 20 7946 0000` ; `-5 degrees` ; `@home`. 2. Export. | Each is exported exactly as entered, with no added apostrophe or space. See open question 5. |

## AC6: Round trip into an empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-24 | D1 survives export and import | 1. Export D1. 2. Sign in as a new user with an empty diary, in the same time zone. 3. Import the file. 4. Compare the 7 nights with D1. | Same 7 nights. Bedtime, wake time (as instants), time zone and notes match field for field. The nights are in the same order. |
| TC-117-25 | Awkward notes survive a round trip | 1. Log the notes from TC-117-19 to TC-117-22 (commas, quotes, line breaks, non-English, long, blank edges). 2. Export. 3. Import into an empty diary. | Each note is byte-for-byte equal to the original. The number of nights is unchanged. |
| TC-117-26 | Daylight-saving and travel nights survive a round trip, even when the importing user is in another zone | 1. Export D1. 2. Import it into an empty diary of a user whose current zone is Pacific/Auckland. | Nights still show their own zones and the same instants. For example the Toronto night of 7 Mar still wakes at 07:00 -04:00 on 8 Mar. Nothing moves by the difference between zones. |
| TC-117-27 | Round trip, then export again | 1. Export D1 as file F1. 2. Import F1 into an empty diary. 3. Export again as F2. | The content of F2 is identical to F1. Only the date in the file name may differ. |

## Edge: Empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-28 | New user with no nights | 1. Create a user and log nothing. 2. Click "Export CSV". | A file `nightjar-diary-2026-11-21.csv` downloads. It contains the header `bedtime,wake_time,timezone,notes` and no data rows. There is no error message. |
| TC-117-29 | Diary emptied by deleting nights | 1. Start with D1 and delete all 7 nights. 2. Export. | Same result as TC-117-28: header only. |
| TC-117-30 | Minimum data: one night | 1. Log one night, notes empty. 2. Export. | The header and exactly one data row, ending with an empty notes field. Importing this file into an empty diary gives that one night. |
| TC-117-31 | Header-only file imports to an empty diary | 1. Export an empty diary. 2. Import the file into an empty diary. | The diary is still empty. Import gives no error, or a clear message. See open question 9. |

## Non-functional: 1,000 nights in under 2 seconds

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-32 | 1,000 nights with typical notes | 1. Load 1,000 nights across several zones and daylight-saving changes, with notes of up to 200 characters. 2. Click "Export CSV". 3. Time from click until the file is ready to save. Repeat 5 times. | Each run takes under 2 seconds. The file has 1 header and 1,000 data rows. See open question 7 for how to measure. |
| TC-117-33 | 1,000 nights with heavy notes | 1. Load 1,000 nights, every note 5,000 characters with commas, quotes and line breaks. 2. Export and time it. | Under 2 seconds. All 1,000 records parse correctly. See open question 7. |

---

## Open questions

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | What does the `timezone` column hold: an IANA name (`America/Toronto`) or an offset? AC3 already puts the offset in the times. | TC-117-8, TC-117-11, TC-117-24, TC-117-26 | IANA name, matching what the import expects. The offset in the times is then an extra check. | Product |
| 2 | How is a night's "night of" date decided, for example for a 00:15 bedtime? The story says "night of" order but does not define it. | TC-117-15, TC-117-16, TC-117-17 | Use the same rule as the rest of the diary: a bedtime just after midnight belongs to the previous date, and the night's own time zone is used. Product to point to the story that defines it. | Product |
| 3 | On a night that crosses a clock change, does each time carry its own offset, or does the wake time reuse the bedtime offset? | TC-117-12, TC-117-13 | Each time gets the offset in force at that instant in the night's zone, as AC3 says "the UTC offset that applied". | Product |
| 4 | Line endings, trailing newline and text encoding of the file. Does a line break inside a note stay as typed? | TC-117-6, TC-117-20, TC-117-21 | UTF-8 without a byte-order mark, CRLF between rows, one newline after the last row, and line breaks inside notes left exactly as typed. Note that Excel may garble non-English text without a byte-order mark. | Product |
| 5 | Notes starting with `=`, `+`, `-` or `@` can run as formulas when opened in a spreadsheet. AC5 says "exactly as entered". | TC-117-23 | Keep AC5: export unchanged. Product accepts the spreadsheet risk, or adds a separate story for a safe export. | Product |
| 6 | "Today's date in the user's current time zone": is that the time zone saved in the user's profile or the device's? | TC-117-2, TC-117-3, TC-117-4 | The zone saved in the user's profile, which is the one the app uses everywhere else. | Product |
| 7 | How is the 2 seconds measured: the device, the network, and where does it start and stop? | TC-117-32, TC-117-33 | From the click until the browser receives the complete file, on a standard laptop on a normal connection, using the 95th percentile of 5 runs. | Product |
| 8 | Can the repeated hour on the fall-back night be entered in the diary, and how is a time in the skipped hour (Toronto 02:30 on 8 Mar) handled? | TC-117-14 | Stored times are exact instants, so export prints the true offset. Times that do not exist cannot be entered, so no export case is needed. Product to confirm. | Product |
| 9 | Should importing a header-only file give an error, an empty result or a message? This belongs to the import story, but AC6 needs a defined result. | TC-117-31 | Empty diary stays empty, with a short message "No nights found in file". | Product |
| 10 | What is exported for a night that has no wake time yet (bedtime logged, still asleep) or no notes? The story does not mention an unfinished night. | Not covered by a case yet | Export the row with an empty `wake_time` field. Add a case once Product confirms. | Product |
