"""Command-line client for NightJar's local bug tracker (a stand-in for Jira).

    python3 tools/tracker/tracker.py search WORDS...       # issues containing every word
    python3 tools/tracker/tracker.py get NJ-12
    python3 tools/tracker/tracker.py create --draft bug-drafts/x.md
    python3 tools/tracker/tracker.py comment NJ-12 --draft bug-drafts/x-comment.md

Reads the address from NJ_TRACKER_URL (default http://127.0.0.1:8765) and the
token from NJ_TRACKER_TOKEN. A draft is a Markdown file whose first line is
"# <summary>"; the rest is the description. Every search is logged to
.tracker/searches.jsonl.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

URL = os.environ.get("NJ_TRACKER_URL", "http://127.0.0.1:8765")


def call(method: str, path: str, body: dict | None = None) -> dict:
    token = os.environ.get("NJ_TRACKER_TOKEN", "")
    request = urllib.request.Request(
        URL + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        sys.exit(f"tracker: {error.code} {json.loads(error.read()).get('error')}")
    except urllib.error.URLError as error:
        sys.exit(f"tracker: can't reach {URL} ({error.reason}). Is `make tracker` running?")


def read_draft(path: str) -> tuple[str, str]:
    lines = Path(path).read_text().splitlines()
    if not lines or not lines[0].startswith("# "):
        sys.exit(f"tracker: {path} must start with '# <summary>'")
    return lines[0][2:].strip(), "\n".join(lines[1:]).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("search", help="issues containing every word")
    p.add_argument("words", nargs="+")
    p = sub.add_parser("get", help="one issue with its description and comments")
    p.add_argument("key")
    p = sub.add_parser("create", help="file a new bug from a draft")
    p.add_argument("--draft", required=True)
    p = sub.add_parser("comment", help="add a draft as a comment on an issue")
    p.add_argument("key")
    p.add_argument("--draft", required=True)
    args = parser.parse_args()

    if args.command == "search":
        query = " ".join(args.words)
        result = call("GET", "/rest/api/2/search?" + urlencode({"text": query}))
        log = Path(".tracker/searches.jsonl")
        log.parent.mkdir(exist_ok=True)
        with log.open("a") as f:
            f.write(
                json.dumps({"time": time.time(), "query": query, "hits": result["total"]}) + "\n"
            )
        print(f"{result['total']} issue(s) contain: {query}")
        for issue in result["issues"]:
            print(f"  {issue['key']}  {issue['status']:<6}  {issue['summary']}")
    elif args.command == "get":
        issue = call("GET", f"/rest/api/2/issue/{args.key}")
        print(f"{issue['key']}  {issue['status']}  {issue['summary']}\n\n{issue['description']}")
        for n, comment in enumerate(issue["comments"], 1):
            print(f"\n--- comment {n}\n{comment}")
    elif args.command == "create":
        summary, description = read_draft(args.draft)
        result = call("POST", "/rest/api/2/issue", {"summary": summary, "description": description})
        print(f"Created {result['key']}: {summary}")
    elif args.command == "comment":
        summary, description = read_draft(args.draft)
        body = {"body": f"{summary}\n\n{description}"}
        call("POST", f"/rest/api/2/issue/{args.key}/comment", body)
        print(f"Commented on {args.key}")


if __name__ == "__main__":
    main()
