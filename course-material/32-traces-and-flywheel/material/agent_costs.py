"""Cost, tokens, duration and turns for every recorded Claude Code run in the course (from the stream-json result event)."""
import glob, json, statistics as st, sys, os
L = sys.argv[1]
TASKS = {"24-grading-the-path/material/run-": "off-topic prompt change",
         "25-regression-testing-the-agent/material/agent/run-off": "off-topic change, new CLAUDE.md rule",
         "25-regression-testing-the-agent/material/agent/run-crash": "crash fix (regression agent eval)",
         "26-quality-gates/material/agents/run-reg": "stop the 'diagnose' fallback",
         "27-reviewing-agent-code/material/agents/run-sum": "weekly summary endpoint",
         "27-reviewing-agent-code/material/agents/review-sum": "AI review of the summary",
         "28-production-gate/material/agents/run-": "production data repair",
         "30-security-gates/material/agents/run-sec": "journal search",
         "30-security-gates/material/agents/run2-sec": "search logging"}
rows = []
for f in sorted(glob.glob(f"{L}/*/material/**/*.jsonl", recursive=True)):
    rel = os.path.relpath(f, L); task = next((t for k, t in TASKS.items() if rel.startswith(k)), None)
    if not task: continue
    res = [json.loads(l) for l in open(f) if '"type":"result"' in l]
    if not res: continue
    r = res[-1]; u = r.get("usage", {})
    rows.append(dict(task=task, run=os.path.basename(f)[:-6], cost=r["total_cost_usd"], secs=r["duration_ms"] / 1000, turns=r["num_turns"],
                     out=u.get("output_tokens", 0), cache_read=u.get("cache_read_input_tokens", 0), cache_write=u.get("cache_creation_input_tokens", 0)))
json.dump(rows, open(f"{L}/32-traces-and-flywheel/material/agent_costs.json", "w"), indent=1)
print(f"{'task':40} {'runs':>4} {'median $':>9} {'min-max $':>13} {'median s':>9} {'turns':>6}")
for t in dict.fromkeys(r["task"] for r in rows):
    g = [r for r in rows if r["task"] == t]; c = [r["cost"] for r in g]
    print(f"{t:40} {len(g):>4} {st.median(c):>9.2f} {min(c):>6.2f}-{max(c):<6.2f} {st.median([r['secs'] for r in g]):>9.0f} {st.median([r['turns'] for r in g]):>6.0f}")
c = [r["cost"] for r in rows]
print(f"\n{len(rows)} runs · total ${sum(c):.2f} · median ${st.median(c):.2f} per run · median {st.median([r['secs'] for r in rows]):.0f} s")
cr = sum(r["cache_read"] for r in rows); cw = sum(r["cache_write"] for r in rows); o = sum(r["out"] for r in rows)
print(f"tokens: cache read {cr:,} · cache write {cw:,} · output {o:,}")
