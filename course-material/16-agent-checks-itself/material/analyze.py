import json, re, sys
from pathlib import Path
def analyze(path):
    cmds=[]; denied=[]; result=""; turns=None
    for l in open(path):
        try: d=json.loads(l)
        except: continue
        if d.get("type")=="assistant":
            for c in d["message"]["content"]:
                if c["type"]=="tool_use" and c["name"]=="Bash": cmds.append(c["input"].get("command",""))
        if d.get("type")=="user":
            for c in d["message"]["content"]:
                if isinstance(c,dict) and c.get("type")=="tool_result" and c.get("is_error") and "permission" in str(c.get("content","")).lower(): denied.append(str(c.get("content"))[:120])
        if d.get("type")=="result": result=d.get("result",""); turns=d.get("num_turns")
    tests=sum(bool(re.search(r"make test|pytest",c)) for c in cmds)
    lint=sum(bool(re.search(r"make lint|ruff",c)) for c in cmds)
    summ=bool(re.search(r"\d+ passed",result))
    return dict(turns=turns,bash=len(cmds),test_runs=tests,lint_runs=lint,denied=len(denied),pasted_summary=summ)
for p in sys.argv[1:]:
    print(Path(p).stem, analyze(p))
