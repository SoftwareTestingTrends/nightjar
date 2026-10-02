"""Shared fixtures."""

from pathlib import Path

import pytest
from builders import TORONTO

from nightjar.diary import parse_csv
from nightjar.models import Night, User

SAMPLE_CSV = Path(__file__).parents[1] / "data" / "sample_nights.csv"


@pytest.fixture
def toronto_user() -> User:
    return User(name="Sam", timezone=TORONTO)


@pytest.fixture
def sample_nights() -> list[Night]:
    return parse_csv(SAMPLE_CSV.read_text(encoding="utf-8"))
