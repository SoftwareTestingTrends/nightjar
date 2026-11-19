"""Story S-114 AC3 on daylight-saving nights: the `silent` flag follows quiet hours.

Quiet hours are wall-clock times in the user's zone, so they must be compared with the
nudge's *local* time on that date (not a fixed UTC offset), and a nudge is never skipped.
"""

from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

import pytest
from builders import LONDON, TORONTO, nights_at

from nightjar.models import User
from nightjar.nudge import next_nudge

TORONTO_TZ, LONDON_TZ = ZoneInfo(TORONTO), ZoneInfo(LONDON)
TORONTO_23_00 = nights_at("23:00", 7, first_night="2026-02-01", tz=TORONTO)  # nudge 22:15
LONDON_23_00 = nights_at("23:00", 7, first_night="2026-02-01", tz=LONDON)  # nudge 22:15
TORONTO_02_45 = nights_at("02:45", 7, first_night="2026-02-01", tz=TORONTO)  # nudge 02:00
TORONTO_01_45 = nights_at("01:45", 7, first_night="2026-09-01", tz=TORONTO)  # nudge 01:00


def local(tz: ZoneInfo, *args: int) -> datetime:
    return datetime(*args, tzinfo=tz)


def user_with_quiet(tz: str, start: time, end: time) -> User:
    return User(name="Sam", timezone=tz, quiet_start=start, quiet_end=end)


# Evening nudges (22:15 local) on the day clocks change, quiet hours 22:00-07:00 wrapping midnight.
# 22:15 is inside the window in every case, whichever UTC offset applies that evening.
@pytest.mark.parametrize(
    ("tz_name", "tz", "nights", "now", "expected_utc"),
    [
        pytest.param(  # Toronto spring forward, Sun 8 Mar 2026: evening is EDT (UTC-4)
            TORONTO,
            TORONTO_TZ,
            TORONTO_23_00,
            (2026, 3, 8, 8, 0),
            datetime(2026, 3, 9, 2, 15, tzinfo=UTC),
            id="toronto-spring-forward",
        ),
        pytest.param(  # Toronto fall back, Sun 1 Nov 2026: evening is EST (UTC-5)
            TORONTO,
            TORONTO_TZ,
            TORONTO_23_00,
            (2026, 11, 1, 8, 0),
            datetime(2026, 11, 2, 3, 15, tzinfo=UTC),
            id="toronto-fall-back",
        ),
        pytest.param(  # London spring forward, Sun 29 Mar 2026: evening is BST (UTC+1)
            LONDON,
            LONDON_TZ,
            LONDON_23_00,
            (2026, 3, 29, 8, 0),
            datetime(2026, 3, 29, 21, 15, tzinfo=UTC),
            id="london-spring-forward",
        ),
        pytest.param(  # London fall back, Sun 25 Oct 2026: evening is GMT (UTC+0)
            LONDON,
            LONDON_TZ,
            LONDON_23_00,
            (2026, 10, 25, 8, 0),
            datetime(2026, 10, 25, 22, 15, tzinfo=UTC),
            id="london-fall-back",
        ),
    ],
)
def test_T_114_3_nudge_on_dst_day_inside_quiet_hours_is_silent_not_skipped(
    tz_name, tz, nights, now, expected_utc
):
    user = user_with_quiet(tz_name, time(22, 0), time(7, 0))
    nudge = next_nudge(user, nights, now=local(tz, *now))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == expected_utc
    assert nudge.silent is True


@pytest.mark.parametrize(
    ("tz_name", "tz", "nights", "now"),
    [
        pytest.param(TORONTO, TORONTO_TZ, TORONTO_23_00, (2026, 3, 8, 8, 0), id="toronto-spring"),
        pytest.param(TORONTO, TORONTO_TZ, TORONTO_23_00, (2026, 11, 1, 8, 0), id="toronto-fall"),
        pytest.param(LONDON, LONDON_TZ, LONDON_23_00, (2026, 3, 29, 8, 0), id="london-spring"),
        pytest.param(LONDON, LONDON_TZ, LONDON_23_00, (2026, 10, 25, 8, 0), id="london-fall"),
    ],
)
def test_T_114_3_nudge_on_dst_day_before_quiet_hours_start_is_not_silent(
    tz_name, tz, nights, now
):
    # Quiet hours begin at 22:30 local; the 22:15 nudge is 15 minutes before them.
    user = user_with_quiet(tz_name, time(22, 30), time(7, 0))
    nudge = next_nudge(user, nights, now=local(tz, *now))
    assert nudge is not None
    assert nudge.silent is False


def test_T_114_3_quiet_hours_are_wall_clock_across_the_spring_forward_boundary():
    # Yesterday (EST) and today (EDT) have the same local nudge time but different UTC
    # instants, so quiet hours must be applied to local time, giving the same answer both days.
    user = user_with_quiet(TORONTO, time(22, 0), time(7, 0))
    day_before = next_nudge(user, TORONTO_23_00, now=local(TORONTO_TZ, 2026, 3, 7, 8, 0))
    dst_day = next_nudge(user, TORONTO_23_00, now=local(TORONTO_TZ, 2026, 3, 8, 8, 0))
    assert day_before.at.astimezone(UTC) == datetime(2026, 3, 8, 3, 15, tzinfo=UTC)  # EST
    assert dst_day.at.astimezone(UTC) == datetime(2026, 3, 9, 2, 15, tzinfo=UTC)  # EDT
    assert day_before.silent is True
    assert dst_day.silent is True


def test_T_114_3_rolling_over_fall_back_keeps_quiet_hours_applied():
    # Asked at 23:00 EDT on Sat 31 Oct: the next nudge is Sun 1 Nov 22:15 EST, still quiet.
    user = user_with_quiet(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(user, TORONTO_23_00, now=local(TORONTO_TZ, 2026, 10, 31, 23, 0))
    assert nudge.at == local(TORONTO_TZ, 2026, 11, 1, 22, 15)
    assert nudge.silent is True


# A nudge time that DST skips is moved forward to a real instant (02:00 -> 03:00 EDT on
# 8 March in Toronto). Silence is judged on the time the nudge is actually delivered.
def test_T_114_3_nudge_moved_forward_by_spring_forward_inside_quiet_hours_is_silent():
    user = user_with_quiet(TORONTO, time(2, 30), time(7, 0))
    nudge = next_nudge(user, TORONTO_02_45, now=local(TORONTO_TZ, 2026, 3, 7, 12, 0))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 8, 7, 0, tzinfo=UTC)  # 03:00 EDT
    assert nudge.silent is True


def test_T_114_3_nudge_moved_forward_by_spring_forward_is_judged_at_its_real_time():
    # Quiet hours end 02:30. The nominal 02:00 would be quiet, but it is delivered at 03:00.
    user = user_with_quiet(TORONTO, time(1, 0), time(2, 30))
    nudge = next_nudge(user, TORONTO_02_45, now=local(TORONTO_TZ, 2026, 3, 7, 12, 0))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 8, 7, 0, tzinfo=UTC)  # 03:00 EDT
    assert nudge.silent is False


# 01:00 happens twice in Toronto on 1 Nov 2026 (EDT then EST). Either way it is local 01:00.
@pytest.mark.parametrize(
    ("quiet_start", "expected_silent"),
    [(time(0, 30), True), (time(1, 30), False)],
    ids=["inside-quiet-hours", "before-quiet-hours"],
)
def test_T_114_3_nudge_in_the_repeated_fall_back_hour_uses_local_wall_time(
    quiet_start, expected_silent
):
    user = user_with_quiet(TORONTO, quiet_start, time(7, 0))
    nudge = next_nudge(user, TORONTO_01_45, now=local(TORONTO_TZ, 2026, 10, 31, 12, 0))
    assert nudge is not None
    assert nudge.at.astimezone(TORONTO_TZ).date().isoformat() == "2026-11-01"
    assert (nudge.at.hour, nudge.at.minute) == (1, 0)
    assert nudge.silent is expected_silent


def test_T_114_3_no_quiet_hours_set_is_never_silent_on_dst_day():
    user = User(name="Sam", timezone=TORONTO)
    nudge = next_nudge(user, TORONTO_23_00, now=local(TORONTO_TZ, 2026, 3, 8, 8, 0))
    assert nudge is not None
    assert nudge.silent is False
