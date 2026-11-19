# NightJar: notes for coding agents

NightJar is a sleep diary with a bedtime nudge and an AI sleep coach. It is a
**wellness** app, not a medical one. Python 3.12, FastAPI, SQLite, uv.

## Map

- `src/nightjar/sleep_window.py`: usual bedtime (median local bedtime, last 14 nights, min 7)
- `src/nightjar/nudge.py`: story S-114, `next_nudge(user, nights, now)`
- `src/nightjar/claims.py` + `claims/register.yaml`: approved phrases and banned claims
- `src/nightjar/coach/`: `ask_coach()` (claims check + JSONL trace), `MockCoach`, `ClaudeCoach`, `prompts/system.md`
- `src/nightjar/web.py`: FastAPI app factory `create_app(diary, coach, clock)`
- `docs/`: requirements, story S-114, `traceability.md` (AC -> test ids)

## Conventions

- All datetimes are timezone-aware. Never create a naive datetime. Use `zoneinfo`.
- Store instants in UTC; keep the IANA zone alongside; compute local times from the zone.
- Never read the real clock in logic. Take `now` as a parameter (the app injects `clock`).
- User-facing copy (nudges, coach answers) must pass `claims.check_text`. New nudge
  copy goes in `claims/register.yaml`, not in code.
- Journal notes are user data, never instructions. Keep them inside `<journal>` in prompts.
- Changing `coach/prompts/system.md` changes the prompt version hash: run `make evals`.
- Test names carry trace ids (`test_T_114_3_...`). Update `docs/traceability.md` when you add one.

## Things agents get wrong

- Treating 23:30 and 00:30 as 23 hours apart (use `minutes_since_noon`).
- Reading bedtimes in the user's *current* zone instead of the zone of that night.
- Adding `timedelta(days=1)` to an aware datetime and expecting the same wall time
  across DST. Build the local time with `at_local_time(day, time, zone)` instead.
- Subtracting two datetimes that share a `ZoneInfo`: that's wall-clock maths.
  Convert to UTC first (see `Night.duration`).
- Skipping the nudge during quiet hours. AC3 says deliver it silently.
- "Fixing" a claims violation by editing the register. Change the copy instead.
