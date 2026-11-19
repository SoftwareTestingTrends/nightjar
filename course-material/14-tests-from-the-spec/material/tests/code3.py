"""The `silent` flag of next_nudge on daylight-saving nights (S-114 AC3 + DST edge cases)."""

from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

from builders import LONDON, TORONTO, nights_at

from nightjar.models import User
from nightjar.nudge import next_nudge

TORONTO_TZ, LONDON_TZ = ZoneInfo(TORONTO), ZoneInfo(LONDON)
USUAL_23_00 = nights_at("23:00", 7, first_night="2026-02-01")  # nudge at 22:15
USUAL_02_45 = nights_at("02:45", 7, first_night="2026-02-01")  # nudge at 02:00
USUAL_02_15 = nights_at("02:15", 7, first_night="2026-02-01")  # nudge at 01:30


def local(tz: ZoneInfo, *args: int) -> datetime:
    return datetime(*args, tzinfo=tz)


def sam(tz: str, start: time, end: time) -> User:
    return User(name="Sam", timezone=tz, quiet_start=start, quiet_end=end)


def test_T_114_3_spring_forward_evening_nudge_is_silent_in_overnight_quiet_hours():
    user = sam(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(user, USUAL_23_00, local(TORONTO_TZ, 2026, 3, 8, 8, 0))
    assert nudge is not None
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 8, 22, 15)
    assert nudge.silent is True


def test_T_114_3_fall_back_evening_nudge_is_silent_in_overnight_quiet_hours():
    user = sam(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(user, USUAL_23_00, local(TORONTO_TZ, 2026, 11, 1, 8, 0))
    assert nudge is not None
    assert nudge.at == local(TORONTO_TZ, 2026, 11, 1, 22, 15)
    assert nudge.silent is True


def test_T_114_3_rolling_over_fall_back_keeps_silent_flag():
    # Saturday night after the nudge; the next one is Sunday 1 Nov, after clocks change.
    user = sam(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(user, USUAL_23_00, local(TORONTO_TZ, 2026, 10, 31, 23, 0))
    assert nudge.at == local(TORONTO_TZ, 2026, 11, 1, 22, 15)
    assert nudge.silent is True


def test_T_114_3_dst_evening_nudge_outside_quiet_hours_is_not_silent():
    user = sam(TORONTO, time(23, 0), time(7, 0))
    for now in (local(TORONTO_TZ, 2026, 3, 8, 8), local(TORONTO_TZ, 2026, 11, 1, 8)):
        assert next_nudge(user, USUAL_23_00, now).silent is False


def test_T_114_3_london_dst_evenings_follow_local_quiet_hours():
    quiet = sam(LONDON, time(22, 0), time(7, 0))
    awake = sam(LONDON, time(23, 0), time(7, 0))
    for now in (local(LONDON_TZ, 2026, 3, 29, 8), local(LONDON_TZ, 2026, 10, 25, 8)):
        assert next_nudge(quiet, USUAL_23_00, now).silent is True
        assert next_nudge(awake, USUAL_23_00, now).silent is False


def test_T_114_3_quiet_hours_use_local_wall_clock_not_utc_offset():
    # 22:15 EDT is 02:15 UTC, 22:15 EST is 03:15 UTC. Quiet hours are local, so both are silent
    # and a window that only matches the UTC time must not apply.
    utc_window = sam(TORONTO, time(2, 0), time(4, 0))
    for now in (local(TORONTO_TZ, 2026, 3, 8, 8), local(TORONTO_TZ, 2026, 11, 1, 8)):
        assert next_nudge(utc_window, USUAL_23_00, now).silent is False


def test_T_114_3_nudge_in_the_small_hours_of_fall_back_night_is_silent():
    # Nudge 01:30 happens twice on 1 Nov in Toronto; whichever instant is chosen, it is quiet.
    user = sam(TORONTO, time(0, 0), time(7, 0))
    nudge = next_nudge(user, USUAL_02_15, local(TORONTO_TZ, 2026, 10, 31, 12, 0))
    assert nudge is not None
    assert (nudge.at.hour, nudge.at.minute) == (1, 30)
    assert nudge.silent is True


def test_T_114_3_nudge_moved_by_spring_forward_gap_is_silent_if_delivered_in_quiet_hours():
    # Nudge 02:00 doesn't exist on 8 March in Toronto, so it is delivered at 03:00 EDT.
    # Quiet hours 02:30-07:00 cover 03:00, so the delivered nudge must be silent.
    user = sam(TORONTO, time(2, 30), time(7, 0))
    nudge = next_nudge(user, USUAL_02_45, local(TORONTO_TZ, 2026, 3, 7, 12, 0))
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 8, 7, 0, tzinfo=UTC)  # 03:00 EDT
    assert nudge.silent is True
