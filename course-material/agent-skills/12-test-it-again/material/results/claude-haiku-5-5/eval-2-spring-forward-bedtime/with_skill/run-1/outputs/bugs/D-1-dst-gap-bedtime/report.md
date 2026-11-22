# D-1: Bedtime entered inside the spring-forward gap is shown an hour later

Status: confirmed
Tracker: not filed

## Steps to reproduce

1. Start with an empty diary.
2. On the home page, log a night with Bedtime `2026-03-08 02:30`, Wake time
   `2026-03-08 08:00`, and zone America/Toronto. Submit.
3. Look at the night in the diary.

## Expected

Not specified. No requirement or story says what a wall-clock time that does not exist
(02:30 on 8 March 2026 in Toronto) should become: keep 02:30, shift it, or reject it.

Question for product: which should happen? Options are to show 02:30 as entered, to
show the shifted time with a note, or to reject the entry with a message.

Context: `nudge.py` `at_local_time` maps skipped times forward to 03:30 on purpose, and
PR-21 / S-114 call for DST correctness. The diary's input path
(`web.py` -> `diary.local_input_to_aware`) does the shift implicitly, through
`replace(tzinfo=...)` with the default fold, and nothing documents it.

## Actual

The entry is accepted and stored as 2026-03-08T07:30:00+00:00 (02:30 EST). The diary
shows it as 03:30 EDT, with no warning. The user's entry is changed silently.

## Reproducibility

3 of 3 runs.

## Repro

Command, from the repository root:

    uv run python bugs/D-1-dst-gap-bedtime/repro.py

Exit codes: 1 means the defect is present (02:30 entered, 03:30 shown). 0 means fixed:
either the entry is rejected with an error, or 02:30 is shown. The script uses a
throwaway database in a temp directory.
