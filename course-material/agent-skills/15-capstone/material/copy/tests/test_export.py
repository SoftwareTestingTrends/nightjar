"""S-117: export the diary as CSV."""

import csv
import io
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from nightjar.coach import MockCoach
from nightjar.diary import Diary
from nightjar.web import create_app

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


def log_night(client, notes="", bedtime="2026-03-18T23:00", wake_time="2026-03-19T07:00"):
    client.post(
        "/nights",
        data={
            "bedtime": bedtime,
            "wake_time": wake_time,
            "timezone": "America/Toronto",
            "notes": notes,
        },
    )


def test_export_downloads_a_dated_file_with_the_import_columns(client):
    log_night(client)
    response = client.get("/export")
    assert response.status_code == 200
    disposition = response.headers["content-disposition"]
    assert disposition == 'attachment; filename="nightjar-diary-2026-03-20.csv"'
    rows = list(csv.reader(io.StringIO(response.text)))
    assert rows[0] == ["bedtime", "wake_time", "timezone", "notes"]
    assert len(rows) == 2


def test_notes_with_commas_and_quotes_survive(client):
    log_night(client, notes='Woke at 3, "rested"')
    rows = list(csv.reader(io.StringIO(client.get("/export").text)))
    assert rows[1][3] == 'Woke at 3, "rested"'


def test_empty_diary_exports_the_header_only(client):
    assert client.get("/export").text == "bedtime,wake_time,timezone,notes\n"


def test_times_use_each_nights_own_offset(client):
    log_night(client, bedtime="2026-03-01T00:25", wake_time="2026-03-01T07:30")
    rows = list(csv.reader(io.StringIO(client.get("/export").text)))
    assert rows[1][:2] == ["2026-03-01T00:25:00-05:00", "2026-03-01T07:30:00-05:00"]


def test_nights_are_oldest_first(client):
    log_night(client, bedtime="2026-03-10T23:00", wake_time="2026-03-11T07:00", notes="second")
    log_night(client, bedtime="2026-03-09T23:00", wake_time="2026-03-10T07:00", notes="first")
    log_night(client, bedtime="2026-03-11T23:00", wake_time="2026-03-12T07:00", notes="third")
    rows = list(csv.reader(io.StringIO(client.get("/export").text)))
    assert [row[3] for row in rows[1:]] == ["first", "second", "third"]
