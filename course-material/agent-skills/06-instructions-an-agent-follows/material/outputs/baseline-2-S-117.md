# Test cases for S-117: Export the diary as CSV

Story: [S-117](../stories/S-117.md). Traces to [BR-07](../requirements/BR-07.md).
Claims policy: [claims.md](../claims.md). Written from the spec only (no code read).

## Test data

**User:** Dana, home time zone `America/Toronto` unless a case says otherwise.
**Default "now":** Sat 21 Nov 2026, 10:00 Toronto (EST, UTC-5) = 15:00 UTC.
**DST dates used (2026):**
- Toronto: spring forward Sun 8 Mar (02:00 EST -> 03:00 EDT); fall back Sun 1 Nov (02:00 EDT -> 01:00 EST).
- London: spring forward Sun 29 Mar (01:00 GMT -> 02:00 BST); fall back Sun 25 Oct (02:00 BST -> 01:00 GMT).

**Standard nights** (each stored in its own time zone; the "night of" date follows S-116 AC1, so a 00:25 bedtime counts for the previous date):

| Name | Night of | Zone | Bedtime | Wake time | Notes |
|---|---|---|---|---|---|
| N1 | Fri 27 Feb | America/Toronto | 2026-02-27T23:40:00-05:00 | 2026-02-28T07:10:00-05:00 | `Slept ok` |
| N2 | Sat 28 Feb | America/Toronto | 2026-03-01T00:25:00-05:00 | 2026-03-01T07:55:00-05:00 | `Late film` |
| N3 | Sun 1 Mar | America/Toronto | 2026-03-01T23:10:00-05:00 | 2026-03-02T06:50:00-05:00 | (empty) |

**Nasty notes** (typed exactly as shown; `⏎` = Enter key):
- K1: `Tired, but "ok"`
- K2: `line one⏎line two`
- K3: `He said ""hi"", then left` (two quote characters in a row, as typed)
- K4: `café, 睡眠不足, نوم, 😴`
- K5: `   leading and trailing spaces   `
- K6: `=1+1`
- K7: `Had insomnia again, need a cure` (words banned by the claims register)
- K8: `a,b,"c"⏎⏎d` (comma, quotes and a blank line together)

---

## AC1: "Export CSV" button, file name `nightjar-diary-YYYY-MM-DD.csv`

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button exists and downloads | 1. Log in as Dana with N1-N3. 2. Open the home page. 3. Click "Export CSV". Now = default. | The button is on the home page, labelled "Export CSV". A file `nightjar-diary-2026-11-21.csv` downloads. |
| TC-117-2 | Last minute of the day in Toronto | Now = Sat 21 Nov 2026 23:59 Toronto (04:59 UTC on 22 Nov). Click "Export CSV". | `nightjar-diary-2026-11-21.csv` (Toronto date, not the UTC date). |
| TC-117-3 | First minute of the next day in Toronto | Now = Sun 22 Nov 2026 00:00 Toronto (05:00 UTC). Click "Export CSV". | `nightjar-diary-2026-11-22.csv`. |
| TC-117-4 | Same instant, London is already tomorrow | Now = Sat 21 Nov 2026 23:30 Toronto = Sun 22 Nov 04:30 London. Dana's current zone is Europe/London. Click "Export CSV". | `nightjar-diary-2026-11-22.csv`. |
| TC-117-5 | Same instant, Toronto zone | Same instant as TC-117-4, Dana's current zone is America/Toronto. | `nightjar-diary-2026-11-21.csv`. |
| TC-117-6 | Time zone changed, then export | 1. Now = Sat 21 Nov 2026 22:00 Toronto (03:00 UTC on 22 Nov), Dana's zone is Toronto. 2. Export and note the name. 3. Change Dana's zone to Europe/London (same instant). 4. Export again. | Step 2: `...-2026-11-21.csv`. Step 4: `...-2026-11-22.csv`. |
| TC-117-7 | London summer time moves the date | Zone Europe/London. Now = 2026-06-30 23:30 UTC (= Wed 1 Jul 00:30 BST). Export. | `nightjar-diary-2026-07-01.csv`. |
| TC-117-8 | Toronto spring-forward day, before the gap | Now = Sun 8 Mar 2026 01:59 EST. Export. | `nightjar-diary-2026-03-08.csv`. |
| TC-117-9 | Toronto spring-forward day, after the gap | Now = Sun 8 Mar 2026 03:00 EDT. Export. | `nightjar-diary-2026-03-08.csv`. |
| TC-117-10 | Toronto fall-back day, both 01:30s | Export at Sun 1 Nov 2026 01:30 EDT (05:30 UTC) and again at 01:30 EST (06:30 UTC). | Both files are `nightjar-diary-2026-11-01.csv`. |
| TC-117-11 | London days around the clock changes | Zone Europe/London. Export at Sun 29 Mar 2026 00:30 GMT and 02:30 BST. Then at Sun 25 Oct 2026 01:30 BST and 01:30 GMT. | March exports: `...-2026-03-29.csv`. October exports: `...-2026-10-25.csv`. |
| TC-117-12 | Year boundary | Now = Thu 31 Dec 2026 23:30 Toronto (04:30 UTC on 1 Jan). Export with zone Toronto, then with zone Europe/London at the same instant. | Toronto: `nightjar-diary-2026-12-31.csv`. London: `nightjar-diary-2027-01-01.csv`. |
| TC-117-13 | Single-digit month and day are zero-padded | Now = Mon 5 Jan 2026 10:00 Toronto. Export. | `nightjar-diary-2026-01-05.csv` (not `2026-1-5`). |
| TC-117-14 | Leap day | Now = Tue 29 Feb 2028 10:00 Toronto. Export. | `nightjar-diary-2028-02-29.csv`. |
| TC-117-15 | Button text passes the claims check | Run `claims.check_text` on "Export CSV" and on any other text added to the home page for this feature. | No violations. |

## AC2: Header row and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-16 | Header is the first line, exact text | Export N1-N3. Open the file in a plain-text editor. | Line 1 is exactly `bedtime,wake_time,timezone,notes`: lower case, underscore, no spaces, no quotes, this order. |
| TC-117-17 | One data row per night, four fields each | Same file as TC-117-16. | Exactly 3 data rows after the header, each with 4 fields. No extra columns. |
| TC-117-18 | Header matches the import | Compare line 1 with the header the import accepts. | Identical text and column order. |
| TC-117-19 | Header appears once | Export a diary with 1 night, then one with 1,000 nights. | The header appears once, at the top, in both files. |

## AC3: ISO 8601 times with the offset from that night's own time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-20 | The story's own example | Export N2. | bedtime is `2026-03-01T00:25:00-05:00`. |
| TC-117-21 | Format of every time value | Export N1-N3. | Every bedtime and wake_time looks like `YYYY-MM-DDTHH:MM:SS±HH:MM`: `T` separator, offset always present. |
| TC-117-22 | Night from another zone keeps its own offset | 1. Dana's current zone is Europe/London (winter, +00:00). 2. Her diary has N1 (Toronto). 3. Export. | N1 still shows `-05:00` on both times; it is not converted to the current zone. |
| TC-117-23 | Zone column agrees with the offsets | Diary: N1 plus a London night 2026-11-10T23:00 -> 2026-11-11T07:00 (GMT). Export. | Each row's `timezone` is that night's own zone, and its offsets match that zone on that date. |
| TC-117-24 | Toronto spring forward: bedtime before, wake after | Bedtime Sat 7 Mar 2026 23:30, wake Sun 8 Mar 07:00, Toronto. Export. | bedtime `2026-03-07T23:30:00-05:00`, wake `2026-03-08T07:00:00-04:00`. |
| TC-117-25 | Toronto fall back: wake at the repeated 01:30 | Two nights, Toronto, bedtime Sat 31 Oct 23:30 EDT. Night A wakes at the first 01:30 (EDT), night B at the second 01:30 (EST). Export. | A wake `2026-11-01T01:30:00-04:00`. B wake `2026-11-01T01:30:00-05:00`. |
| TC-117-26 | London spring forward | Bedtime Sat 28 Mar 2026 23:30 GMT, wake Sun 29 Mar 07:00 BST. Export. | wake `2026-03-29T07:00:00+01:00`; bedtime has the GMT offset (see open question 2 on how it is written). |
| TC-117-27 | London fall back: wake at the repeated 01:30 | Two nights, London, bedtime Sat 24 Oct 23:30 BST. A wakes at 01:30 BST, B at 01:30 GMT. Export. | A wake `2026-10-25T01:30:00+01:00`. B wake `2026-10-25T01:30:00` with the GMT offset. |
| TC-117-28 | A night on the DST day, outside the gap | Toronto bedtime Sun 8 Mar 2026 22:30, wake Mon 9 Mar 06:30. | Both times use `-04:00`. |
| TC-117-29 | Half-hour offset | Asia/Kolkata: bedtime 2026-11-10T23:00, wake 2026-11-11T06:30. Export. | Both end in `+05:30`. |
| TC-117-30 | Positive offset | Pacific/Auckland: bedtime 2026-11-11T21:00 (NZDT). Export. | Ends in `+13:00`. |
| TC-117-31 | Midnight bedtime | Toronto bedtime 2026-11-15 00:00. Export. | `2026-11-15T00:00:00-05:00` (not `24:00`). |
| TC-117-32 | Bed and wake on the same calendar date | Export N2 (bed 00:25, wake 07:55, both on 1 Mar). | Both times show `2026-03-01`, as stored. |

## AC4: "Night of" order, oldest first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-33 | Simple order | Add N3, N1, N2 in that order. Export. | Rows in order N1, N2, N3. |
| TC-117-34 | Order uses "night of", not the date of the bedtime | Diary: N1, N2, N3, entered N3, N2, N1. | N2 (bedtime dated 1 Mar, night of 28 Feb) sits between N1 and N3, even though its bedtime date is the same as N3's bedtime date. |
| TC-117-35 | Just-after-midnight night sorts with the previous date | Nights: Z bedtime Fri 13 Nov 23:00; X bedtime Sun 15 Nov 00:15 (night of Sat 14 Nov); W bedtime Sun 15 Nov 23:30. Enter W, Z, X. Export. | Order Z (13 Nov), X (14 Nov), W (15 Nov). |
| TC-117-36 | Mixed zones: order is not by instant | Honolulu night of Tue 10 Nov, bedtime 2026-11-10T23:00:00-10:00 (09:00 UTC on 11 Nov). Auckland night of Wed 11 Nov, bedtime 2026-11-11T21:00:00+13:00 (08:00 UTC on 11 Nov). Export. | Honolulu (10 Nov) first, Auckland (11 Nov) second, though Auckland's bedtime is the earlier instant. |
| TC-117-37 | Month and year boundaries | Nights of Wed 31 Dec 2025, Thu 1 Jan 2026, Sat 28 Feb 2026, Sun 1 Mar 2026, entered in reverse. | Exported oldest first across the boundaries. |
| TC-117-38 | Nights across a DST change | Toronto nights of Sat 7, Sun 8 and Mon 9 Mar 2026. | In date order; night of 7 Mar first. |
| TC-117-39 | Single night | Diary with only N1. | Header and one data row. |
| TC-117-40 | Order in a large file | 1,000 nights entered in random order. | Strictly oldest first from first row to last. |

## AC5: Notes exported exactly as entered, standard CSV quoting

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-41 | Plain note | Export N1 (`Slept ok`). | Field is `Slept ok`. |
| TC-117-42 | Comma | Note `Tired, but ok`. | Field is quoted: `"Tired, but ok"`. Row still parses to 4 fields. |
| TC-117-43 | Quotes | Note K1. | Field is `"Tired, but ""ok"""`. Parses back to K1. |
| TC-117-44 | Adjacent quotes | Note K3. | Every typed quote is doubled; parses back to K3 exactly. |
| TC-117-45 | Line break | Note K2. | Field is quoted and contains the line break. A standard CSV reader gives one row with `line one⏎line two`. |
| TC-117-46 | Comma, quotes and blank line together | Note K8. | One row after parsing, notes `a,b,"c"⏎⏎d`, blank line kept. |
| TC-117-47 | Non-English and emoji | Note K4. | Unchanged (no `?`, no garbled text) when read as UTF-8. |
| TC-117-48 | Empty note | Export N3. | Notes field empty; row still has 4 fields. |
| TC-117-49 | Leading and trailing spaces | Note K5. | Spaces kept. |
| TC-117-50 | Note starting with `=` | Note K6. | Exported as the text `=1+1`, unchanged (see open question 5). |
| TC-117-51 | Note with claims-register words is not rewritten | Note K7. | Exported exactly as typed (see open question 6). |
| TC-117-52 | Very long note | One note of 10,000 characters with commas and line breaks. | Exported complete, no truncation (see open question 8). |
| TC-117-53 | Note that looks like a CSV row | Note `2026-01-01T00:00:00-05:00,2026-01-01T07:00:00-05:00,America/Toronto,x`. | One quoted field; parsed back it is one night with that note. |
| TC-117-54 | Several nights with mixed notes | Nights with K1, K2, K4, K8 and an empty note. | Parsed row count equals night count; each note equals what was entered. |

## AC6: Round trip into an empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-55 | Basic round trip | 1. Export N1-N3. 2. Sign in as a user with an empty diary. 3. Import the file. | Same 3 nights: same instants and offsets, zone, notes and order. |
| TC-117-56 | Nasty notes | Diary with K1-K8, one per night. Export, import to an empty diary. | All 8 notes identical to what was typed. |
| TC-117-57 | Across DST | Nights from TC-117-24 to 27. Round trip. | Same instants, same durations; the two repeated-01:30 nights stay different. |
| TC-117-58 | Several zones | Toronto, London, Honolulu, Auckland and Kolkata nights (TC-117-22, 23, 29, 30, 36). | Each keeps its zone, offset and "night of" date. |
| TC-117-59 | "Night of" date | N2 (bedtime 00:25 on 1 Mar). | Still the night of Sat 28 Feb, between N1 and N3. |
| TC-117-60 | Export again after import | Round trip, then export the new diary. | Same content as the first file (name differs only if the day differs). |
| TC-117-61 | Empty diary round trip | Export an empty diary, import it into an empty diary. | Diary stays empty. (How the import reports 0 nights is not specified.) |
| TC-117-62 | 1,000 nights | Export 1,000 nights, import into an empty diary. | 1,000 nights, same content and order. |

## Edge: Empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-63 | New user, no nights | Sign in as a user with no nights. Click "Export CSV". | A file downloads, named for today as in AC1. It contains only `bedtime,wake_time,timezone,notes`. |
| TC-117-64 | Minimum data: one night | Diary with N1 only. | Header plus one data row. |
| TC-117-65 | Diary emptied again | Log N1, delete it (if the product allows), export. | Header only. |
| TC-117-66 | Empty diary at midnight | Empty diary. Now = Sun 22 Nov 2026 00:00 Toronto. Export. | Header only, named `nightjar-diary-2026-11-22.csv`. |

## Non-functional: 1,000 nights in under 2 seconds

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-67 | Exactly 1,000 nights | 1,000 nights with short notes. Time from click until the file is ready. Repeat 5 times. | Every run under 2 seconds. |
| TC-117-68 | 1,000 heavy nights | 1,000 nights, each with a 500-character note full of commas, quotes, line breaks and non-English text. | Every run under 2 seconds; file parses to 1,000 rows. |
| TC-117-69 | Many zones and DST | 1,000 nights across Toronto, London, Auckland and Kolkata, including DST-change nights. | Under 2 seconds; offsets correct. |
| TC-117-70 | Either side of 1,000 | Time exports with 999 and 1,001 nights. | Both complete and correct; 999 is under 2 seconds. For 1,001 no limit is stated (open question 7). |

---

## Open questions

| # | Question | Cases affected | Who should answer |
|---|---|---|---|
| 1 | What goes in the `timezone` column (IANA name such as `America/Toronto`, an abbreviation, an offset)? The story says "same columns as the import", but the import format isn't in the story. | TC-117-17, 18, 23, 55, 58 | Product |
| 2 | How is a zero offset written: `+00:00` or `Z`? The examples only show `-05:00`. | TC-117-26, 27 | Product |
| 3 | Are seconds always written (`:00`), even if the user entered only hours and minutes? | TC-117-21, 31 | Product |
| 4 | Line ending (CRLF or LF) and file encoding (UTF-8, with or without BOM). "Standard CSV quoting" doesn't say. | TC-117-45, 47, 54 | Product |
| 5 | A note starting with `=`, `+`, `-` or `@` can run as a formula in a spreadsheet. AC5 says "exactly as entered". Stay exact, or protect against it? | TC-117-50 | Product |
| 6 | Notes can contain words banned by the claims register (e.g. "insomnia"). Confirm the export must not run `check_text` on user notes or alter them. | TC-117-51 | Regulatory & Brand |
| 7 | Is anything required above 1,000 nights? What device, network and browser does the 2-second target assume, and is it measured to download start or to the end of the file? | TC-117-67 to 70 | Product |
| 8 | Is there a maximum note length? Is a long note cut anywhere? | TC-117-52 | Product |
| 9 | How should two nights with the same "night of" date be ordered, and are they allowed? | TC-117-36 (partly) | Product |
| 10 | "Night of" is defined in S-116 AC1, and S-117 doesn't link to it. Confirm the same rule applies to the export order. | TC-117-34, 35, 59 | Product |
| 11 | Is any message shown on export (success, failure, empty diary)? None is specified. Any wording must pass the claims check. | TC-117-15, 63 | Product (wording: Regulatory & Brand) |
| 12 | Does "whole diary" include deleted or hidden nights, or nights dated after "now"? | TC-117-65 | Product |
