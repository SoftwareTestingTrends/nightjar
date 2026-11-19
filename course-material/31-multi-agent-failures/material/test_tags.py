from nightjar.tags import note_tags


def test_note_tags_lists_the_habits_in_a_note():
    tags = note_tags("Herbal tea and a long walk along the river.")
    assert ", ".join(tags) == "tea, walk"
