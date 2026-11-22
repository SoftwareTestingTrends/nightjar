# Test cases: S-117 Export the diary as CSV

| Field | Value |
|---|---|
| Story | [S-117](../stories/S-117.md) |
| Traces to | [BR-07](../requirements/BR-07.md) |
| Status | Draft for review |
| Prepared | 2026-11-19 |
| Reviewers | Tester: ______ · Product: Priya N. |

## How to read this document

Each case has fixed starting data, steps, and one expected result. Reviewers: mark the
**Product check** line on each case as Agreed, Change (say what), or Question. Cases
whose expected result depends on an open question are marked *Proposed*. These are
written for a person to run by hand; automated tests come later.

Conventions used below:

- A night's **"Night of"** date is the evening the night began. A bedtime of 00:25 on
  Sunday 1 March is the night of Saturday 28 February (see Q1).
- Times in the Setup tables are local times in the zone shown on that row.
- In expected file contents, each line is one row of the file. `⏎` marks a line break
  inside a note.

## Coverage

| Criterion | Cases |
|---|---|
| AC1: "Export CSV" button downloads `nightjar-diary-YYYY-MM-DD.csv` with today's date in the user's current zone | TC-117-1, TC-117-2, TC-117-3 |
| AC2: Header row and columns `bedtime,wake_time,timezone,notes` | TC-117-4 |
| AC3: ISO 8601 times with the offset of that night's own zone | TC-117-5, TC-117-6, TC-117-7, TC-117-8, TC-117-9, TC-117-10 |
| AC4: "Night of" order, oldest first | TC-117-11, TC-117-12, TC-117-13 |
| AC5: Notes exported exactly as entered, standard CSV quoting | TC-117-14, TC-117-15, TC-117-16, TC-117-17, TC-117-18, TC-117-19, TC-117-20 |
| AC6: Importing an exported file into an empty diary gives the same nights | TC-117-21, TC-117-22, TC-117-23 |
| Edge: Empty diary exports header only | TC-117-24 |
| Edge-adjacent: night with no wake time (story silent) | TC-117-25 |
| Non-functional: 1,000 nights in under 2 seconds | TC-117-26 |

## Open questions for Product

| # | Question | Why it matters | Proposed answer | Cases affected |
|---|---|---|---|---|
| Q1 | Which "night of" date does a bedtime after midnight belong to? The story relies on "night of" but does not define it. | If a 00:25 bedtime on 1 March belongs to 28 February, it sorts before a 22:55 bedtime on 1 March. If it belongs to 1 March, it sorts after it. | A bedtime before 12:00 noon local time belongs to the previous calendar date. This matches the sample data file. | TC-117-11, 12, 13 |
| Q2 | Two nights have the same "night of" date (for example logged in two different zones). Which comes first? | The file order is otherwise undefined and could change between exports. | Earlier bedtime moment first (compare as absolute instants). | TC-117-13 |
| Q3 | A note that starts with `=`, `+`, `-` or `@` can be run as a formula when the CSV is opened in a spreadsheet. AC5 says "exactly as entered". Do we protect users, or keep notes untouched? | Protecting changes the note text and breaks AC5 and AC6. Not protecting leaves a spreadsheet-safety risk. | Keep notes exactly as entered (AC5 wins). Product and Security to confirm the risk is accepted. | TC-117-20 |
| Q4 | File format details the story does not state: text encoding, whether a byte-order mark is included, line ending between rows, and whether the last row ends with a line break. | Excel may show non-English notes wrongly without a byte-order mark; other importers may reject one. Row ends affect byte-for-byte checks. | UTF-8 without a byte-order mark; rows end with a line break, including the last row; standard CSV line endings. Line breaks inside a note are kept as entered. | TC-117-4, 17, 24 |
| Q5 | At a clock change, a night's bedtime and wake time can have different offsets (for example `-05:00` and `-04:00`). Does each time carry the offset in force at that moment? | AC3 says "the UTC offset that applied in that night's own time zone", which could be read as one offset per night. | Each time carries the offset that applied at that moment, so the two can differ within one row. | TC-117-8, 9 |
| Q6 | Can a night exist without a wake time (for example, logged at bedtime and not yet finished)? If so, what does the file hold? | The story's columns have no way to say "not set". The import may reject an empty wake time. | Ask Product whether this can happen. If yes: empty `wake_time` cell, and import must accept it. | TC-117-25 |
| Q7 | The performance line gives no machine, data shape or start and end points. | "Under 2 seconds" cannot be measured without them. | A normal developer laptop, the app running locally, 1,000 nights with notes of about 100 characters, timed from the button click to the finished download. | TC-117-26 |

## Test cases

### TC-117-1: The button downloads a file named with today's date

- **Covers:** AC1
- **Type:** Normal
- **Setup:** Today is Thursday 2026-03-12, 10:00. The user's time zone is America/Toronto. The diary contains:

  | Night of | Bedtime | Wake time | Zone |
  |---|---|---|---|
  | 2026-03-01 | 22:55 | 06:50 (Mar 2) | America/Toronto |

- **Steps:**
  1. Open the home page.
  2. Look for the button, then select it.
- **Expected result:** A button labelled exactly "Export CSV" is on the home page. Selecting it downloads one file named `nightjar-diary-2026-03-12.csv`. The page shows no medical or treatment wording (none of: insomnia, sleep apnea, treat, cure, diagnose, prescribe, clinically proven).
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-2: Evening in Toronto uses the Toronto date, not the UTC date

- **Covers:** AC1
- **Type:** Boundary
- **Setup:** The moment is Thursday 2026-03-12, 22:30 in Toronto (that is Friday 2026-03-13, 02:30 UTC). The user's time zone is America/Toronto. The diary contains the one night from TC-117-1.
- **Steps:**
  1. Open the home page.
  2. Select "Export CSV".
- **Expected result:** The file is named `nightjar-diary-2026-03-12.csv`.
  Working: Toronto is 4 hours behind UTC on 12 March 2026 (daylight time started 8 March), so 02:30 UTC on the 13th is 22:30 on the 12th.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-3: Same moment, user in Auckland, uses the Auckland date

- **Covers:** AC1
- **Type:** Boundary
- **Setup:** The same moment as TC-117-2 (2026-03-13, 02:30 UTC). The user's current time zone is Pacific/Auckland. The diary contains the one night from TC-117-1.
- **Steps:**
  1. Open the home page.
  2. Select "Export CSV".
- **Expected result:** The file is named `nightjar-diary-2026-03-13.csv`.
  Working: Auckland is 13 hours ahead of UTC in March (summer time), so 02:30 UTC is 15:30 on the 13th.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-4: Header row and column order

- **Covers:** AC2
- **Type:** Normal
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary contains:

  | Night of | Bedtime | Wake time | Zone | Note |
  |---|---|---|---|---|
  | 2026-02-27 | 23:40 | 08:10 (Feb 28) | America/Toronto | Friday. Stayed up finishing a book. |
  | 2026-03-01 | 22:55 | 06:50 (Mar 2) | America/Toronto | (none) |

- **Steps:**
  1. Open the home page and select "Export CSV".
  2. Open the downloaded file in a plain text editor.
- **Expected result:** The file has exactly 3 lines:
  ```
  bedtime,wake_time,timezone,notes
  2026-02-27T23:40:00-05:00,2026-02-28T08:10:00-05:00,America/Toronto,Friday. Stayed up finishing a book.
  2026-03-01T22:55:00-05:00,2026-03-02T06:50:00-05:00,America/Toronto,
  ```
  The header is the first line, with these four names in this order and no extra spaces. The last row ends with a comma because its note is empty. Proposed, see Q4, for how the lines end.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-5: Winter night in Toronto, including a bedtime after midnight

- **Covers:** AC3
- **Type:** Normal
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary contains:

  | Night of | Bedtime | Wake time | Zone |
  |---|---|---|---|
  | 2026-02-28 | 00:25 (Mar 1) | 08:30 (Mar 1) | America/Toronto |

- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** The row is `2026-03-01T00:25:00-05:00,2026-03-01T08:30:00-05:00,America/Toronto,` (the story's own example for the bedtime). Both times show seconds `:00` and the offset `-05:00`.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-6: Summer night in Toronto shows the daylight-time offset

- **Covers:** AC3
- **Type:** Normal
- **Setup:** Today is Friday 2026-07-17. The user's time zone is America/Toronto. The diary contains:

  | Night of | Bedtime | Wake time | Zone |
  |---|---|---|---|
  | 2026-07-14 | 23:15 | 07:05 (Jul 15) | America/Toronto |

- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** The row is `2026-07-14T23:15:00-04:00,2026-07-15T07:05:00-04:00,America/Toronto,`. The offset is `-04:00`, not `-05:00`.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-7: A night logged in London uses London's offset, not the user's

- **Covers:** AC3
- **Type:** Edge
- **Setup:** Today is Friday 2026-07-17. The user's **current** time zone is America/Toronto (offset -04:00). The diary contains:

  | Night of | Bedtime | Wake time | Zone |
  |---|---|---|---|
  | 2026-07-14 | 23:30 | 07:10 (Jul 15) | Europe/London |

- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** The row is `2026-07-14T23:30:00+01:00,2026-07-15T07:10:00+01:00,Europe/London,`. The times are London local times with `+01:00`. Nothing is converted to Toronto time.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-8: Night that crosses spring-forward in Toronto

- **Covers:** AC3
- **Type:** Edge
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. Clocks in Toronto went forward at 02:00 on Sunday 2026-03-08. The diary contains:

  | Night of | Bedtime | Wake time | Zone |
  |---|---|---|---|
  | 2026-03-07 | 23:30 | 07:00 (Mar 8) | America/Toronto |

- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** Proposed, see Q5: `2026-03-07T23:30:00-05:00,2026-03-08T07:00:00-04:00,America/Toronto,`. The bedtime has `-05:00` and the wake time has `-04:00`.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-9: Night that crosses fall-back in London

- **Covers:** AC3
- **Type:** Edge
- **Setup:** Today is Monday 2026-10-26. The user's time zone is Europe/London. Clocks in London went back at 02:00 on Sunday 2026-10-25. The diary contains:

  | Night of | Bedtime | Wake time | Zone |
  |---|---|---|---|
  | 2026-10-24 | 23:30 | 07:00 (Oct 25) | Europe/London |

- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** Proposed, see Q5: `2026-10-24T23:30:00+01:00,2026-10-25T07:00:00+00:00,Europe/London,`. The bedtime has `+01:00` and the wake time has `+00:00` (written that way, not as `Z`).
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-10: Zone with a half-hour offset

- **Covers:** AC3
- **Type:** Boundary
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary contains:

  | Night of | Bedtime | Wake time | Zone |
  |---|---|---|---|
  | 2026-03-05 | 23:00 | 06:30 (Mar 6) | Asia/Kolkata |

- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** The row is `2026-03-05T23:00:00+05:30,2026-03-06T06:30:00+05:30,Asia/Kolkata,`.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-11: Nights added out of order come out oldest first

- **Covers:** AC4
- **Type:** Normal
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The nights were added to the diary in this order (top to bottom):

  | Added | Night of | Bedtime | Wake time | Zone |
  |---|---|---|---|---|
  | 1st | 2026-03-01 | 22:55 | 06:50 (Mar 2) | America/Toronto |
  | 2nd | 2026-02-27 | 23:40 | 08:10 (Feb 28) | America/Toronto |
  | 3rd | 2026-02-28 | 00:25 (Mar 1) | 08:30 (Mar 1) | America/Toronto |

- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** After the header, the rows are in this order: bedtime `2026-02-27T23:40:00-05:00`, then `2026-03-01T00:25:00-05:00`, then `2026-03-01T22:55:00-05:00`. These are the nights of 27 Feb, 28 Feb and 1 Mar. Proposed, see Q1, for the middle row's place.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-12: Order follows "night of", not the absolute moment, across zones

- **Covers:** AC4
- **Type:** Edge
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary contains:

  | Night of | Bedtime | Wake time | Zone | Bedtime in UTC |
  |---|---|---|---|---|
  | 2026-03-02 | 22:00 | 06:00 (Mar 3) | Pacific/Honolulu (-10:00) | Mar 3, 08:00 |
  | 2026-03-03 | 20:00 | 04:00 (Mar 4) | Pacific/Auckland (+13:00) | Mar 3, 07:00 |

  Working: 22:00 at -10:00 is 08:00 UTC; 20:00 at +13:00 is 07:00 UTC the same day. The Auckland night is the later night of the two but the earlier moment.
- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** Proposed, see Q1: the Honolulu row (night of 2 Mar, bedtime `2026-03-02T22:00:00-10:00`) comes first. The Auckland row (night of 3 Mar, bedtime `2026-03-03T20:00:00+13:00`) comes second.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-13: Two nights with the same "night of" date

- **Covers:** AC4
- **Type:** Edge
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary contains:

  | Night of | Bedtime | Wake time | Zone | Bedtime in UTC |
  |---|---|---|---|---|
  | 2026-03-03 | 23:00 | 07:00 (Mar 4) | America/Toronto (-05:00) | Mar 4, 04:00 |
  | 2026-03-03 | 23:30 | 07:00 (Mar 4) | Europe/London (+00:00) | Mar 3, 23:30 |

- **Steps:**
  1. Select "Export CSV" twice, and compare the two files' row order.
- **Expected result:** Proposed, see Q2: the London row first, then the Toronto row, in both downloads. The two files have the same content.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-14: A note with a comma

- **Covers:** AC5
- **Type:** Normal
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary has one night: night of 2026-03-01, bedtime 22:55, wake time 06:50 (Mar 2), America/Toronto. Note: `Dinner with friends, home late.`
- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** The row is `2026-03-01T22:55:00-05:00,2026-03-02T06:50:00-05:00,America/Toronto,"Dinner with friends, home late."`. The note is wrapped in double quotes and the comma inside is untouched. The file has 4 columns on that row when opened in a spreadsheet.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-15: A note with double quotes

- **Covers:** AC5
- **Type:** Edge
- **Setup:** Same night as TC-117-14. Note: `Said "never again", then slept.`
- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** The note field is `"Said ""never again"", then slept."`. The field is wrapped in double quotes and each quote inside is doubled.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-16: A note with a line break

- **Covers:** AC5
- **Type:** Edge
- **Setup:** Same night as TC-117-14. Note, on two lines: `Woke at 3⏎Back to sleep by 4`
- **Steps:**
  1. Select "Export CSV".
  2. Open the file in a spreadsheet app.
- **Expected result:** The note field in the file is wrapped in double quotes and contains the line break: `"Woke at 3⏎Back to sleep by 4"`. The spreadsheet shows one row for the night, with the two-line note in one cell.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-17: A note in a non-English script

- **Covers:** AC5
- **Type:** Edge
- **Setup:** Same night as TC-117-14. Note: `Café tard, 夜遅くまで起きていた 🌙`
- **Steps:**
  1. Select "Export CSV".
  2. Open the file in a text editor that reads UTF-8, and in a spreadsheet app.
- **Expected result:** The text editor shows the note exactly as entered, with every character intact (accent, Japanese text, emoji). The note is wrapped in double quotes because it contains a comma. Spreadsheet display depends on Q4; Proposed: file is UTF-8, no byte-order mark.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-18: Empty note and notes with leading or trailing spaces

- **Covers:** AC5
- **Type:** Boundary
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary contains:

  | Night of | Bedtime | Wake time | Zone | Note |
  |---|---|---|---|---|
  | 2026-03-01 | 22:55 | 06:50 (Mar 2) | America/Toronto | (empty) |
  | 2026-03-02 | 22:50 | 06:45 (Mar 3) | America/Toronto | `  two spaces before and after  ` |

- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** The first row ends with `America/Toronto,` and nothing after the last comma. The second row ends with `America/Toronto,"  two spaces before and after  "` or, if unquoted, with the spaces still present. No spaces are removed.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-19: A very long note

- **Covers:** AC5
- **Type:** Boundary
- **Setup:** Same night as TC-117-14. The note is 5,000 characters: the sentence `Slept badly, restless. ` repeated until it reaches 5,000 characters, with a final marker `END` as the last three characters.
- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** The note in the file has 5,000 characters, starts as entered and ends with `END`. Nothing is cut off. If the app limits note length when entering, use the largest length it allows instead and record it here: ______.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-20: A note that starts with an equals sign

- **Covers:** AC5
- **Type:** Edge
- **Setup:** Same night as TC-117-14. Note: `=1+1 was my mood`
- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** Proposed, see Q3: the note field is `=1+1 was my mood`, exactly as entered, with no added character in front.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-21: Export then import gives the same nights (basic)

- **Covers:** AC6
- **Type:** Normal
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary contains the 7 nights of the sample data file (night of 2026-02-27 to night of 2026-03-05, America/Toronto). Keep a note of the 7 nights for comparing. A second, empty diary is available.
- **Steps:**
  1. In the full diary, select "Export CSV".
  2. Switch to the empty diary.
  3. Import the downloaded file.
  4. Compare the imported nights with the original 7.
- **Expected result:** The empty diary now has 7 nights. For each, the bedtime, wake time, zone, "night of" date and note are the same as the original. No night is missing, duplicated or changed.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-22: Round trip with awkward data

- **Covers:** AC6
- **Type:** Edge
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary contains the nights from TC-117-8 (Toronto spring-forward), TC-117-7 (London), TC-117-12 (Honolulu and Auckland), and one night each with the notes from TC-117-15, TC-117-16 and TC-117-17. A second, empty diary is available.
- **Steps:**
  1. Select "Export CSV".
  2. Switch to the empty diary and import the file.
  3. Compare every night with the original.
- **Expected result:** Every night is present once. Bedtime and wake time are the same moments, the zone name is the same, the "night of" date is the same, and every note is character-for-character the same, including quotes, the line break and non-English text.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-23: Exporting an imported diary gives the same file content

- **Covers:** AC6
- **Type:** Normal
- **Setup:** The result of TC-117-22 (imported diary), same day.
- **Steps:**
  1. In the imported diary, select "Export CSV".
  2. Compare the new file's content with the first export from TC-117-22 (ignore the file name).
- **Expected result:** The two files have identical content.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-24: Empty diary exports the header only

- **Covers:** Edge
- **Type:** Edge
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary has no nights.
- **Steps:**
  1. Open the home page.
  2. Select "Export CSV".
  3. Open the file in a text editor.
- **Expected result:** A file named `nightjar-diary-2026-03-12.csv` is downloaded (no error message). Its only content is the line `bedtime,wake_time,timezone,notes`. Proposed, see Q4, for whether that line ends with a line break.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-25: A night with no wake time

- **Covers:** Edge-adjacent (story is silent)
- **Type:** Edge
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary has one night: night of 2026-03-11, bedtime 23:00, no wake time yet, America/Toronto. (Only run this if Product confirms such a night can exist, see Q6.)
- **Steps:**
  1. Select "Export CSV" and open the file in a text editor.
- **Expected result:** To be decided, see Q6. Proposed: `2026-03-11T23:00:00-04:00,,America/Toronto,` and the file imports back with the same night.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-117-26: Exporting 1,000 nights is fast enough

- **Covers:** Non-functional
- **Type:** Non-functional
- **Setup:** Today is Thursday 2026-03-12. The user's time zone is America/Toronto. The diary has 1,000 nights: one per day from the night of 2023-06-17 to the night of 2026-03-12 (1,000 consecutive nights), bedtime about 23:00, wake time about 07:00, each with a note of about 100 characters, some with commas and quotes. Generate them by importing a prepared file. Machine and timing method: Proposed, see Q7.
- **Steps:**
  1. Open the home page.
  2. Start a timer and select "Export CSV". Stop the timer when the file has finished downloading.
  3. Repeat 3 times.
  4. Open the file and count the lines.
- **Expected result:** Each of the 3 runs takes under 2 seconds. The file has 1,001 lines (1 header plus 1,000 nights) in oldest-first order.
  Working: 2023-06-17 to 2026-06-17 is 1,096 days (one leap day, 29 Feb 2024); 2026-03-12 to 2026-06-17 is 97 days; 1,096 − 97 = 999 days apart, so 1,000 nights counting both ends.
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______
