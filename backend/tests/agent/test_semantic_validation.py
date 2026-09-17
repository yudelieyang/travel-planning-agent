"""Deterministic hard-budget validation boundaries."""

import pytest

from app.agent.execution import ViolationCode
from app.agent.itinerary import Activity, DayPlan, Itinerary, validate_itinerary
from app.agent.requirements import (
    BudgetConstraint,
    ConstraintScope,
    ConstraintStrength,
    OptimizationObjective,
    RequirementsV2,
    TravelRequirements,
)
from app.core.budget import BudgetScope
from app.tools.contracts import BudgetInput, CostItem
from app.tools.mock import calculate_budget


def validation_result(
    actual: float,
    limit: float,
    strength: ConstraintStrength = ConstraintStrength.HARD,
    objective: OptimizationObjective | None = None,
):
    requirements = TravelRequirements(
        destination="Boston",
        duration_days=1,
        travelers=1,
        budget_amount=limit,
        budget_scope=BudgetScope.TOTAL_TRIP,
        budget_constraint_strength=strength,
        objective=objective,
    )
    budget = calculate_budget(
        BudgetInput(
            items=[CostItem(category="food", amount=actual)],
            travelers=1,
            limit=limit,
            budget_scope=BudgetScope.TOTAL_TRIP,
        )
    ).data
    itinerary = Itinerary(
        destination="Boston",
        days=1,
        estimated_total_cost=actual,
        daily_plan=[
            DayPlan(
                day_number=1,
                estimated_cost=actual,
                activities=[Activity(name="Meal", category="food", estimated_cost=actual)],
            )
        ],
    )
    return validate_itinerary(itinerary, budget, requirements)


@pytest.mark.parametrize("actual", [799.99, 800])
def test_hard_budget_at_or_below_limit_passes(actual):
    result = validation_result(actual, 800)

    assert result.is_valid
    assert result.violations == []


def test_hard_budget_over_limit_returns_structured_violation():
    result = validation_result(800.01, 800)

    assert not result.is_valid
    assert result.errors == ["Hard budget exceeded"]
    assert result.violations[0].code == ViolationCode.HARD_BUDGET_EXCEEDED
    assert result.violations[0].model_dump(mode="json") == {
        "code": "HARD_BUDGET_EXCEEDED",
        "category": "budget",
        "expected": 800.0,
        "actual": 800.01,
        "excess": 0.01,
        "message": "Hard budget exceeded",
    }


def test_soft_budget_overage_does_not_fail_validation():
    result = validation_result(900, 800, ConstraintStrength.SOFT)

    assert result.is_valid
    assert result.violations == []


def test_objective_does_not_create_a_hard_validation_failure():
    result = validation_result(100, 800, objective=OptimizationObjective.MAXIMIZE_BUDGET_UTILIZATION)

    assert result.is_valid
    assert result.violations == []


def test_legacy_unspecified_strength_does_not_hard_fail():
    result = validation_result(900, 800, ConstraintStrength.UNSPECIFIED)

    assert result.is_valid
    assert result.violations == []


def test_hotel_total_constraint_uses_the_existing_hotel_cost_breakdown():
    requirements = TravelRequirements(
        destination="Boston",
        duration_days=2,
        travelers=1,
        requirements_v2=RequirementsV2(
            constraints=[BudgetConstraint(scope=ConstraintScope.HOTEL_TOTAL, value=99)]
        ),
    )
    budget = calculate_budget(
        BudgetInput(items=[CostItem(category="hotel", amount=100)], travelers=1)
    ).data
    itinerary = Itinerary(
        destination="Boston",
        days=2,
        estimated_total_cost=100,
        daily_plan=[
            DayPlan(day_number=1, estimated_cost=100, activities=[Activity(name="Hotel", category="hotel", estimated_cost=100)]),
            DayPlan(day_number=2, estimated_cost=0, activities=[]),
        ],
    )

    result = validate_itinerary(itinerary, budget, requirements)

    assert result.violations[0].code == ViolationCode.HOTEL_BUDGET_EXCEEDED
    assert (result.violations[0].expected, result.violations[0].actual) == (99, 100)
