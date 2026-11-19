"""A two-agent pipeline on a NightJar clone: a builder changes the code, a tester checks it.
On FAIL, the builder gets the tester's report and tries again, up to MAX_ROUNDS.
   python3 pipeline.py <clone> <log.jsonl>"""
import json, re, subprocess, sys, time
from pathlib import Path
REPO, LOG = Path(sys.argv[1]), Path(sys.argv[2])
MAX_ROUNDS = 4
TASK = ("When claims/register.yaml has an empty nudge_copy list, next_nudge crashes with "
        "ZeroDivisionError. Make it fail with a clear error message instead.")
BUILDER_TOOLS = "Read,Edit,Write,Glob,Grep,Bash(make test),Bash(make lint),Bash(uv run pytest:*),Bash(git diff:*),Bash(git status)"
TESTER_TOOLS = "Read,Glob,Grep,Bash(make test),Bash(make lint),Bash(uv run pytest:*),Bash(git diff:*),Bash(git status)"
def claude(prompt, tools):
    t = time.time()
    r = subprocess.run(["claude", "-p", prompt, "--model", "claude-sonnet-5-5", "--setting-sources", "project",
                        "--allowedTools", tools, "--output-format", "json"], cwd=REPO, capture_output=True, text=True,
                       stdin=subprocess.DEVNULL, timeout=1200)
    return json.loads(r.stdout)["result"], round(time.time() - t)
def log(**rec):
    with LOG.open("a") as f: f.write(json.dumps(rec) + "\n")
feedback = ""
for rnd in range(1, MAX_ROUNDS + 1):
    prompt = f"You are the builder in a two-agent pipeline. Your task: {TASK}"
    if feedback:
        prompt += f"\n\nThe tester rejected your last attempt. The tester's report:\n{feedback}\n\nFix what the tester reported."
    report, secs = claude(prompt, BUILDER_TOOLS)
    diff = subprocess.run(["git", "diff", "--stat"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    log(round=rnd, role="builder", secs=secs, report=report, diff_stat=diff)
    verdict_text, secs = claude(
        "You are the tester in a two-agent pipeline. The builder has just changed this repository to do this task: "
        f"{TASK}\n\nCheck the change: read the diff, run make test and make lint. Report what you found, then end with "
        "exactly one line: VERDICT: PASS or VERDICT: FAIL.", TESTER_TOOLS)
    v = re.findall(r"VERDICT:\s*(PASS|FAIL)", verdict_text)
    verdict = v[-1] if v else "NONE"
    log(round=rnd, role="tester", secs=secs, verdict=verdict, report=verdict_text)
    if verdict == "PASS":
        break
    feedback = verdict_text
log(round=rnd, role="pipeline", result="PASS" if verdict == "PASS" else f"gave up after {rnd} rounds")
