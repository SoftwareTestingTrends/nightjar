"""Story S-114 AC3 on daylight-saving nights: quiet hours decide `Nudge.silent`.

Quiet hours are wall-clock times in the user's zone, so the flag must follow the
nudge's local time on that night, whatever the UTC offset is.
"""

from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

from builders import LONDON, TORONTO, nights_at

from nightjar.models import User
from nightjar.nudge import next_nudge

TORONTO_TZ, LONDON_TZ = ZoneInfo(TORONTO), ZoneInfo(LONDON)
USUAL_23_00 = nights_at("23:00", 7, first_night="2026-02-01")  # nudge at 22:15 local
USUAL_02_45 = nights_at("02:45", 7, first_night="2026-02-01")  # nudge at 02:00 local


def local(tz: ZoneInfo, *args: int) -> datetime:
    return datetime(*args, tzinfo=tz)


def user(tz: str, start: time, end: time) -> User:
    return User(name="Sam", timezone=tz, quiet_start=start, quiet_end=end)


# Toronto spring forward: Sun 8 March 2026, evening is EDT (UTC-4)
def test_T_114_3_toronto_spring_forward_nudge_in_quiet_hours_is_silent():
    sam = user(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(TORONTO_TZ, 2026, 3, 8, 8, 0))
    assert nudge is not None
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 8, 22, 15)
    assert nudge.silent is True


def test_T_114_3_toronto_spring_forward_nudge_before_quiet_hours_is_not_silent():
    sam = user(TORONTO, time(22, 30), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(TORONTO_TZ, 2026, 3, 8, 8, 0))
    assert nudge is not None
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 8, 22, 15)
    assert nudge.silent is False


def test_T_114_3_rolling_to_tomorrow_across_spring_forward_keeps_silent_flag():
    # Saturday 23:00 EST: the next nudge is Sunday 22:15, after the clocks change.
    sam = user(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(TORONTO_TZ, 2026, 3, 7, 23, 0))
    assert nudge is not None
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 8, 22, 15)
    assert nudge.silent is True


# Toronto fall back: Sun 1 November 2026, evening is EST (UTC-5)
def test_T_114_3_toronto_fall_back_nudge_in_quiet_hours_is_silent():
    sam = user(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(TORONTO_TZ, 2026, 11, 1, 8, 0))
    assert nudge is not None
    assert nudge.at == local(TORONTO_TZ, 2026, 11, 1, 22, 15)
    assert nudge.silent is True


def test_T_114_3_toronto_fall_back_nudge_before_quiet_hours_is_not_silent():
    sam = user(TORONTO, time(22, 30), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(TORONTO_TZ, 2026, 11, 1, 8, 0))
    assert nudge is not None
    assert nudge.at == local(TORONTO_TZ, 2026, 11, 1, 22, 15)
    assert nudge.silent is False


def test_T_114_3_rolling_to_tomorrow_across_fall_back_keeps_silent_flag():
    sam = user(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(TORONTO_TZ, 2026, 10, 31, 23, 0))
    assert nudge is not None
    assert nudge.at == local(TORONTO_TZ, 2026, 11, 1, 22, 15)
    assert nudge.silent is True


# London: the UTC time of the nudge differs from its wall time in BST
def test_T_114_3_london_spring_forward_quiet_hours_use_local_not_utc_time():
    # 22:15 BST is 21:15 UTC. Quiet from 21:30 local, so the nudge is silent;
    # comparing UTC time against the quiet window would say otherwise.
    sam = user(LONDON, time(21, 30), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(LONDON_TZ, 2026, 3, 29, 8, 0))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 29, 21, 15, tzinfo=UTC)
    assert nudge.silent is True


def test_T_114_3_london_spring_forward_nudge_before_quiet_hours_is_not_silent():
    sam = user(LONDON, time(22, 30), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(LONDON_TZ, 2026, 3, 29, 8, 0))
    assert nudge is not None
    assert nudge.silent is False


def test_T_114_3_london_fall_back_nudge_in_quiet_hours_is_silent():
    sam = user(LONDON, time(22, 0), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(LONDON_TZ, 2026, 10, 25, 8, 0))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == datetime(2026, 10, 25, 22, 15, tzinfo=UTC)
    assert nudge.silent is True


def test_T_114_3_london_fall_back_nudge_before_quiet_hours_is_not_silent():
    sam = user(LONDON, time(22, 30), time(7, 0))
    nudge = next_nudge(sam, USUAL_23_00, local(LONDON_TZ, 2026, 10, 25, 8, 0))
    assert nudge is not None
    assert nudge.silent is False


# A nudge time skipped by DST is moved forward, and is still delivered (never skipped)
def test_T_114_3_nudge_time_skipped_by_dst_is_delivered_silently_in_quiet_hours():
    # Nudge 02:00 doesn't exist on 8 March in Toronto; it becomes 03:00 EDT.
    # Quiet hours 01:00-07:00 cover both the skipped and the real time.
    sam = user(TORONTO, time(1, 0), time(7, 0))
    nudge = next_nudge(sam, USUAL_02_45, local(TORONTO_TZ, 2026, 3, 7, 12, 0))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 8, 7, 0, tzinfo=UTC)
    assert nudge.silent is True


def test_T_114_3_nudge_time_skipped_by_dst_outside_quiet_hours_is_not_silent():
    sam = user(TORONTO, time(4, 0), time(7, 0))
    nudge = next_nudge(sam, USUAL_02_45, local(TORONTO_TZ, 2026, 3, 7, 12, 0))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 8, 7, 0, tzinfo=UTC)
    assert nudge.silent is False


def test_T_114_3_small_hours_nudge_after_fall_back_is_silent_in_quiet_hours():
    # 02:00 on 1 Nov in Toronto happens once, after the clocks go back (EST).
    sam = user(TORONTO, time(1, 0), time(7, 0))
    nudge = next_nudge(sam, USUAL_02_45, local(TORONTO_TZ, 2026, 10, 31, 12, 0))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == datetime(2026, 11, 1, 7, 0, tzinfo=UTC)
    assert nudge.silent is True
