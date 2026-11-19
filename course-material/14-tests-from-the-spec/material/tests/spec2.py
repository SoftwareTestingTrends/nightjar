"""Story S-114 AC3 x NFR: the `silent` flag on daylight-saving nights.

Quiet hours are wall-clock times in the user's zone. On a DST night the nudge must be
judged by its local wall time (22:15), not by its UTC time or by a fixed UTC offset.
Test ids (T-114-3) are listed in docs/traceability.md.
"""

from datetime import datetime, time
from zoneinfo import ZoneInfo

import pytest
from builders import LONDON, TORONTO, nights_at

from nightjar.models import User
from nightjar.nudge import next_nudge

# (zone, day of the transition, month, "now" hour on that day)
# Toronto: spring forward Sun 8 Mar 2026, fall back Sun 1 Nov 2026.
# London: spring forward Sun 29 Mar 2026, fall back Sun 25 Oct 2026.
TRANSITIONS = [
    pytest.param(TORONTO, (2026, 3, 8), id="toronto-spring-forward"),
    pytest.param(TORONTO, (2026, 11, 1), id="toronto-fall-back"),
    pytest.param(LONDON, (2026, 3, 29), id="london-spring-forward"),
    pytest.param(LONDON, (2026, 10, 25), id="london-fall-back"),
]


def local(tz_name: str, *args: int) -> datetime:
    return datetime(*args, tzinfo=ZoneInfo(tz_name))


def user_with_quiet(tz_name: str, start: time | None, end: time | None) -> User:
    return User(name="Sam", timezone=tz_name, quiet_start=start, quiet_end=end)


def evening_nights(tz_name: str, bedtime: str = "23:00"):
    return nights_at(bedtime, 7, first_night="2026-02-01", tz=tz_name)


# Usual bedtime 23:00 -> nudge 22:15 local on the transition day itself.
@pytest.mark.parametrize(("tz_name", "day"), TRANSITIONS)
def test_T_114_3_dst_day_nudge_inside_quiet_hours_is_silent_not_skipped(tz_name, day):
    user = user_with_quiet(tz_name, time(22, 0), time(7, 0))
    nudge = next_nudge(user, evening_nights(tz_name), now=local(tz_name, *day, 8, 0))
    assert nudge is not None
    assert nudge.at == local(tz_name, *day, 22, 15)
    assert nudge.silent is True


@pytest.mark.parametrize(("tz_name", "day"), TRANSITIONS)
def test_T_114_3_dst_day_nudge_before_quiet_hours_start_is_not_silent(tz_name, day):
    # Quiet hours begin 22:30, after the 22:15 nudge. A UTC or wrong-offset
    # comparison would put the nudge on the wrong side of the boundary.
    user = user_with_quiet(tz_name, time(22, 30), time(7, 0))
    nudge = next_nudge(user, evening_nights(tz_name), now=local(tz_name, *day, 8, 0))
    assert nudge is not None
    assert nudge.at == local(tz_name, *day, 22, 15)
    assert nudge.silent is False


@pytest.mark.parametrize(("tz_name", "day"), TRANSITIONS)
def test_T_114_3_dst_day_quiet_window_ending_before_nudge_is_not_silent(tz_name, day):
    # A daytime window that does not wrap midnight, ending before 22:15.
    user = user_with_quiet(tz_name, time(21, 0), time(22, 0))
    nudge = next_nudge(user, evening_nights(tz_name), now=local(tz_name, *day, 8, 0))
    assert nudge is not None
    assert nudge.silent is False


@pytest.mark.parametrize(("tz_name", "day"), TRANSITIONS)
def test_T_114_3_dst_day_without_quiet_hours_is_not_silent(tz_name, day):
    user = user_with_quiet(tz_name, None, None)
    nudge = next_nudge(user, evening_nights(tz_name), now=local(tz_name, *day, 8, 0))
    assert nudge is not None
    assert nudge.silent is False


# The nudge rolls onto the transition day from the evening before.
@pytest.mark.parametrize(("tz_name", "day"), TRANSITIONS)
def test_T_114_3_nudge_rolled_to_dst_day_keeps_its_silent_flag(tz_name, day):
    year, month, dom = day
    eve_before = local(tz_name, year, month, dom - 1, 23, 0)  # past the day-before nudge
    quiet = user_with_quiet(tz_name, time(22, 0), time(7, 0))
    loud = user_with_quiet(tz_name, time(22, 30), time(7, 0))
    nights = evening_nights(tz_name)

    quiet_nudge = next_nudge(quiet, nights, now=eve_before)
    loud_nudge = next_nudge(loud, nights, now=eve_before)

    assert quiet_nudge.at == local(tz_name, *day, 22, 15)
    assert quiet_nudge.silent is True
    assert loud_nudge.at == local(tz_name, *day, 22, 15)
    assert loud_nudge.silent is False


# A late usual bedtime puts the nudge in the small hours, inside the DST gap/overlap.
# The quiet windows below are chosen so the answer is the same whichever of the two
# wall times (e.g. 02:00 or 03:00) the implementation reports.
def test_T_114_3_toronto_nudge_in_skipped_hour_is_silent_when_quiet_hours_cover_it():
    # Usual bedtime 02:45 -> nudge 02:00, which does not exist on 8 March; it becomes 03:00.
    user = user_with_quiet(TORONTO, time(1, 0), time(7, 0))
    nudge = next_nudge(
        user, evening_nights(TORONTO, "02:45"), now=local(TORONTO, 2026, 3, 7, 12, 0)
    )
    assert nudge is not None
    assert nudge.silent is True


def test_T_114_3_toronto_nudge_in_skipped_hour_is_not_silent_outside_quiet_hours():
    user = user_with_quiet(TORONTO, time(22, 0), time(1, 0))
    nudge = next_nudge(
        user, evening_nights(TORONTO, "02:45"), now=local(TORONTO, 2026, 3, 7, 12, 0)
    )
    assert nudge is not None
    assert nudge.silent is False


def test_T_114_3_toronto_nudge_in_repeated_hour_is_silent_when_quiet_hours_cover_it():
    # Usual bedtime 01:45 -> nudge 01:00, which happens twice on 1 November.
    user = user_with_quiet(TORONTO, time(0, 0), time(7, 0))
    nudge = next_nudge(
        user, evening_nights(TORONTO, "01:45"), now=local(TORONTO, 2026, 10, 31, 12, 0)
    )
    assert nudge is not None
    assert nudge.silent is True


def test_T_114_3_toronto_nudge_in_repeated_hour_is_not_silent_outside_quiet_hours():
    user = user_with_quiet(TORONTO, time(22, 0), time(0, 30))
    nudge = next_nudge(
        user, evening_nights(TORONTO, "01:45"), now=local(TORONTO, 2026, 10, 31, 12, 0)
    )
    assert nudge is not None
    assert nudge.silent is False


def test_T_114_3_london_nudge_in_skipped_hour_is_silent_when_quiet_hours_cover_it():
    # London springs forward 01:00 -> 02:00 on 29 March; usual bedtime 01:45 -> nudge 01:00.
    user = user_with_quiet(LONDON, time(0, 0), time(7, 0))
    nudge = next_nudge(
        user, evening_nights(LONDON, "01:45"), now=local(LONDON, 2026, 3, 28, 12, 0)
    )
    assert nudge is not None
    assert nudge.silent is True
