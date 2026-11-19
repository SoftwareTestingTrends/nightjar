"""Print each tool call in an agent transcript (stream-json), in order, with errors marked."""
import json, sys
def steps(path):
    out, pending = [], {}
    for line in open(path):
        try: e = json.loads(line)
        except Exception: continue
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use":
                    i = c["input"]
                    arg = i.get("command") or i.get("file_path") or i.get("pattern") or ""
                    s = dict(tool=c["name"], arg=arg, error=False, result="")
                    pending[c["id"]] = s; out.append(s)
        elif e.get("type") == "user":
            cs = e["message"].get("content", [])
            for c in cs if isinstance(cs, list) else []:
                if c.get("type") == "tool_result" and c.get("tool_use_id") in pending:
                    s = pending[c["tool_use_id"]]; s["error"] = bool(c.get("is_error"))
                    r = c.get("content"); r = r if isinstance(r, str) else json.dumps(r)
                    s["result"] = r
        elif e.get("type") == "result":
            out.append(dict(tool="REPORT", arg="", error=False, result=e.get("result", ""), turns=e.get("num_turns"), secs=e.get("duration_ms", 0) / 1000))
    return out
if __name__ == "__main__":
    for s in steps(sys.argv[1]):
        if s["tool"] == "REPORT":
            print(f"--- REPORT ({s['turns']} turns, {s['secs']:.0f}s)\n{s['result']}")
        else:
            tail = s["result"].strip().splitlines()[-1][:90] if s["result"].strip() else ""
            print(f"{'ERR ' if s['error'] else '    '}{s['tool']:6} {s['arg'][-70:]}  | {tail}")
