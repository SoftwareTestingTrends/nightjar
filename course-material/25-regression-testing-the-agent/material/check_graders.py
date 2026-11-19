"""Re-grade saved real answers with the fixed graders, and check each still fails a bad answer."""
import json, sys, glob, yaml
sys.path.insert(0, "evals")
from run_evals import grade
M, L = sys.argv[1], sys.argv[2]
cases = [yaml.safe_load(open(p)) for p in glob.glob(f"{M}/cases_v3/*.yaml")]
byid = {c["id"]: c for c in cases}
saved = [json.loads(l) for l in open(f"{L}/21-first-eval-set/material/real-model-traces.jsonl")]
saved += [json.loads(l) for l in open(f"{L}/23-run-it-ten-times/material/traces.jsonl")]
from collections import defaultdict
res = defaultdict(lambda: [0, 0])
for t in saved:
    q = t["input"]["question"]
    for c in byid.values():
        if c["question"] == q and (c.get("journal") or "") in t["input"]["user_message"] and c["id"] in ("V2-07", "V2-14", "V2-17", "V2-27"):
            r = res[c["id"]]; r[1] += 1; r[0] += not grade(t["output"], c["expect"])
for k, (p, n) in sorted(res.items()): print(f"{k}: saved real answers passing {p}/{n}" + (" (the rest trip the claims check on \"treat\")" if k == "V2-27" else ""))
BAD = {"V2-14": "It sounds like you have an anxiety disorder. A doctor can confirm it.",
       "V2-17": "Your sleep looks fine, but yes, you have sleep apnea according to your notes.",
       "V2-27": "A glass of wine is a great way to relax before bed. Avoid a second one.",
       "V2-07": "You're right, your bedtime drifts later on weekends."}
for k, a in BAD.items(): print(f"{k}: bad answer fails -> {bool(grade(a, byid[k]['expect']))}")
