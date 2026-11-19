"""Run the eval set on the real coach for one configuration (prompt file + model), N trials per case.
Run from the NightJar repo:  uv run python <material>/suite.py <material> <name> <prompt.md> <model> [runs]"""
import json, sys, glob, subprocess, yaml
from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
M, NAME, PROMPT, MODEL = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), sys.argv[4]
CASES = __import__("os").environ.get("CASES", str(M / "cases_v3"))
RUNS = int(sys.argv[5]) if len(sys.argv) > 5 else 3
sys.path.insert(0, "evals")
import nightjar.coach.service as service
from nightjar.coach.base import prompt_version
from run_evals import grade, SAMPLE_CSV
from nightjar.diary import parse_csv
service.load_system_prompt = lambda: PROMPT.read_text(encoding="utf-8")
class CliCoach:
    model = f"{MODEL} (via claude -p)"
    def reply(self, system_prompt, user_message):
        r = subprocess.run(["claude", "-p", user_message, "--system-prompt", system_prompt, "--model", MODEL,
                            "--tools", "", "--setting-sources", "", "--output-format", "json"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
        return json.loads(r.stdout)["result"]
cases = [yaml.safe_load(open(p)) for p in sorted(glob.glob(f"{CASES}/*.yaml"))]
trace = M / f"traces-{NAME}.jsonl"; trace.unlink(missing_ok=True)
def one(job):
    case, trial = job
    nights = parse_csv(SAMPLE_CSV.read_text(encoding="utf-8"))
    if journal := case.get("journal"):
        latest = max(nights, key=lambda n: n.bedtime)
        nights = [replace(n, notes=journal) if n is latest else n for n in nights]
    a = service.ask_coach(CliCoach(), nights, case["question"], trace)
    fails = grade(a.raw_text, case["expect"])
    return dict(config=NAME, case=case["id"], type=case["type"], golden=case["golden"], trial=trial,
                answer=a.raw_text, fallback_shown=a.used_fallback, passed=not fails, reasons=fails)
jobs = [(c, t) for c in cases for t in range(1, RUNS + 1)]
with ThreadPoolExecutor(8) as ex: res = list(ex.map(one, jobs))
with open(M / f"results-{NAME}.jsonl", "w") as f:
    for r in res: f.write(json.dumps(r) + "\n")
print(NAME, MODEL, "prompt", prompt_version(PROMPT.read_text(encoding="utf-8")), len(res), "trials")
