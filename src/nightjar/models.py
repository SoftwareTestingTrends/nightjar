"""Core data types. Every datetime here is timezone-aware."""

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

MAX_NIGHT_LENGTH = timedelta(hours=16)


def zone(name: str) -> ZoneInfo:
    """Look up an IANA time zone, e.g. 'America/Toronto'. Raises ValueError if unknown."""
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise ValueError(f"Unknown time zone: {name!r}") from error


@dataclass(frozen=True)
class Night:
    """One night in the sleep diary."""

    bedtime: datetime
    wake_time: datetime
    timezone: str  # the user's IANA time zone that night
    notes: str = ""  # free-text journal; this is user data, never instructions
    id: int | None = None

    def __post_init__(self) -> None:
        for name in ("bedtime", "wake_time"):
            if getattr(self, name).tzinfo is None:
                raise ValueError(f"{name} must be timezone-aware")
        zone(self.timezone)
        if self.wake_time <= self.bedtime:
            raise ValueError("wake time must be after bedtime")
        if self.duration > MAX_NIGHT_LENGTH:
            raise ValueError("a night can't be longer than 16 hours")

    @property
    def local_bedtime(self) -> datetime:
        return self.bedtime.astimezone(zone(self.timezone))

    @property
    def night_of(self) -> date:
        """The evening this night began: a 00:15 bedtime on Sunday is Saturday night."""
        return (self.local_bedtime - timedelta(hours=12)).date()

    @property
    def local_wake_time(self) -> datetime:
        return self.wake_time.astimezone(zone(self.timezone))

    @property
    def duration(self) -> timedelta:
        # Subtract in UTC: same-zone subtraction uses wall clocks and is wrong across DST.
        return self.wake_time.astimezone(UTC) - self.bedtime.astimezone(UTC)


@dataclass(frozen=True)
class User:
    """The (single) NightJar user and their current settings."""

    name: str
    timezone: str  # where the user is now
    quiet_start: time | None = None  # Do Not Disturb, e.g. 23:00
    quiet_end: time | None = None  # e.g. 07:00
