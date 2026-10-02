"""The claims register: what NightJar may and may not say to users.

NightJar is a wellness product. Copy shown to users (nudges, coach answers)
must not make disease claims. The register is owned by Regulatory & Brand.
"""

import re
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import yaml

REGISTER_PATH = Path(__file__).resolve().parents[2] / "claims" / "register.yaml"


@dataclass(frozen=True)
class Violation:
    rule: str  # id of the banned pattern, e.g. "disease-insomnia"
    matched: str  # the text that matched
    reason: str


@cache
def load_register(path: Path = REGISTER_PATH) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def check_text(text: str) -> list[Violation]:
    """Every banned claim found in `text` (case-insensitive). Empty list means clean."""
    violations = []
    for rule in load_register()["banned"]:
        for match in re.finditer(rule["pattern"], text, flags=re.IGNORECASE):
            violations.append(Violation(rule["id"], match.group(0), rule["reason"]))
    return violations
