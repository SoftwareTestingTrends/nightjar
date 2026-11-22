# Test cases for S-117: Export the diary as CSV

Story: [S-117](../stories/S-117.md). Traces to [BR-07](../requirements/BR-07.md).

## Test data

Conventions come from the team's test-data reference (users, clock, named data sets, tricky notes N1 to N8).

| Item | Value |
|---|---|
| Sam | America/Toronto. The default user. |
| Lee | Europe/London |
| Ana | America/Toronto, then Europe/London (the traveller) |
| Default "now" | Thu 19 Nov 2026 10:00, America/Toronto (EST, -05:00) |
| Standard night | Bed 23:00, wake 06:30 local (7 h 30 min) |
| After-midnight night | Bed 00:25, wake 08:00. Its "night of" date is the day before. |
| D-empty | No nights |
| D-week | Sam's standard nights for the nights of 12 to 18 Nov 2026 |
| D-dst | One Toronto and one London night across each 2026 clock change |
| D-notes | One night for each note N1 to N8 |
| D-1000 | 1,000 standard nights for Sam, notes from D-notes repeated |

Expected CSV lines are written as the raw text in the file, opened in a plain-text editor. "Parsed" means read with a standard CSV parser (RFC 4180 rules).

## AC1: Button and file name

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button exists and downloads the named file | 1. Sam with D-week. Now = Thu 19 Nov 2026 10:00 Toronto. 2. Open the home page. 3. Click "Export CSV". | The button labelled "Export CSV" is on the home page. Exactly one file downloads, named `nightjar-diary-2026-11-19.csv`. |
| TC-117-2 | File-name date follows local midnight, the year end and zero padding | Sam with D-week, clicking "Export CSV" at each "now" (Toronto): 1. Thu 19 Nov 2026 23:59. 2. Fri 20 Nov 2026 00:00. 3. Thu 31 Dec 2026 23:59. 4. Fri 1 Jan 2027 00:00. 5. Sun 8 Mar 2026 10:00 (day of the spring change). | File names: 1. `nightjar-diary-2026-11-19.csv` 2. `nightjar-diary-2026-11-20.csv` 3. `nightjar-diary-2026-12-31.csv` 4. `nightjar-diary-2027-01-01.csv` 5. `nightjar-diary-2026-03-08.csv` |
| TC-117-3 | Date uses the user's current time zone, not UTC or another zone | 1. Lee, time zone Europe/London, with D-week. Export at Thu 19 Nov 2026 23:30 London (18:30 Toronto). 2. Lee exports at Fri 20 Nov 2026 00:30 London (Thu 19 Nov 19:30 Toronto). 3. Ana logs a night in Toronto, then changes her time zone to Europe/London. At Fri 20 Nov 2026 00:30 London she exports. | 1. `nightjar-diary-2026-11-19.csv` 2. `nightjar-diary-2026-11-20.csv` 3. `nightjar-diary-2026-11-20.csv` (London date, not the Toronto date of 19 Nov). |
| TC-117-4 | Export holds only the signed-in user's diary | 1. Sam has D-week. Lee has a standard night for 18 Nov 2026. 2. Sam exports. 3. Lee exports. | Sam's file has 7 data rows (nights of 12 to 18 Nov) and none of Lee's, with `Europe/London` nowhere in it. Lee's file has 1 data row. |

## AC2: Header and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-5 | Header row is exact | 1. Sam with D-week exports. 2. Open the file in a plain-text editor. | Line 1 is exactly `bedtime,wake_time,timezone,notes`: lower case, no spaces, no quotes. It appears once. 7 data rows follow it. |
| TC-117-6 | Every row has four fields, in that order | 1. Sam with D-notes exports. 2. Read the file with a CSV parser. | The header and every one of the 8 data records have exactly 4 fields. Field 1 is the bedtime, 2 the wake time, 3 the time zone, 4 the note, in every row. |
| TC-117-7 | `timezone` column holds each night's own zone | 1. Sam with D-week, Lee with a standard night 18 Nov 2026 and Ana with one Toronto night and one London night each export. 2. Read the `timezone` column. | Sam's rows: `America/Toronto`. Lee's row: `Europe/London`. Ana's rows: `America/Toronto` for the Toronto night and `Europe/London` for the London night. See open question 3. |

## AC3: ISO 8601 times with the night's own offset

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-8 | The story's own example | 1. Sam logs an after-midnight night: bed Sun 1 Mar 2026 00:25, wake Sun 1 Mar 2026 08:00 (night of Sat 28 Feb). 2. Export. | Row begins `2026-03-01T00:25:00-05:00,2026-03-01T08:00:00-05:00,America/Toronto`. Seconds are `:00`, no fractions. See open question 11. |
| TC-117-9 | Offset changes with the season and with the zone, including zero offset | Standard nights, exported: 1. Sam, night of Wed 15 Jul 2026. 2. Sam, night of Wed 18 Nov 2026. 3. Lee, night of Wed 15 Jul 2026. 4. Lee, night of Wed 18 Nov 2026. | 1. Bed `2026-07-15T23:00:00-04:00`, wake `2026-07-16T06:30:00-04:00`. 2. Bed `2026-11-18T23:00:00-05:00`, wake `2026-11-19T06:30:00-05:00`. 3. Bed `2026-07-15T23:00:00+01:00`, wake `2026-07-16T06:30:00+01:00`. 4. Bed `2026-11-18T23:00:00+00:00`, wake `2026-11-19T06:30:00+00:00` (see open question 4). |
| TC-117-10 | A night across a clock change has a different offset for bed and wake | Standard nights from D-dst, exported: 1. Toronto, night of Sat 7 Mar 2026. 2. Toronto, night of Sat 31 Oct 2026. 3. London, night of Sat 28 Mar 2026. 4. London, night of Sat 24 Oct 2026. | 1. Bed `2026-03-07T23:00:00-05:00`, wake `2026-03-08T06:30:00-04:00`. 2. Bed `2026-10-31T23:00:00-04:00`, wake `2026-11-01T06:30:00-05:00`. 3. Bed `2026-03-28T23:00:00+00:00`, wake `2026-03-29T06:30:00+01:00`. 4. Bed `2026-10-24T23:00:00+01:00`, wake `2026-10-25T06:30:00+00:00`. |
| TC-117-11 | Repeated hour on the fall-back day carries the offset that applied | 1. Sam, Toronto. In two separate runs, log a night of Sat 31 Oct 2026 with wake Sun 1 Nov 08:00 and bed: run A at the first 01:30 on Sun 1 Nov (EDT, 05:30 UTC); run B at the second 01:30 (EST, 06:30 UTC). 2. Export after each run. | Run A bed `2026-11-01T01:30:00-04:00`. Run B bed `2026-11-01T01:30:00-05:00`. Wake in both: `2026-11-01T08:00:00-05:00`. See open question 9. |
| TC-117-12 | Traveller's older nights keep their own zone's offset | 1. Ana in Toronto logs a standard night for Mon 16 Nov 2026. 2. Ana changes her time zone to Europe/London. 3. Ana logs a standard night for Tue 17 Nov 2026. 4. Export, with London as her current zone. | Row 1: `2026-11-16T23:00:00-05:00,2026-11-17T06:30:00-05:00,America/Toronto`. Row 2: `2026-11-17T23:00:00+00:00,2026-11-18T06:30:00+00:00,Europe/London`. The Toronto night is not shifted to London time. |

## AC4: "Night of" order, oldest first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-13 | Rows are oldest first whatever the entry order | 1. Sam logs standard nights for 15, 12, 18, 13, 17, 14 and 16 Nov 2026, in that order. 2. Export. | The 7 rows are the nights of 12, 13, 14, 15, 16, 17, 18 Nov, in that order. |
| TC-117-14 | After-midnight night is placed by its "night of" date | 1. Sam logs, in this order: a standard night of Sun 15 Nov; an after-midnight night of Sat 14 Nov (bed Sun 15 Nov 00:25, wake 08:00); a standard night of Fri 13 Nov. 2. Export. | Rows in order: night of 13 Nov (bed `2026-11-13T23:00:00-05:00`), night of 14 Nov (bed `2026-11-15T00:25:00-05:00`), night of 15 Nov (bed `2026-11-15T23:00:00-05:00`). |
| TC-117-15 | Order holds across single and double digits, month, year and clock change | 1. Sam logs standard nights in newest-first order for: 30 Oct, 31 Oct, 1 Nov, 9 Nov, 10 Nov, 31 Dec 2026 and 1 Jan 2027. 2. Export. | Rows run 30 Oct, 31 Oct, 1 Nov, 9 Nov, 10 Nov, 31 Dec 2026, 1 Jan 2027. Night of 9 Nov comes before 10 Nov, and 31 Dec before 1 Jan. |

## AC5: Journal notes exactly as entered

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-16 | Commas and double quotes | 1. Sam logs two nights, with notes N1 `Slept well, woke once` and N2 `Felt "rested" today`. 2. Export. 3. Look at the raw text, then parse. | Raw note fields are `"Slept well, woke once"` and `"Felt ""rested"" today"`. Parsed, each row has 4 fields and the notes equal N1 and N2 exactly. |
| TC-117-17 | Line break inside a note | 1. Sam logs three nights; the middle one has N3 (`Late dinner`, line break, `then reading`). 2. Export. 3. Parse. | The N3 field is wrapped in quotes and contains the line break. The parser returns 3 data records (not 4). The note equals `Late dinner` + line break + `then reading`. Neighbouring rows are unchanged. |
| TC-117-18 | Non-English text and emoji | 1. Sam logs a night with N4 `Très bien 😴`. 2. Export. 3. Parse the file as UTF-8. | The note reads `Très bien 😴`. No `?`, no garbled characters such as `TrÃ¨s`. See open question 2. |
| TC-117-19 | Spaces, very long text and empty note are kept as they are | Sam logs three nights and exports: 1. N5 `  padded  ` (two spaces each side). 2. N7 (2,000 × `a`). 3. N8 (empty note). | 1. Field is `  padded  ` with the 4 spaces kept, not trimmed. 2. All 2,000 `a` characters are present. 3. The 4th field is empty and the row still has 4 fields (it ends in `,`). |
| TC-117-20 | A note that a spreadsheet may run as a formula | 1. Sam logs a night with N6 `=1+1`. 2. Export. 3. Look at the raw text. | The note is exported exactly as `=1+1`, per AC5. See open question 5. |

## AC6: Import gives the same nights

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-21 | Round trip of a normal week | 1. Sam with D-week exports. 2. Sam uses an empty diary. 3. Import the exported file. 4. Compare. 5. Export again. | The diary has the same 7 nights: same bedtime, wake time, time zone and note for each, with nights of 12 to 18 Nov. The second file's rows are identical to the first file's. See open question 7. |
| TC-117-22 | Round trip across clock changes | 1. Sam's diary holds the 4 nights of D-dst (see TC-117-10). 2. Export. 3. Import into an empty diary. | The 4 nights come back with the same bed and wake instants and the same offsets. Toronto spring night is 6 h 30 min long, Toronto fall night 8 h 30 min, as before the export. |
| TC-117-23 | Round trip of every tricky note | 1. Sam with D-notes exports. 2. Import into an empty diary. | All 8 notes (N1 to N8) match the originals character for character, including the line break, emoji, padding, 2,000-character note, empty note and `=1+1`. |
| TC-117-24 | Round trip for a traveller keeps the night's own zone | 1. Ana in Toronto logs an after-midnight night: bed Sun 1 Mar 2026 00:25, wake 08:00 (night of Sat 28 Feb). 2. Ana changes to Europe/London. 3. Export. 4. Import into an empty diary, still in London. | The night is still the night of Sat 28 Feb, with time zone `America/Toronto`, bed `00:25 -05:00`. It is not moved to 1 Mar or shown as 05:25 London time. |

## Edge: empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-25 | Empty diary exports the header only | 1. Sam with D-empty. Now = Thu 19 Nov 2026 10:00 Toronto. 2. Click "Export CSV". 3. Open the file. 4. Import it into an empty diary. | A file `nightjar-diary-2026-11-19.csv` downloads. It contains only `bedtime,wake_time,timezone,notes`: no data rows, no blank rows. After import the diary is still empty (AC6, zero nights). |
| TC-117-26 | One night, then back to none | 1. Sam with D-empty logs one standard night for 18 Nov 2026. 2. Export. 3. Delete that night. 4. Export again. | First file: header and exactly 1 data row. Second file: header only. |

## Non-functional: export 1,000 nights in under 2 seconds

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-27 | Time for 1,000 nights | 1. Sam with D-1000. 2. Click "Export CSV". 3. Time from click to the download finishing. 4. Repeat 5 times, including the first run after a fresh sign-in. | Every one of the 5 runs takes under 2 seconds. See open question 10 for how and where it is measured. |
| TC-117-28 | The 1,000-night file is complete | 1. Sam with D-1000 exports. 2. Count records and check first and last rows. | Header plus 1,000 data records, parsed. The oldest and the newest night are present, in oldest-first order, and all notes match their originals (including the 2,000-character N7). |
| TC-117-29 | Just over 1,000 nights is not cut off | 1. Sam with D-1000 plus one more standard night. 2. Export. | The file has header plus 1,001 data records. The story asks for the whole diary, so there is no cap at 1,000. |

## Open questions

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | Which line ending ends each row: CRLF or LF? | TC-117-5, TC-117-17 | CRLF, as in RFC 4180 "standard CSV". Line breaks inside notes are kept as entered. | Product |
| 2 | Is the file UTF-8 with or without a byte-order mark (BOM)? Some spreadsheets need the BOM to show accents correctly. | TC-117-18, TC-117-23 | UTF-8 without BOM. The header line must then start with `bedtime` exactly. | Product |
| 3 | What does the `timezone` column hold? The story names the column but not its values. | TC-117-7, TC-117-8, TC-117-12 | The IANA name of the night's own zone, such as `America/Toronto`, the same as the import accepts. | Product |
| 4 | Is a zero offset written `+00:00` or `Z`? | TC-117-9 | `+00:00`, so every time has the same shape. | Product |
| 5 | A note starting with `=`, `+`, `-` or `@` can run as a formula in a spreadsheet. Export exactly as entered, or prefix it for safety? | TC-117-20, TC-117-23 | Export exactly as entered, because AC5 and AC6 require it. Flag the spreadsheet risk to Product for a later story. | Product |
| 6 | "User's current time zone" in AC1: the zone in the NightJar profile, or the browser's zone? | TC-117-2, TC-117-3 | The zone in the user's NightJar profile, the same one used for the rest of the app. | Product |
| 7 | AC6 relies on an import, but no linked document describes it. Does it exist today, and where is it in the app? | TC-117-21, TC-117-22, TC-117-23, TC-117-24, TC-117-25 | Assume the import exists and accepts the four columns in AC2. If it does not, AC6 cannot be run until it does. | Product |
| 8 | Can two nights have the same "night of" date (a second sleep, a nap)? If so, which comes first? | TC-117-13, TC-117-14, TC-117-15 | Assume one night per date. If two are allowed, the earlier bedtime comes first. | Product |
| 9 | How does a user pick the first or second 01:30 on the fall-back day? | TC-117-11 | The offset follows the instant that was stored (EDT for the first 01:30, EST for the second). | Product |
| 10 | Where is the 2-second limit measured, and on what device? | TC-117-27 | From the click to the file finishing downloading, on a standard team laptop with a local network, worst of 5 runs. | Product |
| 11 | Are seconds always written, and are fractions ever written? The example shows `:00` and no fraction. | TC-117-8, TC-117-9, TC-117-10, TC-117-11, TC-117-12 | Always `HH:MM:SS`, never a fraction. | Product |
