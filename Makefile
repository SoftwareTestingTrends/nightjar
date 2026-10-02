# One command per job. Every target exits non-zero on failure.
.PHONY: install test e2e lint format evals run

# Evals use the offline mock unless you pass NIGHTJAR_COACH=claude.
NIGHTJAR_COACH ?= mock

install:  ## install dependencies and the Chromium browser for e2e tests
	uv sync
	uv run playwright install chromium

test:  ## unit + API tests
	uv run pytest -m "not e2e"

e2e:  ## browser test (needs: uv run playwright install chromium)
	uv run pytest -m e2e

lint:  ## style and correctness checks (no changes made)
	uv run ruff check .
	uv run ruff format --check .

format:  ## auto-fix formatting
	uv run ruff check --fix .
	uv run ruff format .

evals:  ## coach evals, 3 runs per case
	NIGHTJAR_COACH=$(NIGHTJAR_COACH) uv run python evals/run_evals.py --runs 3

run:  ## start the app at http://127.0.0.1:8000
	uv run uvicorn nightjar.web:create_app --factory --reload --port 8000
