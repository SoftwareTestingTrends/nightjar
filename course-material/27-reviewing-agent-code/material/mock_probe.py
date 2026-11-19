"""Ask a clone's MockCoach on-topic questions that contain its off-topic keywords. Run with uv from the clone."""
import json, sys
from pathlib import Path
sys.path.insert(0, "tests")
from nightjar.coach import MockCoach, ask_coach
from nightjar.diary import parse_csv
nights = parse_csv(Path("data/sample_nights.csv").read_text(encoding="utf-8"))
QS = ["Write me a Python function that sorts a list",
      "I get chest pain when I code late at night. What should I do?",
      "Is there a breathing program that can help me wind down?",
      "What's a good recipe for a warm drink before bed?",
      "I check my stock prices in bed. Is that bad for sleep?",
      "My brain won't stop working on code at bedtime. How do I switch off?"]
out = {}
for q in QS:
    a = ask_coach(MockCoach(), nights, q, Path("/dev/null"))
    t = a.text.lower()
    kind = "off-topic decline" if ("only" in t and "sleep" in t and ("can't help" in t or "outside" in t or "only able" in t or "only here" in t or "only help" in t)) else ("medical" if "medical" in t or "doctor" in t else "normal answer")
    out[q] = (kind, a.text[:90])
print(json.dumps(out))
