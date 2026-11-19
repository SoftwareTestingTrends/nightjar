"""Story S-114: a gentle wind-down nudge before the user's usual bedtime."""

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from nightjar.claims import load_register
from nightjar.models import Night, User, zone
from nightjar.sleep_window import usual_bedtime

WIND_DOWN_LEAD = timedelta(minutes=45)


@dataclass(frozen=True)
class Nudge:
    at: datetime  # aware, in the user's current time zone
    silent: bool  # True during quiet hours: deliver without sound, don't skip
    text: str


def next_nudge(user: User, nights: list[Night], now: datetime) -> Nudge | None:
    """The next wind-down nudge after `now`, or None on a cold start (< 7 nights)."""
    raise NotImplementedError


def at_local_time(day: date, clock_time: time, user_zone: ZoneInfo) -> datetime:
    """`clock_time` on `day` in `user_zone`.

    The UTC round trip normalises wall times that DST skips (02:30 on
    spring-forward day becomes 03:30) so the result is a real instant.
    """
    raise NotImplementedError


def clock_minus(clock_time: time, delta: timedelta) -> time:
    """Time-of-day arithmetic that wraps around midnight (00:10 - 45 min = 23:25)."""
    raise NotImplementedError


def in_quiet_hours(user: User, clock_time: time) -> bool:
    raise NotImplementedError


def nudge_text(bedtime: time, day: date) -> str:
    """Pick approved copy from the claims register (AC4); it varies by day."""
    raise NotImplementedError
