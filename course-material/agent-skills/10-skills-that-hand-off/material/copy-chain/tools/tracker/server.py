"""A small local bug tracker that stands in for Jira in the course.

Run it with `make tracker`. It keeps its data outside the repository, in
$NJ_TRACKER_HOME (default ~/.nightjar-tracker), and checks a token on every request:
the read token can search and read issues; only the write token can
create issues or add comments.

    python3 tools/tracker/server.py --seed      # reset the issues to the seed
    python3 tools/tracker/server.py             # keep existing issues

Tokens are created once, in tokens.json, and kept across restarts.
"""

import argparse
import json
import os
import re
import secrets
import shutil
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).parent


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def matches(issue: dict, query: str) -> bool:
    """Every query word must start a word in the summary or description."""
    haystack = words(issue["summary"] + " " + issue["description"])
    return all(any(w.startswith(q) for w in haystack) for q in words(query))


class Tracker:
    def __init__(self, home: Path) -> None:
        self.home = home
        self.issues_path = home / "issues.json"
        self.tokens = json.loads((home / "tokens.json").read_text())

    def load(self) -> list[dict]:
        return json.loads(self.issues_path.read_text())

    def save(self, issues: list[dict]) -> None:
        self.issues_path.write_text(json.dumps(issues, indent=2) + "\n")

    def role(self, header: str | None) -> str | None:
        token = (header or "").removeprefix("Bearer ").strip()
        for role in ("write", "read"):
            if token and secrets.compare_digest(token, self.tokens[role]):
                return role
        return None


def make_handler(tracker: Tracker):
    class Handler(BaseHTTPRequestHandler):
        def send(self, status: int, body: dict) -> None:
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *args) -> None:  # keep the terminal quiet
            pass

        def do_GET(self) -> None:
            if tracker.role(self.headers.get("Authorization")) is None:
                return self.send(401, {"error": "missing or unknown token"})
            url = urlparse(self.path)
            if url.path == "/rest/api/2/search":
                query = parse_qs(url.query).get("text", [""])[0]
                hits = [i for i in tracker.load() if matches(i, query)]
                return self.send(200, {"total": len(hits), "issues": hits})
            m = re.fullmatch(r"/rest/api/2/issue/(NJ-\d+)", url.path)
            if m:
                for issue in tracker.load():
                    if issue["key"] == m.group(1):
                        return self.send(200, issue)
                return self.send(404, {"error": f"{m.group(1)} not found"})
            self.send(404, {"error": "unknown path"})

        def do_POST(self) -> None:
            role = tracker.role(self.headers.get("Authorization"))
            if role is None:
                return self.send(401, {"error": "missing or unknown token"})
            if role != "write":
                return self.send(403, {"error": "this token can only read"})
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            issues = tracker.load()
            if self.path == "/rest/api/2/issue":
                key = f"NJ-{max(int(i['key'][3:]) for i in issues) + 1}"
                issues.append(
                    {
                        "key": key,
                        "type": "Bug",
                        "status": "Open",
                        "summary": body["summary"],
                        "description": body["description"],
                        "comments": [],
                    }
                )
                tracker.save(issues)
                return self.send(201, {"key": key})
            m = re.fullmatch(r"/rest/api/2/issue/(NJ-\d+)/comment", self.path)
            if m:
                for issue in issues:
                    if issue["key"] == m.group(1):
                        issue["comments"].append(body["body"])
                        tracker.save(issues)
                        return self.send(201, {"key": issue["key"]})
                return self.send(404, {"error": f"{m.group(1)} not found"})
            self.send(404, {"error": "unknown path"})

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    default_home = os.environ.get("NJ_TRACKER_HOME", str(Path.home() / ".nightjar-tracker"))
    parser.add_argument("--home", type=Path, default=Path(default_home))
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--seed", action="store_true", help="reset the issues to the seed")
    args = parser.parse_args()
    try:  # take the port before touching any data
        server = ThreadingHTTPServer(("127.0.0.1", args.port), BaseHTTPRequestHandler)
    except OSError:
        msg = f"Port {args.port} is in use: the tracker is probably already running."
        raise SystemExit(msg) from None
    args.home.mkdir(parents=True, exist_ok=True)
    if args.seed or not (args.home / "issues.json").exists():
        shutil.copy(HERE / "seed.json", args.home / "issues.json")
    if not (args.home / "tokens.json").exists():
        tokens = {"read": secrets.token_hex(16), "write": secrets.token_hex(16)}
        (args.home / "tokens.json").write_text(json.dumps(tokens, indent=2) + "\n")
        (args.home / "tokens.json").chmod(0o600)
    tracker = Tracker(args.home)
    server.RequestHandlerClass = make_handler(tracker)
    print(f"NightJar tracker on http://127.0.0.1:{args.port} (data and tokens in {args.home})")
    server.serve_forever()


if __name__ == "__main__":
    main()
