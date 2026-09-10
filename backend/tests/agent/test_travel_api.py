import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.agent.evaluation import scenario_runner
from app.agent.graph import build_graph
from app.agent.requirements import parse_requirements
from app.agent.service import TravelService
from app.api.travel import get_travel_service
from app.main import app

DATASET = Path(__file__).resolve().parents[3] / "evals" / "datasets" / "travel_smoke_v1.json"


@pytest.mark.parametrize(
    "query,status",
    [
        ("Plan a 3-day trip to New York City under $1000. I like museums and food.", "success"),
        ("Plan a trip for me.", "needs_clarification"),
    ],
)
def test_api_contract(query, status):
    with TestClient(app) as client:
        result = client.post("/api/v1/travel/plan", json={"query": query})
    assert result.status_code == 200
    body = result.json()
    assert body["status"] == status
    if status == "success":
        assert body["itinerary"]["days"] == 3
        assert body["budget"]["estimated_total_cost"] <= 1000
    else:
        assert body["itinerary"] is None
        assert body["missing_fields"] == ["destination", "duration"]


@pytest.mark.parametrize(
    "query",
    [
        " ",
        "Plan a 0-day trip to Boston.",
        "Plan a -3-day trip to Boston.",
        "Plan a 3-day trip to Boston for -2 travelers.",
        "Plan a 3-day trip to Boston for 0 travelers.",
        "Plan a trip to Boston from 2026-10-03 to 2026-10-01.",
    ],
)
def test_api_invalid_input(query):
    with TestClient(app) as client:
        assert client.post("/api/v1/travel/plan", json={"query": query}).status_code == 422


@pytest.mark.parametrize(
    "case", json.loads(DATASET.read_text(encoding="utf-8")), ids=lambda c: c["id"]
)
def test_evaluation_seed(case):
    requirements = parse_requirements(case["input"])
    for field, value in case["expected_requirement_fields"].items():
        assert requirements.model_dump(mode="json")[field] == value
    state = build_graph(tool_runner=scenario_runner(case)).invoke(
        {"requirements": requirements, "messages": []}
    )
    assert state["requirement_status"].value == case["expected_status"]
    called = {result.tool_name for result in state["tool_results"]}
    assert set(case["required_tools"]) <= called
    assert not set(case["forbidden_tools"]) & called
    app.dependency_overrides[get_travel_service] = lambda: TravelService(
        tool_runner=scenario_runner(case)
    )
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/travel/plan", json={"query": case["input"]})
    finally:
        app.dependency_overrides.pop(get_travel_service, None)
    assert response.status_code == 200
    assert response.json()["status"] == case["expected_api_status"]
    constraint = case["budget_constraint"]
    if constraint:
        cost = state["budget_summary"].estimated_total_cost
        if "max_total" in constraint:
            assert cost <= constraint["max_total"] or state["budget_summary"].warnings
        if "within_budget" in constraint:
            assert state["budget_summary"].within_budget == constraint["within_budget"]
        if "scope" in constraint:
            assert state["budget_summary"].budget_scope == constraint["scope"]
        if constraint.get("must_exceed"):
            assert cost > constraint["max_total"]
            assert state["budget_summary"].within_budget is False
