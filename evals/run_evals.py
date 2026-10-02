"""Run the coach eval cases N times and report a pass rate per case.

    uv run python evals/run_evals.py --runs 3              # coach from NIGHTJAR_COACH
    NIGHTJAR_COACH=claude uv run python evals/run_evals.py # real model (costs money)

Graders are plain code: contains_any, not_contains, claims_clean. They grade
the model's raw output (before NightJar's claims fallback), because the eval
asks "how does the model behave?", not "does the guardrail work?".
Exit code is 1 if any case falls below --min-pass-rate.
"""

import argparse
import sys
from dataclasses import replace
from pathlib import Path

import yaml

from nightjar.claims import check_text
from nightjar.coach import ask_coach, get_coach
from nightjar.coach.base import load_system_prompt, prompt_version
from nightjar.diary import parse_csv

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_CSV = ROOT / "data" / "sample_nights.csv"
TRACE_PATH = ROOT / "traces" / "evals.jsonl"


def grade(output: str, expect: dict) -> list[str]:
    """Return the reasons this output failed (empty list means pass)."""
    failures = []
    lowered = output.lower()
    if "contains_any" in expect and not any(w.lower() in lowered for w in expect["contains_any"]):
        failures.append(f"missing any of {expect['contains_any']}")
    for word in expect.get("not_contains", []):
        if word.lower() in lowered:
            failures.append(f"contains {word!r}")
    if expect.get("claims_clean") and (violations := check_text(output)):
        failures.append(f"claims violations {[v.matched for v in violations]}")
    return failures


def run_case(case: dict, coach, runs: int) -> tuple[int, list[str]]:
    nights = parse_csv(SAMPLE_CSV.read_text(encoding="utf-8"))
    if journal := case.get("journal"):
        latest = max(nights, key=lambda night: night.bedtime)
        nights = [replace(n, notes=journal) if n is latest else n for n in nights]
    passes, reasons = 0, []
    for _ in range(runs):
        answer = ask_coach(coach, nights, case["question"], TRACE_PATH)
        failures = grade(answer.raw_text, case["expect"])
        passes += not failures
        reasons += failures
    return passes, reasons


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--cases", type=Path, default=ROOT / "evals" / "cases")
    parser.add_argument("--min-pass-rate", type=float, default=1.0)
    args = parser.parse_args()

    coach = get_coach()
    print(
        f"NightJar coach evals: model={coach.model} "
        f"prompt={prompt_version(load_system_prompt())} runs={args.runs}\n"
    )
    below_bar = 0
    for path in sorted(args.cases.glob("*.yaml")):
        case = yaml.safe_load(path.read_text(encoding="utf-8"))
        passes, reasons = run_case(case, coach, args.runs)
        rate = passes / args.runs
        ok = rate >= args.min_pass_rate
        below_bar += not ok
        print(
            f"{'PASS' if ok else 'FAIL'}  {case['id']}  {passes}/{args.runs} ({rate:4.0%})"
            f"  {case['title']}"
        )
        if reasons:
            print(f"        first failure: {reasons[0]}")
    total = len(list(args.cases.glob("*.yaml")))
    print(f"\n{total - below_bar}/{total} cases at or above {args.min_pass_rate:.0%} pass rate")
    return 1 if below_bar else 0


if __name__ == "__main__":
    sys.exit(main())
