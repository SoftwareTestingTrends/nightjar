from datetime import time

import pytest
from builders import nights_at

from nightjar.sleep_window import (
    minutes_since_noon,
    time_from_minutes_since_noon,
    usual_bedtime,
)


@pytest.mark.parametrize(
    ("clock", "expected"),
    [
        (time(12, 0), 0),
        (time(23, 30), 690),
        (time(0, 0), 720),
        (time(0, 30), 750),
        (time(11, 59), 1439),
    ],
)
def test_minutes_since_noon(clock, expected):
    assert minutes_since_noon(clock) == expected


def test_23_30_and_00_30_are_one_hour_apart():
    assert minutes_since_noon(time(0, 30)) - minutes_since_noon(time(23, 30)) == 60


@pytest.mark.parametrize("clock", [time(0, 0), time(12, 0), time(23, 59), time(6, 5)])
def test_minutes_round_trip(clock):
    assert time_from_minutes_since_noon(minutes_since_noon(clock)) == clock


def test_time_from_minutes_wraps_past_a_full_day():
    assert time_from_minutes_since_noon(1440) == time(12, 0)


def test_median_of_an_even_count_rounds_to_a_whole_minute():
    # 8 nights: median of 22:00 x4 and 22:01 x4 is 22:00.5 -> rounds to an even minute.
    nights = nights_at("22:00", 4) + nights_at("22:01", 4, first_night="2026-03-05")
    assert usual_bedtime(nights) == time(22, 0)


def test_six_nights_is_cold_start_but_seven_is_not():
    assert usual_bedtime(nights_at("23:00", 6)) is None
    assert usual_bedtime(nights_at("23:00", 7)) == time(23, 0)


def test_input_order_does_not_matter():
    nights = nights_at("23:00", 5) + nights_at("23:20", 5, first_night="2026-03-06")
    assert usual_bedtime(nights) == usual_bedtime(list(reversed(nights)))
