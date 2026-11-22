# D-1: Bedtime 02:30 on the spring-forward night is silently saved and shown as 03:30

Status: confirmed
Tracker: not filed

## Steps to reproduce
1. Open the diary, time zone America/Toronto.
2. Log a night with bedtime `2026-03-08 02:30` and wake time `2026-03-08 09:00`.
3. Submit. The diary lists the bedtime as 03:30.

Cause: 02:30 does not exist in Toronto on 8 March 2026 (clocks jump 02:00 to 03:00).
`diary.local_input_to_aware` attaches the zone with `replace(tzinfo=...)`, so Python picks
the pre-jump offset (-05:00, i.e. 07:30 UTC), which displays as 03:30 EDT. Nothing
tells the user.

## Expected
Not specified. S-114 only requires the nudge to be correct across DST; no requirement
covers entering a time that doesn't exist. Question for product: should the form reject
it with a message, shift it and tell the user, or something else?

## Actual
The entry is accepted (HTTP 303) and shown as 03:30, with no warning that the time was
changed. The user's 02:30 is lost.

## Reproducibility
3 of 3 runs.

## Repro
`uv run python bugs/D-1-spring-forward-bedtime-shifted/repro.py`

Exits 1 while the entry is silently changed. Exits 0 once the app rejects it (HTTP 400)
or shows 02:30. Product hasn't decided the intended behaviour; this exit condition is
my reading of "not silent" and may need adjusting after the decision.
