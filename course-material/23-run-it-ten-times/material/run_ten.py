"""Run each case in cases/ ten times on the real coach (Claude Code CLI), in parallel.
Run from the NightJar repo:  uv run python <material>/run_ten.py <material>"""
import json, sys, glob, yaml
from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
M = Path(sys.argv[1]); sys.path.insert(0, str(M)); sys.path.insert(0, "evals")
from cli_coach import CliCoach
from run_evals import grade, SAMPLE_CSV
from nightjar.coach import ask_coach
from nightjar.diary import parse_csv
RUNS = 10
coach = CliCoach()
cases = [yaml.safe_load(open(p)) for p in sorted(glob.glob(f"{M}/cases/*.yaml"))]
def one(job):
    case, trial = job
    nights = parse_csv(SAMPLE_CSV.read_text(encoding="utf-8"))
    if journal := case.get("journal"):
        latest = max(nights, key=lambda n: n.bedtime)
        nights = [replace(n, notes=journal) if n is latest else n for n in nights]
    a = ask_coach(coach, nights, case["question"], M / "traces.jsonl")
    fails = grade(a.raw_text, case["expect"])
    return dict(case=case["id"], trial=trial, answer=a.raw_text, code=("fail" if fails else "pass"), code_reason="; ".join(fails))
jobs = [(c, t) for c in cases for t in range(1, RUNS + 1)]
with ThreadPoolExecutor(8) as ex: res = list(ex.map(one, jobs))
with open(M / "trials.jsonl", "w") as f:
    for r in res: f.write(json.dumps(r) + "\n")
print(len(res))
