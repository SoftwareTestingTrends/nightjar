"""Cost and latency per coach answer, Sonnet vs Haiku, through the Claude Code CLI. Run from the NightJar repo with uv."""
import json, sys, glob, subprocess, yaml
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
sys.path.insert(0, "evals")
from run_evals import SAMPLE_CSV
from nightjar.coach.base import build_user_message, load_system_prompt
from nightjar.diary import parse_csv
L, OUT = Path(sys.argv[1]), Path(sys.argv[2])
cases = [yaml.safe_load(open(p)) for p in sorted(glob.glob(f"{L}/25-regression-testing-the-agent/material/cases_v3/*.yaml"))][:15]
system = load_system_prompt()
def one(job):
    model, case = job
    nights = parse_csv(SAMPLE_CSV.read_text(encoding="utf-8"))
    if case.get("journal"):
        latest = max(nights, key=lambda n: n.bedtime); nights = [replace(n, notes=case["journal"]) if n is latest else n for n in nights]
    r = subprocess.run(["claude", "-p", build_user_message(nights, case["question"]), "--system-prompt", system, "--model", model,
                        "--tools", "", "--setting-sources", "", "--output-format", "json"], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
    j = json.loads(r.stdout); u = j.get("usage", {})
    return dict(model=model, case=case["id"], cost=j["total_cost_usd"], api_ms=j["duration_api_ms"], total_ms=j["duration_ms"],
                input=u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0), output=u.get("output_tokens", 0))
jobs = [(m, c) for m in ("claude-sonnet-5-5", "claude-haiku-4-5-20251001") for c in cases]
with ThreadPoolExecutor(6) as ex: rows = list(ex.map(one, jobs))
OUT.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
import statistics as st
for m in ("claude-sonnet-5-5", "claude-haiku-4-5-20251001"):
    g = [r for r in rows if r["model"] == m]
    print(f"{m:28} {len(g)} answers · median ${st.median(r['cost'] for r in g):.4f} per answer · "
          f"median API latency {st.median(r['api_ms'] for r in g)/1000:.1f} s (CLI total {st.median(r['total_ms'] for r in g)/1000:.1f} s) · "
          f"median tokens in {st.median(r['input'] for r in g):,.0f} / out {st.median(r['output'] for r in g):,.0f}")
