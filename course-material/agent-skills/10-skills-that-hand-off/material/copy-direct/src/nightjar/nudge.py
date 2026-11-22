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
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    bedtime = usual_bedtime(nights)
    if bedtime is None:
        return None

    user_zone = zone(user.timezone)  # the user's *current* zone (AC2)
    nudge_time = clock_minus(bedtime, WIND_DOWN_LEAD)
    today = now.astimezone(user_zone).date()
    at = at_local_time(today, nudge_time, user_zone)
    if at.astimezone(UTC) <= now.astimezone(UTC):  # compare instants, not wall clocks
        at = at_local_time(today + timedelta(days=1), nudge_time, user_zone)

    return Nudge(
        at=at,
        silent=in_quiet_hours(user, nudge_time),
        text=nudge_text(bedtime, at.date()),
    )


def at_local_time(day: date, clock_time: time, user_zone: ZoneInfo) -> datetime:
    """`clock_time` on `day` in `user_zone`.

    The UTC round trip normalises wall times that DST skips (02:30 on
    spring-forward day becomes 03:30) so the result is a real instant.
    """
    wall_clock = datetime.combine(day, clock_time, tzinfo=user_zone)
    return wall_clock.astimezone(UTC).astimezone(user_zone)


def clock_minus(clock_time: time, delta: timedelta) -> time:
    """Time-of-day arithmetic that wraps around midnight (00:10 - 45 min = 23:25)."""
    start = datetime.combine(date(2000, 1, 2), clock_time, tzinfo=UTC)
    return (start - delta).time()


def in_quiet_hours(user: User, clock_time: time) -> bool:
    start, end = user.quiet_start, user.quiet_end
    if start is None or end is None:
        return False
    if start <= end:
        return start <= clock_time < end
    return clock_time >= start or clock_time < end  # window wraps midnight


def nudge_text(bedtime: time, day: date) -> str:
    """Pick approved copy from the claims register (AC4); it varies by day."""
    templates = load_register()["nudge_copy"]
    template = templates[day.toordinal() % len(templates)]
    return template.format(bedtime=bedtime.strftime("%H:%M"))
