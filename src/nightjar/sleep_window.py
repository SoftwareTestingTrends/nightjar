"""The sleep window: when does this user usually go to bed?"""

import statistics
from datetime import time

from nightjar.models import Night

WINDOW_NIGHTS = 14  # look at the most recent two weeks
MIN_NIGHTS = 7  # fewer than this is a cold start: we don't guess
MINUTES_PER_DAY = 24 * 60
NOON = 12 * 60


def usual_bedtime(nights: list[Night]) -> time | None:
    """Median *local* bedtime over the last 14 nights, or None with fewer than 7 nights.

    Each bedtime is read in the time zone the user was in that night, so a
    23:00 bedtime in London counts as 23:00, not 18:00 Toronto time.
    """
    recent = sorted(nights, key=lambda night: night.bedtime, reverse=True)[:WINDOW_NIGHTS]
    if len(recent) <= MIN_NIGHTS:
        return None
    minutes = [minutes_since_noon(night.local_bedtime.time()) for night in recent]
    return time_from_minutes_since_noon(round(statistics.median(minutes)))


def minutes_since_noon(clock_time: time) -> int:
    """Count from noon so bedtimes either side of midnight sit on one line.

    23:30 -> 690 and 00:30 -> 750: one hour apart, not 23 hours.
    """
    return (clock_time.hour * 60 + clock_time.minute - NOON) % MINUTES_PER_DAY


def time_from_minutes_since_noon(minutes: int) -> time:
    total = (minutes + NOON) % MINUTES_PER_DAY
    return time(total // 60, total % 60)
