"""Builders for test data. Every datetime a test builds is timezone-aware."""

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from nightjar.models import Night

TORONTO = "America/Toronto"
LONDON = "Europe/London"


def night(
    night_of: str, bedtime: str, tz: str = TORONTO, hours: float = 8, notes: str = ""
) -> Night:
    """A night that starts on the evening of `night_of` (a bedtime after midnight rolls over)."""
    clock = time.fromisoformat(bedtime)
    day = date.fromisoformat(night_of) + timedelta(days=1 if clock.hour < 12 else 0)
    start = datetime.combine(day, clock, tzinfo=ZoneInfo(tz))
    return Night(bedtime=start, wake_time=start + timedelta(hours=hours), timezone=tz, notes=notes)


def nights_at(bedtime: str, count: int, first_night: str = "2026-03-01", tz: str = TORONTO):
    """`count` consecutive nights, all with the same local bedtime."""
    start = date.fromisoformat(first_night)
    return [night((start + timedelta(days=i)).isoformat(), bedtime, tz) for i in range(count)]
