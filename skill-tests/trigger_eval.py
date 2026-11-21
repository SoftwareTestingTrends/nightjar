"""Trigger test for one installed skill (method from skill-creator's run_eval.py).

For each query: fresh `claude -p` in the project, watch the stream, and decide on the
agent's FIRST tool call: Skill(<name>) or a Read of the skill's file counts as a trigger;
any other first tool call, or none, is a miss. The session is stopped at that point.

    python3 trigger_eval.py <project_dir> <skill_name> <queries.json> <runs> <out.json>
"""

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

proj, skill, qfile, runs, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
MODEL = "claude-sonnet-5-5"


def once(query):
    cmd = [
        "claude",
        "-p",
        query,
        "--model",
        MODEL,
        "--setting-sources",
        "project",
        "--output-format",
        "stream-json",
        "--verbose",
        "--include-partial-messages",
    ]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    p = subprocess.Popen(
        cmd,
        cwd=proj,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        env=env,
        text=True,
    )
    first, args, t0 = None, "", time.time()
    try:
        for line in p.stdout:
            if time.time() - t0 > 120:
                break
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") == "stream_event":
                se = e["event"]
                if (
                    se.get("type") == "content_block_start"
                    and se.get("content_block", {}).get("type") == "tool_use"
                ):
                    first = se["content_block"]["name"]
                elif (
                    se.get("type") == "content_block_delta"
                    and first
                    and se["delta"].get("type") == "input_json_delta"
                ):
                    args += se["delta"].get("partial_json", "")
                elif se.get("type") == "content_block_stop" and first:
                    break
                elif se.get("type") == "message_stop" and not first:
                    break
            elif e.get("type") == "result":
                break
    finally:
        if p.poll() is None:
            p.kill()
            p.wait()
    hit = (first == "Skill" and skill in args) or (first == "Read" and f"skills/{skill}" in args)
    return {"first_tool": first, "args": args[:200], "triggered": hit}


qs = json.load(open(qfile))
jobs = [(q, r) for q in qs for r in range(runs)]
with ThreadPoolExecutor(max_workers=5) as ex:
    res = list(ex.map(lambda j: (j[0]["id"], once(j[0]["query"])), jobs))
summary = []
for q in qs:
    rs = [r for i, r in res if i == q["id"]]
    rate = sum(r["triggered"] for r in rs) / len(rs)
    ok = rate >= 0.5 if q["should_trigger"] else rate < 0.5
    summary.append({**q, "trigger_rate": rate, "pass": ok, "runs": rs})
json.dump(summary, open(out, "w"), indent=1)
for s in summary:
    verdict = "PASS" if s["pass"] else "FAIL"
    firsts = [r["first_tool"] for r in s["runs"]]
    print(f"{s['id']:4} {verdict} {s['trigger_rate']:.2f}  first: {firsts}  {s['query'][:70]}")
t = [s for s in summary if s["should_trigger"]]
n = [s for s in summary if not s["should_trigger"]]
t_pass = sum(s["pass"] for s in t)
n_pass = sum(s["pass"] for s in n)
print(f"should trigger: {t_pass}/{len(t)} pass · should not: {n_pass}/{len(n)} pass")
