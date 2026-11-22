"""Score S-117 test-case documents. Usage: score.py <run-name>... (reads copy-<name>/docs/test-cases/S-117.md and run-<name>.jsonl)"""
import json, re, sys, os
H = os.path.dirname(os.path.abspath(__file__))
CONDS = {
 "E1 file name near midnight/zone": lambda t: "nightjar-diary-" in t and re.search(r"23:5\d|00:0\d|midnight", t, re.I),
 "E2 header + columns": lambda t: "bedtime,wake_time,timezone,notes" in t,
 "E3 offsets per zone and DST": lambda t: "-04:00" in t and "-05:00" in t,
 "E4 night-of order": lambda t: re.search(r"oldest|order", t, re.I),
 "E5 comma, quote, line break, non-English": lambda t: re.search(r"comma", t, re.I) and re.search(r"quot", t, re.I) and re.search(r"line break|newline|new line", t, re.I) and re.search(r"non-english|emoji|accent|é|ü|ñ|ç|ö|日|中|Ω|🙂|😴|é", t, re.I),
 "E6 round trip": lambda t: re.search(r"round.trip|re-?import|import.{0,60}same nights", t, re.I),
 "E7 empty diary → header only": lambda t: re.search(r"empty diary|no nights", t, re.I) and re.search(r"header", t, re.I),
 "E8 1,000 nights < 2 s": lambda t: re.search(r"1,000|1000", t),
 "E9 button / download": lambda t: re.search(r"Export CSV", t),
 "Q1 leading/trailing spaces": lambda t: re.search(r"leading|trailing|padded|surrounding (white)?space", t, re.I),
 "Q2 formula injection": lambda t: re.search(r"formula|csv injection", t, re.I),
 "Q3 encoding / BOM": lambda t: re.search(r"BOM|byte.order|UTF-8", t, re.I),
}
def sections(t):
    out, cur = {}, None
    for line in t.splitlines():
        m = re.match(r"#{2,4}\s+(.*)", line)
        if m:
            h = m.group(1)
            cur = None
            mm = re.search(r"\b(AC\s?\d|Edge|Non-functional|NFR|Open questions)", h, re.I)
            if mm: cur = mm.group(1).replace(" ", "").upper()
            continue
        if cur and cur != "OPENQUESTIONS":
            row = re.match(r"\|\s*TC-117-(\d+)\s*\|", line)
            if row:  # case rows only, not cross-references (corrected 2026-11-21)
                out.setdefault(cur, set()).add(row.group(1))
    return {k: len(v) for k, v in out.items()}
def oq(t):
    m = re.search(r"#+\s*Open questions(.*)", t, re.I | re.S)
    if not m: return 0, 0
    lines = m.group(1).splitlines()
    header = next((l for l in lines if l.startswith("|")), "")
    rows = [l for l in lines if re.match(r"\|\s*\**(?:OQ-|Q)?\d+\**\s*\|", l)]
    if "proposed" not in header.lower(): return len(rows), 0
    col = [c.strip().lower() for c in header.split("|")].index(next(c.strip().lower() for c in header.split("|") if "proposed" in c.lower()))
    prop = [r for r in rows if len(r.split("|")) > col and r.split("|")[col].strip() not in ("", "-")]
    return len(rows), len(prop)
def trace(name):
    reads, turns, secs = [], None, None
    for l in open(f"{H}/run-{name}.jsonl"):
        if not l.startswith("{"): continue
        e = json.loads(l)
        if e.get("type") == "assistant":
            for b in e["message"]["content"]:
                if b["type"] == "tool_use":
                    s = json.dumps(b["input"])
                    if re.search(r'"(src|tests)/|/src/|/tests/', s): reads.append(b["name"])
        if e.get("type") == "result": turns, secs = e.get("num_turns"), round(e.get("duration_ms", 0) / 1000)
    return reads, turns, secs
rows = []
for name in sys.argv[1:]:
    f = f"{H}/copy-{name}/docs/test-cases/S-117.md"
    if not os.path.exists(f):
        print(f"{name}: no document"); continue
    t = open(f).read()
    ids = sorted(set(re.findall(r"TC-117-(\d+)", t)), key=int)
    sec = sections(t); q, qp = oq(t); r, turns, secs = trace(name)
    miss = [k for k, fn in CONDS.items() if not fn(t)]
    rows.append({"run": name, "cases": len(ids), "per_section": sec, "max_per_ac": max([v for k, v in sec.items() if k.startswith("AC")] or [0]),
                 "open_q": q, "with_proposal": qp, "conditions": 12 - len(miss), "missing": miss, "read_src_or_tests": r, "turns": turns, "secs": secs, "words": len(t.split())})
for x in rows:
    print(f'{x["run"]:14} cases {x["cases"]:3}  max/AC {x["max_per_ac"]:2}  questions {x["open_q"]:2} (proposed {x["with_proposal"]:2})  conds {x["conditions"]}/12  words {x["words"]:5}  turns {x["turns"]} {x["secs"]}s  src/tests {len(x["read_src_or_tests"])}  missing {x["missing"]}')
json.dump(rows, open(f"{H}/scores.json", "w"), indent=1)
