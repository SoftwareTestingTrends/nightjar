# NightJar test data conventions

Use these in every test-case document, so cases from different stories and different people use the same users, dates and data, and anyone can reproduce them.

## Users

| User | Time zone | Notes |
|---|---|---|
| Sam | America/Toronto | The default user. Quiet hours 23:00–07:00. |
| Lee | Europe/London | Use for London cases and zero UTC offset. |
| Ana | America/Toronto, then Europe/London | The traveller: changes time zone mid-week. |

## The clock

- Default "now": **Thu 19 Nov 2026 10:00, America/Toronto**. Say so at the top of the document and in any case that uses a different "now".
- Just before and after local midnight: Thu 19 Nov 23:59 and Fri 20 Nov 00:00 Toronto.

## Daylight saving, 2026

| Zone | Spring forward | Fall back |
|---|---|---|
| America/Toronto | Sun 8 Mar, 02:00 → 03:00 (EST −05:00 → EDT −04:00) | Sun 1 Nov, 02:00 → 01:00 (EDT → EST) |
| Europe/London | Sun 29 Mar, 01:00 → 02:00 (GMT +00:00 → BST +01:00) | Sun 25 Oct, 02:00 → 01:00 (BST → GMT) |

A night that crosses a change is an hour shorter (spring) or longer (fall) than the clock suggests.

## Standard nights

- **Standard night:** bed 23:00, wake 06:30 local (7 h 30 min).
- **After-midnight night:** bed 00:25, wake 08:00. Its "night of" date is the day before.

## Named data sets

| Name | Contents |
|---|---|
| D-empty | No nights. |
| D-week | Sam's standard nights for the nights of 12 to 18 Nov 2026. |
| D-dst | One Toronto and one London night across each change above. |
| D-notes | One night for each tricky note below. |
| D-1000 | 1,000 standard nights for Sam, notes from D-notes repeated. |

## Tricky journal notes

Use these exact values, so a failure points to the same text every time.

| # | Note | What it tests |
|---|---|---|
| N1 | `Slept well, woke once` | comma |
| N2 | `Felt "rested" today` | double quotes |
| N3 | `Late dinner` + line break + `then reading` | line break |
| N4 | `Très bien 😴` | non-English text and emoji |
| N5 | `  padded  ` (two spaces each side) | leading and trailing spaces |
| N6 | `=1+1` | a value a spreadsheet may run as a formula |
| N7 | 2,000 × `a` | very long text |
| N8 | (empty) | empty note |

## Wording

Any text the user sees must pass the claims check in `docs/claims.md`. Banned patterns include insomnia, sleep apnea, treat, cure, diagnose, anxiety disorder, prescribe and clinically proven.
