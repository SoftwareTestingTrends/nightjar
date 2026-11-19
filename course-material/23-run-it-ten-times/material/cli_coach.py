"""A NightJar coach that calls the real model through the Claude Code CLI (no API key needed).
No tools, no project settings: the model only sees NightJar's system prompt and user message."""
import json, subprocess
class CliCoach:
    model = "claude-sonnet-5-5 (via claude -p)"
    def reply(self, system_prompt: str, user_message: str) -> str:
        r = subprocess.run(["claude","-p",user_message,"--system-prompt",system_prompt,"--model","claude-sonnet-5-5",
                            "--tools","","--setting-sources","","--output-format","json"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
        return json.loads(r.stdout)["result"]
