"""Gate a candidate run against the baseline run from main.
   python3 gate.py results-baseline.jsonl results-<candidate>.jsonl
Rules: golden cases must pass every trial; regression cases must not drop below the baseline;
capability cases are reported, not gated. Known issues are reported, not gated. Exit 1 if blocked."""
import json, sys
from collections import defaultdict
from pathlib import Path
import yaml
def load(p):
    r = defaultdict(lambda: dict(n=0, p=0))
    for l in open(p):
        x = json.loads(l); c = r[x["case"]]; c["n"] += 1; c["p"] += x["passed"]; c["type"] = x["type"]; c["golden"] = x["golden"]
    return r
base, cand = load(sys.argv[1]), load(sys.argv[2])
known = yaml.safe_load(open(Path(__file__).with_name("known_issues.yaml")))
block, notes = [], []
for case in sorted(cand):
    b, c = base.get(case), cand[case]
    rate = f"{c['p']}/{c['n']}"; was = f"{b['p']}/{b['n']}" if b else "new"
    if case in known:
        if c["p"] < c["n"]: notes.append(f"known   {case}  {rate}  (was {was})  {known[case]['issue']} · owner: {known[case]['owner']}")
        else: notes.append(f"FIXED?  {case}  {rate}  (was {was})  passes now: take it off the known-issues list")
        continue
    if c["golden"] and c["p"] < c["n"]:
        block.append(f"BLOCK   {case}  {rate}  (was {was})  golden case failed a trial")
    elif c["type"] == "regression" and b and c["p"] / c["n"] < b["p"] / b["n"]:
        block.append(f"BLOCK   {case}  {rate}  (was {was})  regression case dropped below the baseline")
    elif b and c["p"] != b["p"]:
        notes.append(f"{'better' if c['p'] > b['p'] else 'worse '}  {case}  {rate}  (was {was})  {c['type']}")
total = lambda r: (sum(x["p"] for x in r.values()), sum(x["n"] for x in r.values()))
print(f"candidate {Path(sys.argv[2]).stem}: {total(cand)[0]}/{total(cand)[1]} trials passed (baseline {total(base)[0]}/{total(base)[1]})")
for l in block + notes: print("  " + l)
print("GATE: " + ("BLOCKED" if block else "PASS"))
sys.exit(1 if block else 0)
