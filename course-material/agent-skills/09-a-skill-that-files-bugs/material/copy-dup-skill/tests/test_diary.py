from datetime import UTC, datetime, timedelta

import pytest
from builders import LONDON, night

from nightjar.diary import Diary, local_input_to_aware, parse_csv
from nightjar.models import Night


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
