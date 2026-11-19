"""Journal tags: which wind-down habits a note mentions."""

HABITS = ("tea", "walk", "shower", "journal", "reading")


def note_tags(notes: str) -> set[str]:
    text = notes.lower()
    return {habit for habit in HABITS if habit in text}
