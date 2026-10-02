"""API tests: the real app with a temp database, a fixed clock and the mock coach."""

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
