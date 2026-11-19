"""Grade every answer in dataset.jsonl with NightJar's own code graders (run from the NightJar repo)."""
import json, sys, yaml, glob
sys.path.insert(0, "evals")
from run_evals import grade
M = sys.argv[1]
cases = {c["id"]: c for c in (yaml.safe_load(open(p)) for p in glob.glob(f"{M}/cases/*.yaml"))}
out = []
import os
DATA = os.environ.get("DATA", "dataset.jsonl")
for l in open(f"{M}/{DATA}"):
    d = json.loads(l)
    fails = grade(d["answer"], cases[d["case"]]["expect"])
    out.append(dict(id=d["id"], verdict="fail" if fails else "pass", reason="; ".join(fails)))
json.dump(out, open(f"{M}/code_grader{'_heldout' if 'heldout' in DATA else ''}.json", "w"), indent=1)
