"""Bounded, structured hard-budget repair tests."""

from unittest.mock import Mock

from app.agent import graph as graph_module
from app.agent.execution import ViolationCode
from app.agent.itinerary import ItineraryValidationResult, validate_itinerary
from app.agent.planner import DeterministicTestPlanner
from app.agent.service import TravelService
from app.tools.contracts import SearchInput, ToolResult, ToolStatus
from app.tools.mock import run_tool


class FeedbackPlanner(DeterministicTestPlanner):
    def __init__(self):
        self.feedback = []

    def plan(self, requirements, feedback=None):
        self.feedback.append(feedback)
        return super().plan(requirements, feedback)


def reached_names(response):
    return [stage.name for stage in response.execution.stages if stage.sequence]


def test_hard_budget_violation_replans_with_structured_feedback_and_revalidates(monkeypatch):
    planner = FeedbackPlanner()
    validator = Mock(wraps=validate_itinerary)
    monkeypatch.setattr(graph_module, "validate_itinerary", validator)

    response = TravelService(planner=planner).plan(
        "Plan a 2-day trip to Boston for 2 travelers under $400 total."
    )

    feedback = planner.feedback[1]
    assert response.status == "success"
    assert response.execution.replan_attempts == 1
    assert len(planner.feedback) == validator.call_count == 2
    assert planner.feedback[0] is None
    assert feedback.attempt == 1
    assert feedback.violations[0].code == ViolationCode.HARD_BUDGET_EXCEEDED
    assert (feedback.violations[0].expected, feedback.violations[0].actual) == (400, 446)
    assert feedback.previous_itinerary.estimated_total_cost == 446
    assert response.itinerary.estimated_total_cost == response.budget.estimated_total_cost == 392
    assert response.execution.repair is not None
    assert response.execution.repair.attempt == response.execution.repair.maximum_attempts == 1
    assert response.execution.repair.initial_total == 446
    assert response.execution.repair.final_total == 392
    assert response.execution.repair.savings == 54
    assert response.execution.repair.final_outcome == "passed"
    assert response.execution.repair.trigger[0].code == ViolationCode.HARD_BUDGET_EXCEEDED
    assert response.execution.repair.changes
    assert response.itinerary.daily_plan[1].activities[0].name != (
        feedback.previous_itinerary.daily_plan[1].activities[0].name
    )
    assert reached_names(response).count("planner") == 2
    assert reached_names(response).count("validation") == 2


def test_unrecoverable_hard_budget_stops_after_one_replan():
    planner = FeedbackPlanner()
    response = TravelService(planner=planner).plan(
        "Plan a 2-day trip to Boston for 2 travelers under $50 total."
    )

    assert response.status == "error"
    assert response.execution.replan_attempts == 1
    assert len(planner.feedback) == 2
    assert response.execution.validation.outcome == "failed"
    assert response.execution.validation.violations[0].code == ViolationCode.HARD_BUDGET_EXCEEDED
    assert response.execution.repair is not None
    assert response.execution.repair.maximum_attempts == 1
    assert response.execution.repair.final_outcome == "failed"
    assert response.execution.repair.final_total == 392
    assert reached_names(response).count("planner") == 2
    assert reached_names(response).count("validation") == 2


def test_initially_valid_plan_does_not_replan():
    planner = FeedbackPlanner()
    response = TravelService(planner=planner).plan(
        "Plan a 2-day trip to Boston for 2 travelers under $500 total."
    )

    assert response.status == "success"
    assert response.execution.replan_attempts == 0
    assert planner.feedback == [None]
    assert reached_names(response).count("validation") == 1


def test_soft_budget_and_objective_do_not_trigger_replan():
    soft = FeedbackPlanner()
    objective = FeedbackPlanner()

    soft_response = TravelService(planner=soft).plan(
        "Plan a 2-day trip to Boston for 2 travelers around $50 total."
    )
    objective_response = TravelService(planner=objective).plan(
        "Plan a 2-day trip to Boston for 2 travelers under $500 total. "
        "Spend as much of the budget as reasonably possible."
    )

    assert soft_response.status == objective_response.status == "success"
    assert soft_response.execution.replan_attempts == objective_response.execution.replan_attempts == 0
    assert soft.feedback == objective.feedback == [None]


def test_tool_and_noneligible_validation_failures_do_not_replan(monkeypatch):
    planner = FeedbackPlanner()

    def tool_failure(request):
        if request.tool_name == "search_hotels":
            return ToolResult(
                tool_name=request.tool_name,
                status=ToolStatus.ERROR,
                source="mock",
            )
        return run_tool(request)

    tool_response = TravelService(planner=planner, tool_runner=tool_failure).plan(
        "Plan a 2-day trip to Boston for 2 travelers under $500 total."
    )
    monkeypatch.setattr(
        graph_module,
        "validate_itinerary",
        Mock(return_value=ItineraryValidationResult(errors=["Structural validation failed"])),
    )
    validation_response = TravelService(planner=planner).plan(
        "Plan a 2-day trip to Boston for 2 travelers under $500 total."
    )

    assert tool_response.execution.replan_attempts == validation_response.execution.replan_attempts == 0
    assert len(planner.feedback) == 2
    assert tool_response.status == validation_response.status == "error"


def test_replan_state_is_isolated_between_requests():
    service = TravelService(planner=FeedbackPlanner())
    repaired = service.plan("Plan a 2-day trip to Boston for 2 travelers under $400 total.")
    valid = service.plan("Plan a 2-day trip to Boston for 2 travelers under $500 total.")

    assert repaired.execution.replan_attempts == 1
    assert valid.execution.replan_attempts == 0


def test_hotel_budget_violation_replans_with_a_cheaper_hotel():
    def ignore_hotel_price_ceiling(request):
        if request.tool_name == "search_hotels":
            request = request.model_copy(
                update={"arguments": SearchInput(destination=request.arguments.destination, preferences=request.arguments.preferences)}
            )
        return run_tool(request)

    response = TravelService(tool_runner=ignore_hotel_price_ceiling).plan(
        "Plan a 3-day trip to Columbus for 1 traveler under $900 total. "
        "I prefer a luxury hotel. Hotel spending must not exceed $300."
    )

    hotels = next(group for group in response.execution.candidate_groups if group.category == "hotel")
    assert response.status == "success"
    assert response.execution.replan_attempts == 1
    assert response.budget.breakdown["hotel"] <= 300
    assert hotels.selected[0].price == 82
