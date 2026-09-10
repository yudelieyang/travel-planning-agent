from datetime import date

import pytest
from pydantic import ValidationError

from app.agent.requirements import TravelRequirements, parse_requirements

QUERY = "Plan a 3-day trip to New York City under $1000. I like museums and food."


def test_parse_vertical_slice_without_inventing_travelers():
    requirements = parse_requirements(QUERY)
    assert requirements.destination == "New York City"
    assert requirements.duration_days == 3
    assert requirements.budget_amount == 1000
    assert requirements.currency == "USD"
    assert requirements.interests == ["museums", "food"]
    assert requirements.travelers is None
    assert requirements.origin is None
    assert requirements.start_date is None


def test_no_invented_requirements():
    requirements = parse_requirements("Plan a trip for me.")
    assert requirements.destination is None
    assert requirements.duration_days is None
    assert requirements.budget_amount is None
    assert requirements.travelers is None


def test_dates_origin_preferences_and_travelers():
    r = parse_requirements(
        "Travel from Boston to NYC from 2026-10-01 to 2026-10-03 "
        "for 2 travelers under USD 1,000. Vegetarian food and quiet hotels."
    )
    assert r.origin == "Boston"
    assert r.destination == "New York City"
    assert r.start_date == date(2026, 10, 1)
    assert r.trip_days == 3
    assert r.travelers == 2
    assert r.food_preferences == ["vegetarian"]
    assert r.hotel_preferences == ["quiet"]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"duration_days": 0},
        {"travelers": 0},
        {"budget_amount": -1},
        {"budget_amount": float("nan")},
        {"start_date": "2026-10-03", "end_date": "2026-10-01"},
        {"start_date": "2026-10-01", "end_date": "2026-10-03", "duration_days": 2},
    ],
)
def test_invalid_requirements(kwargs):
    with pytest.raises(ValidationError):
        TravelRequirements(**kwargs)
