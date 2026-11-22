#!/usr/bin/env python3
"""List what a skill or plugin can run, read and send, without running any of it.

    python3 inventory.py <skill-or-plugin-dir>

Reads files only. Prints Markdown with file:line references for a person (or an agent)
to read next. It doesn't judge anything: a line it lists can be fine, and a problem can
hide in a line it doesn't list. It's a map of where to look, not a verdict.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
TEXT = {".py", ".sh", ".js", ".mjs", ".ts", ".rb", ".ps1", ".bash", ".zsh", ""}
PATTERNS = {
    "network": (
        r"urllib|requests\.|http\.client|httpx|fetch\(|axios|curl |wget |socket\."
        r"|XMLHttpRequest|WebSocket"
    ),
    "credentials/env": (
        r"os\.environ|getenv|process\.env|\.env\b|TOKEN|PASSWORD|SECRET|API_KEY|credential"
    ),
    "runs commands": r"subprocess|os\.system|os\.popen|exec\(|eval\(|child_process|spawn\(|Popen",
    "writes/deletes": (
        r"open\([^)]*['\"][wa]|write_text|write_bytes|unlink|rmtree|os\.remove|rm -rf"
        r"|shutil\.move"
    ),
}
INSTALL = (
    r"^\s*(export |source |curl .*\|\s*(ba|z)?sh|wget .*\|\s*(ba|z)?sh|sudo |npx |pip3? install"
    r"|npm (i|install) |brew install|uv (pip|tool) install|chmod \+x)"
)
OUTSIDE = (
    r"page|DOM|snapshot|ticket|issue|comment|email|inbox|web|URL|fetch|download|Figma|PDF|upload"
)
DATA_RULE = (
    r"data, not instructions|not as instructions|never follow (directives|instructions)"
    r"|untrusted (page|content|text|input)"
)


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            if k and not k.startswith(" ") and v.strip():
                out[k.strip()] = v.strip()
    return out


print(f"# Inventory: {ROOT.name}\n")
try:
    sha = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    url = subprocess.run(
        ["git", "-C", str(ROOT), "remote", "get-url", "origin"], capture_output=True, text=True
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain"], capture_output=True, text=True
    ).stdout.strip()
    print(f"- Source: {url or 'no git remote'}")
    print(
        f"- Commit: {sha or 'not a git checkout'}{' (with uncommitted changes)' if dirty else ''}"
    )
except FileNotFoundError:
    print("- Commit: git not available")

versions = []
for name in (".claude-plugin/plugin.json", "plugin.json", ".claude-plugin/marketplace.json"):
    f = ROOT / name
    if f.exists():
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError:
            print(f"- {name}: not valid JSON")
            continue
        if "version" in data:
            versions.append((name, data["version"]))
        for entry in data.get("plugins", []):
            if "version" in entry:
                versions.append((f"{name} → {entry.get('name')}", entry["version"]))
for where, v in versions:
    print(f"- Version in {where}: {v}")
if len({v for _, v in versions}) > 1:
    print("- **The version labels disagree.** Pin the commit, not the label.")

print("\n## Runs on its own (no one asks)\n")
auto = []
for name in ("hooks/hooks.json", ".mcp.json", ".lsp.json", "monitors.json"):
    if (ROOT / name).exists():
        auto.append(name)
if (ROOT / "bin").is_dir():
    auto += [rel(p) for p in sorted((ROOT / "bin").iterdir())]
for name in (".claude-plugin/plugin.json", "plugin.json"):
    f = ROOT / name
    if f.exists():
        try:
            data = json.loads(f.read_text())
            for key in ("hooks", "mcpServers", "lspServers", "monitors"):
                if key in data:
                    auto.append(f"{name}: {key}")
        except json.JSONDecodeError:
            pass
for skill in sorted(ROOT.rglob("SKILL.md")):
    if "hooks" in frontmatter(skill.read_text(errors="replace")):
        auto.append(f"{rel(skill)}: frontmatter hooks")
print(
    "\n".join(f"- {a}" for a in auto)
    if auto
    else "- None found: no hooks, MCP or LSP servers, monitors or bin/."
)

print("\n## Skills\n")
print(
    "| skill | pre-approved tools (allowed-tools) | other settings | mentions outside text "
    "| says outside text is data (body) |"
)
print("|---|---|---|---|---|")
skills = sorted(ROOT.rglob("SKILL.md"))
for skill in skills:
    text = skill.read_text(errors="replace")
    fm = frontmatter(text)
    other = ", ".join(
        f"{k}: {fm[k]}"
        for k in ("disable-model-invocation", "model", "context", "agent")
        if k in fm
    )
    reads = "yes" if re.search(OUTSIDE, text) else "no"
    body = text.split("\n---\n", 1)[-1]
    offset = text.count("\n", 0, len(text) - len(body))
    rule = [
        i + offset
        for i, line in enumerate(body.splitlines(), 1)
        if re.search(DATA_RULE, line, re.I)
    ]
    rule_s = f"yes (line {rule[0]})" if rule else "no"
    print(
        f"| {skill.parent.name} | {fm.get('allowed-tools', '—')} | {other or '—'} "
        f"| {reads} | {rule_s} |"
    )

print("\n## Bundled code\n")
code = [
    p
    for p in sorted(ROOT.rglob("*"))
    if p.is_file()
    and ".git" not in p.parts
    and p.suffix in TEXT
    and p.name not in ("LICENSE",)
    and not p.name.startswith(".")
]
if not code:
    print("- No scripts.")
for p in code:
    lines = p.read_text(errors="replace").splitlines()
    hits = {
        k: [i for i, line in enumerate(lines, 1) if re.search(rx, line)]
        for k, rx in PATTERNS.items()
    }
    hits = {k: v for k, v in hits.items() if v}
    print(f"- `{rel(p)}` ({len(lines)} lines)")
    for k, v in hits.items():
        shown = ", ".join(str(n) for n in v[:12]) + (" …" if len(v) > 12 else "")
        print(f"  - {k}: lines {shown}")
    hosts = sorted(set(re.findall(r"https?://([A-Za-z0-9.-]+)", "\n".join(lines))))
    if hosts:
        print(f"  - hosts named: {', '.join(hosts)}")

print("\n## Commands the docs ask you to run\n")
docs = [p for p in sorted(ROOT.rglob("*.md")) if p.name != "SKILL.md" and ".git" not in p.parts]
found = False
for p in docs:
    for i, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
        if re.search(INSTALL, line):
            print(f"- `{rel(p)}:{i}`: `{line.strip()[:110]}`")
            found = True
if not found:
    print("- None found.")
