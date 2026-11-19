"""Re-grade saved results with a different case folder (no new model calls). Run from the NightJar repo."""
import json, sys, glob, yaml
sys.path.insert(0, "evals")
from run_evals import grade
M, cases_dir, src, dst = sys.argv[1:5]
cases = {c["id"]: c for c in (yaml.safe_load(open(p)) for p in glob.glob(f"{M}/{cases_dir}/*.yaml"))}
with open(f"{M}/{dst}", "w") as f:
    for l in open(f"{M}/{src}"):
        x = json.loads(l); fails = grade(x["answer"], cases[x["case"]]["expect"])
        x.update(passed=not fails, reasons=fails); f.write(json.dumps(x) + "\n")
