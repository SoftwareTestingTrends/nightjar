"""Build dataset.jsonl: 87 real coach answers (lesson 20) + 12 seeded unsafe answers, with our human labels."""
import json, yaml, glob
cases = [yaml.safe_load(open(p)) for p in sorted(glob.glob("cases/*.yaml"))]
traces = [json.loads(l) for l in open("real-model-traces.jsonl")]
assert len(traces) == 87
items, by_case = [], {}
for i, t in enumerate(traces):
    c = cases[i // 3]
    assert t["input"]["question"] == c["question"], (i, c["id"])
    it = dict(id=f"R{i+1:02d}", case=c["id"], golden=c["golden"], question=c["question"],
              user_message=t["input"]["user_message"], answer=t["output"], source="real", human="pass")
    items.append(it); by_case.setdefault(c["id"], it)
for b in json.load(open("seeded_bad.json")):
    base = by_case[b["case"]]
    items.append(dict(id=b["id"], case=b["case"], golden=base["golden"], question=base["question"],
                      user_message=base["user_message"], answer=b["answer"], source="seeded",
                      human="fail", why=b["why"]))
with open("dataset.jsonl", "w") as f:
    for it in items: f.write(json.dumps(it) + "\n")
print(len(items))
