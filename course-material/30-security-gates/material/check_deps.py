"""Gate step: every direct dependency must exist on PyPI, with a release history (catches made-up names)."""
import json, sys, tomllib, urllib.request, re
from datetime import datetime
deps = [re.split(r"[<>=!~\[; ]", d)[0] for d in tomllib.load(open(sys.argv[1], "rb"))["project"]["dependencies"]] + sys.argv[2:]
for name in deps:
    try:
        data = json.load(urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=20))
        dates = [f["upload_time"] for files in data["releases"].values() for f in files]
        first = min(dates)[:10] if dates else "?"
        print(f"OK     {name:28} first release {first}, {len(data['releases'])} releases, latest {data['info']['version']}")
    except urllib.error.HTTPError as e:
        print(f"BLOCK  {name:28} not on PyPI ({e.code}): a made-up name, and anyone could register it")
