"""Deterministic detection: the coach's fallback rate in windows of 30 answers, against a control band.
Baseline = the windows from the main prompt on Sonnet. 1 sigma: log · 2 sigma: diagnose (read-only agent) · 3 sigma: propose a fix."""
import glob, json, statistics as st, sys
L, OUT = sys.argv[1], sys.argv[2]
files = sorted(set(glob.glob(f"{L}/*/material/*traces*.jsonl")) - {f"{L}/22-graders/material/real-model-traces.jsonl"})
ts = sorted((json.loads(l) for f in files for l in open(f)), key=lambda t: t["timestamp"])
W = 30
wins = [ts[i:i + W] for i in range(0, len(ts) - W + 1, W)]
rate = lambda w: sum(t["shown_to_user"] != t["output"] for t in w) / len(w)
base = [rate(w) for w in wins if all(t["prompt_version"] == "b21f95582895" and t["model"].startswith("claude-sonnet") for t in w)]
mu, sd = st.mean(base), st.stdev(base)
print(f"baseline: {len(base)} windows of {W} answers · fallback rate mean {mu:.0%}, sd {sd:.0%} · bands: 1σ {mu+sd:.0%} · 2σ {mu+2*sd:.0%} · 3σ {mu+3*sd:.0%}")
breach = None
for i, w in enumerate(wins):
    r = rate(w); z = (r - mu) / sd
    tier = "3σ propose" if z >= 3 else "2σ diagnose" if z >= 2 else "1σ log" if z >= 1 else ""
    pv = sorted({t["prompt_version"] for t in w}); md = sorted({t["model"].split(" ")[0].replace("-20251001", "") for t in w})
    print(f"window {i:2} {w[0]['timestamp'][:16]}  fallback {r:4.0%}  z {z:+.1f}  {tier:12} prompt {','.join(pv)} model {','.join(md)}")
    if tier.startswith(("2", "3")) and breach is None: breach = (i, w)
if breach:
    open(OUT, "w").write("\n".join(json.dumps({k: t[k] for k in ("timestamp", "model", "prompt_version", "input", "output", "shown_to_user", "claims_violations")}) for t in breach[1]) + "\n")
    print(f"first breach: window {breach[0]} → {OUT}")
