"""User settings validation: the wind-down lead (S-114)."""

import pytest
from builders import TORONTO

from nightjar.models import User


@pytest.mark.parametrize("lead", [30, 45, 60])
def test_T_114_7_allowed_leads_are_accepted(lead):
    user = User(name="Sam", timezone=TORONTO, wind_down_lead_minutes=lead)
    assert user.wind_down_lead_minutes == lead


@pytest.mark.parametrize("lead", [50, 0, -5, 45.0, True])
def test_T_114_7_any_other_lead_is_rejected(lead):
    with pytest.raises(ValueError):
        User(name="Sam", timezone=TORONTO, wind_down_lead_minutes=lead)
