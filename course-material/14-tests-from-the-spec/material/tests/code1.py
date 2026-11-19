"""AC3 (silent, never skipped) on daylight-saving nights. Extends the T-114-3 / T-114-6 cases."""

from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

import pytest
from builders import LONDON, TORONTO, nights_at

from nightjar.models import User
from nightjar.nudge import next_nudge

TORONTO_TZ, LONDON_TZ = ZoneInfo(TORONTO), ZoneInfo(LONDON)
USUAL_23_00 = nights_at("23:00", 7, first_night="2026-02-01")  # nudge at 22:15
USUAL_02_45 = nights_at("02:45", 7, first_night="2026-02-01")  # nudge at 02:00


def local(tz: ZoneInfo, *args: int) -> datetime:
    return datetime(*args, tzinfo=tz)


def quiet_user(tz: str, start: time, end: time) -> User:
    return User(name="Sam", timezone=tz, quiet_start=start, quiet_end=end)


@pytest.mark.parametrize(
    ("tz", "now", "expected_utc"),
    [
        (TORONTO_TZ, local(TORONTO_TZ, 2026, 3, 8, 8), datetime(2026, 3, 9, 2, 15, tzinfo=UTC)),
        (TORONTO_TZ, local(TORONTO_TZ, 2026, 10, 31, 23), datetime(2026, 11, 2, 3, 15, tzinfo=UTC)),
        (LONDON_TZ, local(LONDON_TZ, 2026, 3, 28, 23), datetime(2026, 3, 29, 21, 15, tzinfo=UTC)),
        (LONDON_TZ, local(LONDON_TZ, 2026, 10, 24, 23), datetime(2026, 10, 25, 22, 15, tzinfo=UTC)),
    ],
    ids=["toronto-spring", "toronto-fall", "london-spring", "london-fall"],
)
def test_T_114_3_evening_nudge_inside_quiet_hours_is_silent_on_dst_days(tz, now, expected_utc):
    user = quiet_user(str(tz), time(22, 0), time(7, 0))
    nudge = next_nudge(user, USUAL_23_00, now)
    assert nudge is not None
    assert nudge.silent is True
    assert nudge.at.astimezone(UTC) == expected_utc


@pytest.mark.parametrize(
    ("tz", "now"),
    [
        (TORONTO_TZ, local(TORONTO_TZ, 2026, 3, 8, 8)),
        (TORONTO_TZ, local(TORONTO_TZ, 2026, 10, 31, 23)),
        (LONDON_TZ, local(LONDON_TZ, 2026, 3, 28, 23)),
        (LONDON_TZ, local(LONDON_TZ, 2026, 10, 24, 23)),
    ],
    ids=["toronto-spring", "toronto-fall", "london-spring", "london-fall"],
)
def test_T_114_3_evening_nudge_outside_quiet_hours_is_not_silent_on_dst_days(tz, now):
    user = quiet_user(str(tz), time(23, 0), time(7, 0))  # nudge 22:15 is before the window
    nudge = next_nudge(user, USUAL_23_00, now)
    assert nudge is not None
    assert nudge.silent is False


def test_T_114_3_quiet_check_uses_wall_clock_not_utc_offset_after_fall_back(toronto_user):
    # 22:15 on 1 Nov is 03:15 UTC (EST) but 02:15 UTC on 31 Oct (EDT): the window is wall-clock.
    user = quiet_user(TORONTO, time(22, 15), time(23, 0))  # start is inclusive
    nudge = next_nudge(user, USUAL_23_00, local(TORONTO_TZ, 2026, 10, 31, 23))
    assert nudge.silent is True


def test_T_114_3_ambiguous_fall_back_nudge_time_is_silent_inside_quiet_hours():
    # Nudge 01:15 on 1 Nov happens twice in Toronto; either way it's inside 01:00-07:00.
    user = quiet_user(TORONTO, time(1, 0), time(7, 0))
    nudge = next_nudge(user, nights_at("02:00", 7, first_night="2026-02-01"), local(TORONTO_TZ, 2026, 10, 31, 12))
    assert nudge is not None
    assert nudge.silent is True
    assert nudge.at.astimezone(TORONTO_TZ).time() == time(1, 15)


def test_T_114_3_nudge_skipped_by_spring_forward_is_still_delivered_and_silent():
    # Nudge 02:00 doesn't exist on 8 March; it moves to 03:00 EDT, inside the 01:00-07:00 window.
    user = quiet_user(TORONTO, time(1, 0), time(7, 0))
    nudge = next_nudge(user, USUAL_02_45, local(TORONTO_TZ, 2026, 3, 7, 12))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 8, 7, 0, tzinfo=UTC)
    assert nudge.silent is True


def test_T_114_3_silent_follows_the_delivered_time_when_dst_shifts_it_into_quiet_hours():
    # Nudge 02:00 doesn't exist on 8 March; delivered at 03:00 EDT, which is inside 02:30-07:00.
    # The user is woken by what actually fires (03:00), so it must be silent.
    user = quiet_user(TORONTO, time(2, 30), time(7, 0))
    nudge = next_nudge(user, USUAL_02_45, local(TORONTO_TZ, 2026, 3, 7, 12))
    assert nudge.at.astimezone(TORONTO_TZ).time() == time(3, 0)
    assert nudge.silent is True
