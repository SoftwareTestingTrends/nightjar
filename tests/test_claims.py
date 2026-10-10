import re
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from nightjar.claims import check_text
from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app


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


def test_settings_lead_label_and_options_are_claims_clean(tmp_path):
    app = create_app(
        diary=Diary(tmp_path / "test.db"),
        coach=MockCoach(),
        clock=lambda: datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto")),
        trace_path=tmp_path / "coach.jsonl",
    )
    page = TestClient(app).get("/").text

    field = re.search(
        r'<label>([^<]*)<select[^>]*data-testid="settings-lead"[^>]*>(.*?)</select>',
        page,
        re.DOTALL,
    )
    assert field, "no <label>...<select data-testid='settings-lead'> on the page"
    label = field.group(1).strip()
    options = [
        text.strip() for text in re.findall(r"<option[^>]*>([^<]*)</option>", field.group(2))
    ]

    assert label == "Wind down before bedtime"
    assert options == ["30 minutes", "45 minutes", "60 minutes"]
    for text in [label, *options]:
        assert check_text(text) == []
        assert "recommend" not in text.lower()  # no option is presented as better for sleep
