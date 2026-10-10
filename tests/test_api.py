"""API tests: the real app with a temp database, a fixed clock and the mock coach."""

import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

SAMPLE_CSV = Path(__file__).parents[1] / "data" / "sample_nights.csv"
NOON_IN_TORONTO = datetime(2026, 3, 20, 12, 0, tzinfo=ZoneInfo("America/Toronto"))


@pytest.fixture
def client(tmp_path):
    app = create_app(
        diary=Diary(tmp_path / "test.db"),
        coach=MockCoach(),
        clock=lambda: NOON_IN_TORONTO,
        trace_path=tmp_path / "coach.jsonl",
    )
    return TestClient(app)


def import_sample(client):
    with SAMPLE_CSV.open("rb") as csv_file:
        return client.post("/import", files={"file": ("nights.csv", csv_file, "text/csv")})


def test_empty_diary_shows_cold_start(client):
    page = client.get("/")
    assert page.status_code == 200
    assert 'data-testid="nudge-cold-start"' in page.text
    assert client.get("/api/nudge").json()["nudge"] is None


def test_T_114_1_import_csv_then_see_the_nudge(client):
    response = import_sample(client)
    assert response.status_code == 200  # followed the redirect
    assert "Imported 21 nights." in response.text
    assert 'Your next wind-down nudge: <strong data-testid="nudge-time">22:15</strong>' in (
        response.text
    )

    nudge = client.get("/api/nudge").json()["nudge"]
    assert nudge["local_time"] == "22:15"
    assert nudge["at"] == "2026-03-20T22:15:00-04:00"
    assert nudge["silent"] is False


def test_add_night_from_the_form(client):
    response = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-19T23:05",
            "wake_time": "2026-03-20T07:00",
            "timezone": "America/Toronto",
            "notes": "Quiet evening.",
        },
    )
    assert response.status_code == 200
    assert response.text.count('data-testid="diary-row"') == 1
    assert "Quiet evening." in response.text


def test_invalid_night_shows_an_error(client):
    response = client.post(
        "/nights",
        data={
            "bedtime": "2026-03-20T07:00",
            "wake_time": "2026-03-19T23:00",
            "timezone": "America/Toronto",
        },
    )
    assert response.status_code == 400
    assert "wake time must be after bedtime" in response.text


def test_bad_csv_shows_an_error(client):
    response = client.post("/import", files={"file": ("x.csv", b"hello,world\n", "text/csv")})
    assert response.status_code == 400
    assert "Import failed" in response.text


def test_T_114_2_changing_time_zone_moves_the_nudge(client):
    import_sample(client)
    client.post(
        "/settings",
        data={"timezone": "Europe/London", "quiet_start": "23:00", "quiet_end": "07:00"},
    )
    nudge = client.get("/api/nudge").json()["nudge"]
    assert nudge["at"] == "2026-03-20T22:15:00+00:00"  # 22:15 in London


def test_T_114_3_quiet_hours_setting_makes_nudge_silent(client):
    import_sample(client)
    client.post(
        "/settings",
        data={"timezone": "America/Toronto", "quiet_start": "22:00", "quiet_end": "07:00"},
    )
    assert client.get("/api/nudge").json()["nudge"]["silent"] is True
    assert 'data-testid="nudge-silent"' in client.get("/").text


def test_coach_chat_on_the_page(client):
    import_sample(client)
    response = client.post("/coach", data={"question": "How can I wind down tonight?"})
    assert 'data-testid="coach-answer"' in response.text
    assert "23:00" in response.text


def test_coach_json_api(client):
    response = client.post("/api/coach", json={"question": "I get chest pain at night"})
    assert response.status_code == 200
    assert "seek medical care" in response.json()["answer"]


# --- User-selectable wind-down lead ---
TORONTO_SETTINGS = {"timezone": "America/Toronto", "quiet_start": "23:00", "quiet_end": "07:00"}


def nudge_of(client):
    return client.get("/api/nudge").json()["nudge"]


def test_T_114_8_default_lead_is_45_and_reported_by_the_api(client):
    import_sample(client)
    assert nudge_of(client)["lead_minutes"] == 45


@pytest.mark.parametrize(
    ("lead", "local_time"), [("30", "22:30"), ("45", "22:15"), ("60", "22:00")]
)
def test_T_114_8_chosen_lead_is_saved_and_moves_the_nudge(client, lead, local_time):
    import_sample(client)
    response = client.post("/settings", data=TORONTO_SETTINGS | {"wind_down_lead": lead})
    assert response.status_code == 200  # followed the redirect
    nudge = nudge_of(client)
    assert nudge["lead_minutes"] == int(lead)
    assert nudge["local_time"] == local_time


def test_T_114_8_settings_form_shows_the_current_lead(client):
    client.post("/settings", data=TORONTO_SETTINGS | {"wind_down_lead": "60"})
    page = client.get("/").text
    assert 'data-testid="settings-lead"' in page
    assert re.search(r'<option(?=[^>]*value="60")(?=[^>]*\bselected\b)[^>]*>', page)
    assert not re.search(r'<option(?=[^>]*value="45")(?=[^>]*\bselected\b)[^>]*>', page)


@pytest.mark.parametrize("omitted", ["absent", "empty"])
def test_T_114_8_saving_other_settings_without_a_lead_keeps_the_saved_lead(client, omitted):
    import_sample(client)
    client.post("/settings", data=TORONTO_SETTINGS | {"wind_down_lead": "60"})
    other = {"timezone": "Europe/London", "quiet_start": "23:00", "quiet_end": "07:00"}
    if omitted == "empty":
        other["wind_down_lead"] = ""
    client.post("/settings", data=other)
    nudge = nudge_of(client)
    assert nudge["lead_minutes"] == 60
    assert nudge["at"] == "2026-03-20T22:00:00+00:00"  # 22:00 in London


@pytest.mark.parametrize("bad", ["abc", "50"])
def test_T_114_8_invalid_lead_is_rejected_and_nothing_is_saved(client, bad):
    import_sample(client)
    client.post("/settings", data=TORONTO_SETTINGS | {"wind_down_lead": "60"})
    response = client.post(
        "/settings",
        data={"timezone": "Europe/London", "quiet_start": "21:00", "quiet_end": "06:00"}
        | {"wind_down_lead": bad},
    )
    assert response.status_code == 400
    nudge = nudge_of(client)  # still the previous settings: Toronto, 60 minutes
    assert nudge["lead_minutes"] == 60
    assert nudge["at"] == "2026-03-20T22:00:00-04:00"
    assert 'name="quiet_start" value="23:00"' in client.get("/").text
