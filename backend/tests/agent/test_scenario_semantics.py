"""Offline scenario tests for observable planning semantics and explicit capability gaps."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.agent.execution import ViolationCode
from app.agent.itinerary import Activity, DayPlan, Itinerary, validate_itinerary
from app.agent.requirements import ConstraintStrength, TravelRequirements, parse_requirements
from app.agent.service import TravelService
from app.core.budget import BudgetScope
from app.tools.contracts import BudgetInput, CostItem, ToolResult, ToolStatus
from app.tools.mock import calculate_budget, run_tool

SCENARIOS = json.loads(
    (Path(__file__).parents[3] / "evals/datasets/scenario_semantics_v1.json").read_text("utf-8")
)["cases"]
HAPPY, GOLDEN = SCENARIOS


def test_happy_path_preserves_requirements_and_completes_valid_itinerary():
    response = TravelService().plan(HAPPY["query"])
    expected = HAPPY["expected"]

    assert response.status == expected["status"]
    for field in ("destination", "duration_days", "travelers", "budget_amount", "budget_scope"):
        assert getattr(response.requirements, field) == expected[field]
    assert response.requirements.interests == expected["interests"]
    assert response.requirements.food_preferences == expected["food_preferences"]
    assert response.execution.planner_invoked is True
    assert {tool.tool_name for tool in response.execution.tools} == {
        "search_attractions",
        "search_hotels",
        "search_restaurants",
        "search_transport",
        "calculate_budget",
    }
    assert all(tool.status == "SUCCESS" for tool in response.execution.tools)
    assert response.execution.validation.performed is True
    assert response.execution.validation.outcome == "passed"
    assert response.itinerary is not None
    assert response.budget is not None
    assert response.budget.estimated_total_cost <= response.requirements.budget_amount


def test_preserves_specific_food_preference_in_recruiter_golden_case():
    requirements = parse_requirements(GOLDEN["query"])
    assert requirements.food_preferences == GOLDEN["expected"]["food_preferences"]


def test_preserves_budget_utilization_objective_in_recruiter_golden_case():
    requirements = parse_requirements(GOLDEN["query"])
    assert requirements.objective == GOLDEN["expected"]["objective"]


def test_marks_around_budget_as_soft_while_plain_limit_remains_hard_default():
    hard = parse_requirements("Plan a 3-day trip to Boston. I must stay under $800.")
    soft = parse_requirements("Plan a 3-day trip to Boston. I would prefer to stay around $800.")

    assert hard.budget_amount == soft.budget_amount == 800
    assert "approximate budget" not in hard.constraints
    assert "approximate budget" in soft.constraints


@pytest.mark.parametrize(
    "query,missing",
    [
        ("I want a relaxing 3-day vacation with good food.", ["destination"]),
        ("Plan a trip to Boston.", ["duration"]),
    ],
)
def test_missing_required_information_triggers_targeted_clarification(query, missing):
    response = TravelService().plan(query)

    assert response.status == "needs_clarification"
    assert response.missing_fields == missing
    assert response.execution.planner_invoked is False
    assert response.execution.tools == []
    assert response.clarification_question


def test_conflicting_luxury_request_fails_hard_budget_validation():
    response = TravelService().plan(
        "Plan a 3-day trip to New York City for 1 traveler under $150 total. "
        "Stay in a luxury hotel and eat at expensive restaurants."
    )

    assert response.status == "error"
    assert response.itinerary is response.budget is None
    assert response.execution.validation.outcome == "failed"
    assert response.execution.validation.violations[0].code == ViolationCode.HARD_BUDGET_EXCEEDED


@pytest.mark.parametrize("limit,within", [(999.99, False), (1000, True), (1000.01, True), (0, False)])
def test_budget_boundaries_use_exact_decimal_comparison(limit, within):
    summary = calculate_budget(
        BudgetInput(
            items=[CostItem(category="food", amount=1000)],
            travelers=1,
            limit=limit,
            budget_scope=BudgetScope.TOTAL_TRIP,
        )
    ).data

    assert summary is not None
    assert summary.within_budget is within
    assert summary.comparison_cost == pytest.approx(1000)
    assert summary.remaining_budget == pytest.approx(limit - 1000)


@pytest.mark.parametrize(
    "query",
    [
        "Plan a -3-day trip to Boston.",
        "Plan a 0-day trip to Boston.",
        "Plan a 3-day trip to Boston for -0 travelers.",
        "Plan a 3-day trip to Boston for 1000 travelers.",
        "Plan a 3-day trip to Boston under $-500.",
    ],
)
def test_invalid_numeric_input_is_rejected_at_requirements_boundary(query):
    with pytest.raises(ValidationError):
        parse_requirements(query)


def test_invalid_textual_budget_is_not_silently_dropped():
    with pytest.raises(ValueError, match="Budget amount must be numeric"):
        TravelService().plan("Plan a 3-day trip to Boston with budget abc.")


def test_traveler_count_scales_group_cost_without_changing_per_traveler_cost():
    one = TravelService().plan("Plan a 2-day trip to Boston for 1 traveler.").budget
    two = TravelService().plan("Plan a 2-day trip to Boston for 2 travelers.").budget

    assert one is not None and two is not None
    assert two.per_traveler_cost == pytest.approx(one.per_traveler_cost)
    assert two.estimated_total_cost == pytest.approx(one.estimated_total_cost * 2)
    assert two.breakdown == {
        category: pytest.approx(amount * 2) for category, amount in one.breakdown.items()
    }


@pytest.mark.parametrize("days,hotel_nights", [(1, 0), (2, 1), (3, 2)])
def test_duration_uses_days_minus_one_hotel_nights(days, hotel_nights):
    response = TravelService().plan(f"Plan a {days}-day trip to Boston for 1 traveler.")

    assert response.itinerary is not None
    assert sum(activity.category == "hotel" for day in response.itinerary.daily_plan for activity in day.activities) == hotel_nights


def test_transport_preferences_and_rental_car_avoidance_are_preserved_for_planner():
    requirements = parse_requirements(
        "Plan a 3-day trip to Boston. I prefer walking and public transit. Avoid rental cars."
    )

    assert requirements.transport_preferences == ["walking", "public transit"]
    assert "no rental car" in requirements.constraints


def test_preserves_halal_restriction_as_a_food_requirement():
    assert "halal" in parse_requirements("Plan a 3-day trip to Boston. I need halal food.").food_preferences


@pytest.mark.xfail(
    reason="No location, distance, travel-time, or geographic-feasibility validator exists in this mock slice.",
    strict=False,
)
def test_rejects_geographically_impossible_daily_schedule():
    response = TravelService().plan("Plan a 3-day trip to Boston for 1 traveler.")
    assert any("geographic" in error.lower() for error in response.errors)


def test_tool_exception_is_exposed_as_error_without_faking_partial_success():
    def restaurant_failure(request):
        if request.tool_name == "search_restaurants":
            raise TimeoutError("fixture timeout")
        return run_tool(request)

    response = TravelService(tool_runner=restaurant_failure).plan("Plan a 2-day trip to Boston.")

    assert response.status == "error"
    assert response.itinerary is None and response.budget is None
    tools = {tool.tool_name: tool for tool in response.execution.tools}
    assert tools["search_restaurants"].status == "ERROR"
    assert tools["calculate_budget"].status == "SKIPPED"
    assert response.execution.validation.reason == "prior_errors"


def test_partial_tool_data_is_distinct_from_tool_exception_but_still_not_success():
    def no_restaurants(request):
        if request.tool_name == "search_restaurants":
            return ToolResult(
                tool_name=request.tool_name,
                status=ToolStatus.NO_RESULTS,
                source="mock",
            )
        return run_tool(request)

    response = TravelService(tool_runner=no_restaurants).plan("Plan a 2-day trip to Boston.")

    assert response.status == "error"
    tools = {tool.tool_name: tool for tool in response.execution.tools}
    assert tools["search_restaurants"].status == "NO_RESULTS"
    assert tools["calculate_budget"].status == "SKIPPED"


def test_unsupported_destination_does_not_hallucinate_a_complete_itinerary():
    response = TravelService().plan("Plan a 2-day trip to Atlantis.")

    assert response.status == "error"
    assert response.itinerary is None and response.budget is None
    assert all(tool.status == "NO_RESULTS" for tool in response.execution.tools[:4])


def test_validator_rejects_hard_budget_violation_directly():
    budget = calculate_budget(
        BudgetInput(
            items=[CostItem(category="food", amount=100)],
            travelers=1,
            limit=99,
            budget_scope=BudgetScope.TOTAL_TRIP,
        )
    ).data
    itinerary = Itinerary(
        destination="Boston",
        days=1,
        estimated_total_cost=100,
        daily_plan=[
            DayPlan(
                day_number=1,
                estimated_cost=100,
                activities=[Activity(name="Meal", category="food", estimated_cost=100)],
            )
        ],
    )

    requirements = TravelRequirements(
        destination="Boston",
        duration_days=1,
        travelers=1,
        budget_amount=99,
        budget_scope=BudgetScope.TOTAL_TRIP,
        budget_constraint_strength=ConstraintStrength.HARD,
    )

    result = validate_itinerary(itinerary, budget, requirements)

    assert not result.is_valid
    assert result.violations[0].code == ViolationCode.HARD_BUDGET_EXCEEDED
    assert result.violations[0].expected == 99
    assert result.violations[0].actual == 100
    assert result.violations[0].excess == 1


def test_validation_failure_triggers_a_second_planner_attempt():
    response = TravelService().plan("Plan a 2-day trip to Boston for 2 travelers under $400 total.")

    assert response.status == "success"
    assert response.execution.replan_attempts == 1
    assert [stage.name for stage in response.execution.stages if stage.sequence] == [
        "preflight",
        "planner",
        "tools",
        "validation",
        "replan",
        "planner",
        "tools",
        "validation",
        "finalization",
    ]


@pytest.mark.xfail(
    reason="TravelService is stateless; itinerary revisions cannot preserve prior-day selections.",
    strict=False,
)
def test_multiturn_revision_preserves_unchanged_days():
    assert TravelService().plan("Keep Day 2 unchanged, but replace Day 1 with outdoor activities.").status == "success"


def test_parser_accepts_equivalent_casual_trip_request():
    formal = parse_requirements("Plan a 3-day trip to Boston for one traveler under $1000.")
    casual = parse_requirements("Boston, 3 days, just me, max 1k.")
    assert (casual.destination, casual.duration_days, casual.travelers) == (
        formal.destination,
        formal.duration_days,
        formal.travelers,
    )
    assert [(item.scope, item.value) for item in casual.requirements_v2.constraints] == [
        (item.scope, item.value) for item in formal.requirements_v2.constraints
    ]


def test_parser_ignores_irrelevant_context_and_extracts_trip_fields():
    requirements = parse_requirements(
        "I'm graduating soon and tired. Anyway, can you plan a 3-day Boston trip for under $900? I like museums."
    )
    assert requirements.destination == "Boston"
    assert requirements.duration_days == 3
    assert requirements.budget_amount == 900
    assert requirements.interests == ["museums"]


def test_later_budget_constraint_overrides_earlier_statement():
    requirements = parse_requirements(
        "Plan a 3-day trip to Boston. My budget is $1000. Actually, don't spend more than $700."
    )
    assert requirements.budget_amount == 700


def test_natural_language_columbus_request_completes_end_to_end():
    response = TravelService().plan(
        "Plan a 3-day trip to Columbus. I like zoos and I love fried chicken. "
        "I only want to spend $1300 on the trip."
    )

    assert response.status == "success"
    assert response.requirements.destination == "Columbus"
    assert response.requirements.duration_days == 3
    assert response.requirements.interests == ["zoo", "food"]
    assert response.requirements.food_preferences == ["fried chicken"]
    assert response.requirements.budget_amount == 1300
    assert response.requirements.currency == "USD"
    assert response.requirements.budget_scope == BudgetScope.TOTAL_TRIP
    assert response.requirements.budget_constraint_strength == ConstraintStrength.UNSPECIFIED
    assert all(tool.status == "SUCCESS" for tool in response.execution.tools)
    assert response.itinerary is not None
    assert response.execution.validation.outcome == "passed"


@pytest.mark.xfail(
    reason="This product supports full-trip planning only; attraction-only requests have no dedicated tool-selection mode.",
    strict=False,
)
def test_attraction_only_request_selects_no_unneeded_trip_tools():
    response = TravelService().plan("Find me three attractions in Boston.")
    assert [tool.tool_name for tool in response.execution.tools] == ["search_attractions"]


def test_same_fixture_has_a_stable_semantic_contract_across_runs():
    first = TravelService().plan(HAPPY["query"])
    second = TravelService().plan(HAPPY["query"])

    assert first.model_dump(exclude={"execution"}) == second.model_dump(exclude={"execution"})
    assert first.execution.model_dump(exclude={"run_id", "latency_ms"}) == second.execution.model_dump(
        exclude={"run_id", "latency_ms"}
    )
