"""Story S-116: weekly sleep summary. Test ids (T-116-n) are listed in docs/traceability.md.

Written before the code. Assumed interface (adjust the names below if the
implementation differs; the behaviour under test is what matters):

    nightjar.summary.weekly_summary(user, nights, now) -> WeeklySummary
        .nights_logged: int
        .average_asleep: timedelta | None   (already rounded to 5 min)
        .usual_bedtime: time | None
        .text: str                          (all user-facing wording)
    nightjar.summary.format_duration(timedelta) -> str   e.g. "7 h 25 min"

The whole module is skipped until nightjar.summary exists.
"""

from datetime import UTC, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest
from builders import LONDON, TORONTO, night

from nightjar.claims import check_text
from nightjar.models import Night, User

summary_module = pytest.importorskip("nightjar.summary")
weekly_summary = summary_module.weekly_summary
format_duration = summary_module.format_duration

TORONTO_TZ = ZoneInfo(TORONTO)
TOO_FEW = "Log at least 3 nights this week to see your summary."
NOW = datetime(2026, 3, 20, 12, 0, tzinfo=TORONTO_TZ)  # window: nights of 13..19 March


def toronto_user() -> User:
    return User(name="Sam", timezone=TORONTO)


def slept(night_of: str, bedtime: str, minutes: int, tz: str = TORONTO) -> Night:
    """A night of `minutes` (wall-clock addition: only use away from DST changes)."""
    start = night(night_of, bedtime, tz).bedtime
    return Night(bedtime=start, wake_time=start + timedelta(minutes=minutes), timezone=tz)


def local_night(bed: datetime, wake: datetime) -> Night:
    """A night from two aware local datetimes; Night.duration converts to UTC."""
    return Night(bedtime=bed, wake_time=wake, timezone=TORONTO)


def three_nights(*durations: tuple[int, int], bedtime: str = "23:00") -> list[Night]:
    days = ["2026-03-15", "2026-03-16", "2026-03-17"]
    return [
        slept(day, bedtime, hours * 60 + minutes)
        for day, (hours, minutes) in zip(days, durations, strict=False)
    ]


# AC1: the window is the seven "night of" dates before today
def test_T_116_1_window_is_seven_nights_ending_last_night():
    nights = [slept(f"2026-03-{d}", "23:00", 480) for d in range(13, 20)]  # 13..19
    assert weekly_summary(toronto_user(), nights, NOW).nights_logged == 7


def test_T_116_1_night_of_seven_days_ago_is_in_and_eight_days_ago_is_out():
    nights = [slept(f"2026-03-{d}", "23:00", 480) for d in (12, 13, 14, 15)]
    assert weekly_summary(toronto_user(), nights, NOW).nights_logged == 3


def test_T_116_1_tonights_night_of_today_is_not_in_the_window():
    nights = [*three_nights((8, 0), (8, 0), (8, 0)), slept("2026-03-20", "11:00", 60)]
    assert weekly_summary(toronto_user(), nights, NOW).nights_logged == 3


def test_T_116_1_after_midnight_bedtime_counts_for_the_night_before():
    # 00:15 on 20 March is the night of the 19th: last night, so inside the window.
    nights = [slept("2026-03-19", "00:15", 480), *three_nights((8, 0), (8, 0))]
    assert weekly_summary(toronto_user(), nights, NOW).nights_logged == 3


def test_T_116_1_after_midnight_bedtime_is_judged_by_its_night_of_date():
    # Bedtime 00:15 on the 13th belongs to the night of the 12th: outside the window,
    # even though the 13th is inside it.
    nights = [slept("2026-03-12", "00:15", 480), *three_nights((8, 0), (8, 0))]
    assert weekly_summary(toronto_user(), nights, NOW).nights_logged == 2


def test_T_116_1_today_follows_the_users_current_time_zone():
    # 22:00 on 20 March in Toronto, but already 02:00 on the 21st in London.
    now = datetime(2026, 3, 21, 2, 0, tzinfo=UTC)
    nights = [slept(f"2026-03-{d}", "23:00", 480) for d in (14, 15, 20)]
    london_user = User(name="Sam", timezone=LONDON)
    assert weekly_summary(toronto_user(), nights, now).nights_logged == 2  # window 13..19
    assert weekly_summary(london_user, nights, now).nights_logged == 3  # window 14..20


def test_T_116_1_window_is_by_calendar_date_not_168_hours():
    now = datetime(2026, 3, 20, 0, 30, tzinfo=TORONTO_TZ)  # 00:30: still nights of 13..19
    nights = [slept(f"2026-03-{d}", "23:00", 480) for d in (13, 14, 19)]
    assert weekly_summary(toronto_user(), nights, now).nights_logged == 3


# AC2: shows nights logged, average time asleep, usual bedtime
def test_T_116_2_summary_reports_count_average_and_usual_bedtime():
    result = weekly_summary(toronto_user(), three_nights((8, 0), (7, 0), (6, 0)), NOW)
    assert result.nights_logged == 3
    assert result.average_asleep == timedelta(hours=7)
    assert result.usual_bedtime == time(23, 0)
    assert "3" in result.text
    assert "7 h 0 min" in result.text
    assert "23:00" in result.text


def test_T_116_2_input_order_does_not_matter():
    nights = three_nights((8, 0), (7, 0), (6, 0))
    forward = weekly_summary(toronto_user(), nights, NOW)
    assert weekly_summary(toronto_user(), nights[::-1], NOW) == forward


# AC3: mean duration, rounded to the nearest 5 minutes, "7 h 25 min"
def test_T_116_3_average_is_the_mean_of_durations():
    result = weekly_summary(toronto_user(), three_nights((7, 0), (7, 30), (7, 45)), NOW)
    assert result.average_asleep == timedelta(hours=7, minutes=25)  # 22 h 15 min / 3
    assert "7 h 25 min" in result.text


def test_T_116_3_rounds_up_to_the_nearest_five_minutes():
    result = weekly_summary(toronto_user(), three_nights((7, 0), (7, 0), (7, 8)), NOW)
    assert result.average_asleep == timedelta(hours=7, minutes=5)  # mean 7:02:40


def test_T_116_3_rounds_down_to_the_nearest_five_minutes():
    result = weekly_summary(toronto_user(), three_nights((7, 0), (7, 0), (7, 6)), NOW)
    assert result.average_asleep == timedelta(hours=7)  # mean 7:02:00


def test_T_116_3_rounding_carries_into_the_next_hour():
    result = weekly_summary(toronto_user(), three_nights((7, 58), (7, 58), (7, 58)), NOW)
    assert result.average_asleep == timedelta(hours=8)


@pytest.mark.parametrize(
    ("duration", "expected"),
    [
        (timedelta(hours=7, minutes=25), "7 h 25 min"),
        (timedelta(hours=8), "8 h 0 min"),
        (timedelta(minutes=45), "0 h 45 min"),
    ],
)
def test_T_116_3_duration_format(duration, expected):
    assert format_duration(duration) == expected


# AC4: usual bedtime is the median local bedtime, each night in its own zone
def test_T_116_4_median_not_mean_of_bedtimes():
    bedtimes = ["22:00", "22:10", "22:20", "22:30", "01:00"]  # the mean would be ~23:12
    nights = [
        slept(f"2026-03-{day}", bed, 480) for day, bed in zip(range(14, 19), bedtimes, strict=True)
    ]
    assert weekly_summary(toronto_user(), nights, NOW).usual_bedtime == time(22, 20)


def test_T_116_4_bedtimes_either_side_of_midnight_sit_on_one_line():
    bedtimes = ["23:30", "23:45", "00:15", "00:30", "23:00"]
    nights = [
        slept(f"2026-03-{day}", bed, 480) for day, bed in zip(range(14, 19), bedtimes, strict=True)
    ]
    # Ordered from noon: 23:00, 23:30, 23:45, 00:15, 00:30 -> median 23:45.
    assert weekly_summary(toronto_user(), nights, NOW).usual_bedtime == time(23, 45)


def test_T_116_4_23_30_and_00_30_are_one_hour_apart():
    bedtimes = ["23:30", "00:30", "23:30", "00:30"]
    nights = [
        slept(f"2026-03-{day}", bed, 480) for day, bed in zip(range(15, 19), bedtimes, strict=True)
    ]
    assert weekly_summary(toronto_user(), nights, NOW).usual_bedtime == time(0, 0)


def test_T_116_4_each_night_is_read_in_its_own_time_zone():
    # Sam is in Toronto now, but three nights were logged in London at 23:00 local.
    nights = [slept(f"2026-03-{d}", "23:00", 480, tz=LONDON) for d in (14, 15, 16)]
    nights += [slept(f"2026-03-{d}", "23:00", 480) for d in (17, 18)]
    assert weekly_summary(toronto_user(), nights, NOW).usual_bedtime == time(23, 0)


def test_T_116_4_night_logged_in_another_zone_is_windowed_by_its_own_night_of_date():
    nights = [slept("2026-03-19", "23:00", 480, tz=LONDON), *three_nights((8, 0), (8, 0))]
    assert weekly_summary(toronto_user(), nights, NOW).nights_logged == 3


# AC5: fewer than 3 nights, no figures
@pytest.mark.parametrize("count", [0, 1, 2])
def test_T_116_5_fewer_than_three_nights_shows_only_the_prompt(count):
    nights = three_nights((8, 0), (8, 0), (8, 0))[:count]
    result = weekly_summary(toronto_user(), nights, NOW)
    assert result.text == TOO_FEW
    assert result.average_asleep is None
    assert result.usual_bedtime is None


def test_T_116_5_exactly_three_nights_shows_figures():
    result = weekly_summary(toronto_user(), three_nights((8, 0), (8, 0), (8, 0)), NOW)
    assert result.text != TOO_FEW
    assert result.average_asleep is not None


def test_T_116_5_nights_outside_the_window_do_not_count_toward_the_three():
    older = [slept(f"2026-03-{d}", "23:00", 480) for d in (1, 2, 3, 4, 5, 6, 12)]
    two_recent = three_nights((8, 0), (8, 0))
    assert weekly_summary(toronto_user(), older + two_recent, NOW).text == TOO_FEW


def test_T_116_5_figures_ignore_nights_outside_the_window():
    old = slept("2026-03-01", "03:00", 600)  # a 3 am, 10 h night would skew both figures
    result = weekly_summary(toronto_user(), [old, *three_nights((8, 0), (8, 0), (8, 0))], NOW)
    assert result.nights_logged == 3
    assert result.average_asleep == timedelta(hours=8)
    assert result.usual_bedtime == time(23, 0)


# AC6: wording passes the claims check
def test_T_116_6_figures_wording_is_claims_clean():
    result = weekly_summary(toronto_user(), three_nights((8, 0), (7, 0), (6, 0)), NOW)
    assert check_text(result.text) == []


def test_T_116_6_prompt_wording_is_claims_clean():
    assert check_text(TOO_FEW) == []
    assert check_text(weekly_summary(toronto_user(), [], NOW).text) == []


# Non-functional: durations are real elapsed time across DST changes
def test_T_116_8_spring_forward_night_is_an_hour_shorter():
    now = datetime(2026, 3, 12, 12, 0, tzinfo=TORONTO_TZ)
    spring = local_night(  # 23:00 EST -> 07:00 EDT is 7 h of real time, not 8
        datetime(2026, 3, 7, 23, 0, tzinfo=TORONTO_TZ),
        datetime(2026, 3, 8, 7, 0, tzinfo=TORONTO_TZ),
    )
    assert spring.duration == timedelta(hours=7)  # guards the test helper itself
    others = [slept("2026-03-09", "23:00", 480), slept("2026-03-10", "23:00", 480)]
    result = weekly_summary(toronto_user(), [spring, *others], now)
    assert result.average_asleep == timedelta(hours=7, minutes=40)


def test_T_116_8_fall_back_night_is_an_hour_longer():
    now = datetime(2026, 11, 5, 12, 0, tzinfo=TORONTO_TZ)
    fall = local_night(  # 23:00 EDT -> 07:00 EST is 9 h of real time
        datetime(2026, 10, 31, 23, 0, tzinfo=TORONTO_TZ),
        datetime(2026, 11, 1, 7, 0, tzinfo=TORONTO_TZ),
    )
    assert fall.duration == timedelta(hours=9)
    others = [slept("2026-11-02", "23:00", 480), slept("2026-11-03", "23:00", 480)]
    result = weekly_summary(toronto_user(), [fall, *others], now)
    assert result.average_asleep == timedelta(hours=8, minutes=20)
