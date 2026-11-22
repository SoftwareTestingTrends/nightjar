# Test cases: S-117 Export the diary as CSV

Story: [S-117](../stories/S-117.md). Traces to [BR-07](../requirements/BR-07.md).

## Test data

**User:** Aisha, home time zone America/Toronto. She starts every case with an empty diary unless the case says otherwise. "Now" is Sat 21 Nov 2026 10:00 Toronto (EST, UTC-5) unless the case says otherwise.

**DST dates in 2026:**

- Toronto: clocks go forward Sun 8 Mar 02:00 (EST -05:00 to EDT -04:00). They go back Sun 1 Nov 02:00 (EDT to EST), so 01:00-01:59 happens twice.
- London: clocks go forward Sun 29 Mar 01:00 UTC (GMT +00:00 to BST +01:00). They go back Sun 25 Oct 01:00 UTC.

**Reusable nights** ("night of" date, time zone, bed, wake, note):

| Name | Night of | Zone | Bed | Wake | Note |
|---|---|---|---|---|---|
| N1 | Sat 28 Feb | Toronto | Sun 1 Mar 00:25 | Sun 1 Mar 07:30 | `ok` |
| N2 | Fri 6 Mar | Toronto | Fri 6 Mar 23:00 | Sat 7 Mar 07:00 | `plain` |
| N3 | Sat 7 Mar (DST start) | Toronto | Sat 7 Mar 23:30 (-05:00) | Sun 8 Mar 07:00 (-04:00) | `spring` |
| N4 | Sat 31 Oct (DST end) | Toronto | Sat 31 Oct 23:00 (-04:00) | Sun 1 Nov 07:00 (-05:00) | `fall` |
| N5 | Sat 28 Mar | London | Sat 28 Mar 23:30 (+00:00) | Sun 29 Mar 07:00 (+01:00) | `uk spring` |
| N6 | Sat 18 Jul | London | Sat 18 Jul 23:15 (+01:00) | Sun 19 Jul 07:15 (+01:00) | `uk summer` |
| N7 | Sat 31 Oct | Toronto | Sun 1 Nov 01:30 EDT (first 01:30) | Sun 1 Nov 07:00 | `first` |
| N8 | Sat 31 Oct | Toronto | Sun 1 Nov 01:30 EST (second 01:30) | Sun 1 Nov 07:00 | `second` |

---

## AC1: "Export CSV" button, file name `nightjar-diary-YYYY-MM-DD.csv`

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Normal day: button on home page and file name | 1. Log N2. 2. Open the home page. 3. Click "Export CSV". | The button is on the home page. A file named `nightjar-diary-2026-11-21.csv` downloads. |
| TC-117-2 | Late evening: date comes from the user's zone, not UTC | 1. Log N2. 2. Set now to Sat 21 Nov 23:50 Toronto (Sun 22 Nov 04:50 UTC). 3. Click "Export CSV". | The file is `nightjar-diary-2026-11-21.csv`, not `-22`. |
| TC-117-3 | Time zone change moves the date | 1. Log N2. 2. Now = Sat 21 Nov 19:30 Toronto (Sun 22 Nov 00:30 London). 3. Export in Toronto. 4. Change the user's time zone to Europe/London and export again. | First file is `nightjar-diary-2026-11-21.csv`. Second file is `nightjar-diary-2026-11-22.csv`. |
| TC-117-4 | Just after local midnight and a leading-zero date | 1. Now = Sun 1 Nov 2026 00:05 Toronto (still EDT, before the clocks go back). 2. Export. 3. Now = Mon 4 Jan 2027 00:05 Toronto. 4. Export. | Files are `nightjar-diary-2026-11-01.csv` and `nightjar-diary-2027-01-04.csv`. Month and day are zero-padded. |
| TC-117-5 | Button label passes the claims check | 1. Run `claims.check_text("Export CSV")`. 2. Read the visible button text and any tooltip or confirmation message. | No violations. The text uses no banned or disease wording. |

## AC2: Header row and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-6 | Header text and order | 1. Log N1, N2, N3. 2. Export. 3. Open the file as plain text. | Line 1 is exactly `bedtime,wake_time,timezone,notes`. The header appears once. Data lines follow with 4 fields each. |
| TC-117-7 | Columns hold the right values | 1. Log N6. 2. Export. | One data row. `bedtime` is the bed time, `wake_time` is the wake time, `timezone` is `Europe/London`, `notes` is `uk summer`. No value is in the wrong column. |
| TC-117-8 | Header matches the import | 1. Take the import sample or template file. 2. Compare its header with the export header. | Both headers are identical, character for character and in the same order. |

## AC3: ISO 8601 times with the night's own UTC offset

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-9 | Story example: winter night in Toronto | 1. Log N1. 2. Export. | `bedtime` is `2026-03-01T00:25:00-05:00`. `wake_time` is `2026-03-01T07:30:00-05:00`. |
| TC-117-10 | Offset changes within a night: Toronto spring forward | 1. Log N3. 2. Export. | `bedtime` is `2026-03-07T23:30:00-05:00`. `wake_time` is `2026-03-08T07:00:00-04:00`. Each time carries the offset in force at that moment. |
| TC-117-11 | Toronto fall back, including the repeated hour | 1. Log N4, N7 and N8. 2. Export. | N4 bed is `...-04:00` and wake is `2026-11-01T07:00:00-05:00`. N7 bed is `2026-11-01T01:30:00-04:00`. N8 bed is `2026-11-01T01:30:00-05:00`. The two 01:30 times are different. |
| TC-117-12 | London nights, exported while the user is set to Toronto | 1. Log N5 and N6. 2. Keep the user's current zone as Toronto. 3. Export. | N5 bed is `2026-03-28T23:30:00` with the London offset `+00:00` (see open question 1) and wake is `2026-03-29T07:00:00+01:00`. N6 bed is `2026-07-18T23:15:00+01:00`. No time uses the Toronto offset (-04:00 or -05:00). |
| TC-117-13 | Time zone changed after logging | 1. Log N1 while the user is in Toronto. 2. Change the user's zone to Europe/London. 3. Export. | N1 is still `2026-03-01T00:25:00-05:00`. The export does not convert it to the current zone. |

## AC4: "Night of" order, oldest first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-14 | Logged out of order | 1. Log N4, then N1, then N3, then N2 (newest and oldest mixed). 2. Export. | Rows are in the order N1 (28 Feb), N2 (6 Mar), N3 (7 Mar), N4 (31 Oct). |
| TC-117-15 | Order uses "night of", across midnight | 1. Log N1 (bed Sun 1 Mar 00:25, night of Sat 28 Feb). 2. Log a night of Sun 1 Mar with bed Sun 1 Mar 23:00. 3. Log a night of Fri 27 Feb with bed Fri 27 Feb 23:00. 4. Export. | Order is Fri 27 Feb, Sat 28 Feb (N1), Sun 1 Mar. N1 sits between the other two even though its bed time is on 1 Mar. |
| TC-117-16 | Month, year and day-number boundaries | 1. Log nights of Fri 9 Oct 2026, Sat 10 Oct, Thu 31 Dec 2026 and Fri 1 Jan 2027, all in Toronto. 2. Export. | Order is 9 Oct, 10 Oct, 31 Dec, 1 Jan. `10` does not sort before `9`. |
| TC-117-17 | Two nights with the same "night of" date | 1. Log N7 and N8 (same night of, different instants), in reverse order. 2. Export. | Both rows are present. Their order is the one decided in open question 2. |
| TC-117-18 | Nights in different zones | 1. Log N6 (London, night of 18 Jul) and a Toronto night of Fri 17 Jul, bed 23:00 (-04:00). 2. Export. | Toronto night of 17 Jul comes first, then N6 (night of 18 Jul). Zones do not affect "night of" order. |

## AC5: Notes exported as entered, standard CSV quoting

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-19 | Comma, double quote and line break | 1. Log N2 with the note `Slept ok, "mostly"` + line break + `woke at 3`. 2. Export. 3. Open in a standard CSV parser (and as plain text). | In plain text the field is wrapped in double quotes, inner quotes are doubled (`""mostly""`), and the line break stays inside the quotes. The parser returns 1 data row and the note matches the input exactly. |
| TC-117-20 | Non-English text and emoji | 1. Log notes: `Je n'ai pas bien dormi, très fatigué`; `昨晩はよく眠れた`; `Спал плохо`; `😴🌙`. 2. Export. 3. Open the file in a UTF-8 reader. | Every note reads back identical. No `?` or garbled characters. |
| TC-117-21 | Empty and whitespace-only notes | 1. Log N1 with no note. 2. Log N2 with the note `  two spaces both sides  `. 3. Export. | N1 has an empty `notes` field and its row still has 4 fields. N2's note keeps its leading and trailing spaces. |
| TC-117-22 | Note that looks like a formula or a header | 1. Log notes `=1+1`, `+44 phone`, `@home`, `-5 min`, and `bedtime,wake_time,timezone,notes`. 2. Export. | Each note reads back exactly as entered (see open question 3 on spreadsheet formulas). The last note stays inside one quoted field and does not create a second header. |
| TC-117-23 | Long note with several line breaks (CRLF and LF) | 1. Log N3 with a 2,000-character note with 3 line breaks (one CRLF, two LF). 2. Export. | One row. The note reads back with the same length and line breaks (see open question 4 on line endings). |

## AC6: Import of an exported file gives the same nights

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-24 | Round trip of a mixed diary | 1. Log N1 to N6 (Toronto and London, DST nights). 2. Export. 3. Clear the diary or use a second empty account. 4. Import the file. | The diary has 6 nights. Each one has the same night of date, bed time, wake time, zone and note as before. The durations are the same (N3 is 6 h 30 min, N4 is 9 h). |
| TC-117-25 | Repeated hour survives the round trip | 1. Log N7 and N8. 2. Export. 3. Import into an empty diary. | Two nights. One has bed at 01:30 EDT and the other 01:30 EST. Their durations are 5 h 30 min and 5 h 30 min plus the extra hour (N7 is 6 h 30 min, N8 is 5 h 30 min). |
| TC-117-26 | Notes survive the round trip | 1. Log the notes from TC-117-19, TC-117-20 and TC-117-22 on three nights. 2. Export. 3. Import into an empty diary. | The three notes are identical to the originals, including quotes, line break, non-English text and spaces. |
| TC-117-27 | "Night of" date survives | 1. Log N1 (bed Sun 1 Mar 00:25). 2. Export. 3. Import into an empty diary. | The night appears as the night of Sat 28 Feb, not Sun 1 Mar. |
| TC-117-28 | Second round trip is stable | 1. Do TC-117-24. 2. Export the imported diary. 3. Compare the two exported files. | The two files have identical rows (file names may differ by date). |

## Edge: Empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-29 | No nights at all | 1. Use an account with no nights. 2. Click "Export CSV". | A file `nightjar-diary-2026-11-21.csv` downloads. It contains only `bedtime,wake_time,timezone,notes`. No error and no blank data row. |
| TC-117-30 | Minimum data: exactly one night | 1. Log N1 only. 2. Export. | The file has the header and exactly 1 data row. |
| TC-117-31 | Empty export imports cleanly | 1. Export an empty diary. 2. Import the file into an empty diary. | The import succeeds and the diary stays empty. |
| TC-117-32 | Diary becomes empty again | 1. Log N1 and N2. 2. Delete both nights. 3. Export. | Header only. Deleted nights do not appear. |

## Non-functional: 1,000 nights in under 2 seconds

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-33 | At the limit: 1,000 nights | 1. Load 1,000 nights across Toronto and London, including DST nights, 20% with notes of about 200 characters with commas and line breaks. 2. Click "Export CSV". 3. Time from the click until the file is ready to save (see open question 5). | Under 2 seconds on the reference device. The file has 1 header and 1,000 data rows, in order. |
| TC-117-34 | Just above the limit: 1,001 nights and 2,000 nights | 1. Repeat TC-117-33 with 1,001 nights, then 2,000. | All rows exported and correct. Times are recorded. Nothing breaks or truncates. 2,000 nights is for information only, not a pass/fail. |
| TC-117-35 | Slow case: every night has a large note | 1. Load 1,000 nights each with a 2,000-character note with quotes and line breaks. 2. Export and time it. | Still under 2 seconds, or the result goes to Product as a risk. |

---

## Open questions

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | A UTC offset of zero: `+00:00` or `Z`? | TC-117-12, TC-117-24 | `+00:00`, to match the numeric offsets in the example and the import. | Product |
| 2 | How are nights with the same "night of" date ordered (repeated hour, or two zones)? | TC-117-17 | By bed time instant, earliest first. | Product |
| 3 | Notes starting with `=`, `+`, `-` or `@` can run as formulas in a spreadsheet. AC5 says "exactly as entered". Do we leave them unchanged? | TC-117-22, TC-117-26 | Leave unchanged, as AC5 and AC6 need exact round trips. Add a short warning in the help text. | Product, with Regulatory & Brand for any added help text |
| 4 | Encoding and line endings: UTF-8 with or without a byte order mark, CRLF or LF between rows, and a final newline? Excel needs the mark to read non-English text. | TC-117-20, TC-117-23 | UTF-8 without mark, CRLF between rows (standard CSV), final newline. Revisit if Excel shows garbled text. | Product |
| 5 | What does the 2-second limit measure, and on which device and network? | TC-117-33 to TC-117-35 | From the click until the browser has the whole file, on a mid-range phone on 4G. | Product |
| 6 | What does the `timezone` column hold, and how are nights with no wake time yet (still in progress) exported? | TC-117-7, TC-117-24 | IANA names like `America/Toronto`. A night with no wake time is exported with an empty `wake_time`. | Product |
| 7 | Does the file name use the time zone saved in the user's profile or the device's current zone when the two differ? | TC-117-2, TC-117-3 | The zone saved in the profile, as that is "the user's current time zone" elsewhere (S-114, S-116). | Product |
