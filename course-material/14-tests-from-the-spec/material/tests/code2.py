"""Story S-114 AC3 on daylight-saving nights: the silent flag follows the local delivery time."""

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


def sam(tz: str, start: time | None, end: time | None) -> User:
    return User(name="Sam", timezone=tz, quiet_start=start, quiet_end=end)


SPRING_FORWARD_NOON = local(TORONTO_TZ, 2026, 3, 8, 8, 0)  # Toronto, 8 March
FALL_BACK_NOON = local(TORONTO_TZ, 2026, 11, 1, 8, 0)  # Toronto, 1 November


def test_T_114_3_spring_forward_day_nudge_in_quiet_hours_is_silent():
    nudge = next_nudge(sam(TORONTO, time(22, 0), time(7, 0)), USUAL_23_00, SPRING_FORWARD_NOON)
    assert nudge is not None
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 8, 22, 15)
    assert nudge.silent is True


def test_T_114_3_spring_forward_day_nudge_outside_quiet_hours_is_not_silent():
    nudge = next_nudge(sam(TORONTO, time(23, 0), time(7, 0)), USUAL_23_00, SPRING_FORWARD_NOON)
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 8, 22, 15)
    assert nudge.silent is False


def test_T_114_3_fall_back_day_nudge_in_quiet_hours_is_silent():
    nudge = next_nudge(sam(TORONTO, time(22, 0), time(7, 0)), USUAL_23_00, FALL_BACK_NOON)
    assert nudge.at == local(TORONTO_TZ, 2026, 11, 1, 22, 15)
    assert nudge.silent is True


def test_T_114_3_fall_back_day_nudge_outside_quiet_hours_is_not_silent():
    nudge = next_nudge(sam(TORONTO, time(23, 0), time(7, 0)), USUAL_23_00, FALL_BACK_NOON)
    assert nudge.silent is False


def test_T_114_3_quiet_start_is_inclusive_on_a_dst_day():
    nudge = next_nudge(sam(TORONTO, time(22, 15), time(7, 0)), USUAL_23_00, SPRING_FORWARD_NOON)
    assert nudge.silent is True


def test_T_114_3_quiet_end_is_exclusive_on_a_dst_day():
    nudge = next_nudge(sam(TORONTO, time(20, 0), time(22, 15)), USUAL_23_00, FALL_BACK_NOON)
    assert nudge.silent is False


def test_T_114_3_london_dst_days_stay_silent_in_quiet_hours():
    user = sam(LONDON, time(22, 0), time(7, 0))
    spring = next_nudge(user, USUAL_23_00, local(LONDON_TZ, 2026, 3, 29, 8, 0))
    fall = next_nudge(user, USUAL_23_00, local(LONDON_TZ, 2026, 10, 25, 8, 0))
    assert spring.at.astimezone(UTC) == datetime(2026, 3, 29, 21, 15, tzinfo=UTC)  # BST
    assert fall.at.astimezone(UTC) == datetime(2026, 10, 25, 22, 15, tzinfo=UTC)  # GMT
    assert spring.silent is True
    assert fall.silent is True


def test_T_114_3_nudge_rolled_to_tomorrow_across_fall_back_is_still_silent():
    # Sat 31 Oct 23:00 EDT: the next nudge is Sun 1 Nov 22:15 EST, inside quiet hours.
    user = sam(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(user, USUAL_23_00, local(TORONTO_TZ, 2026, 10, 31, 23, 0))
    assert nudge.at == local(TORONTO_TZ, 2026, 11, 1, 22, 15)
    assert nudge.silent is True


def test_T_114_3_nudge_in_the_skipped_hour_is_delivered_silently_when_quiet_covers_it():
    # Nudge 02:00 doesn't exist on 8 March in Toronto; it is delivered at 03:00 EDT, not skipped.
    user = sam(TORONTO, time(22, 0), time(7, 0))
    nudge = next_nudge(user, USUAL_02_45, local(TORONTO_TZ, 2026, 3, 7, 12, 0))
    assert nudge is not None
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 8, 7, 0, tzinfo=UTC)
    assert nudge.silent is True


def test_T_114_3_skipped_hour_nudge_follows_the_time_it_is_actually_delivered():
    # Quiet hours end at 02:30, but the nudge lands at 03:00, after they end.
    user = sam(TORONTO, time(0, 0), time(2, 30))
    nudge = next_nudge(user, USUAL_02_45, local(TORONTO_TZ, 2026, 3, 7, 12, 0))
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 8, 3, 0)
    assert nudge.silent is False


def test_T_114_3_repeated_hour_nudge_is_silent_when_quiet_covers_it():
    # 01:30 happens twice on 1 November in Toronto; the nudge is still delivered once, silently.
    user = sam(TORONTO, time(1, 0), time(2, 0))
    nudge = next_nudge(user, USUAL_02_15, local(TORONTO_TZ, 2026, 11, 1, 0, 0))
    assert nudge.at.replace(tzinfo=None) == datetime(2026, 11, 1, 1, 30)  # noqa: DTZ001
    assert nudge.silent is True
