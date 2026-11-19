"""Per-case results over 10 trials, and pass@k / pass^k from the per-trial rate."""
import json
from collections import defaultdict
d = {json.loads(l)["id"]: json.loads(l) for l in open("dataset.jsonl")}
safe = {x["id"]: x["verdict"] for x in json.load(open("judge_rubric_1.json"))}
grnd = {x["id"]: x["verdict"] for x in json.load(open("judge_grounded_1.json"))}
rows = defaultdict(lambda: defaultdict(int))
for k, x in d.items():
    r = rows[x["case"]]
    r["code"] += x["code"] == "pass"; r["safe"] += safe[k] == "pass"; r["grounded"] += grnd[k] == "pass"
    r["shown"] += x["shown_to_user"] == x["answer"]
print(f"{'case':6} {'code':>5} {'safe':>5} {'grnd':>5} {'shown':>6}   (passes out of 10; shown = the user saw the model's answer)")
for c in sorted(rows):
    r = rows[c]; print(f"{c:6} {r['code']:>5} {r['safe']:>5} {r['grounded']:>5} {r['shown']:>6}")
print("\npass@k = 1-(1-p)^k, pass^k = p^k")
for p in (1.0, 0.9, 0.75, 0.6):
    print(f"p={p:.2f}  " + "  ".join(f"k={k}: pass@k {1-(1-p)**k:5.1%} pass^k {p**k:5.1%}" for k in (3, 10)))
print(f"\nchance that 3 trials all miss a 40% event: {0.6**3:.1%}")
print("rule of three: 0 failures in n trials -> 95% upper bound on the failure rate is about 3/n (exact 1-0.05^(1/n): n=10: 26%, n=300: 1%)")
