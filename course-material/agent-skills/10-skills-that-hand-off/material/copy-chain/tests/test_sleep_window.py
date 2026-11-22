from datetime import time

from builders import LONDON, night, nights_at

from nightjar.sleep_window import usual_bedtime


def test_usual_bedtime_is_the_median_local_bedtime():
    nights = [
        night(f"2026-03-0{i}", t)
        for i, t in enumerate(
            ["22:30", "22:45", "23:00", "23:10", "23:20", "23:30", "23:50"], start=1
        )
    ]
    assert usual_bedtime(nights) == time(23, 10)


def test_bedtimes_either_side_of_midnight_are_close_together():
    # 23:30 and 00:30 are one hour apart; the middle is midnight, not noon.
    nights = nights_at("23:30", 4) + nights_at("00:30", 4, first_night="2026-03-05")
    assert usual_bedtime(nights) == time(0, 0)


def test_median_of_mostly_after_midnight_bedtimes():
    nights = nights_at("23:50", 3) + nights_at("00:40", 4, first_night="2026-03-04")
    assert usual_bedtime(nights) == time(0, 40)


def test_T_114_5_cold_start_with_fewer_than_7_nights_returns_none():
    assert usual_bedtime(nights_at("23:00", 6)) is None
    assert usual_bedtime([]) is None


def test_exactly_7_nights_is_enough():
    assert usual_bedtime(nights_at("23:00", 7)) == time(23, 0)


def test_only_the_last_14_nights_count():
    old_late_nights = nights_at("02:00", 10, first_night="2026-01-01")
    recent = nights_at("22:30", 14, first_night="2026-02-01")
    assert usual_bedtime(old_late_nights + recent) == time(22, 30)


def test_bedtimes_are_read_in_the_zone_the_user_was_in_that_night():
    # 23:00 in London is 18:00 in Toronto; it must still count as 23:00.
    nights = nights_at("23:00", 4) + nights_at("23:00", 4, first_night="2026-03-10", tz=LONDON)
    assert usual_bedtime(nights) == time(23, 0)


def test_sample_data_usual_bedtime(sample_nights):
    assert usual_bedtime(sample_nights) == time(23, 0)
