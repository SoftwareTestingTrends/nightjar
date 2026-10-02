"""ClaudeCoach: answers with Claude via the official Anthropic SDK (Messages API)."""

import os

import anthropic

from nightjar.coach.base import CoachError

DEFAULT_MODEL = "claude-sonnet-5-5"
MAX_TOKENS = 1024  # coach answers are short by design


class ClaudeCoach:
    def __init__(self, model: str | None = None, client: anthropic.Anthropic | None = None):
        self.model = model or os.environ.get("NIGHTJAR_COACH_MODEL", DEFAULT_MODEL)
        self._client = client or anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

    def reply(self, system_prompt: str, user_message: str) -> str:
        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
        except anthropic.APIError as error:
            raise CoachError(f"Claude API error: {error}") from error
        if response.stop_reason == "refusal":
            raise CoachError("Claude declined to answer")
        return "".join(block.text for block in response.content if block.type == "text")
