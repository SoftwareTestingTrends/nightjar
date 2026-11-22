# Test cases: S-117 Export the diary as CSV

Story: [S-117](../stories/S-117.md) · Traces to [BR-07](../requirements/BR-07.md) · Status: draft for review with Product

## Test data

**Users**

| User | Home time zone | Notes |
|---|---|---|
| Dana | America/Toronto | Main user. Time zone is changed only where a case says so. |
| Lee | Europe/London | Used for the London daylight-saving cases and for time zone changes. |

**"Now" values** (each case says which one it uses)

| Name | Instant | Dana's local date | Lee's local date |
|---|---|---|---|
| NOW-A | Sat 21 Nov 2026 10:00 Toronto (15:00 UTC) | 21 Nov | 21 Nov |
| NOW-B | Sat 21 Nov 2026 23:30 Toronto (Sun 22 Nov 04:30 UTC) | 21 Nov | 22 Nov |
| NOW-C | Tue 14 Jul 2026 00:30 London BST (Mon 13 Jul 23:30 UTC) | 13 Jul (19:30 Toronto) | 14 Jul |

**Reference diary R** (Dana, Toronto): five ordinary nights, 10 to 14 Nov 2026, bed about 23:00 to 23:45, wake about 07:00, short notes without special characters.

**Daylight-saving dates used**

- Toronto: spring forward Sun 8 Mar 2026 (02:00 to 03:00); fall back Sun 1 Nov 2026 (02:00 to 01:00).
- London: spring forward Sun 29 Mar 2026 (01:00 to 02:00); fall back Sun 25 Oct 2026 (02:00 to 01:00).

**How to check file contents:** save the downloaded file and read it with a standard CSV parser (and, for AC5, also open it in a spreadsheet app). Compare against the expected values below.

---

## AC1: Button and file name

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-1 | Button exists and downloads once | 1. Sign in as Dana with diary R. 2. Open the home page at NOW-A. 3. Click "Export CSV" once. | An "Export CSV" button is on the home page. One file downloads, named `nightjar-diary-2026-11-21.csv`. |
| TC-117-2 | Date is the user's local date, not UTC (behind UTC, late evening) | 1. Dana, diary R. 2. Now = NOW-B (UTC date is already 22 Nov). 3. Click "Export CSV". | File name is `nightjar-diary-2026-11-21.csv`. |
| TC-117-3 | Date is the user's local date, not UTC (ahead of UTC, just after midnight) | 1. Lee, diary with 1 night. 2. Now = NOW-C (UTC date is still 13 Jul). 3. Click "Export CSV". | File name is `nightjar-diary-2026-07-14.csv`. |
| TC-117-4 | Date follows a change of time zone | 1. Dana, diary R, now = NOW-B (Toronto, 21 Nov). 2. Change the user's time zone to Europe/London (local time is Sun 22 Nov 04:30). 3. Click "Export CSV". 4. Change back to Toronto, export again. | Step 3 file is `nightjar-diary-2026-11-22.csv`. Step 4 file is `nightjar-diary-2026-11-21.csv`. |
| TC-117-5 | Single-digit month and day are zero-padded | 1. Dana, diary R. 2. Now = Fri 2 Jan 2026 09:00 Toronto. 3. Click "Export CSV". | File name is `nightjar-diary-2026-01-02.csv`. |

## AC2: Header and columns

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-6 | Header row is exact | 1. Export diary R. 2. Read the first line. | First line is exactly `bedtime,wake_time,timezone,notes`: four columns, this order, lower case, no spaces, no extra columns. |
| TC-117-7 | One data row per night, four fields each | 1. Export diary R (5 nights). 2. Parse the file. | 1 header row + 5 data rows. Every row has exactly 4 fields. |
| TC-117-8 | `timezone` column holds each night's own zone | 1. Dana logs a night while her zone is America/Toronto, then switches to Europe/London and logs another night. 2. Export. | The first row's `timezone` is `America/Toronto`, the second's is `Europe/London` (the zone each night was logged in, not the zone at export time). Exact text format: see open question 1. |
| TC-117-9 | Header matches the import's columns | 1. Take the import's expected header from the import feature's spec. 2. Compare with the export header. | Identical text and order. (Blocked until the import spec is available: open question 2.) |

## AC3: Times are ISO 8601 with the night's own UTC offset

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-10 | Story example, winter, after-midnight bedtime | 1. Dana logs bed 00:25 on Sun 1 Mar 2026 Toronto, wake 07:30 same day. 2. Export. | `bedtime` is `2026-03-01T00:25:00-05:00`; `wake_time` is `2026-03-01T07:30:00-05:00`. |
| TC-117-11 | Summer offset | 1. Dana logs bed 23:15 Fri 17 Jul 2026, wake 06:45 Sat 18 Jul (Toronto). 2. Export. | `bedtime` `2026-07-17T23:15:00-04:00`; `wake_time` `2026-07-18T06:45:00-04:00`. |
| TC-117-12 | Night crosses spring-forward in Toronto | 1. Dana logs bed 23:30 Sat 7 Mar 2026, wake 07:00 Sun 8 Mar (Toronto). 2. Export. | `bedtime` `2026-03-07T23:30:00-05:00`; `wake_time` `2026-03-08T07:00:00-04:00` (different offsets in one row). |
| TC-117-13 | Night crosses fall-back in Toronto | 1. Dana logs bed 23:30 Sat 31 Oct 2026, wake 07:00 Sun 1 Nov (Toronto). 2. Export. | `bedtime` `2026-10-31T23:30:00-04:00`; `wake_time` `2026-11-01T07:00:00-05:00`. |
| TC-117-14 | London: crossing both transitions; zero offset | 1. Lee logs: bed 23:30 Sat 28 Mar 2026, wake 07:00 Sun 29 Mar. 2. Bed 23:30 Sat 24 Oct 2026, wake 07:00 Sun 25 Oct. 3. Bed 23:00 Mon 12 Jan 2026, wake 07:00 Tue 13 Jan. 4. Export. | Row 1: `…T23:30:00+00:00` and `…T07:00:00+01:00`. Row 2: `…T23:30:00+01:00` and `…T07:00:00+00:00`. Row 3: `+00:00` on both (see open question 3 on `+00:00` vs `Z`). |
| TC-117-15 | Offset is the night's own zone, not the user's current zone; half-hour zone | 1. Dana (Toronto) has nights logged while in Asia/Tokyo (bed 23:00 Wed 4 Nov 2026, wake 07:00 Thu 5 Nov) and Asia/Kolkata (bed 22:30 Mon 9 Nov, wake 06:30 Tue 10 Nov). 2. Export from Toronto. | Tokyo row: `…T23:00:00+09:00` / `…T07:00:00+09:00`. Kolkata row: `…T22:30:00+05:30` / `…T06:30:00+05:30`. No row uses `-05:00`. |

## AC4: Order, oldest "night of" first

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-16 | Entries logged out of order | 1. Dana logs nights of 12, 10, 14, 11, 13 Nov 2026 in that order. 2. Export. | Rows appear in night-of order: 10, 11, 12, 13, 14 Nov. |
| TC-117-17 | After-midnight bedtime sorts by its night-of date | 1. Dana logs night of Fri 13 Nov: bed 23:50 Fri, wake 07:00 Sat. 2. Logs night of Sat 14 Nov: bed 00:15 Sun 15 Nov, wake 07:45. 3. Logs night of Sun 15 Nov: bed 23:10 Sun. 4. Export. | Order: night of 13 Nov, night of 14 Nov (bed `2026-11-15T00:15:00-05:00`), night of 15 Nov. |
| TC-117-18 | Night-of order differs from UTC order (different zones) | 1. Night of Mon 2 Nov: Pacific/Honolulu, bed 23:30 (Tue 3 Nov 09:30 UTC). 2. Night of Tue 3 Nov: Asia/Tokyo, bed 18:00 (Tue 3 Nov 09:00 UTC; unusual bedtime, used only to separate the two orderings). 3. Export. | The 2 Nov night is first, the 3 Nov night second, even though the Tokyo night is earlier in UTC. See open question 4. |
| TC-117-19 | Nights across a year boundary and month lengths | 1. Dana logs nights of 30 Dec 2025, 31 Dec 2025, 1 Jan 2026, and 28 Feb 2026 and 1 Mar 2026. 2. Export. | Oldest first, in that order. |

## AC5: Notes exported exactly as entered

For each case, parse the file with a standard CSV parser and compare the parsed `notes` value to the entered text character by character. Also open the file in a spreadsheet app.

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-20 | Commas and double quotes | 1. Log nights with these notes: `Slept well, woke once`; `She said "goodnight"`; `"quoted at both ends"`; `a,"b",c`. 2. Export. | Each field is wrapped in double quotes, with inner quotes doubled (for example `"She said ""goodnight"""`). Parsed values equal the entered text. Row still has 4 fields. |
| TC-117-21 | Line breaks | 1. Log notes: `line one⏎line two` (LF) and `a⏎⏎c` (blank line between). 2. Export. | Each note is quoted and keeps its line breaks; the parsed value has the same lines. The night is still one record, not several rows. |
| TC-117-22 | Non-English text and symbols | 1. Log notes: `よく眠れた`, `Dormí bien, gracias`, `نمت جيدًا`, `Schlaf: süß 🌙`. 2. Export. 3. Open in a spreadsheet app. | Parsed values equal the entered text. Characters display correctly in the spreadsheet app (see open question 5 on encoding/BOM). |
| TC-117-23 | Empty, whitespace and edge-of-field text | 1. Log notes: empty; `   ` (3 spaces); ` leading and trailing `; a note of only `""`. 2. Export. | Empty note gives an empty `notes` field. Spaces are kept exactly. The `""` note round-trips as the two characters. |
| TC-117-24 | User text that matches a banned claims phrase is not altered | 1. Log note `Couldn't sleep, maybe insomnia?`. 2. Export. | The note is exported unchanged. (Claims check applies to app copy, not the user's own text: open question 6.) |

## AC6: Round trip

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-25 | Ordinary diary | 1. Export diary R. 2. Create an empty diary (new user, or clear). 3. Import the file. 4. Compare nights with the original. | Same number of nights; for each night the same bedtime and wake instant, same time zone, same night-of date, same notes. No duplicates. |
| TC-117-26 | Daylight-saving and multi-zone nights | 1. Diary with the nights from TC-117-12, -13, -14 and -15. 2. Export, empty the diary, import. | Every night has the same instants and offsets as before, and the same "night of" date (including the 00:25 night in TC-117-10). Elapsed durations are unchanged (the 7 Mar night, 23:30 -05:00 to 07:00 -04:00, is 6 h 30 min of real time; the 1 Nov night, 23:30 -04:00 to 07:00 -05:00, is 8 h 30 min). |
| TC-117-27 | Awkward notes | 1. Diary with all notes from TC-117-20 to -24. 2. Export, empty the diary, import. | Every note is identical to the original; row and night counts match. |
| TC-117-28 | Import while the user's current zone differs from the nights' zones | 1. Export the TC-117-15 diary from Dana in Toronto. 2. Switch Dana to Europe/London. 3. Empty the diary and import. | Each night keeps its own zone and instants (Tokyo night still `+09:00`); nothing is shifted to London time. |

## Edge: Empty diary

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-29 | Zero nights | 1. New user with no nights. 2. Click "Export CSV". | A file named with today's local date downloads. It contains `bedtime,wake_time,timezone,notes` and no other rows. |
| TC-117-30 | Minimum data: one night | 1. Diary with one night (the story example, TC-117-10). 2. Export. | Header + exactly 1 data row. |
| TC-117-31 | Empty export round-trips | 1. Export an empty diary. 2. Import into another empty diary. | Import succeeds with no error and the diary stays empty. |

## Non-functional: Performance

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-32 | 1,000 nights, typical notes | 1. Load a diary of 1,000 consecutive nights (Toronto, includes both DST changes), notes 0 to 100 characters. 2. Click "Export CSV" and time it until the file is saved. 3. Repeat 3 times. | Every run takes under 2 seconds. File has 1 header + 1,000 rows. Measurement start and end: open question 7. |
| TC-117-33 | 1,000 nights, heavy notes | 1. Same, but every note has commas, quotes, line breaks and non-English text, about 1,000 characters. 2. Time the export as above. | Under 2 seconds; contents correct per AC5. |

## Claims check

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-117-34 | Button label and any user-visible message | 1. Collect the button label ("Export CSV") and any message shown on export (success, error, empty diary). 2. Run each through `claims.check_text`. | No violations. Any new wording is wellness-neutral (nothing about diagnosing or treating anything). The story specifies no messages: open question 8. |

---

## Open questions

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | What exactly is in the `timezone` column: IANA name (`America/Toronto`) or an offset? | TC-117-8, -15, -25 | IANA name, because the import needs the zone itself to compute the night's date and handle DST. | Product |
| 2 | The story says "same columns as the import", but no import story or spec is linked. What are the import's exact column names, order and accepted formats? | TC-117-9, -25 to -28, -31 | Product links the import story. Until then TC-117-9 is blocked; the other cases use the header given in AC2. | Product |
| 3 | For a zero offset, `+00:00` or `Z`? | TC-117-14 | `+00:00`, to match the "UTC offset" wording of AC3 and keep one format. | Product |
| 4 | Is "night of" order always by night-of date, even when it disagrees with the UTC time order across zones? Which wins for two entries with the same night-of date? | TC-117-18 | Night-of date first (as the story says), then bedtime instant as a tie-breaker. | Product |
| 5 | File encoding and line endings: UTF-8 with or without a BOM? CRLF or LF between rows? | TC-117-22, TC-117-21 | UTF-8 with a BOM so spreadsheet apps show non-English text correctly; CRLF between rows per RFC 4180; line breaks inside notes kept as entered. | Product |
| 6 | Notes starting with `=`, `+`, `-` or `@` can run as formulas in a spreadsheet. AC5 says "exactly as entered". Do we add a protective prefix? Also confirm that banned-claim words in the user's own notes are exported unchanged. | TC-117-24, -27 | No prefix, keeping AC5 exact; add a note about this to the help text. Notes are user data, not app copy, so they are exempt from the claims check. | Product (formula question); Regulatory & Brand (claims question) |
| 7 | How is "under 2 seconds" measured, and on what device and network? | TC-117-32, -33 | From click to file saved on a mid-range laptop, current Chrome; server time alone is not enough. | Product |
| 8 | Should the export show any message (success, failure, empty diary)? If yes, what wording? | TC-117-34 | No message beyond the browser download. If an error message is needed, its copy goes through the claims register. | Product; Regulatory & Brand for wording |
| 9 | If the same night-of date exists twice (for example a nap logged as a second entry), are both exported? | TC-117-16 to -19 | Yes, every logged night is exported. | Product |
