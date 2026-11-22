"""ask_coach: the one path every coach answer takes (claims check + trace log)."""

import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from nightjar.claims import Violation, check_text
from nightjar.coach.base import (
    Coach,
    CoachError,
    build_user_message,
    load_system_prompt,
    prompt_version,
)
from nightjar.models import Night

log = logging.getLogger(__name__)

DEFAULT_TRACE_PATH = Path(os.environ.get("NIGHTJAR_TRACE_PATH", "traces/coach.jsonl"))
SAFE_FALLBACK = (
    "I can help with winding down and building a consistent bedtime routine, but I can't "
    "help with that question. If you have symptoms like chest pain or breathing that stops "
    "at night, please seek medical care."
)


@dataclass
class CoachAnswer:
    text: str  # what the user sees
    raw_text: str  # what the model said, before the claims check
    violations: list[Violation] = field(default_factory=list)
    used_fallback: bool = False


def ask_coach(
    coach: Coach, nights: list[Night], question: str, trace_path: Path = DEFAULT_TRACE_PATH
) -> CoachAnswer:
    system_prompt = load_system_prompt()
    user_message = build_user_message(nights, question)

    started = time.perf_counter()
    error = None
    try:
        raw_text = coach.reply(system_prompt, user_message)
    except CoachError as exc:
        raw_text, error = "", str(exc)
    latency_ms = round((time.perf_counter() - started) * 1000)

    violations = check_text(raw_text)
    if violations:
        log.warning("Coach output broke the claims register: %s", [v.rule for v in violations])
    used_fallback = bool(violations or error or not raw_text.strip())
    answer = CoachAnswer(
        text=SAFE_FALLBACK if used_fallback else raw_text,
        raw_text=raw_text,
        violations=violations,
        used_fallback=used_fallback,
    )

    write_trace(
        trace_path,
        {
            "timestamp": datetime.now(UTC).isoformat(),
            "model": coach.model,
            "prompt_version": prompt_version(system_prompt),
            "input": {"question": question, "user_message": user_message},
            "output": raw_text,
            "shown_to_user": answer.text,
            "latency_ms": latency_ms,
            "claims_violations": [{"rule": v.rule, "matched": v.matched} for v in violations],
            "error": error,
        },
    )
    return answer


def write_trace(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as trace_file:
        trace_file.write(json.dumps(record) + "\n")
