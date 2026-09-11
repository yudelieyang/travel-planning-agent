"""Public observability reflects execution, without changing domain behavior."""

from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.agent import graph as graph_module
from app.agent.execution import PublicExecutionSummary
from app.agent.openai_planner import OpenAIPlanner
from app.agent.planner import DeterministicTestPlanner, PlannerDecision
from app.agent.service import PlanResponse, TravelService
from app.api.travel import get_travel_service
from app.core.config import Settings
from app.main import app
from app.tools.contracts import BudgetInput, CostItem, ToolResult
from app.tools.mock import calculate_budget, run_tool

BOSTON = "Plan a 2-day trip to Boston for 1 traveler under $500 total."
CLARIFICATION = "Plan a trip for me."
ATLANTIS = "Plan a 2-day trip to Atlantis."
TIGHT = "Plan a 2-day trip to Boston for 2 travelers under $50 total."
TOOLS = [
    "search_attractions",
    "search_hotels",
    "search_restaurants",
    "search_transport",
    "calculate_budget",
]


def stages(execution):
    return {stage.name: stage for stage in execution.stages}


@pytest.mark.parametrize("query", [BOSTON, CLARIFICATION, ATLANTIS, TIGHT])
def test_http_public_contract(query):
    with TestClient(app) as client:
        response = client.post("/api/v1/travel/plan", json={"query": query})
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {
        "status",
        "requirements",
        "itinerary",
        "budget",
        "missing_fields",
        "clarification_question",
        "warnings",
        "errors",
        "execution",
    }
    assert PlanResponse.model_validate(body).execution is not None
    execution = PublicExecutionSummary.model_validate(body["execution"])
    assert execution.mode == "demo"
    assert execution.planner_type == "DeterministicTestPlanner"
    assert execution.prompt_version is None
    assert execution.latency_ms >= 0
    visited = [s for s in execution.stages if s.sequence is not None]
    assert [s.sequence for s in visited] == list(range(1, len(visited) + 1))
    assert len(stages(execution)) == 6
    assert all(s.outcome == "not_reached" for s in execution.stages if s.sequence is None)


def test_success_records_match_observed_calls_and_internal_state():
    calls = []

    def runner(request):
        calls.append(request.model_copy(deep=True))
        return run_tool(request)

    service = TravelService(tool_runner=runner)
    response = service.plan(BOSTON)
    execution = response.execution
    assert response.status == "success"
    assert execution.planner_invoked and execution.planner_outcome == "accepted"
    assert [(s.name, s.outcome) for s in execution.stages if s.sequence] == [
        ("preflight", "completed"),
        ("planner", "completed"),
        ("tools", "completed"),
        ("validation", "completed"),
        ("finalization", "completed"),
    ]
    assert stages(execution)["clarification"].outcome == "not_reached"
    assert execution.validation.model_dump() == {
        "performed": True,
        "outcome": "passed",
        "reason": None,
    }
    assert [t.tool_name for t in execution.tools] == TOOLS
    for index, (record, call) in enumerate(zip(execution.tools, calls, strict=True), 1):
        assert record.selected and record.executed
        assert record.execution_order == index
        assert record.runtime_arguments == call.arguments
        assert record.status == "SUCCESS"
        assert record.error_code is None
    budget = execution.tools[-1]
    assert budget.requested_arguments is None
    assert budget.runtime_arguments is not None
    assert budget.source == "deterministic"
    assert budget.data == response.budget
    state, trace = service.run(BOSTON)
    assert state["approved_tool_requests"][-1].arguments is None
    assert state["tool_requests"][-1].arguments == budget.runtime_arguments
    assert [r.status.value for r in state["tool_results"]] == [t.status for t in execution.tools]
    assert trace.validation_status == "passed"


def test_clarification_has_no_fabricated_execution():
    planner, runner = Mock(), Mock()
    response = TravelService(planner=planner, tool_runner=runner).plan(CLARIFICATION)
    execution = response.execution
    assert execution.mode == "custom"
    assert not execution.planner_invoked
    assert execution.planner_outcome == "not_invoked"
    assert execution.tools == []
    assert [(s.name, s.outcome) for s in execution.stages if s.sequence] == [
        ("preflight", "clarification"),
        ("clarification", "completed"),
    ]
    for name in ("planner", "tools", "validation", "finalization"):
        assert stages(execution)[name].outcome == "not_reached"
    assert execution.validation.model_dump() == {
        "performed": False,
        "outcome": "not_performed",
        "reason": "not_reached",
    }
    planner.plan.assert_not_called()
    runner.assert_not_called()


def test_search_failure_skips_budget_and_validation_but_finalizes():
    response = TravelService().plan(ATLANTIS)
    execution = response.execution
    assert response.status == "error" and response.budget is None and response.itinerary is None
    assert execution.planner_invoked and execution.planner_outcome == "accepted"
    for record in execution.tools[:4]:
        assert record.selected and record.executed
        assert record.status == "NO_RESULTS"
        assert record.data == []
    budget = execution.tools[-1]
    assert budget.selected and not budget.executed
    assert budget.status == "SKIPPED"
    assert budget.runtime_arguments is budget.execution_order is budget.source is None
    assert budget.requested_arguments is budget.data is budget.error_code is None
    assert stages(execution)["tools"].outcome == "failed"
    assert stages(execution)["validation"].outcome == "skipped"
    assert stages(execution)["validation"].sequence == 4
    assert stages(execution)["finalization"].outcome == "completed"
    assert execution.validation.model_dump() == {
        "performed": False,
        "outcome": "not_performed",
        "reason": "prior_errors",
    }
    _, trace = TravelService().run(ATLANTIS)
    assert trace.validation_status == "failed"  # Preserve evaluation's historical aggregate.


def test_over_budget_is_successful_execution():
    response = TravelService().plan(TIGHT)
    assert response.status == "success"
    assert response.budget.within_budget is False
    assert response.budget.comparison_cost == 446
    assert response.budget.remaining_budget == -396
    assert response.budget.estimated_total_cost == 446
    assert all(t.status == "SUCCESS" for t in response.execution.tools)
    assert response.execution.validation.outcome == "passed"


@pytest.mark.parametrize(
    "scope,travelers,limit,currency,comparison,remaining,within",
    [
        ("TOTAL_TRIP", 2, 1.0, "USD", 0.6, 0.4, True),
        ("TOTAL_TRIP", 2, 0.0, "USD", 0.6, -0.6, False),
        ("PER_PERSON", 2, 0.4, "USD", 0.3, 0.1, True),
        ("PER_PERSON", None, 0.2, "USD", 0.3, -0.1, False),
        ("PER_PERSON", None, 0.3, "USD", 0.3, 0.0, True),
        ("UNKNOWN", 2, 1.0, "USD", None, None, None),
        ("TOTAL_TRIP", None, 1.0, "USD", None, None, None),
        ("TOTAL_TRIP", 2, 1.0, "EUR", None, None, None),
        ("PER_PERSON", 2, 1.0, "GBP", None, None, None),
        ("TOTAL_TRIP", 2, None, "USD", None, None, None),
    ],
)
def test_budget_comparison_fields(scope, travelers, limit, currency, comparison, remaining, within):
    result = calculate_budget(
        BudgetInput(
            items=[CostItem(category="food", amount=0.1), CostItem(category="food", amount=0.2)],
            travelers=travelers,
            limit=limit,
            limit_currency=currency,
            budget_scope=scope,
        )
    ).data
    assert result.comparison_cost == comparison
    assert result.remaining_budget == remaining
    assert result.within_budget is within


def test_unknown_comparison_in_http_response():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/travel/plan",
            json={
                "query": "Plan a 2-day trip to Boston under $500 total.",
            },
        )
    budget = response.json()["budget"]
    assert (
        budget["within_budget"] is budget["comparison_cost"] is budget["remaining_budget"] is None
    )


@pytest.mark.parametrize("failure", ["blocked", "invalid", "exception", "destination"])
def test_planner_failures_have_no_approved_tools(failure):
    planner, runner = Mock(), Mock()
    if failure == "blocked":
        planner.plan.return_value = PlannerDecision(
            can_proceed=False, tool_requests=[], warnings=[]
        )
    elif failure == "invalid":
        planner.plan.return_value = PlannerDecision.model_construct(
            can_proceed=True,
            tool_requests=[],
            warnings=[],
        )
    elif failure == "exception":
        planner.plan.side_effect = RuntimeError("private planner exception")
    else:
        from app.agent.requirements import parse_requirements

        planner.plan.return_value = DeterministicTestPlanner().plan(parse_requirements(ATLANTIS))
    response = TravelService(planner=planner, tool_runner=runner).plan(BOSTON)
    execution = response.execution
    assert response.status == "error"
    assert execution.planner_invoked and execution.planner_outcome == "failed"
    assert execution.tools == []
    assert stages(execution)["planner"].outcome == "failed"
    assert stages(execution)["tools"].outcome == "skipped"
    assert execution.validation.reason == "prior_errors"
    assert stages(execution)["finalization"].outcome == "completed"
    assert "private planner exception" not in response.model_dump_json()
    runner.assert_not_called()


def test_validation_executed_failure_is_distinct(monkeypatch):
    validator = Mock(return_value=["Itinerary cost does not match budget calculation"])
    monkeypatch.setattr(graph_module, "validate_itinerary", validator)
    response = TravelService().plan(BOSTON)
    validator.assert_called_once()
    assert response.status == "error"
    assert response.itinerary is response.budget is None
    assert response.execution.validation.model_dump() == {
        "performed": True,
        "outcome": "failed",
        "reason": None,
    }
    assert stages(response.execution)["validation"].outcome == "failed"
    assert stages(response.execution)["finalization"].outcome == "completed"


def test_budget_tool_failure_is_executed_and_validation_skipped():
    def runner(request):
        result = run_tool(request)
        if request.tool_name == "calculate_budget":
            result.data.remaining_budget = 12345
        return result

    response = TravelService(tool_runner=runner).plan(BOSTON)
    budget = response.execution.tools[-1]
    assert budget.executed and budget.status == "ERROR"
    assert budget.runtime_arguments is not None and budget.requested_arguments is None
    assert budget.error_code == "tool_execution_failed"
    assert budget.data is None
    assert response.execution.validation.reason == "prior_errors"


def test_public_projection_excludes_internal_metadata_and_private_objects():
    canary = "PRIVATE_CANARY_DO_NOT_EXPOSE"

    class InstrumentedPlanner(DeterministicTestPlanner):
        settings = {"api_key": canary}
        client = object()
        messages = [canary]
        system_prompt = canary
        developer_prompt = canary
        raw_response = {"reasoning": canary}

    def runner(request):
        if request.tool_name == "search_hotels":
            return ToolResult(
                tool_name=request.tool_name,
                status="ERROR",
                source=canary,
                error=canary,
                metadata={"private": canary},
            )
        result = run_tool(request)
        result.metadata["private"] = canary
        return result

    app.dependency_overrides[get_travel_service] = lambda: TravelService(
        planner=InstrumentedPlanner(),
        tool_runner=runner,
    )
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/travel/plan", json={"query": BOSTON})
    finally:
        app.dependency_overrides.pop(get_travel_service, None)
    assert response.status_code == 200
    assert canary not in response.text
    execution = response.json()["execution"]
    assert set(execution) == {
        "run_id",
        "mode",
        "planner_type",
        "planner_invoked",
        "prompt_version",
        "latency_ms",
        "requirement_status",
        "planner_outcome",
        "stages",
        "tools",
        "validation",
    }
    hotel = execution["tools"][1]
    assert hotel["source"] is None
    assert hotel["error_code"] == "tool_execution_failed"
    assert all("metadata" not in record and "error" not in record for record in execution["tools"])


def test_live_identity_on_clarification_does_not_claim_provider_call():
    client = Mock()
    settings = Settings(
        _env_file=None,
        postgres_db="test",
        postgres_user="test",
        postgres_password="private-db",
        openai_api_key="private-key",
        openai_model="offline-test-model",
    )
    planner = OpenAIPlanner(settings, client=client)
    response = TravelService(planner=planner).plan(CLARIFICATION)
    assert response.execution.mode == "live"
    assert response.execution.planner_type == "OpenAIPlanner"
    assert response.execution.prompt_version == "planner_v1"
    assert not response.execution.planner_invoked
    assert response.execution.planner_outcome == "not_invoked"
    client.responses.parse.assert_not_called()
    assert "private-key" not in response.model_dump_json()
    assert "private-db" not in response.model_dump_json()


def test_request_local_execution_isolation():
    service = TravelService()
    with ThreadPoolExecutor(max_workers=3) as pool:
        success, clarification, error = list(
            pool.map(service.plan, [BOSTON, CLARIFICATION, ATLANTIS])
        )
    assert len({r.execution.run_id for r in (success, clarification, error)}) == 3
    assert success.execution.validation.performed
    assert clarification.execution.tools == []
    assert error.execution.tools[-1].status == "SKIPPED"
    success.execution.stages.clear()
    assert service.plan(BOSTON).execution.stages


def test_selection_order_and_actual_execution_order_are_distinct():
    class BudgetFirstPlanner(DeterministicTestPlanner):
        def plan(self, requirements):
            decision = super().plan(requirements)
            decision.tool_requests = decision.tool_requests[-1:] + decision.tool_requests[:-1]
            return decision

    calls = []

    def runner(request):
        calls.append(request.tool_name)
        return run_tool(request)

    response = TravelService(planner=BudgetFirstPlanner(), tool_runner=runner).plan(BOSTON)
    records = response.execution.tools
    assert records[0].tool_name == "calculate_budget"
    assert records[0].requested_arguments is None
    assert records[0].runtime_arguments is not None
    assert records[0].execution_order == 5
    assert [r.tool_name for r in sorted(records, key=lambda r: r.execution_order)] == calls == TOOLS
