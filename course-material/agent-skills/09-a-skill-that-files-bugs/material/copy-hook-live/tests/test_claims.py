import pytest

from nightjar.claims import check_text


@pytest.mark.parametrize(
    "text",
    [
        "This routine will cure your insomnia.",
        "You might have sleep apnea.",
        "Magnesium can treat poor sleep.",
        "I can't diagnose you, but...",
        "That sounds like an anxiety disorder.",
        "Ask your doctor to prescribe something.",
        "Our method is clinically proven.",
    ],
)
def test_banned_claims_are_flagged(text):
    assert check_text(text), f"expected a violation in: {text!r}"


@pytest.mark.parametrize(
    "text",
    [
        "Time to wind down. Your usual bedtime is 23:00.",
        "Try to relax and build a consistent bedtime routine.",
        "A weekend retreat by the sea sounds lovely.",  # 'retreat' is not 'treat'
        "Secure your phone in another room.",  # 'secure' is not 'cure'
        "If your breathing stops at night, please seek medical care.",
    ],
)
def test_wellness_copy_is_clean(text):
    assert check_text(text) == []


def test_check_is_case_insensitive_and_reports_each_match():
    violations = check_text("INSOMNIA? We Cure insomnia.")
    assert [v.rule for v in violations] == ["disease-insomnia", "disease-insomnia", "claim-cure"]
    assert {v.matched for v in violations} == {"INSOMNIA", "insomnia", "Cure"}
