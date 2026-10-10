"""MockCoach: deterministic canned answers, so tests and demos run offline."""

import re

from nightjar.coach.base import QUESTION_HEADING

URGENT_WORDS = ("breathing", "breathe", "chest pain", "gasping", "choking", "faint")
MEDICAL_WORDS = (
    "insomnia",
    "apnea",
    "disorder",
    "diagnos",
    "do i have",
    "cure",
    "medication",
    "pill",
    "supplement",
    "melatonin",
)
ROUTINE_WORDS = ("wind down", "relax", "routine", "tonight", "bedtime", "fall asleep")

SEEK_CARE = (
    "That's something a doctor should look at, and I can't tell you what's causing it. "
    "If your breathing stops at night or you have chest pain, please seek medical care, "
    "and call emergency services if it feels severe. When you're ready, I'm happy to help "
    "with a calm wind-down routine."
)
NOT_MEDICAL = (
    "I can't answer medical questions or recommend medicines or supplements; a doctor or "
    "pharmacist is the right person for that. What I can help with is a calm evening and "
    "a consistent bedtime routine. Want some ideas?"
)


class MockCoach:
    model = "mock-coach-v1"

    def reply(self, system_prompt: str, user_message: str) -> str:
        question = user_message.rsplit(QUESTION_HEADING, 1)[-1].lower()
        bedtime = _find(r"Usual bedtime: (\d\d:\d\d)", user_message)
        if any(word in question for word in URGENT_WORDS):
            return SEEK_CARE
        if any(word in question for word in MEDICAL_WORDS):
            return NOT_MEDICAL
        if any(word in question for word in ROUTINE_WORDS):
            return (
                f"Your usual bedtime is around {bedtime or 'the same time each night'}. "
                "A little before bedtime, start to wind down: dim the lights, put your phone "
                "in another room, and do something slow like reading or a warm shower. "
                "Doing the same steps each night helps you build a consistent bedtime routine."
            )
        hours = _find(r"Average sleep over the last \d+ nights: ([\d.]+) hours", user_message)
        return (
            f"Looking at your diary, your usual bedtime is around {bedtime or 'not clear yet'} "
            f"and you've been sleeping about {hours or 'an unknown number of'} hours a night. "
            "Keeping a regular sleep schedule, even on weekends, is a great way to relax "
            "into the evening."
        )


def _find(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text)
    return match.group(1) if match else None
