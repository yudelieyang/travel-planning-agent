from unittest.mock import Mock

from app.agent.graph import build_graph
from app.agent.itinerary import validate_itinerary
from app.agent.requirements import parse_requirements
from app.agent.service import TravelService
from app.tools.contracts import BudgetRequest, ToolResult, ToolStatus
from app.tools.mock import run_tool


def test_success_graph_stores_structured_results_and_budget():
    graph = build_graph()
    state = graph.invoke(
        {
            "requirements": parse_requirements(
                "Plan a 3-day trip to New York City under $1000. I like museums and food."
            ),
            "messages": [],
        }
    )
    assert not state["errors"]
    assert state["itinerary"].days == 3
    assert {result.tool_name for result in state["tool_results"]} == {
        "search_attractions",
        "search_hotels",
        "search_restaurants",
        "search_transport",
        "calculate_budget",
    }
    assert all(result.status == ToolStatus.SUCCESS for result in state["tool_results"])
    assert isinstance(state["tool_requests"][-1], BudgetRequest)
    assert state["tool_requests"][-1].arguments is not None
    assert state["budget_summary"].estimated_total_cost <= 1000
    assert state["budget_summary"].travelers is None
    assert not validate_itinerary(state["itinerary"], state["budget_summary"])


def test_insufficient_never_calls_planner_or_tools():
    planner = Mock()
    runner = Mock(side_effect=AssertionError("Travel tools must not run"))
    service = TravelService(planner=planner, tool_runner=runner)
    response = service.plan("Plan a trip for me.")
    assert response.status == "needs_clarification"
    assert response.missing_fields == ["destination", "duration"]
    assert response.clarification_question
    planner.plan.assert_not_called()
    runner.assert_not_called()


def test_unknown_destination_and_tool_failure_do_not_fake_success():
    assert TravelService().plan("Plan a 2-day trip to Atlantis.").status == "error"

    def failure(request):
        if request.tool_name == "search_hotels":
            raise RuntimeError("private provider detail")
        return run_tool(request)

    response = TravelService(tool_runner=failure).plan("Plan a 2-day trip to Boston.")
    assert response.status == "error"
    assert response.itinerary is None
    assert "private provider detail" not in response.model_dump_json()


def test_replaceable_planner_and_no_cross_request_state():
    planner = Mock()
    from app.agent.planner import DeterministicTestPlanner

    planner.plan.side_effect = DeterministicTestPlanner().plan
    service = TravelService(planner=planner)
    query = "Plan a 2-day trip to Boston for 1 traveler under $500."
    first = service.plan(query)
    assert first.status == "success"
    assert service.plan("Plan a trip for me.").status == "needs_clarification"
    repeated = service.plan(query)
    assert first.model_dump(exclude={"execution"}) == repeated.model_dump(exclude={"execution"})
    assert first.execution.run_id != repeated.execution.run_id
    assert first.execution.model_dump(exclude={"run_id", "latency_ms"}) == (
        repeated.execution.model_dump(exclude={"run_id", "latency_ms"})
    )
    assert planner.plan.call_count == 2


def test_budget_corruption_is_caught_by_validator():
    def corrupt(request):
        result = run_tool(request)
        if request.tool_name == "calculate_budget":
            changed = result.data.model_copy(update={"estimated_total_cost": 0})
            return ToolResult(
                tool_name=result.tool_name,
                status=ToolStatus.SUCCESS,
                source="deterministic",
                data=changed,
            )
        return result

    response = TravelService(tool_runner=corrupt).plan("Plan a 2-day trip to Boston.")
    assert response.status == "error"
    assert response.itinerary is None
    assert response.errors
