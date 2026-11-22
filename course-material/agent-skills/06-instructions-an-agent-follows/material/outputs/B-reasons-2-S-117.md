# Test cases: S-117 Export the diary as CSV

Source: [S-117](../stories/S-117.md), traces to [BR-07](../requirements/BR-07.md). The "night of" rule is taken from [S-116](../stories/S-116.md) AC1 (a 00:15 bedtime on Sunday is Saturday night).

## Test data

**Users**

- **Una**: current time zone America/Toronto.
- **Lou**: current time zone Europe/London.

**"Now" values**

| Name | Instant | Una's local date | Lou's local date |
|---|---|---|---|
| NOW-A | Sat 21 Nov 2026 15:00 Toronto (20:00 UTC) | 2026-11-21 | 2026-11-21 |
| NOW-B | Sat 21 Nov 2026 23:30 Toronto (04:30 UTC, 22 Nov) | 2026-11-21 | 2026-11-22 |
| NOW-C | Sun 22 Nov 2026 00:30 Toronto (05:30 UTC) | 2026-11-22 | 2026-11-22 |
| NOW-D | Thu 31 Dec 2026 23:30 Toronto (04:30 UTC, 1 Jan 2027) | 2026-12-31 | 2027-01-01 |

**Standard diary (D1)**, all in America/Toronto:

| Night of | Bedtime | Wake time |
|---|---|---|
| Sat 14 Nov 2026 | 2026-11-14T23:10:00-05:00 | 2026-11-15T07:00:00-05:00 |
| Sun 15 Nov 2026 | 2026-11-15T22:50:00-05:00 | 2026-11-16T06:45:00-05:00 |
| Mon 16 Nov 2026 | 2026-11-16T23:30:00-05:00 | 2026-11-17T07:15:00-05:00 |

**Daylight-saving nights** (2026 transitions: Toronto spring forward Sun 8 Mar, fall back Sun 1 Nov; London spring forward Sun 29 Mar, fall back Sun 25 Oct):

| Name | Zone | Bedtime | Wake time |
|---|---|---|---|
| DST-T-spring | America/Toronto | 2026-03-07T23:00:00-05:00 | 2026-03-08T07:00:00-04:00 |
| DST-T-fall | America/Toronto | 2026-10-31T23:00:00-04:00 | 2026-11-01T07:00:00-05:00 |
| DST-L-spring | Europe/London | 2026-03-28T23:00:00+00:00 | 2026-03-29T07:00:00+01:00 |
| DST-L-fall | Europe/London | 2026-10-24T23:00:00+01:00 | 2026-10-25T07:00:00+00:00 |

**Notes values** (N1 to N8): `Slept well`; `Tired, but calm`; `He said "go to bed"`; a note with a line break (`Line one` Enter `Line two`); a note with a Windows line break (CR+LF); `Café — 眠れた 😴`; `=SUM(A1)`; a 2,000-character note.

---

## AC1: Export CSV button and file name

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button is on the home page and downloads a correctly named file | 1. Una has D1. 2. Now = NOW-A. 3. Open the home page and select "Export CSV". | A "Export CSV" button is shown on the home page. A file named `nightjar-diary-2026-11-21.csv` downloads. |
| TC-117-2 | The date comes from the user's time zone, not UTC (evening) | 1. Una has D1. 2. Now = NOW-B (04:30 UTC on 22 Nov). 3. Export. | File name is `nightjar-diary-2026-11-21.csv` (Toronto date), not 22 Nov. |
| TC-117-3 | The date comes from the user's time zone, not UTC (other side of midnight) | 1. Lou (London) has D1. 2. Now = NOW-B. 3. Export. 4. Repeat with Una and Now = NOW-C. | Lou: `nightjar-diary-2026-11-22.csv`. Una at NOW-C: `nightjar-diary-2026-11-22.csv`. |
| TC-117-4 | Year boundary and a time zone change | 1. Una has D1. Now = NOW-D. 2. Export. 3. Change Una's current time zone to Europe/London (same instant, 1 Jan 2027 local). 4. Export again. | First file: `nightjar-diary-2026-12-31.csv`. Second file: `nightjar-diary-2027-01-01.csv`. The name follows the zone current at the moment of export. |
| TC-117-5 | Single-digit month and day are zero-padded | 1. Una has D1. 2. Now = Fri 2 Jan 2026 10:00 Toronto. 3. Export. | File name is `nightjar-diary-2026-01-02.csv`. |

## AC2: Header row and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-6 | Header is the first row with the import's columns in order | 1. Una has D1. 2. Export. 3. Open the file in a plain-text editor. | Line 1 is exactly `bedtime,wake_time,timezone,notes`. Lines 2 to 4 are data rows. No extra columns. |
| TC-117-7 | The `timezone` column holds the night's own time zone | 1. Una logs DST-T-spring (Toronto) and DST-L-spring (London) nights. 2. Export. | The `timezone` value is `America/Toronto` for the first row and `Europe/London` for the second (see open question 1 on format). |
| TC-117-8 | A night with no note | 1. Una has D1 with no notes on any night. 2. Export. | Each row still has 4 fields; `notes` is empty (row ends with a trailing comma). |

## AC3: ISO 8601 times with the offset of the night's own time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-9 | Standard offset format | 1. Una logs bed 00:25 on Sun 1 Mar 2026, wake 08:00. 2. Export. | `bedtime` is `2026-03-01T00:25:00-05:00` (the story's example). Seconds are present and offset is `-05:00`, not `Z` or `-0500`. |
| TC-117-10 | Spring-forward night crosses the offset change (Toronto) | 1. Una has DST-T-spring. 2. Export. | `bedtime` `2026-03-07T23:00:00-05:00`, `wake_time` `2026-03-08T07:00:00-04:00`. Each time carries the offset in force at that time. |
| TC-117-11 | Fall-back night crosses the offset change (Toronto) | 1. Una has DST-T-fall. 2. Export. | `bedtime` `2026-10-31T23:00:00-04:00`, `wake_time` `2026-11-01T07:00:00-05:00`. |
| TC-117-12 | London transitions (offset is 0 in winter) | 1. Lou has DST-L-spring and DST-L-fall. 2. Export. | Spring: `...T23:00:00+00:00` and `...T07:00:00+01:00`. Fall: `...T23:00:00+01:00` and `...T07:00:00+00:00`. See open question 2 on `+00:00` versus `Z`. |
| TC-117-13 | Nights from different zones in one diary, exported after a zone change | 1. Una logs D1 nights in Toronto. 2. She changes her current zone to Europe/London and logs the night of Fri 20 Nov, bed 23:00, wake 07:00 London. 3. Export. | D1 rows keep `-05:00` and `America/Toronto`. The new row is `2026-11-20T23:00:00+00:00` with `Europe/London`. Old rows are not shifted to the current zone. |
| TC-117-14 | Wall time that does not exist or repeats (the ambiguous hour) | 1. Una logs a wake time of 01:30 on Sun 1 Nov 2026 (occurs twice in Toronto), once the first and once the second occurrence. 2. Export. | The two exports show `-04:00` and `-05:00` respectively, so the real instants are preserved. See open question 3 if the app cannot tell them apart. |

## AC4: "Night of" order, oldest first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-15 | Nights entered out of order | 1. Una logs night of 16 Nov, then 14 Nov, then 15 Nov. 2. Export. | Rows are ordered 14 Nov, 15 Nov, 16 Nov. |
| TC-117-16 | After-midnight bedtime sorts by its "night of" date | 1. Una logs Sat 14 Nov night as bed 23:10, and Sun 15 Nov night as bed Mon 16 Nov 00:15 (wake 07:45). 2. Also log Mon 16 Nov night as bed 23:30. 3. Export. | Order is by "night of": 14 Nov, 15 Nov (the 00:15 Mon bedtime), 16 Nov (23:30 Mon bedtime). The 00:15 row is not placed after 23:30 on its calendar date. |
| TC-117-17 | Nights in different zones where "night of" order and UTC order disagree | 1. Log night of Sat 21 Nov in Asia/Tokyo: bed 2026-11-21T00:30:00+09:00 (15:30 UTC on 20 Nov). 2. Log night of Fri 20 Nov in America/Los_Angeles: bed 2026-11-20T23:30:00-08:00 (07:30 UTC on 21 Nov). 3. Export. | Order follows "night of": Fri 20 Nov (Los Angeles) first, then Sat 21 Nov (Tokyo), even though Tokyo's bedtime is the earlier instant. See open question 4. |
| TC-117-18 | Two nights with the same "night of" date | 1. Una logs two sleeps for Mon 16 Nov (a night and a nap or a split night). 2. Export. | Both rows are present and adjacent. Order between them is defined (see open question 5). |
| TC-117-19 | Year boundary | 1. Una logs nights of Wed 31 Dec 2025 and Thu 1 Jan 2026. 2. Export. | 31 Dec row precedes 1 Jan row. |

## AC5: Journal notes exported exactly, with standard CSV quoting

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-20 | Commas | 1. Log a night with note `Tired, but calm`. 2. Export and open in a text editor. | Field is written `"Tired, but calm"`; the row still has exactly 4 fields when parsed. |
| TC-117-21 | Double quotes | 1. Log a note `He said "go to bed"`. 2. Export. | Field is written `"He said ""go to bed"""` (inner quotes doubled, field wrapped in quotes). |
| TC-117-22 | Line breaks, both kinds | 1. Log one note with LF (`Line one` Enter `Line two`) and one with CR+LF. 2. Export. 3. Parse with a standard CSV reader. | Each note is quoted and contains the line break; the file still parses to the same number of records. The text read back equals the text entered, including the line break character (see open question 6). |
| TC-117-23 | Non-English text, accents, emoji | 1. Log notes `Café — 眠れた 😴`, `Dormí bien`, and an Arabic note `نمت جيدا`. 2. Export. 3. Open in a UTF-8 reader and in Excel. | Text reads back character-for-character in a UTF-8 reader. Encoding is UTF-8 (see open question 7 on BOM and Excel). |
| TC-117-24 | Text that could be altered: spaces, formula characters, long text | 1. Log notes: `  padded  `; one space only; `=SUM(A1)`; `+1`; `-1`; `@x`; a 2,000-character note with commas and quotes. 2. Export. | Each note is unchanged: spaces kept, nothing prefixed or stripped, no truncation. See open question 8 on formula injection. |

## AC6: Round trip through the import

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-25 | Standard diary round trip | 1. Una has D1 with notes N1 and N2. 2. Export. 3. Start with an empty diary (new account). 4. Import the exported file. | The diary has the same nights: same "night of" dates, bedtimes, wake times, time zones, notes. The diary view shows the same entries in the same order. |
| TC-117-26 | Awkward notes round trip | 1. Diary with notes N3, N4, N5, N6, N7 on separate nights. 2. Export. 3. Import into an empty diary. | Every note is identical to the original (commas, quotes, line breaks, non-English, `=SUM(A1)`). |
| TC-117-27 | Daylight-saving and mixed-zone round trip | 1. Diary with DST-T-spring, DST-T-fall, DST-L-spring, DST-L-fall and the London night from TC-117-13. 2. Export. 3. Import into an empty diary. | Each night has the same real instants and the same zone, so the same durations (spring night 7 h, fall night 9 h on Toronto's clock). Nights show under the same "night of" dates. |
| TC-117-28 | Round trip while the user's current zone is different | 1. Export D1 as Una (Toronto). 2. In a new account whose current zone is Europe/London, import the file. | Nights keep `America/Toronto` and their original offsets, not converted to London. |
| TC-117-29 | Exporting the imported diary again | 1. Export D1. 2. Import into an empty diary. 3. Export again on the same day. | The two files are identical in content. |

## Edge: empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-30 | No nights logged | 1. A new user with no nights. 2. Now = NOW-A. 3. Export. | A file `nightjar-diary-2026-11-21.csv` downloads containing the header row `bedtime,wake_time,timezone,notes` and no other rows. |
| TC-117-31 | Empty export imports cleanly | 1. Export the empty diary. 2. Import it into an empty diary. | Import succeeds (or reports nothing to import, see open question 9); the diary stays empty. |
| TC-117-32 | Minimum data: one night | 1. Una has only the night of 14 Nov from D1. 2. Export. | Header plus exactly one data row. |
| TC-117-33 | Diary emptied after having data | 1. Una has D1, then deletes all nights. 2. Export. | Header only. No stale rows. |

## Non-functional: performance (1,000 nights under 2 seconds)

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-34 | 1,000 plain nights | 1. Load a diary of 1,000 nights spanning 3 years (include DST changes), short notes. 2. Select "Export CSV" and time from the click to the file being offered. | Under 2 seconds. File has 1,001 lines. Measure 3 runs; all under 2 s (see open question 10 on the test machine). |
| TC-117-35 | 1,000 nights with heavy notes | 1. Same diary, but every night has a 2,000-character note with commas, quotes, line breaks and non-English text. 2. Export. | Under 2 seconds. File has 1,000 records plus header. |
| TC-117-36 | Just over the stated volume | 1. Diary of 1,001 nights and of 5,000 nights. 2. Export. | Export completes with every night present. No time limit stated beyond 1,000 nights; record the time (see open question 10). |

## User-facing text and the claims check

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-37 | Button label and any message pass the claims check | 1. Run `claims.check_text` on the button label "Export CSV" and on any text shown on export (success or error messages). | No violations. No disease or treatment wording. |
| TC-117-38 | User's own notes are not blocked by the claims check | 1. Log a note `Can't sleep, maybe insomnia?` (contains a banned word). 2. Export. | Behaviour is as defined in open question 11. Until decided, the proposal is that the note is exported unchanged. |

---

## Open questions

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | What exactly goes in the `timezone` column: IANA name (`America/Toronto`) or something else? The story says "same columns as the import" but does not give the value format. | TC-117-7, 13, 25, 28 | IANA name, matching what the import accepts. Tester to check against the import's documented format. | Product |
| 2 | For a zero offset, is `+00:00` or `Z` expected? AC3 says "with the UTC offset". | TC-117-12 | `+00:00`, so every time has the same shape. | Product |
| 3 | How is a repeated wall time (01:30 on fall-back day) stored and exported? | TC-117-14 | Export the real instant, so the two occurrences show `-04:00` and `-05:00`. If the app cannot record which occurrence was meant, drop the case. | Product |
| 4 | Does "night of" order use the "night of" date (as in S-116) or the raw bedtime instant? Can they differ across zones? | TC-117-16, 17 | Order by "night of" date, as the story says; for a tie, see question 5. | Product |
| 5 | Can two entries share one "night of" date, and if so, what is their order? | TC-117-18 | Order by bedtime instant, earlier first. If a diary allows only one entry per night, remove the case. | Product |
| 6 | Are CR+LF and LF line breaks in notes kept as entered, or normalized? "Exactly as entered" suggests kept. | TC-117-22, 26 | Kept exactly as entered. Records separated by LF or CRLF per the CSV standard (RFC 4180 uses CRLF). | Product |
| 7 | File encoding: UTF-8 with or without a BOM? Excel needs the BOM to show non-English text correctly. | TC-117-23 | UTF-8 without a BOM, since the main use is re-import and other apps. Revisit if users open it in Excel. | Product |
| 8 | A note starting with `=`, `+`, `-` or `@` can run as a formula when opened in a spreadsheet. The story says "exactly as entered". Do we protect, which would change the text and break the round trip? | TC-117-24, 26 | Export exactly as entered (matches AC5 and AC6). Record the risk for a security decision. | Product, with security |
| 9 | Should importing a header-only file succeed silently or show a message? Out of this story's scope but affects AC6 for an empty diary. | TC-117-31 | Succeeds with "0 nights imported" or equivalent. Raise on the import story. | Product |
| 10 | What device and data does the 2-second target apply to? What is expected beyond 1,000 nights? | TC-117-34, 35, 36 | Reference laptop, warm start, 1,000 nights as measured from the click to the download starting. No target above 1,000 nights; just record it. | Product |
| 11 | Does the claims check apply to notes in the export? Claims policy covers app copy and coach answers, not users' own text. | TC-117-38 | No; the user's own words are exported unchanged. Regulatory & Brand to confirm. | Regulatory & Brand |
