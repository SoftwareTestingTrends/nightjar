"""The AI sleep coach. Pick a backend with NIGHTJAR_COACH=mock|claude."""

import os

from nightjar.coach.base import Coach, CoachError
from nightjar.coach.mock import MockCoach
from nightjar.coach.service import CoachAnswer, ask_coach

__all__ = ["Coach", "CoachAnswer", "CoachError", "MockCoach", "ask_coach", "get_coach"]


def get_coach() -> Coach:
    """Claude when NIGHTJAR_COACH=claude (or a key is set and no choice is made), else mock."""
    choice = os.environ.get("NIGHTJAR_COACH")
    if choice is None:
        choice = "claude" if os.environ.get("ANTHROPIC_API_KEY") else "mock"
    if choice == "claude":
        from nightjar.coach.claude import ClaudeCoach

        return ClaudeCoach()
    return MockCoach()
