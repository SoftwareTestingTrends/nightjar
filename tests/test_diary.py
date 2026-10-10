import sqlite3
from dataclasses import replace
from datetime import UTC, datetime, time, timedelta

import pytest
from builders import LONDON, night

from nightjar.diary import Diary, local_input_to_aware, parse_csv
from nightjar.models import Night, User


def test_nights_round_trip_through_sqlite_with_their_time_zone(tmp_path):
    diary = Diary(tmp_path / "test.db")
    london_night = night("2026-03-12", "23:30", tz=LONDON, notes="Hotel room was warm.")
    diary.add_night(london_night)

    [stored] = diary.nights()
    assert stored.bedtime == london_night.bedtime  # same instant
    assert stored.local_bedtime.strftime("%H:%M") == "23:30"
    assert stored.timezone == LONDON
    assert stored.notes == "Hotel room was warm."


def test_nights_come_back_newest_first_even_across_zones(tmp_path):
    diary = Diary(tmp_path / "test.db")
    diary.add_nights(
        [
            night("2026-03-01", "23:00"),
            night("2026-03-03", "22:00", tz=LONDON),
            night("2026-03-02", "23:00"),
        ]
    )
    assert [n.local_bedtime.day for n in diary.nights()] == [3, 2, 1]


def test_sample_csv_imports_21_nights(sample_nights):
    assert len(sample_nights) == 21
    assert {n.timezone for n in sample_nights} == {"America/Toronto", "Europe/London"}


def test_csv_without_utc_offset_is_rejected():
    csv_text = (
        "bedtime,wake_time,timezone,notes\n2026-03-01T23:00,2026-03-02T07:00,America/Toronto,\n"
    )
    with pytest.raises(ValueError, match="Line 2: .*no UTC offset"):
        parse_csv(csv_text)


def test_csv_missing_columns_is_rejected():
    with pytest.raises(ValueError, match="missing columns: notes, timezone"):
        parse_csv("bedtime,wake_time\n")


def test_night_duration_is_correct_across_spring_forward():
    # 00:15 EST -> 08:20 EDT on 8 March 2026 is 7h05m of sleep, not 8h05m.
    sleep = Night(
        bedtime=local_input_to_aware("2026-03-08T00:15", "America/Toronto"),
        wake_time=local_input_to_aware("2026-03-08T08:20", "America/Toronto"),
        timezone="America/Toronto",
    )
    assert sleep.duration == timedelta(hours=7, minutes=5)


@pytest.mark.parametrize(
    "bad",
    [
        {"wake_time": datetime(2026, 3, 1, 22, tzinfo=UTC)},  # wakes before bed
        {"wake_time": datetime(2026, 3, 2, 17, tzinfo=UTC)},  # 18 hours
        {"timezone": "Mars/Olympus_Mons"},
        {"bedtime": datetime(2026, 3, 1, 23)},  # noqa: DTZ001 - naive on purpose
    ],
)
def test_invalid_nights_are_rejected(bad):
    fields = {
        "bedtime": datetime(2026, 3, 1, 23, tzinfo=UTC),
        "wake_time": datetime(2026, 3, 2, 7, tzinfo=UTC),
        "timezone": "UTC",
    } | bad
    with pytest.raises(ValueError):
        Night(**fields)


def test_night_of_is_the_evening_the_night_began():
    after_midnight = night("2026-03-07", "00:15")  # bedtime is early Sunday 8 March
    assert after_midnight.local_bedtime.day == 8
    assert after_midnight.night_of.isoformat() == "2026-03-07"


OLD_USER_SETTINGS_TABLE = """
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT NOT NULL,
    timezone TEXT NOT NULL,
    quiet_start TEXT,
    quiet_end TEXT
);
"""


def make_old_schema_database(path):
    """A database as an earlier NightJar version left it: no wind-down lead column."""
    db = sqlite3.connect(path)
    db.executescript(OLD_USER_SETTINGS_TABLE)
    db.execute("INSERT INTO user_settings VALUES (1, 'Sam', 'Europe/London', '22:00', '06:00')")
    db.commit()
    db.close()


def test_T_114_9_a_database_from_the_old_schema_migrates_and_reads_as_45(tmp_path):
    path = tmp_path / "old.db"
    make_old_schema_database(path)

    user = Diary(path).user()
    assert user.wind_down_lead_minutes == 45
    assert (user.timezone, user.quiet_start, user.quiet_end) == (
        LONDON,
        time(22, 0),
        time(6, 0),
    )


def test_T_114_9_a_migrated_database_saves_and_keeps_a_chosen_lead(tmp_path):
    path = tmp_path / "old.db"
    make_old_schema_database(path)
    diary = Diary(path)
    diary.save_user(replace(diary.user(), wind_down_lead_minutes=60))

    reopened = Diary(path)  # opening again must not fail on the already-added column
    assert reopened.user().wind_down_lead_minutes == 60
    assert reopened.user().timezone == LONDON


def test_T_114_9_a_new_database_persists_the_lead_across_restarts(tmp_path):
    path = tmp_path / "new.db"
    assert Diary(path).user().wind_down_lead_minutes == 45
    Diary(path).save_user(User(name="Sam", timezone=LONDON, wind_down_lead_minutes=30))
    assert Diary(path).user().wind_down_lead_minutes == 30
