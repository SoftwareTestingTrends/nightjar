"""Code grader for one triage run, in skill-creator's grading.json format.

usage: python3 grade.py <evals.json> <eval-id> <nightjar-copy> <run-dir>

Every check runs code against the copy the agent worked in. Nothing is judged
by reading the agent's prose.
"""

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

evals_path, eval_id, copy, run_dir = sys.argv[1], int(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
case = next(e for e in json.loads(Path(evals_path).read_text())["evals"] if e["id"] == eval_id)
expectations = []


def check(text: str, passed: bool, evidence: str) -> None:
    expectations.append({"text": text, "passed": bool(passed), "evidence": evidence})


def run_repro(path: Path) -> tuple[int, str]:
    try:
        done = subprocess.run(
            ["uv", "run", "python", str(path.relative_to(copy))],
            cwd=copy, capture_output=True, text=True, timeout=120,
        )
        out = (done.stdout + done.stderr).strip().splitlines()
        return done.returncode, out[-1] if out else ""
    except subprocess.TimeoutExpired:
        return -1, "timed out"


db_after_agent = (copy / "nightjar.db").exists()
repros = sorted(copy.glob("bugs/**/repro.py"))
results = {p: run_repro(p) for p in repros}
failing = [p for p, (code, _) in results.items() if code == 1]
listing = "; ".join(f"{p.relative_to(copy)} → exit {c} ({line[:80]})" for p, (c, line) in results.items()) or "no repro.py in bugs/"

if case["kind"] == "bug":
    check("A repro script exists in bugs/", bool(repros), listing)
    check("The repro exits 1 on today's code (the bug is present)", bool(failing), listing)
    chosen = failing[0] if failing else (repros[0] if repros else None)
    if chosen:
        codes = [run_repro(chosen)[0] for _ in range(3)]
        check("The repro gives exit 1 three more times in a row", codes == [1, 1, 1], f"exit codes {codes}")
    else:
        check("The repro gives exit 1 three more times in a row", False, "no repro to run")
    if case.get("fix_patch"):
        patch = Path(evals_path).parent / case["fix_patch"]
        if chosen and subprocess.run(["git", "apply", str(patch)], cwd=copy).returncode == 0:
            code, line = run_repro(chosen)
            subprocess.run(["git", "apply", "-R", str(patch)], cwd=copy)
            check("The repro exits 0 with the developer's fix applied", code == 0, f"exit {code} ({line[:80]})")
        else:
            check("The repro exits 0 with the developer's fix applied", False, "no repro, or the fix didn't apply")
else:
    check("No repro script reports a bug (none exits 1 on today's code)", not failing, listing)

db_now = (copy / "nightjar.db").exists()
check("The real nightjar.db wasn't created or used", not db_after_agent and not db_now,
      f"nightjar.db after the agent: {db_after_agent}; after the grader ran the repros: {db_now}")

# timing and tool calls from the transcript
tools, result = Counter(), {}
for line in (run_dir / "transcript.jsonl").read_text().splitlines():
    event = json.loads(line)
    if event.get("type") == "assistant":
        for part in event["message"]["content"]:
            if part.get("type") == "tool_use":
                tools[part["name"]] += 1
    if event.get("type") == "result":
        result = event
usage = result.get("usage", {})
tokens = sum(usage.get(k, 0) for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
(run_dir / "reply.md").write_text(result.get("result", ""))
(run_dir / "timing.json").write_text(json.dumps({
    "total_duration_seconds": round(result.get("duration_ms", 0) / 1000, 1),
    "total_tokens": tokens, "output_tokens": usage.get("output_tokens", 0), "num_turns": result.get("num_turns", 0),
}, indent=2))

passed = sum(e["passed"] for e in expectations)
(run_dir / "grading.json").write_text(json.dumps({
    "expectations": expectations,
    "summary": {"passed": passed, "failed": len(expectations) - passed, "total": len(expectations),
                "pass_rate": round(passed / len(expectations), 2)},
    "execution_metrics": {"tool_calls": dict(tools), "total_tool_calls": sum(tools.values())},
}, indent=2))
print(f"eval {eval_id} {run_dir.parent.name} {run_dir.name}: {passed}/{len(expectations)}")
