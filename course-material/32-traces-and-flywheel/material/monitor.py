"""Monitor NightJar's coach from its JSONL traces: per prompt version and model, how often users saw the fallback, and latency."""
import glob, json, statistics as st, sys
from collections import defaultdict
L = sys.argv[1]
files = sorted(set(glob.glob(f"{L}/*/material/*traces*.jsonl")) - {f"{L}/22-graders/material/real-model-traces.jsonl"})
g = defaultdict(list)
for f in files:
    for l in open(f):
        t = json.loads(l)
        g[(t["prompt_version"], t["model"].split(" ")[0])].append(t)
names = {"b21f95582895": "main prompt", "c69ae180a358": "off-topic prompt", "87bd6dedf159": "reg1 prompt (avoid flagged words)", "a1748c6c9081": "reg3 prompt"}
print(f"{'prompt':34} {'model':26} {'answers':>7} {'fallback shown':>15} {'median latency':>15}")
for (pv, model), ts in sorted(g.items(), key=lambda kv: -len(kv[1])):
    fb = sum(t["shown_to_user"] != t["output"] for t in ts)
    lat = st.median(t["latency_ms"] for t in ts) / 1000
    print(f"{names.get(pv, pv):34} {model:26} {len(ts):>7} {fb:>6} ({fb/len(ts):4.0%})   {lat:>10.1f} s")
