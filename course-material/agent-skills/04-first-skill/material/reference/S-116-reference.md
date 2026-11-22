# S-116 reference: the tester's own test conditions

Written by hand from docs/stories/S-116.md before any agent run (2026-11-19). Used to score every agent output. Each condition is one thing a good test set must check. "Q" items are open questions the story doesn't answer; a good set asks them instead of guessing.

| # | Condition | Why it matters |
|---|---|---|
| R1 | Window edges: the night of 7 days ago is in; 8 days ago is out; tonight (today) is out | Off-by-one on the window |
| R2 | A bedtime after midnight belongs to the previous night (00:15 Sunday = Saturday), including at the window edge | The "night of" rule |
| R3 | The count of nights logged is shown and correct | AC2 |
| R4 | Average time asleep rounds to the nearest 5 minutes (e.g. 7 h 22 → 7 h 20, 7 h 23 → 7 h 25) | AC3 boundary |
| R5 | Median bedtime across midnight: 23:30 and 00:30 give 00:00, not 12:00 | AC4, the classic bug |
| R6 | Each night's bedtime is read in that night's own time zone (a trip mid-week) | AC4 |
| R7 | "Today" uses the user's current time zone, e.g. just after a time zone change or near midnight | AC1 |
| R8 | Threshold: 2 nights → the message; 3 nights → figures | AC5 boundary |
| R9 | No nights at all → the message, no figures, no error | AC5 / empty state |
| R10 | A night across the spring-forward change counts an hour less; fall-back an hour more (Toronto and/or London) | NFR |
| R11 | All summary wording, including the message, passes the claims check | AC6 |
| R12 | The summary appears on the home page above the diary, and updates after a night is added | NFR / AC2 |
| Q1 | Median of an even number of nights (e.g. 4): average of the two middle times? How is it rounded? | Not specified |
| Q2 | Rounding a value exactly between two 5-minute steps (7 h 22.5) | Not specified |
| Q3 | Two diary entries for the same "night of" date: one night or two? | Not specified |
| Q4 | Format for 10+ hours or under 1 hour ("0 h 45 min"?) | Not specified |
