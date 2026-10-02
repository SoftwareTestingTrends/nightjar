# NightJar

NightJar is a sleep diary with a gentle bedtime nudge and an AI sleep coach.
It is the running example in the course **Testing in the AI-Native SDLC**.

The company and team around NightJar are fictional. The app is real: it runs on
your laptop with no hardware, no phone and (by default) no API key.

> NightJar is a wellness demo, not a medical product. It never diagnoses anything.

## What it does

- **Sleep diary**: log nights (bedtime, wake time, time zone, journal notes) or import a CSV.
- **Sleep window**: your usual bedtime is the median local bedtime of your last 14 nights.
- **Wind-down nudge** (story S-114): 45 minutes before your usual bedtime, in your
  current local time, silent during quiet hours.
- **Claims register**: every phrase shown to users is checked against approved
  wellness phrases and banned disease claims (`claims/register.yaml`).
- **AI sleep coach**: answers questions from your diary. Runs on a deterministic mock
  offline, or on Claude when you add an API key. Every call is traced to `traces/coach.jsonl`.

## Setup

You need [uv](https://docs.astral.sh/uv/). It installs Python 3.12 for you.

```bash
make install        # uv sync + Chromium for the browser test
make run            # http://127.0.0.1:8000
```

Then click **Import CSV** and choose `data/sample_nights.csv`: 21 nights for a user
in Toronto, including the March daylight-saving change and a 3-night trip to London.
The nudge panel should show **Your next wind-down nudge: 22:15**.

## Offline (mock) mode

With no `ANTHROPIC_API_KEY` set, the coach uses `MockCoach`: canned, deterministic
answers. Force it any time with `NIGHTJAR_COACH=mock`.

## With Claude

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export NIGHTJAR_COACH=claude                     # optional; a key alone selects Claude
export NIGHTJAR_COACH_MODEL=claude-sonnet-5-5    # optional; this is the default
make run
NIGHTJAR_COACH=claude make evals                 # real model calls cost money
```

## Checks

```bash
make test    # unit + API tests
make lint    # ruff
make e2e     # Playwright: add a night in a real browser, see the nudge
make evals   # coach evals (mock by default)
```

## Where things are

| Path | What |
|---|---|
| `src/nightjar/` | the app (`sleep_window.py`, `nudge.py`, `claims.py`, `coach/`, `web.py`) |
| `tests/` | pytest; test names carry trace ids like `T_114_2` |
| `evals/` | coach eval cases (`cases/*.yaml`) and `run_evals.py` |
| `docs/` | requirements, story S-114, claims policy, traceability |
| `CLAUDE.md` / `AGENTS.md` | instructions for coding agents |

Environment variables: `NIGHTJAR_DB` (default `nightjar.db`), `NIGHTJAR_COACH`
(`mock` or `claude`), `NIGHTJAR_COACH_MODEL`, `NIGHTJAR_TRACE_PATH`, `ANTHROPIC_API_KEY`.

MIT licensed.
