"""Sleep diary storage (SQLite) and CSV import.

Datetimes are stored in UTC (ISO 8601) so they sort correctly; each night keeps
the IANA time zone the user was in, so local times can always be rebuilt.
"""

import csv
import io
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime, time
from pathlib import Path

from nightjar.models import Night, User, zone

DEFAULT_USER = User(
    name="Sam", timezone="America/Toronto", quiet_start=time(23, 0), quiet_end=time(7, 0)
)
CSV_COLUMNS = {"bedtime", "wake_time", "timezone", "notes"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS nights (
    id INTEGER PRIMARY KEY,
    bedtime_utc TEXT NOT NULL,
    wake_time_utc TEXT NOT NULL,
    timezone TEXT NOT NULL,
    notes TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS user_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT NOT NULL,
    timezone TEXT NOT NULL,
    quiet_start TEXT,
    quiet_end TEXT
);
"""


class Diary:
    """All reads and writes for one user's diary."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        with self._connect() as db:
            db.executescript(SCHEMA)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path)
        try:
            with db:  # commits on success, rolls back on error
                yield db
        finally:
            db.close()

    def add_night(self, night: Night) -> None:
        with self._connect() as db:
            db.execute(
                "INSERT INTO nights (bedtime_utc, wake_time_utc, timezone, notes)"
                " VALUES (?, ?, ?, ?)",
                (
                    _to_utc_text(night.bedtime),
                    _to_utc_text(night.wake_time),
                    night.timezone,
                    night.notes,
                ),
            )

    def add_nights(self, nights: list[Night]) -> int:
        for night in nights:
            self.add_night(night)
        return len(nights)

    def nights(self) -> list[Night]:
        """All nights, newest first."""
        with self._connect() as db:
            rows = db.execute(
                "SELECT id, bedtime_utc, wake_time_utc, timezone, notes"
                " FROM nights ORDER BY bedtime_utc DESC"
            ).fetchall()
        return [
            Night(
                id=row[0],
                bedtime=datetime.fromisoformat(row[1]),
                wake_time=datetime.fromisoformat(row[2]),
                timezone=row[3],
                notes=row[4],
            )
            for row in rows
        ]

    def user(self) -> User:
        with self._connect() as db:
            row = db.execute(
                "SELECT name, timezone, quiet_start, quiet_end FROM user_settings"
            ).fetchone()
        if row is None:
            return DEFAULT_USER
        return User(
            name=row[0],
            timezone=row[1],
            quiet_start=_parse_time(row[2]),
            quiet_end=_parse_time(row[3]),
        )

    def save_user(self, user: User) -> None:
        zone(user.timezone)  # validate before saving
        with self._connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO user_settings VALUES (1, ?, ?, ?, ?)",
                (
                    user.name,
                    user.timezone,
                    _format_time(user.quiet_start),
                    _format_time(user.quiet_end),
                ),
            )


def parse_csv(text: str) -> list[Night]:
    """Parse diary CSV: bedtime,wake_time,timezone,notes (ISO 8601 with UTC offsets)."""
    reader = csv.DictReader(io.StringIO(text))
    missing = CSV_COLUMNS - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"CSV is missing columns: {', '.join(sorted(missing))}")
    nights = []
    for line_number, row in enumerate(reader, start=2):
        try:
            nights.append(
                Night(
                    bedtime=parse_aware(row["bedtime"]),
                    wake_time=parse_aware(row["wake_time"]),
                    timezone=row["timezone"].strip(),
                    notes=(row["notes"] or "").strip(),
                )
            )
        except ValueError as error:
            raise ValueError(f"Line {line_number}: {error}") from error
    return nights


def parse_aware(text: str) -> datetime:
    """Parse an ISO 8601 datetime that must include a UTC offset."""
    value = datetime.fromisoformat(text.strip())
    if value.tzinfo is None:
        raise ValueError(f"{text!r} has no UTC offset")
    return value


def local_input_to_aware(text: str, timezone: str) -> datetime:
    """Turn an HTML datetime-local value ('2026-03-19T23:00') into an aware datetime."""
    return datetime.fromisoformat(text).replace(tzinfo=zone(timezone))


def _to_utc_text(value: datetime) -> str:
    return value.astimezone(UTC).isoformat()


def _parse_time(text: str | None) -> time | None:
    return time.fromisoformat(text) if text else None


def _format_time(value: time | None) -> str | None:
    return value.strftime("%H:%M") if value else None
