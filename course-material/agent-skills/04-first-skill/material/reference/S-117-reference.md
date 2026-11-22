# S-117 reference: the tester's own test conditions

Written by hand from docs/stories/S-117.md before any agent run (2026-11-19). Used to score the skill's output on a story it never saw while being written.

| # | Condition | Why it matters |
|---|---|---|
| E1 | File name uses today's date in the user's current zone, including near midnight or after a zone change | AC1 |
| E2 | Header row and exactly the four columns, in order | AC2 |
| E3 | Each night's offset is its own zone's offset at that time: two zones in one diary, and -05:00 vs -04:00 across DST | AC3 |
| E4 | Order is by "night of", oldest first, including an after-midnight bedtime | AC4 |
| E5 | Notes with a comma, a double quote, a line break, and non-English text or emoji survive | AC5 |
| E6 | Round trip: export → import into an empty diary → the same nights | AC6 |
| E7 | Empty diary → header row only | Edge |
| E8 | 1,000 nights export in under 2 seconds | NFR |
| E9 | The button is on the home page and the download works (content type, file opens) | AC1 |
| Q1 | Notes with leading or trailing spaces: "exactly as entered" vs an import that may trim them | Round trip may change data |
| Q2 | Notes starting with = + - @ (spreadsheet formula injection): escape or not? | Security, not in the story |
| Q3 | Encoding: UTF-8, with or without a byte-order mark for Excel? | Not specified |
