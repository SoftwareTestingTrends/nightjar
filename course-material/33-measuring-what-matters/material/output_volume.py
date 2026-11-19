"""Output volume of the agent changes recorded in this course: lines added and test functions added, per saved diff."""
import glob, os, re, sys
L = sys.argv[1]
pats = ["24-grading-the-path/material/diffs/*.diff", "25-regression-testing-the-agent/material/agent/*.diff",
        "26-quality-gates/material/agents/*.diff", "27-reviewing-agent-code/material/agents/*.diff",
        "30-security-gates/material/agents/*-search.diff", "30-security-gates/material/agents/*-logging.diff"]
rows = []
for p in pats:
    for f in sorted(glob.glob(f"{L}/{p}")):
        if "claude-md-change" in f: continue
        added = tests = 0; newfile = False
        for line in open(f, errors="ignore"):
            if line.startswith("=== new file:"): newfile = True; continue
            if line.startswith("diff --git"): newfile = False
            is_add = (line.startswith("+") and not line.startswith("+++")) or newfile
            if is_add and line.strip("+ \n"):
                added += 1
                if re.match(r"\+?\s*def test_", line): tests += 1
        rows.append((os.path.relpath(f, L).split("/")[0], os.path.basename(f), added, tests))
tot_a = sum(r[2] for r in rows); tot_t = sum(r[3] for r in rows)
for r in rows: print(f"{r[0]:32} {r[1]:22} +{r[2]:4} lines  {r[3]:2} tests")
print(f"\n{len(rows)} agent changes · {tot_a:,} lines added · {tot_t} test functions added")
