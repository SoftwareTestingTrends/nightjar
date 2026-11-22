#!/usr/bin/env python3
"""Start NightJar on a free port with an empty, throwaway database, run a command,
then stop the app.

    python3 with_app.py [--csv nights.csv] -- <command, with {url} where the app's address goes>

Run it from the NightJar repository root. The app gets a fresh SQLite file in a temporary
folder (never the real nightjar.db) and the offline mock coach. With --csv, the nights in
that file are loaded before the command runs. The exit code is the command's.

Example:
    python3 with_app.py -- uv run python /tmp/check.py {url}
"""

import argparse
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

LOAD_CSV = (
    "import sys; from nightjar.diary import Diary, parse_csv; "
    "d = Diary(sys.argv[1]); "
    "n = d.add_nights(parse_csv(open(sys.argv[2], encoding='utf-8').read())); "
    "print(f'loaded {n} nights')"
)


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--csv", help="diary CSV to load first (bedtime,wake_time,timezone,notes)")
    parser.add_argument(
        "command", nargs=argparse.REMAINDER, help="command to run; {url} becomes the app's URL"
    )
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("give the command to run after --")
    if not os.path.exists("pyproject.toml"):
        sys.exit("Run this from the NightJar repository root.")

    work = tempfile.mkdtemp(prefix="nightjar-check-")
    db = os.path.join(work, "check.db")
    env = {**os.environ, "NIGHTJAR_DB": db, "NIGHTJAR_COACH": "mock"}
    if args.csv:
        subprocess.run(["uv", "run", "python", "-c", LOAD_CSV, db, args.csv], env=env, check=True)

    port = free_port()
    url = f"http://127.0.0.1:{port}"
    server = subprocess.Popen(
        [
            "uv",
            "run",
            "uvicorn",
            "nightjar.web:create_app",
            "--factory",
            "--port",
            str(port),
            "--log-level",
            "warning",
        ],
        env=env,
    )
    try:
        for _ in range(150):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except OSError:
                time.sleep(0.2)
        else:
            print("NightJar didn't start within 30 seconds.", file=sys.stderr)
            return 1
        print(f"NightJar is running at {url} with an empty test database.", flush=True)
        return subprocess.run([part.replace("{url}", url) for part in command], env=env).returncode
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
