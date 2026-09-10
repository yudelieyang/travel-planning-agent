import pytest

from app.agent.requirements import parse_requirements
from app.core.budget import BudgetScope
from app.tools.contracts import BudgetInput, CostItem
from app.tools.mock import calculate_budget


@pytest.mark.parametrize(
    "suffix,expected",
    [
        ("", BudgetScope.UNKNOWN),
        (" total", BudgetScope.TOTAL_TRIP),
        (" per person", BudgetScope.PER_PERSON),
        (" per traveler", BudgetScope.PER_PERSON),
        (" for the whole trip", BudgetScope.TOTAL_TRIP),
    ],
)
@pytest.mark.parametrize("party", ["", " for 2 travelers"])
def test_explicit_scope_only(suffix, expected, party):
    req = parse_requirements(f"Plan a 2-day trip to Boston{party} under $100{suffix}.")
    assert req.budget_amount == 100
    assert req.budget_scope == expected


@pytest.mark.parametrize(
    "scope,travelers,expected",
    [
        ("UNKNOWN", None, None),
        ("UNKNOWN", 2, None),
        ("TOTAL_TRIP", None, None),
        ("TOTAL_TRIP", 2, False),
        ("PER_PERSON", None, True),
        ("PER_PERSON", 2, True),
    ],
)
def test_budget_comparison_respects_scope(scope, travelers, expected):
    budget = calculate_budget(
        BudgetInput(
            items=[CostItem(category="food", amount=60)],
            travelers=travelers,
            limit=100,
            budget_scope=scope,
        )
    ).data
    assert budget.within_budget is expected
    assert budget.budget_scope == scope
    assert budget.per_traveler_cost == 60
