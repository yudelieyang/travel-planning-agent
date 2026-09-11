from unittest.mock import Mock

import pytest

from app.agent.extractor import RuleBasedRequirementsExtractor
from app.agent.graph import build_graph
from app.agent.planner import DeterministicTestPlanner, PlannerDecision
from app.agent.requirements import TravelRequirements, assess_requirements, parse_requirements
from app.agent.service import TravelService
from app.core.budget import BudgetScope
from app.tools.contracts import ToolStatus
from app.tools.mock import run_tool

QUERY = "Plan a 2-day trip to Boston for 2 travelers under $300 total. Vegetarian food."


def test_extractor_is_replaceable_without_modifying_graph():
    extractor = Mock()
    extractor.extract.return_value = TravelRequirements(destination="Boston", duration_days=2)
    result = TravelService(extractor=extractor).plan("Unrecognized input handled by test extractor")
    assert result.status == "success"
    extractor.extract.assert_called_once()
    assert isinstance(TravelService().extractor, RuleBasedRequirementsExtractor)


@pytest.mark.parametrize(
    "field,value",
    [
        ("destination", "Atlantis"),
        ("travelers", 20),
        ("budget_amount", 1000000),
        ("duration_days", 30),
        ("food_preferences", []),
        ("budget_scope", BudgetScope.PER_PERSON),
    ],
)
def test_planner_cannot_mutate_graph_requirements(field, value):
    class Mutator:
        def plan(self, requirements):
            setattr(requirements, field, value)
            return DeterministicTestPlanner().plan(requirements)

    original = parse_requirements(QUERY)
    snapshot = original.model_dump(mode="json")
    runner = Mock()
    state = build_graph(planner=Mutator(), tool_runner=runner).invoke(
        {"requirements": original, "messages": []}
    )
    assert original.model_dump(mode="json") == snapshot
    assert state["requirements"].model_dump(mode="json") == snapshot
    assert state["errors"] == ["planner_modified_requirements"]
    assert state["itinerary"] is None
    runner.assert_not_called()


def test_nested_mutation_then_exception_cannot_leak_into_state():
    class Mutator:
        def plan(self, requirements):
            requirements.food_preferences.clear()
            raise ValueError("private detail")

    response = TravelService(planner=Mutator()).plan(QUERY)
    assert response.requirements.food_preferences == ["vegetarian"]
    assert response.status == "error"


def test_dropped_preferences_are_rejected():
    decision = DeterministicTestPlanner().plan(parse_requirements(QUERY))
    decision.tool_requests[2].arguments.preferences.clear()
    planner, runner = Mock(), Mock()
    planner.plan.return_value = decision
    response = TravelService(planner=planner, tool_runner=runner).plan(QUERY)
    assert response.errors == ["planner_dropped_preferences"]
    runner.assert_not_called()


def test_model_construct_cannot_bypass_boundary_validation():
    planner, runner = Mock(), Mock()
    planner.plan.return_value = PlannerDecision.model_construct(
        can_proceed=True, tool_requests=[], warnings=[]
    )
    assert TravelService(planner=planner, tool_runner=runner).plan(QUERY).status == "error"
    runner.assert_not_called()


@pytest.mark.parametrize("query", ["Plan a trip.", "Plan a trip to Boston.", "Plan a 3-day trip."])
def test_clarification_missing_fields_and_trace_remain_consistent(query):
    planner, runner = Mock(), Mock()
    state, trace = TravelService(planner=planner, tool_runner=runner).run(query)
    assert state["missing_fields"] == assess_requirements(state["requirements"]).missing_fields
    assert trace.final_status == "needs_clarification"
    assert trace.validation_status == "not_reached"
    assert state["tool_results"] == []
    planner.plan.assert_not_called()
    runner.assert_not_called()


@pytest.mark.parametrize(
    "failure", ["wrong_tool", "failed_with_data", "budget_source", "budget_value"]
)
def test_results_are_validated_and_budget_is_calculator_owned(failure):
    executed = []

    def runner(request):
        executed.append(request.tool_name)
        result = run_tool(request)
        if failure == "wrong_tool" and request.tool_name == "search_hotels":
            return result.model_copy(update={"tool_name": "invented_tool"})
        if failure == "failed_with_data" and request.tool_name == "search_hotels":
            return result.model_copy(update={"status": ToolStatus.ERROR, "error": "failure"})
        if request.tool_name == "calculate_budget":
            if failure == "budget_source":
                return result.model_copy(update={"source": "model"})
            if failure == "budget_value":
                return result.model_copy(
                    update={"data": result.data.model_copy(update={"within_budget": True})}
                )
        return result

    state, trace = TravelService(tool_runner=runner).run(QUERY)
    assert [r.tool_name for r in state["tool_results"]] == executed
    assert any(r.status == ToolStatus.ERROR for r in state["tool_results"])
    assert all(r.data is None for r in state["tool_results"] if r.status == ToolStatus.ERROR)
    assert state["budget_summary"] is None
    assert state["itinerary"] is None
    assert state["errors"]
    assert trace.final_status == "error"
    assert trace.validation_status == "failed"


def test_trace_is_metadata_only_and_not_in_api_response():
    service = TravelService()
    state, trace = service.run(QUERY)
    second_state, second = service.run(QUERY)
    assert trace.run_id != second.run_id
    assert set(trace.model_dump()) == {
        "run_id",
        "planner_type",
        "prompt_version",
        "requirement_status",
        "selected_tools",
        "tool_statuses",
        "validation_status",
        "final_status",
        "latency_ms",
        "model",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "api_latency_ms",
        "api_error_type",
    }
    assert trace.final_status == "success"
    assert not state["errors"] and not second_state["errors"]
    assert state["budget_summary"] == state["tool_results"][-1].data
    assert state["tool_results"][-1].source == "deterministic"
    assert "trace" not in service.plan(QUERY).model_dump()
    assert trace.latency_ms >= 0
