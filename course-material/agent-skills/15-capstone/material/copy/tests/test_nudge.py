"""Story S-114: bedtime nudge. Test ids (T-114-n) are listed in docs/traceability.md."""

from datetime import UTC, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest
from builders import LONDON, TORONTO, nights_at

from nightjar.claims import check_text, load_register
from nightjar.models import User
from nightjar.nudge import next_nudge

TORONTO_TZ, LONDON_TZ = ZoneInfo(TORONTO), ZoneInfo(LONDON)
USUAL_23_00 = nights_at("23:00", 7, first_night="2026-02-01")  # usual bedtime 23:00


def local(tz: ZoneInfo, *args: int) -> datetime:
    return datetime(*args, tzinfo=tz)


# AC1: 45 minutes before the usual bedtime, in the user's current local time
def test_T_114_1_nudge_is_45_minutes_before_usual_bedtime(toronto_user):
    nudge = next_nudge(toronto_user, USUAL_23_00, now=local(TORONTO_TZ, 2026, 3, 20, 12, 0))
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 20, 22, 15)
    assert nudge.at.tzinfo == TORONTO_TZ


def test_T_114_1_after_todays_nudge_time_the_next_nudge_is_tomorrow(toronto_user):
    nudge = next_nudge(toronto_user, USUAL_23_00, now=local(TORONTO_TZ, 2026, 3, 20, 22, 30))
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 21, 22, 15)


def test_T_114_1_now_can_be_given_in_any_zone(toronto_user):
    now_utc = datetime(2026, 3, 20, 16, 0, tzinfo=UTC)  # 12:00 in Toronto
    nudge = next_nudge(toronto_user, USUAL_23_00, now=now_utc)
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 21, 2, 15, tzinfo=UTC)


# AC2: after a time zone change, the nudge follows the new local time
def test_T_114_2_after_moving_to_london_nudge_is_at_london_local_time():
    user = User(name="Sam", timezone=LONDON)
    nudge = next_nudge(user, USUAL_23_00, now=local(LONDON_TZ, 2026, 3, 20, 9, 0))
    assert nudge.at == local(LONDON_TZ, 2026, 3, 20, 22, 15)
    assert nudge.at.astimezone(UTC).hour == 22  # London is on GMT in March


def test_T_114_2_zone_change_in_the_evening_applies_from_the_next_day():
    # It's 20:00 in Toronto = 00:00 in London on the 21st. Sam has just landed in London.
    user = User(name="Sam", timezone=LONDON)
    nudge = next_nudge(user, USUAL_23_00, now=local(TORONTO_TZ, 2026, 3, 20, 20, 0))
    assert nudge.at == local(LONDON_TZ, 2026, 3, 21, 22, 15)


# AC3: quiet hours make the nudge silent, never skipped
def test_T_114_3_nudge_during_quiet_hours_is_silent_not_skipped():
    user = User(name="Sam", timezone=TORONTO, quiet_start=time(22, 0), quiet_end=time(7, 0))
    nudge = next_nudge(user, USUAL_23_00, now=local(TORONTO_TZ, 2026, 3, 20, 12, 0))
    assert nudge is not None
    assert nudge.silent is True
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 20, 22, 15)


def test_T_114_3_nudge_outside_quiet_hours_is_not_silent():
    user = User(name="Sam", timezone=TORONTO, quiet_start=time(23, 0), quiet_end=time(7, 0))
    assert next_nudge(user, USUAL_23_00, local(TORONTO_TZ, 2026, 3, 20, 12)).silent is False


def test_T_114_3_daytime_quiet_hours_that_do_not_wrap_midnight():
    user = User(name="Sam", timezone=TORONTO, quiet_start=time(21, 0), quiet_end=time(22, 30))
    assert next_nudge(user, USUAL_23_00, local(TORONTO_TZ, 2026, 3, 20, 12)).silent is True


# AC4: nudge copy comes from the claims register
def test_T_114_4_nudge_text_is_approved_copy_from_the_claims_register(toronto_user):
    allowed = [t.format(bedtime="23:00") for t in load_register()["nudge_copy"]]
    for day in range(1, 8):
        nudge = next_nudge(toronto_user, USUAL_23_00, local(TORONTO_TZ, 2026, 3, day, 12))
        assert nudge.text in allowed
        assert check_text(nudge.text) == []


def test_T_114_4_every_nudge_template_uses_an_approved_phrase_and_is_claims_clean():
    register = load_register()
    for template in register["nudge_copy"]:
        assert any(phrase in template.lower() for phrase in register["approved_phrases"])
        assert check_text(template) == []


# Edge: cold start
def test_T_114_5_no_nudge_with_fewer_than_7_nights(toronto_user):
    six_nights = nights_at("23:00", 6)
    assert next_nudge(toronto_user, six_nights, local(TORONTO_TZ, 2026, 3, 20, 12)) is None


# Daylight-saving transitions
def test_T_114_6_toronto_spring_forward_day(toronto_user):
    # Clocks jump 02:00 -> 03:00 on Sun 8 March 2026; the evening is on EDT (UTC-4).
    nudge = next_nudge(toronto_user, USUAL_23_00, local(TORONTO_TZ, 2026, 3, 8, 8, 0))
    assert nudge.at == local(TORONTO_TZ, 2026, 3, 8, 22, 15)
    assert nudge.at.utcoffset() == timedelta(hours=-4)
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 9, 2, 15, tzinfo=UTC)


def test_T_114_6_toronto_rolling_to_tomorrow_across_fall_back(toronto_user):
    # Sat 31 Oct 23:00 EDT; the next nudge is Sun 1 Nov after clocks fall back to EST.
    nudge = next_nudge(toronto_user, USUAL_23_00, local(TORONTO_TZ, 2026, 10, 31, 23, 0))
    assert nudge.at == local(TORONTO_TZ, 2026, 11, 1, 22, 15)
    assert nudge.at.astimezone(UTC) == datetime(2026, 11, 2, 3, 15, tzinfo=UTC)


def test_T_114_6_london_spring_forward():
    user = User(name="Sam", timezone=LONDON)
    nudge = next_nudge(user, USUAL_23_00, local(LONDON_TZ, 2026, 3, 28, 23, 0))
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 29, 21, 15, tzinfo=UTC)  # BST


def test_T_114_6_london_fall_back():
    user = User(name="Sam", timezone=LONDON)
    nudge = next_nudge(user, USUAL_23_00, local(LONDON_TZ, 2026, 10, 24, 23, 0))
    assert nudge.at.astimezone(UTC) == datetime(2026, 10, 25, 22, 15, tzinfo=UTC)  # GMT


def test_T_114_6_nudge_time_skipped_by_dst_moves_forward_an_hour(toronto_user):
    # Usual bedtime 02:45 -> nudge 02:00, which doesn't exist on 8 March in Toronto.
    late_nights = nights_at("02:45", 7, first_night="2026-02-01")
    nudge = next_nudge(toronto_user, late_nights, local(TORONTO_TZ, 2026, 3, 7, 12, 0))
    assert nudge.at.astimezone(UTC) == datetime(2026, 3, 8, 7, 0, tzinfo=UTC)  # 03:00 EDT


def test_naive_now_is_rejected(toronto_user):
    with pytest.raises(ValueError, match="timezone-aware"):
        next_nudge(toronto_user, USUAL_23_00, datetime(2026, 3, 20, 12, 0))  # noqa: DTZ001
