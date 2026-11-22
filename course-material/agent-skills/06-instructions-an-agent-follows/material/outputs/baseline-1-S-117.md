# Test cases: S-117 Export the diary as CSV

Source: [S-117](../stories/S-117.md), traces to [BR-07](../requirements/BR-07.md). Claims check: [claims](../claims.md).
These cases come from the story only. Where the story is silent, the case points to an open question (OQ) instead of guessing.

## Test data

**Users**

| User | Time zone | Notes |
|---|---|---|
| Ana | America/Toronto | Main user. Diary below. |
| Ben | Europe/London | Used for London DST and for the time zone change cases. |
| Empty | America/Toronto | No nights logged. |

**"Now" values** (each case says which one it uses)

| Name | Instant | Toronto local | London local |
|---|---|---|---|
| NOW-A | 2026-11-21 15:00 UTC | Sat 21 Nov 2026 10:00 (EST, -05:00) | Sat 21 Nov 2026 15:00 (GMT) |
| NOW-B | 2026-11-22 04:30 UTC | Sat 21 Nov 2026 23:30 | Sun 22 Nov 2026 04:30 |
| NOW-C | 2026-11-22 05:00 UTC | Sun 22 Nov 2026 00:00 | Sun 22 Nov 2026 05:00 |
| NOW-D | 2026-11-22 04:59 UTC | Sat 21 Nov 2026 23:59 | Sun 22 Nov 2026 04:59 |

**DST dates in 2026** (Toronto: spring forward Sun 8 Mar, 02:00 to 03:00; fall back Sun 1 Nov, 02:00 to 01:00. London: spring forward Sun 29 Mar, 01:00 to 02:00; fall back Sun 25 Oct, 02:00 to 01:00.)

**Ana's standard diary (D-STD)**, "night of" date is the date the evening began:

| Night of | Bedtime (local) | Wake (local) | Time zone | Notes |
|---|---|---|---|---|
| Fri 27 Feb 2026 | 23:10 | Sat 28 Feb 07:00 | America/Toronto | `Slept well` |
| Sat 28 Feb 2026 | Sun 1 Mar 00:25 | Sun 1 Mar 07:45 | America/Toronto | (empty) |
| Sun 1 Mar 2026 | 22:50 | Mon 2 Mar 06:30 | America/Toronto | `Read, then lights out` |

Expected rows for D-STD, used by several cases:

```
bedtime,wake_time,timezone,notes
2026-02-27T23:10:00-05:00,2026-02-28T07:00:00-05:00,America/Toronto,Slept well
2026-03-01T00:25:00-05:00,2026-03-01T07:45:00-05:00,America/Toronto,
2026-03-01T22:50:00-05:00,2026-03-02T06:30:00-05:00,America/Toronto,"Read, then lights out"
```

(The timezone column format is an assumption, see OQ-1.)

---

## AC1: "Export CSV" button downloads `nightjar-diary-YYYY-MM-DD.csv`

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button is on the home page and downloads a file | 1. Log in as Ana with D-STD. 2. Open the home page. 3. Click "Export CSV". Now = NOW-A. | The button labelled "Export CSV" is on the home page. One file downloads, named `nightjar-diary-2026-11-21.csv`. |
| TC-117-2 | Date uses the user's time zone, late evening (UTC is already the next day) | 1. As Ana, click "Export CSV". Now = NOW-B (Toronto 23:30 Sat 21 Nov, UTC Sun 22 Nov). | File is named `nightjar-diary-2026-11-21.csv`, not `-22`. |
| TC-117-3 | Just before local midnight | 1. As Ana, click "Export CSV". Now = NOW-D (Toronto 23:59). | `nightjar-diary-2026-11-21.csv` |
| TC-117-4 | Exactly local midnight | 1. As Ana, click "Export CSV". Now = NOW-C (Toronto 00:00 Sun 22 Nov). | `nightjar-diary-2026-11-22.csv` |
| TC-117-5 | Time zone change: file date follows the current zone | 1. Ben's profile is Europe/London. 2. Click "Export CSV" at NOW-B (London 04:30 Sun 22 Nov). 3. Change Ben's time zone to America/Toronto. 4. Click "Export CSV" at the same instant. | Step 2 file: `nightjar-diary-2026-11-22.csv`. Step 4 file: `nightjar-diary-2026-11-21.csv`. |
| TC-117-6 | Single-digit month and day are zero-padded | 1. As Ana, click "Export CSV". Now = Sun 5 Apr 2026 10:00 Toronto. | `nightjar-diary-2026-04-05.csv` |
| TC-117-7 | DST day in Toronto: date is still the local date | 1. As Ana, click "Export CSV". Now = Sun 8 Mar 2026 03:30 EDT (07:30 UTC). | `nightjar-diary-2026-03-08.csv` |
| TC-117-8 | DST day in London, hour that doesn't exist or repeats | 1. As Ben, click "Export CSV". Now = Sun 25 Oct 2026 01:30 GMT (the second 01:30; UTC 01:30), then again at the first 01:30 BST (UTC 00:30). | Both files are named `nightjar-diary-2026-10-25.csv`. |
| TC-117-9 | Year boundary | 1. As Ana, click "Export CSV". Now = Thu 31 Dec 2026 23:30 Toronto (UTC is 1 Jan 2027). | `nightjar-diary-2026-12-31.csv` |
| TC-117-10 | Exporting twice in a row | 1. Click "Export CSV" twice at NOW-A. | Two downloads with the same name and the same content. (Browser may add "(1)" to the second file name. That is the browser, not the app.) |
| TC-117-11 | Button text passes the claims check | 1. Read every visible word the export adds to the home page (button label, any tooltip or message). 2. Run each through `claims.check_text`. | No violations. The label is "Export CSV". See OQ-9 for any other text. |

## AC2: Header row and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-12 | Header is the first line, exact text | 1. Export D-STD at NOW-A. 2. Read line 1. | `bedtime,wake_time,timezone,notes` (lower case, in this order, no spaces, no extra columns). |
| TC-117-13 | Header appears once | 1. Export D-STD. 2. Count lines that equal the header. | Exactly one. |
| TC-117-14 | Every row has four fields | 1. Export D-STD. 2. Parse with a standard CSV parser. | Header plus 3 records, each with 4 fields. |
| TC-117-15 | Columns match the import | 1. Compare the export header with the header the import expects. | Same names, same order. (Import spec is not in the docs, see OQ-2.) |
| TC-117-16 | File encoding and line ends | 1. Export D-STD. 2. Open in a hex viewer. | Not specified. See OQ-3. |

## AC3: ISO 8601 times with the offset of the night's own time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-17 | Story example | 1. Use D-STD, the night of Sat 28 Feb. 2. Export. | Bedtime is `2026-03-01T00:25:00-05:00`. Wake is `2026-03-01T07:45:00-05:00`. |
| TC-117-18 | Format has seconds and a colon in the offset | 1. Export D-STD. 2. Check each time. | Every time looks like `YYYY-MM-DDTHH:MM:SS±HH:MM`. No `Z`, no `-0500`, no missing seconds. |
| TC-117-19 | Offset is the night's zone, not the viewer's | 1. Ben (London) logs a night: bed Mon 2 Feb 2026 23:00, wake Tue 3 Feb 07:00, zone Europe/London. 2. Change Ben's current zone to America/Toronto. 3. Export. | Bedtime `2026-02-02T23:00:00+00:00`, wake `2026-02-03T07:00:00+00:00`. Times are not shifted to Toronto. |
| TC-117-20 | Two nights in two zones in one file | 1. Ana's night of Mon 2 Mar in America/Toronto: bed 23:00, wake 07:00. 2. Ana flies, then logs the night of Wed 4 Mar in Europe/London: bed 23:30, wake 07:30. 3. Export. | Row 1 offsets `-05:00`. Row 2 offsets `+00:00`. Each row has its own zone in the timezone column. |
| TC-117-21 | Toronto night in summer time | 1. Ana logs bed Mon 6 Jul 2026 23:00, wake Tue 7 Jul 06:30, America/Toronto. 2. Export. | `2026-07-06T23:00:00-04:00`, `2026-07-07T06:30:00-04:00`. |
| TC-117-22 | London night in summer time | 1. Ben logs bed Mon 6 Jul 2026 23:00, wake Tue 7 Jul 06:30, Europe/London. 2. Export. | `2026-07-06T23:00:00+01:00`, `2026-07-07T06:30:00+01:00`. |
| TC-117-23 | Toronto night just before spring forward | 1. Ana logs bed Sat 7 Mar 2026 23:30, wake Sun 8 Mar 07:00, America/Toronto. 2. Export. | Bedtime `2026-03-07T23:30:00-05:00`. Wake `2026-03-08T07:00:00-04:00` (the wake time is after the change). See OQ-4 on whether wake uses its own offset. |
| TC-117-24 | Toronto night just before fall back | 1. Ana logs bed Sat 31 Oct 2026 23:30, wake Sun 1 Nov 07:00, America/Toronto. 2. Export. | Bedtime `2026-10-31T23:30:00-04:00`. Wake `2026-11-01T07:00:00-05:00`. See OQ-4. |
| TC-117-25 | London night across spring forward | 1. Ben logs bed Sat 28 Mar 2026 23:30, wake Sun 29 Mar 07:00, Europe/London. 2. Export. | Bedtime `2026-03-28T23:30:00+00:00`. Wake `2026-03-29T07:00:00+01:00`. See OQ-4. |
| TC-117-26 | London night across fall back | 1. Ben logs bed Sat 24 Oct 2026 23:30, wake Sun 25 Oct 07:00, Europe/London. 2. Export. | Bedtime `2026-10-24T23:30:00+01:00`. Wake `2026-10-25T07:00:00+00:00`. See OQ-4. |
| TC-117-27 | Bedtime inside the repeated hour (fall back) | 1. Ana's diary has a bedtime at the second 01:30 on Sun 1 Nov 2026 (06:30 UTC), zone America/Toronto. 2. Export. | Offset should be `-05:00`. The first 01:30 (05:30 UTC) should be `-04:00`. The two must not both come out the same. See OQ-5. |
| TC-117-28 | Zone with a half-hour or odd offset | 1. Ana logs a night in Asia/Kolkata: bed 23:00, wake 06:30. 2. Export. | `+05:30` on both times. |
| TC-117-29 | Bedtime at exactly midnight | 1. Ana logs bed Mon 2 Mar 00:00, wake 08:00, America/Toronto (night of Sun 1 Mar). 2. Export. | `2026-03-02T00:00:00-05:00`. Row is placed as the night of Sun 1 Mar (see AC4). |
| TC-117-30 | Bedtime one minute before and after midnight | 1. Log bed 23:59 on Mon 2 Mar (night of Mon 2 Mar) and bed 00:01 on Wed 4 Mar (night of Tue 3 Mar). 2. Export. | `2026-03-02T23:59:00-05:00` and `2026-03-04T00:01:00-05:00`. |

## AC4: "Night of" order, oldest first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-31 | Normal order | 1. Log D-STD in the order 1 Mar, 27 Feb, 28 Feb. 2. Export. | Rows come out night of 27 Feb, 28 Feb, 1 Mar. |
| TC-117-32 | Midnight bedtime sorts by the night it belongs to | 1. Log night of Sat 28 Feb with bed Sun 1 Mar 00:25. 2. Log night of Sun 1 Mar with bed 22:50. 3. Export. | The 00:25 row comes before the 22:50 row, because its "night of" date is earlier, though its bedtime date (1 Mar) is the same. |
| TC-117-33 | Across a month and year end | 1. Log nights of Wed 30 Dec 2026, Thu 31 Dec 2026, Fri 1 Jan 2027 (bed 00:30 on Sat 2 Jan counts as Fri 1 Jan). 2. Export. | Order: 30 Dec, 31 Dec, 1 Jan. |
| TC-117-34 | Nights in different zones | 1. Night of Mon 2 Mar in Toronto (bed 23:00 -05:00 = 04:00 UTC Tue 3 Mar). 2. Night of Tue 3 Mar in London (bed 22:00 +00:00 = 22:00 UTC Tue 3 Mar). 3. Export. | Mon 2 Mar night first, Tue 3 Mar night second. Order follows the "night of" date. |
| TC-117-35 | Zone change makes the clock order and the night order disagree | 1. Night of Tue 3 Mar in London: bed 22:00 (22:00 UTC Tue 3 Mar). 2. Night of Wed 4 Mar in Pacific/Auckland: bed Wed 4 Mar 23:00 NZDT (10:00 UTC Wed 4 Mar). The later "night of" has the earlier UTC time. 3. Export. | Rows follow "night of" (3 Mar then 4 Mar), as the story says. |
| TC-117-36 | Two nights with the same "night of" date | Depends on whether the diary allows it. | See OQ-6. |
| TC-117-37 | 7-night export, 1 Nov DST weekend | 1. Log nights from Wed 28 Oct to Tue 3 Nov 2026 in Toronto (bed 23:00 each, wake 07:00). 2. Export. | 7 rows in date order. Offsets `-04:00` through the night of Sat 31 Oct bedtime. Night of Sat 31 Oct wake is `-05:00`. Nights from Sun 1 Nov onward use `-05:00`. |

## AC5: Journal notes exported exactly as entered, standard CSV quoting

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-38 | Plain note | 1. Note `Slept well`. 2. Export. | `Slept well`, unquoted or quoted, and a parser returns exactly `Slept well`. |
| TC-117-39 | Comma | 1. Note `Read, then lights out`. | Field is quoted: `"Read, then lights out"`. Parsed value matches. |
| TC-117-40 | Double quote | 1. Note `He said "shh" twice`. | `"He said ""shh"" twice"`. Parsed value matches. |
| TC-117-41 | Note that is only a quote | 1. Note `"`. | `""""`. Parsed value is `"`. |
| TC-117-42 | Line break (LF) | 1. Note `Line one` + new line + `Line two`. | Field is quoted and holds the line break inside the quotes. The file still has one record for that night. Parsed value is the same text. |
| TC-117-43 | Line break (CRLF), as typed on Windows | 1. Note with `\r\n`. | Field quoted. Parsed value keeps the break as entered. See OQ-7 on whether `\r\n` stays `\r\n`. |
| TC-117-44 | Several line breaks, blank line and trailing break | 1. Note `A\n\nB\n`. | Parsed value is exactly `A\n\nB\n`, trailing break kept. |
| TC-117-45 | Comma, quote and line break together | 1. Note `Ana said, "ok"` + new line + `done`. | Quoted, doubled quotes, break kept. Parsed value matches. |
| TC-117-46 | Non-English text | 1. Notes: `Dormí bien`, `よく眠れた`, `نمت جيدا`, `Спал хорошо`. 2. Export, open as UTF-8. | Each parsed value matches exactly. Nothing is replaced by `?` or garbled. |
| TC-117-47 | Emoji and combining characters | 1. Note `😴 café` (with `e` + combining accent). | Parsed value matches exactly, with no normalisation. |
| TC-117-48 | Leading and trailing spaces | 1. Note `  spaced  `. | Parsed value is `  spaced  `, spaces kept. |
| TC-117-49 | Empty note | 1. Night with no note. | Empty field, still four fields per row. |
| TC-117-50 | Note that looks like a header or a row | 1. Note `bedtime,wake_time,timezone,notes`. | Quoted. It is not treated as a second header. Parsed value matches. |
| TC-117-51 | Note that starts with `=`, `+`, `-` or `@` | 1. Note `=SUM(A1:A2)`. 2. Export. | "Exactly as entered": value is unchanged. Whether to prefix it for spreadsheet safety is not in the story, see OQ-8. |
| TC-117-52 | Very long note | 1. Note of 10,000 characters with commas and line breaks. | Parsed value matches exactly. Max note length is not in the story. |
| TC-117-53 | Note text passes through without a claims check | 1. Note `I think I have insomnia`. 2. Export. | Journal text is the user's own words. The export does not change or hide it. (Claims check applies to NightJar's own text.) See OQ-9. |
| TC-117-54 | Note with tab and backslash | 1. Note `a\tb \ c`. | Parsed value matches exactly. Nothing is escaped with backslashes. |

## AC6: Round trip (import the export into an empty diary)

The import's behaviour is not described in the docs (OQ-2), so these cases check that the imported nights equal the exported ones: bedtime and wake instants, time zone, notes, and "night of" date.

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-55 | Standard round trip | 1. Export D-STD from Ana. 2. Create a new user with an empty diary, Toronto. 3. Import the file. | Three nights with the same bedtime, wake time, zone, notes and "night of" dates (27 Feb, 28 Feb, 1 Mar). |
| TC-117-56 | Round trip is stable | 1. Export from Ana. 2. Import into empty diary. 3. Export again. | The second file is byte for byte the same as the first, apart from the date in the file name if "now" differs. |
| TC-117-57 | Round trip with mixed zones | 1. Use the TC-117-20 diary. 2. Export and import into an empty diary whose current zone is Europe/London. | Each night keeps its own zone and offset. The Toronto night is not shifted to London. |
| TC-117-58 | Round trip across DST | 1. Use the diaries from TC-117-23 to TC-117-26. 2. Export and import. | Same instants. Durations are the same real elapsed time (for example, Toronto night 7 Mar 23:30 to 8 Mar 07:00 is 6 h 30 min of real time). |
| TC-117-59 | Round trip, repeated hour | 1. Use the TC-117-27 diary. 2. Export and import. | Both 01:30 times keep their distinct instants. |
| TC-117-60 | Round trip of all notes in AC5 | 1. Use a diary with the notes from TC-117-38 to TC-117-54. 2. Export and import. | Every note is identical, character for character. |
| TC-117-61 | Midnight bedtime keeps its "night of" | 1. Use night of Sat 28 Feb, bed 00:25 Sun 1 Mar. 2. Export and import. | The imported night is still the night of Sat 28 Feb. |
| TC-117-62 | Round trip of an empty diary | 1. Export Empty. 2. Import into an empty diary. | Import succeeds with 0 nights, and the diary is empty. (Whether import accepts a header-only file is not stated, see OQ-2.) |
| TC-117-63 | Large round trip | 1. Use 1,000 nights. 2. Export and import. | 1,000 nights, all equal. |

## Edge: Empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-64 | Empty diary | 1. Log in as Empty. 2. Click "Export CSV" at NOW-A. | File `nightjar-diary-2026-11-21.csv` downloads. Its content is the header row `bedtime,wake_time,timezone,notes` only, no data rows. |
| TC-117-65 | Minimum data: one night | 1. Log one night. 2. Export. | Header plus exactly one row. |
| TC-117-66 | Diary becomes empty again | 1. Export D-STD. 2. Delete all three nights (if the product allows). 3. Export. | Second file has header only. |
| TC-117-67 | Empty diary shows no extra text | 1. Click "Export CSV" with an empty diary. | Any message the user sees is not defined by the story, see OQ-9. |

## Non-functional: 1,000 nights in under 2 seconds

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-68 | Exactly 1,000 nights | 1. Load 1,000 nights (varied notes, 1 to 200 characters, some with commas, quotes and line breaks; mix of Toronto and London nights, some across DST). 2. Click "Export CSV". 3. Time from click until the download is ready. Repeat 5 times. | Each run is under 2 seconds. File has 1,001 lines of records (header plus 1,000). |
| TC-117-69 | Just under the number | 1. Same as above with 999 nights. | Under 2 seconds. 999 data rows. |
| TC-117-70 | Just over the number | 1. Same as above with 1,001 nights, then 5,000 nights. | The story sets no limit above 1,000. Record the times. The export must still be complete (all rows present). A 2-second target above 1,000 is not required, see OQ-10. |
| TC-117-71 | Large notes | 1. 1,000 nights each with a 5,000-character note. | Complete file. Timing recorded. See OQ-10 for whether this is in scope. |
| TC-117-72 | Page stays usable | 1. During TC-117-68, try to scroll or click elsewhere. | Not specified. Record what happens. |

---

## Open questions

| # | Question | Cases affected | Who should answer |
|---|---|---|---|
| OQ-1 | What goes in the `timezone` column: an IANA name such as `America/Toronto`, or an offset? The story shows only the column name. | Test data, TC-117-14, 19, 20, 28, 57 | Product |
| OQ-2 | The import is not described in the story or linked documents. What does it accept (header row required? header-only file? what happens on bad rows or duplicates)? | TC-117-15, 55 to 63 | Product |
| OQ-3 | File encoding (UTF-8? with a byte-order mark so Excel opens it right?), and the line ending between records (`\n` or `\r\n`). | TC-117-16, 42, 43, 46 | Product |
| OQ-4 | When a night crosses a DST change, does the wake time carry its own offset (as in my cases, for example `-05:00` to `-04:00`), or the bedtime's offset? AC3 says "the offset that applied" in the night's zone, which I read as the offset at that moment. | TC-117-23 to 26, 37, 58 | Product |
| OQ-5 | For a time in the repeated hour at fall back (Toronto 1 Nov, 01:00 to 02:00; London 25 Oct, 01:00 to 02:00), which offset is exported, and how is that time stored? | TC-117-8, 27, 59 | Product |
| OQ-6 | Can a diary hold two nights with the same "night of" date (for example a nap, or a second entry)? If so, what is the order between them? | TC-117-36 | Product |
| OQ-7 | Are line breaks in notes kept as entered (`\r\n` stays `\r\n`) or normalised? AC5 says "exactly as entered". | TC-117-43, 44 | Product |
| OQ-8 | A note starting with `=`, `+`, `-` or `@` can run as a formula when the CSV is opened in a spreadsheet. AC5 says notes are exported exactly as entered. Do we keep that, or add protection? | TC-117-51 | Product (with Regulatory & Brand if it affects user wording) |
| OQ-9 | Is there any text beyond the button label (for example a message on an empty diary, an error if the export fails, a tooltip)? If yes, the exact words must come from the claims register. Does Regulatory & Brand want journal text in the export reviewed? I assumed not (it is the user's own text). | TC-117-11, 53, 67 | Product for the wording; Regulatory & Brand for the claims register |
| OQ-10 | For the 2-second target: on what device and data (note length, zones)? Does it include the browser download, or just the server response? What is expected above 1,000 nights? | TC-117-68 to 72 | Product |
