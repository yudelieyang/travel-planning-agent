import pytest

from app.agent.requirements import RequirementStatus, TravelRequirements, assess_requirements


@pytest.mark.parametrize(
    "values,missing",
    [
        ({}, ["destination", "duration"]),
        ({"destination": "   ", "duration_days": 3}, ["destination"]),
        ({"destination": "Boston"}, ["duration"]),
        ({"destination": "Boston", "start_date": "2026-10-01"}, ["duration"]),
        ({"destination": "Boston", "duration_days": 2}, []),
        ({"destination": "Boston", "start_date": "2026-10-01", "end_date": "2026-10-02"}, []),
    ],
)
def test_preflight_minimum_fields(values, missing):
    result = assess_requirements(TravelRequirements(**values))
    assert result.missing_fields == missing
    expected = RequirementStatus.INSUFFICIENT if missing else RequirementStatus.SUFFICIENT
    assert result.status == expected
