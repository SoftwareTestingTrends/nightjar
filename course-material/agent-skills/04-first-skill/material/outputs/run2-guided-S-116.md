# Test cases: S-116 Weekly sleep summary

Status: **Draft for review, before development.**
Sources: [S-116](../stories/S-116.md), [BR-07](../requirements/BR-07.md), [PR-21](../requirements/PR-21.md) (midnight handling "as for the nudge"), [S-114](../stories/S-114.md), [claims policy](../claims.md) and the [claims register](../../claims/register.yaml) (version 3). No code was read.

## How to read these cases

- **Test user:** Toronto user, time zone `America/Toronto`, unless a case says otherwise.
- **Calendar (2026):** Wed 11 Nov, Thu 12, Fri 13, Sat 14, Sun 15, Mon 16, Tue 17, Wed 18, Thu 19, Fri 20 Nov. Toronto is on EST (UTC-5) and London on GMT (UTC+0) on those dates.
- **Clock:** every case sets "now" explicitly. Times are 24-hour local time in the zone named.
- **Nights:** written as "night of DATE: bed HH:MM, wake HH:MM". The duration is wake minus bed in real elapsed time. "Standard night" means bed 23:00, wake 06:30 (7 h 30 min = 450 min).
- **Window:** for "today" = D, the window is the night-of dates D-7 to D-1, inclusive (7 dates). With today = Thu 19 Nov, that is Thu 12 Nov to Wed 18 Nov.
- **Figures** means the three things in AC2: nights logged, average time asleep, usual bedtime. How they are laid out and worded is not in the story (see Open questions 1 and 2).
- **Message** means exactly: `Log at least 3 nights this week to see your summary.`

## AC1: Window of seven nights, in the user's current time zone

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-116-1 | Normal week: only the seven window nights count | 1. Log night of 10 Nov and 11 Nov: bed 23:00, wake 03:00 (4 h). 2. Log night of 12, 13, 14, 15, 16, 17, 18 Nov: standard nights. 3. Set now to Thu 19 Nov 2026 10:00 Toronto. 4. Open the home page. | Nights logged = 7. Average time asleep = 7 h 30 min. The 4 h nights of 10 and 11 Nov are not counted. |
| TC-116-2 | Oldest night of the window (7 days ago) is included | 1. Log night of 12 Nov: bed 23:00, wake 05:30 (6 h 30 min). 2. Log standard nights for 13, 14, 15 Nov. 3. Now = Thu 19 Nov 10:00 Toronto. | Nights logged = 4. Average = 7 h 15 min ((390 + 3 × 450) / 4 = 435 min). |
| TC-116-3 | One night older than the window is excluded | 1. Log night of 11 Nov: bed 23:00, wake 05:30. 2. Log standard nights for 13, 14, 15 Nov. 3. Now = Thu 19 Nov 10:00 Toronto. | Nights logged = 3. Average = 7 h 30 min. The 11 Nov night is not counted. |
| TC-116-4 | Last night is included | 1. Log night of 18 Nov: bed 23:00, wake 07:30 (8 h 30 min). 2. Log standard nights for 13, 14, 15 Nov. 3. Now = Thu 19 Nov 10:00 Toronto. | Nights logged = 4. Average = 7 h 45 min ((510 + 1350) / 4 = 465 min). |
| TC-116-5 | A night whose "night of" date is today is excluded | 1. Import a night of 19 Nov: bed 23:00, wake 06:30 (20 Nov). 2. Log standard nights for 13, 14, 15 Nov. 3. Now = Thu 19 Nov 10:00 Toronto. | Nights logged = 3. The 19 Nov night is not counted. |
| TC-116-6 | Midnight, one minute before: window has not moved | 1. Log night of 12 Nov: bed 23:00, wake 05:30. 2. Log standard nights for 13, 14, 15 Nov. 3. Now = Thu 19 Nov 23:59 Toronto. | Window = 12 to 18 Nov. Nights logged = 4. Average = 7 h 15 min. |
| TC-116-7 | Midnight, window moves by one night | Same data as TC-116-6. Now = Fri 20 Nov 00:00 Toronto. | Window = 13 to 19 Nov. The 12 Nov night drops out. Nights logged = 3. Average = 7 h 30 min. |
| TC-116-8 | 00:15 bedtime counts for the previous date (the story's own example) | 1. Log standard nights for 12 and 13 Nov. 2. Log a night with bed 00:15 on Sun 15 Nov, wake 07:45. 3. Now = Thu 19 Nov 10:00 Toronto. | The diary shows that night as night of Sat 14 Nov. It is inside the window. Nights logged = 3. |
| TC-116-9 | 00:15 on today's date is last night (upper edge) | 1. Log standard nights for 16 and 17 Nov. 2. Log a night with bed 00:15 on Thu 19 Nov, wake 07:45. 3. Now = Thu 19 Nov 10:00 Toronto. | That night is night of Wed 18 Nov. It is counted. Nights logged = 3. |
| TC-116-10 | 00:15 on the oldest window date belongs to the day before the window | 1. Log standard nights for 13 and 14 Nov. 2. Log a night with bed 00:15 on Thu 12 Nov, wake 07:45. 3. Now = Thu 19 Nov 10:00 Toronto. | That night is night of Wed 11 Nov. It is outside the window. Nights logged = 2, so the message shows (see AC5). |
| TC-116-11 | 00:15 on the day after the oldest window date | 1. Log standard nights for 14 and 15 Nov. 2. Log a night with bed 00:15 on Fri 13 Nov, wake 07:45. 3. Now = Thu 19 Nov 10:00 Toronto. | That night is night of Thu 12 Nov. It is inside the window. Nights logged = 3. |
| TC-116-12 | Time zone Toronto: "today" is taken in Toronto | 1. Log night of 11 Nov: bed 23:00, wake 05:30. 2. Log standard nights for 13, 14, 15 Nov. 3. Set zone to America/Toronto. 4. Now = 2026-11-19 03:30 UTC (22:30 Wed 18 Nov in Toronto). | Today = 18 Nov. Window = 11 to 17 Nov. Nights logged = 4. Average = 7 h 15 min. |
| TC-116-13 | Same instant, London: "today" is taken in London | Same data and same instant as TC-116-12, but zone = Europe/London (03:30 Thu 19 Nov). | Today = 19 Nov. Window = 12 to 18 Nov. The 11 Nov night drops out. Nights logged = 3. Average = 7 h 30 min. |
| TC-116-14 | Changing time zone while viewing updates the window | 1. Use the data from TC-116-12 at the same instant. 2. Open the home page in America/Toronto and note the summary. 3. Change the user's time zone to Europe/London. 4. Reload the home page. | Step 2 matches TC-116-12 (4 nights, 7 h 15 min). After step 4 it matches TC-116-13 (3 nights, 7 h 30 min). |
| TC-116-15 | Large time zone change (flight to Auckland, UTC+13 in November) | 1. Log night of 12 Nov: bed 23:00, wake 05:30 (Toronto time). 2. Log standard nights for 14 and 15 Nov. 3. Import night of 19 Nov: bed 22:00 NZDT 19 Nov, wake 06:00 NZDT 20 Nov (8 h). 4. Now = 2026-11-19 20:00 UTC. 5. View with zone America/Toronto (15:00 Thu 19 Nov), then with zone Pacific/Auckland (09:00 Fri 20 Nov). | Toronto: window 12 to 18 Nov, nights logged = 3, average 7 h 10 min ((390 + 450 + 450) / 3 = 430 min). Auckland: window 13 to 19 Nov, nights logged = 3 (14, 15, 19 Nov), average 7 h 40 min ((450 + 450 + 480) / 3 = 460 min). |
| TC-116-16 | A night logged in another zone keeps its diary date | 1. Zone is Europe/London, now = Thu 19 Nov 09:00 GMT. 2. Log standard nights for 13, 14, 15 Nov in London. 3. Log a night in Toronto: bed 23:30 EST Wed 11 Nov (04:30 UTC 12 Nov, 04:30 on 12 Nov in London), wake 07:00 EST. | The night keeps its diary date, night of 11 Nov. It is outside the window (12 to 18 Nov). Nights logged = 3. |
| TC-116-17 | Daylight-saving day in Toronto (spring forward, 23-hour day) | 1. Log standard nights for 1 Mar (bed 23:00 1 Mar, wake 06:30 2 Mar), 7 Mar and also a night of 28 Feb and a night of 8 Mar. 2. Now = Sun 8 Mar 2026 03:30 EDT (just after the clock change). | Today = 8 Mar. Window = 1 to 7 Mar. The nights of 1 Mar and 7 Mar are counted. The nights of 28 Feb and 8 Mar are not. Nights logged = 2. |
| TC-116-18 | Daylight-saving day in London (fall back, 25-hour day) | 1. Log standard nights for 17, 18, 19, 24 and 25 Oct (London time). 2. Now = Sun 25 Oct 2026 12:00 GMT. | Today = 25 Oct. Window = 18 to 24 Oct. The nights of 18, 19 and 24 Oct are counted. The nights of 17 and 25 Oct are not. Nights logged = 3. |

## AC2: What the summary shows

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-116-19 | Full week logged | 1. Log standard nights (bed 23:00, wake 06:30) for 12 to 18 Nov. 2. Now = Thu 19 Nov 10:00 Toronto. 3. Open the home page. | The summary shows all three figures: nights logged = 7, average time asleep = 7 h 30 min, usual bedtime = 23:00. |
| TC-116-20 | Minimum data that shows figures (exactly 3 nights) | 1. Log standard nights for 14, 15, 16 Nov. 2. Now = Thu 19 Nov 10:00 Toronto. | All three figures are shown: nights logged = 3, average 7 h 30 min, usual bedtime 23:00. The message is not shown. |
| TC-116-21 | Gaps: count and average use logged nights only | 1. Log nights (bed 23:00) for 12 Nov (6 h, 360 min), 14 Nov (7 h), 15 Nov (8 h), 17 Nov (7 h 30), 18 Nov (9 h). 2. Do not log 13 or 16 Nov. 3. Now = Thu 19 Nov 10:00 Toronto. | Nights logged = 5 (not 7). Average = 7 h 30 min (2250 / 5 = 450 min). A divisor of 7 would give 5 h 20 min and is wrong. Usual bedtime = 23:00. |
| TC-116-22 | Older diary entries are not counted | 1. Log standard nights for every night from 5 Nov to 18 Nov (14 nights). 2. Now = Thu 19 Nov 10:00 Toronto. | Nights logged = 7, not 14. |
| TC-116-23 | Figures follow the diary | 1. Log standard nights for 14, 15, 16 Nov and note the summary (3 nights). 2. Log a standard night for 17 Nov. 3. Reload the home page. | Nights logged = 4. Average and usual bedtime are recomputed from the 4 nights. |

## AC3: Average time asleep (mean, nearest 5 minutes, "h" and "min")

Each case uses three nights in the window, bed 23:00, with the durations shown. Now = Thu 19 Nov 10:00 Toronto.

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-116-24 | The story's example | Log durations 7 h 00 (420), 7 h 30 (450), 7 h 45 (465) on 15, 16, 17 Nov. | Mean = 445 min. Shows `7 h 25 min`. |
| TC-116-25 | Already a multiple of 5 | Log 7 h 30 on 15, 16, 17 Nov. | Mean = 450 min. Shows `7 h 30 min`. |
| TC-116-26 | Rounds down (2 min above a multiple of 5) | Log 440, 442, 444 min. | Mean = 442 min. Shows `7 h 20 min`. |
| TC-116-27 | Rounds up (3 min above a multiple of 5) | Log 441, 443, 445 min. | Mean = 443 min. Shows `7 h 25 min`. |
| TC-116-28 | Just below the halfway point (442.33) | Log 442, 442, 443 min. | Mean = 442.33 min. Shows `7 h 20 min`. |
| TC-116-29 | Just above the halfway point (442.67) | Log 442, 443, 443 min. | Mean = 442.67 min. Shows `7 h 25 min`. |
| TC-116-30 | Rounding is applied to the mean, not to each night | Log 442, 443, 444 min. | Mean = 443 min. Shows `7 h 25 min`. Rounding each night first would give 7 h 20 min and is wrong. |
| TC-116-31 | Mean, not median | Log 360, 480, 540 min. | Mean = 460 min. Shows `7 h 40 min`. The median (480 min, 8 h) is wrong. |
| TC-116-32 | Rounding up carries into the next hour | Log 478 min (7 h 58) three times. | Mean = 478 min, rounds to 480. Shows 8 hours and 0 minutes (how the zero minutes are written: see Open question 4). |
| TC-116-33 | Rounding down to a whole hour | Log 422 min (7 h 02) three times. | Mean = 422 min, rounds to 420. Shows 7 hours and 0 minutes (zero-minute wording: Open question 4). |
| TC-116-34 | Short mean (under one hour) | Log bed 23:00, wake 23:45 (45 min) three times. | Mean = 45 min. Shows 45 minutes (wording when hours are 0: Open question 4). |

## AC4: Usual bedtime (median local bedtime, midnight handled as for the nudge)

Each case uses three nights in the window, now = Thu 19 Nov 10:00 Toronto, durations 7 h 30 min. Bedtimes are on the night-of dates shown, or just after midnight where stated.

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-116-35 | Median of three, logged out of order | Log bed 23:30 (night of 14 Nov), 22:30 (15 Nov), 23:00 (16 Nov). | Usual bedtime = 23:00. |
| TC-116-36 | Median, not mean | Log bed 22:00 (14 Nov), 22:15 (15 Nov), 23:45 (16 Nov). | Usual bedtime = 22:15. The mean (about 22:50) is wrong. |
| TC-116-37 | Both sides of midnight, median before midnight | Log bed 23:30 (night of 14 Nov), 23:45 (15 Nov), and 00:30 on 17 Nov (night of 16 Nov). | Usual bedtime = 23:45 (order is 23:30, 23:45, 00:30; 23:30 and 00:30 are one hour apart). |
| TC-116-38 | Both sides of midnight, median after midnight | Log bed 23:50 (14 Nov), 00:30 on 16 Nov (night of 15 Nov), 00:45 on 17 Nov (night of 16 Nov). | Usual bedtime = 00:30. |
| TC-116-39 | Both sides of midnight, other mix | Log bed 23:45 (14 Nov), 00:15 on 16 Nov (night of 15 Nov), 00:30 on 17 Nov (night of 16 Nov). | Usual bedtime = 00:15. |
| TC-116-40 | A few minutes either side of midnight, median before | Log bed 23:55 (14 Nov), 23:58 (15 Nov), 00:02 on 17 Nov (night of 16 Nov). | Usual bedtime = 23:58. |
| TC-116-41 | A few minutes either side of midnight, median after | Log bed 23:58 (14 Nov), 00:02 on 16 Nov (night of 15 Nov), 00:05 on 17 Nov (night of 16 Nov). | Usual bedtime = 00:02. |
| TC-116-42 | All bedtimes after midnight | Log bed 00:30 on 15 Nov (night of 14 Nov), 01:00 on 16 Nov, 01:30 on 17 Nov. | Usual bedtime = 01:00. |
| TC-116-43 | Five nights straddling midnight | Log bed 23:00 (13 Nov), 23:30 (14 Nov), 23:45 (15 Nov), 00:15 on 17 Nov (night of 16 Nov), 00:30 on 18 Nov (night of 17 Nov). | Usual bedtime = 23:45. |
| TC-116-44 | Only nights in the window count | 1. Log bed 23:00, 23:15, 23:30 on 14, 15, 16 Nov. 2. Log bed 21:00 on 10 Nov and 21:30 on 11 Nov (outside the window). | Usual bedtime = 23:15. Including the old nights would give 23:00 and is wrong. |
| TC-116-45 | Each night in its own time zone | 1. Zone is Europe/London, now = Thu 19 Nov 10:00 GMT. 2. Log night of 14 Nov in Toronto: bed 23:00 EST. 3. Log night of 15 Nov in London: bed 23:30 GMT. 4. Log night of 16 Nov in Toronto: bed 22:30 EST. | Local bedtimes 22:30, 23:00, 23:30. Usual bedtime = 23:00. Converting to London time first (03:30, 04:00, 23:30) would give 04:00 and is wrong. |
| TC-116-46 | Same bedtime every night | Log bed 23:00 on 14, 15, 16 Nov. | Usual bedtime = 23:00. |

## AC5: Fewer than 3 nights logged in the window

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-116-47 | No data: new user, empty diary | 1. Create a user with no nights. 2. Now = Thu 19 Nov 10:00 Toronto. 3. Open the home page. | The summary shows the message. No nights-logged figure, no average, no usual bedtime. |
| TC-116-48 | 1 night | Log a standard night for 16 Nov. Now = Thu 19 Nov 10:00 Toronto. | The message is shown. No figures. |
| TC-116-49 | 2 nights (one below the limit) | Log standard nights for 16 and 17 Nov. Now = Thu 19 Nov 10:00 Toronto. | The message is shown. No figures. |
| TC-116-50 | 3 nights (the limit) | Log standard nights for 16, 17, 18 Nov. Now = Thu 19 Nov 10:00 Toronto. | The figures are shown. The message is not shown. |
| TC-116-51 | 2 nights in the window, 3 older nights outside | Log standard nights for 17 and 18 Nov, and for 9, 10, 11 Nov. Now = Thu 19 Nov 10:00 Toronto. | The message is shown. No figures (only window nights count). |
| TC-116-52 | 2 nights in the window plus today's night | Log standard nights for 17 and 18 Nov, and import a night of 19 Nov. Now = Thu 19 Nov 10:00 Toronto. | The message is shown (19 Nov is not in the window). |
| TC-116-53 | Third night arrives | 1. Log standard nights for 16 and 17 Nov and see the message. 2. Log a standard night for 18 Nov. 3. Reload the home page. | The message is replaced by the figures (3 nights). |
| TC-116-54 | Midnight takes the summary below 3 | 1. Log standard nights for 12, 13, 14 Nov. 2. Now = Thu 19 Nov 23:59 Toronto: note the summary. 3. Now = Fri 20 Nov 00:00 Toronto: reload. | 23:59: figures shown (3 nights, window 12 to 18 Nov). 00:00: window is 13 to 19 Nov, 2 nights, the message is shown. |
| TC-116-55 | Time zone change takes the summary below 3 | 1. Log standard nights for 11, 12, 13 Nov. 2. Now = 2026-11-19 03:30 UTC. 3. View in America/Toronto (window 11 to 17 Nov), then in Europe/London (window 12 to 18 Nov). | Toronto: figures shown (3 nights). London: 2 nights, the message is shown. |
| TC-116-56 | Exact wording of the message | Reach the message state (TC-116-49) and read the text. | The text is exactly `Log at least 3 nights this week to see your summary.` (capital L, number 3 as a digit, full stop at the end). |
| TC-116-57 | The message state shows no figures at all | Reach the message state with 2 nights logged (TC-116-49). Look at the whole summary. | No count (not even "2 nights"), no average, no usual bedtime, no placeholder such as "0 h 0 min" or "--:--". See Open question 3. |

## AC6: All summary wording passes the claims check

The claims check is the one in the [claims policy](../claims.md) (case-insensitive, word boundaries, banned patterns in register version 3). Collect every piece of text the summary can show: heading, labels, units, helper text, tooltips and screen-reader text. Run each through the check. The register must not be edited to make a case pass.

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-116-58 | Figures state, minimum data | 1. Log standard nights for 14, 15, 16 Nov. 2. Now = Thu 19 Nov 10:00 Toronto. 3. Collect all summary text and run the claims check. | No violations. |
| TC-116-59 | Figures state, full week, bedtime after midnight | 1. Log 7 nights for 12 to 18 Nov with bed 00:30 (after midnight) and 7 h 25 min durations. 2. Collect all summary text and run the claims check. | No violations (the text with the figures, such as `7 h 25 min`, also passes). |
| TC-116-60 | Message state, 2 nights | 1. Log 2 nights. 2. Run `Log at least 3 nights this week to see your summary.` and all other text in this state through the check. | No violations. |
| TC-116-61 | Message state, empty diary | 1. Empty diary. 2. Collect all text and run the check. | No violations. |
| TC-116-62 | Banned-pattern sweep | Compare all summary text, in every state above, with the banned patterns: insomnia, sleep apnea / sleep apnoea / apnea, treat (treat, treats, treated, treating, treatment), cure (cure, cures, cured, curing), diagnos*, anxiety disorder, prescribe (prescribe, prescription and forms), clinically proven. | No match. The check uses word boundaries, so a word that merely contains a banned word (for example "retreat" contains "treat") is not a violation; the banned words themselves are. |
| TC-116-63 | No health claim in text that explains the figures | Read the text that explains what the average and the usual bedtime mean (heading, labels, hints), in every state. | The text describes routine consistency only (as in the story: "how consistent my routine has been"). It does not say or imply diagnosis, treatment, cure or a medical benefit. |
| TC-116-64 | Register is not changed to pass | Check the register version and contents before and after the run. | The register is still version 3, unchanged. |

## Non-functional: real elapsed time across daylight saving, and placement

Each DST case uses three nights, all bed 23:00 and wake 07:00 local, with the DST night shorter or longer on the clock.

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-116-65 | Toronto, spring forward (clock +1 h at 02:00 on Sun 8 Mar 2026) | 1. Zone America/Toronto. Log nights of 6, 7 and 8 Mar (bed 23:00, wake 07:00 next day, local). 2. Now = Tue 10 Mar 2026 12:00 EDT. | Night of 7 Mar is 7 h of real time (23:00 EST to 07:00 EDT). Others are 8 h. Mean = 460 min. Shows `7 h 40 min`. A clock-based 8 h 0 min is wrong. |
| TC-116-66 | Toronto, fall back (clock -1 h at 02:00 on Sun 1 Nov 2026) | 1. Log nights of 30, 31 Oct and 1 Nov (bed 23:00, wake 07:00 next day, local). 2. Now = Tue 3 Nov 2026 12:00 EST. | Night of 31 Oct is 9 h of real time (23:00 EDT to 07:00 EST). Others are 8 h. Mean = 500 min. Shows `8 h 20 min`. |
| TC-116-67 | London, spring forward (clock +1 h at 01:00 on Sun 29 Mar 2026) | 1. Zone Europe/London. Log nights of 27, 28, 29 Mar (bed 23:00, wake 07:00 next day, local). 2. Now = Tue 31 Mar 2026 12:00 BST. | Night of 28 Mar is 7 h of real time (23:00 GMT to 07:00 BST). Mean = 460 min. Shows `7 h 40 min`. |
| TC-116-68 | London, fall back (clock -1 h at 02:00 on Sun 25 Oct 2026) | 1. Log nights of 23, 24, 25 Oct (bed 23:00, wake 07:00 next day, local). 2. Now = Tue 27 Oct 2026 12:00 GMT. | Night of 24 Oct is 9 h of real time (23:00 BST to 07:00 GMT). Mean = 500 min. Shows `8 h 20 min`. |
| TC-116-69 | DST night viewed from another zone | 1. Use the Toronto data of TC-116-65. 2. Set the user's zone to Europe/London. 3. Now = Tue 10 Mar 2026 12:00 GMT. | The night of 7 Mar is still 7 h of real time. The window is 3 to 9 Mar. Shows `7 h 40 min`. |
| TC-116-70 | Usual bedtime is local clock time across DST | 1. Zone America/Toronto. Log bed 23:00 local on 31 Oct (EDT), 1 Nov (EST), 2 Nov (EST). 2. Now = Tue 3 Nov 2026 12:00 EST. | Usual bedtime = 23:00. |
| TC-116-71 | Placement, figures state | 1. Log 3 standard nights in the window. 2. Open the home page. | The summary is on the home page and appears above the sleep diary. |
| TC-116-72 | Placement, message state | 1. Log 2 nights in the window. 2. Open the home page. | The message is on the home page, above the sleep diary. |
| TC-116-73 | Placement, empty diary | 1. Empty diary. 2. Open the home page. | The message is on the home page, above the sleep diary section. |

## Open questions

Each of these is left without an expected result because the story and its linked documents do not say.

| # | Question | Who should answer |
|---|---|---|
| 1 | **Layout and wording of the figures.** How is "nights logged" worded (for example "5 nights" or "5 of 7")? Is the usual bedtime shown as 24-hour `23:00` (as the nudge page does) or 12-hour? What are the heading and the labels? | Product (Priya N.); the wording also needs Regulatory & Brand review |
| 2 | **Summary wording and the register.** The register has templates only for the nudge. Must summary text come from a new register section, or is it enough that it matches no banned pattern? What does the user see if the claims check fails on summary text (a safe fallback, as for the coach)? | Regulatory & Brand |
| 3 | **Is the count a "figure" in AC5?** With 2 nights, we assume "no figures" also hides the nights-logged number. Please confirm. | Product |
| 4 | **Display of zero minutes and short durations.** How is a mean of exactly 8 hours written (`8 h 0 min`, `8 h 00 min` or `8 h`)? How is a mean under one hour written (`45 min` or `0 h 45 min`)? Affects TC-116-32, 33 and 34. | Product |
| 5 | **Exact halfway rounding.** A mean of 442.5 min is exactly between 440 and 445. Round up, down or to even? (Example: nights of 442, 443, 442, 443 min.) | Product |
| 6 | **Median with an even number of nights.** With 4 or 6 nights, is the usual bedtime the average of the two middle bedtimes (23:00 and 23:30 gives 23:15?), the earlier one or the later one? Rounded to the minute? | Product |
| 7 | **Where the "night of" date rolls over.** The story gives 00:15 as the previous night. What about exactly 00:00, 03:00, 05:00 or 12:00? Test cases use only 23:xx and 00:xx times. | Product |
| 8 | **Bedtimes far apart on the clock.** "As for the nudge" is only defined in PR-21 for 23:30 and 00:30 (one hour apart). What is the usual bedtime for nights such as 23:30 and 11:30, where there is no single "closest" side of midnight? | Product (owner of PR-21) |
| 9 | **More than one entry for the same night-of date** (a nap, a split night, a duplicate import). Counted once or more than once? Included in the mean? | Product |
| 10 | **What "duration" and "time asleep" mean.** Is the duration bedtime to wake time (time in bed), or time actually asleep? The test data assumes wake minus bed. Are entries with no wake time counted as logged? | Product |
| 11 | **Bedtime in a daylight-saving gap or repeat.** On 8 Mar 2026 in Toronto 02:30 does not exist. On 1 Nov 2026 01:30 happens twice. Which local bedtime is stored and shown? | Engineering with Product |
| 12 | **When "current time zone" and "today" are evaluated.** On page load only, or live if the page stays open past midnight or the zone changes? The nudge (S-114 AC2) follows a zone change "from the next day"; AC1 here says current zone. TC-116-14 assumes the summary changes on the next reload. | Product |
| 13 | **Other states.** Is there wording for loading and error states of the summary? If so, it needs the claims check (AC6) and cases. | Product |
