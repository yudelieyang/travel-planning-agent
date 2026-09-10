import json
from types import SimpleNamespace
from unittest.mock import Mock

import httpx
import pytest
from fastapi.testclient import TestClient
from openai import OpenAI
from pydantic import SecretStr, ValidationError

from app.agent.openai_planner import OpenAIPlanner, PlannerConfigurationError, create_planner
from app.agent.planner import DeterministicTestPlanner, PlannerDecision
from app.agent.requirements import parse_requirements
from app.agent.service import TravelService
from app.core.config import Settings
from app.main import app

QUERY = "Plan a 2-day trip to Boston for 2 travelers under $500 total."


def settings(**changes):
    return Settings(
        _env_file=None,
        postgres_db="test",
        postgres_user="test",
        postgres_password=SecretStr("test"),
        **{
            "openai_api_key": SecretStr("offline-test-placeholder"),
            "openai_model": "offline-model",
            **changes,
        },
    )


def payload():
    return DeterministicTestPlanner().plan(parse_requirements(QUERY)).model_dump(mode="json")


def response_body(text):
    return {
        "id": "resp_offline",
        "object": "response",
        "created_at": 0,
        "model": "offline-model",
        "status": "completed",
        "error": None,
        "incomplete_details": None,
        "instructions": None,
        "metadata": {},
        "output": [
            {
                "id": "msg_offline",
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": text, "annotations": []}],
            }
        ],
        "parallel_tool_calls": False,
        "temperature": 1,
        "tool_choice": "auto",
        "tools": [],
        "top_p": 1,
        "usage": None,
    }


def sdk_planner(handler):
    client = OpenAI(
        api_key="offline-test-placeholder",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    return OpenAIPlanner(settings(), client=client)


@pytest.mark.parametrize("missing", ["openai_api_key", "openai_model"])
def test_missing_configuration(missing):
    with pytest.raises(PlannerConfigurationError, match=missing.upper()):
        OpenAIPlanner(settings(**{missing: ""}))


def test_default_is_offline_without_key():
    assert isinstance(create_planner(settings(openai_api_key="")), DeterministicTestPlanner)


def test_http_missing_key_fails_fast(monkeypatch):
    monkeypatch.setenv("AGENT_PLANNER", "openai")
    with TestClient(app) as client:
        result = client.post("/api/v1/travel/plan", json={"query": QUERY})
    assert result.status_code == 503
    assert result.json()["detail"] == "OPENAI_API_KEY is required for the OpenAI planner"


def test_actual_sdk_structured_parsing_and_request_options():
    requests = []

    def handler(request):
        body = json.loads(request.content)
        requests.append(body)
        assert body["text"]["format"]["strict"] is True
        assert body["text"]["format"]["schema"]["additionalProperties"] is False
        assert body["store"] is False
        assert body["model"] == "offline-model"
        assert body["max_output_tokens"] == 2000
        assert json.loads(body["input"])["destination"] == "Boston"
        return httpx.Response(200, json=response_body(json.dumps(payload())))

    planner = sdk_planner(handler)
    try:
        result = TravelService(planner=planner).plan(QUERY)
        assert result.status == "success"
        assert result.budget.budget_scope == "TOTAL_TRIP"
        assert len(requests) == 1
    finally:
        planner.client.close()


@pytest.mark.parametrize(
    "kind",
    [
        "unknown",
        "negative_price",
        "blank_destination",
        "string_price",
        "extra",
        "budget_fabrication",
        "malformed",
        "duplicate",
        "missing_arguments",
        "missing_destination",
        "verified_facts",
        "changed_requirements",
    ],
)
def test_invalid_provider_decision_never_executes_tools(kind):
    data = payload()
    first = data["tool_requests"][0]
    if kind == "unknown":
        first["tool_name"] = "book_flight"
    elif kind == "negative_price":
        first["arguments"]["max_price"] = -1
    elif kind == "string_price":
        first["arguments"]["max_price"] = "10"
    elif kind == "blank_destination":
        first["arguments"]["destination"] = " "
    elif kind == "extra":
        data["unrecognized"] = "private provider detail"
    elif kind == "budget_fabrication":
        data["tool_requests"][-1]["arguments"] = {"items": []}
    elif kind == "duplicate":
        data["tool_requests"][1] = first
    elif kind == "missing_arguments":
        del first["arguments"]
    elif kind == "missing_destination":
        del first["arguments"]["destination"]
    elif kind == "verified_facts":
        data["verified_facts"] = {"wheelchair_access": True}
    elif kind == "changed_requirements":
        data["requirements"] = {"budget_amount": 1000000}
    text = "not-json" if kind == "malformed" else json.dumps(data)
    planner = sdk_planner(lambda _: httpx.Response(200, json=response_body(text)))
    runner = Mock()
    try:
        result = TravelService(planner=planner, tool_runner=runner).plan(QUERY)
        assert result.status == "error"
        assert result.itinerary is None
        runner.assert_not_called()
        assert "private provider detail" not in result.model_dump_json()
    finally:
        planner.client.close()


@pytest.mark.parametrize(
    "status,code",
    [
        (401, "authentication_error"),
        (429, "rate_limit"),
        (500, "provider_error"),
        (400, "provider_error"),
    ],
)
def test_provider_errors_are_safe_and_never_retried(status, code):
    handler = Mock(
        return_value=httpx.Response(
            status,
            json={"error": {"message": "private provider detail", "type": "test", "code": "test"}},
        )
    )
    planner = sdk_planner(handler)
    try:
        result = TravelService(planner=planner).plan(QUERY)
        assert result.status == "error"
        assert code in result.errors[0]
        assert "private provider detail" not in result.model_dump_json()
        assert handler.call_count == 1
    finally:
        planner.client.close()


def test_timeout_is_retryable_but_not_retried():
    handler = Mock(side_effect=httpx.ReadTimeout("private provider detail"))
    planner = sdk_planner(handler)
    try:
        result = TravelService(planner=planner).plan(QUERY)
        assert result.status == "error"
        assert result.errors == ["timeout (retryable; no automatic retry)"]
        assert handler.call_count == 1
    finally:
        planner.client.close()


@pytest.mark.parametrize("status,decision", [("completed", None), ("incomplete", None)])
def test_empty_and_incomplete_response(status, decision):
    client = Mock()
    client.responses.parse.return_value = SimpleNamespace(status=status, output_parsed=decision)
    runner = Mock()
    result = TravelService(
        planner=OpenAIPlanner(settings(), client=client), tool_runner=runner
    ).plan(QUERY)
    assert result.status == "error"
    runner.assert_not_called()


def test_clarification_never_calls_provider():
    client = Mock()
    result = TravelService(planner=OpenAIPlanner(settings(), client=client)).plan("Plan a trip.")
    assert result.status == "needs_clarification"
    client.responses.parse.assert_not_called()


def test_blocked_decision_and_destination_mismatch():
    for decision in [
        PlannerDecision(can_proceed=False, tool_requests=[], warnings=["Unavailable"]),
        DeterministicTestPlanner().plan(parse_requirements("Plan a 2-day trip to NYC.")),
    ]:
        runner = Mock()
        planner = Mock()
        planner.plan.return_value = decision
        result = TravelService(planner=planner, tool_runner=runner).plan(QUERY)
        assert result.status == "error"
        runner.assert_not_called()


def test_decision_rejects_duplicates_and_incomplete_tool_set():
    for requests in [payload()["tool_requests"][:1], [payload()["tool_requests"][0]] * 5]:
        with pytest.raises(ValidationError):
            PlannerDecision.model_validate(
                {"can_proceed": True, "warnings": [], "tool_requests": requests}
            )


def test_refusal_from_actual_sdk_is_an_error():
    body = response_body("")
    body["output"][0]["content"] = [{"type": "refusal", "refusal": "Unavailable"}]
    planner = sdk_planner(lambda _: httpx.Response(200, json=body))
    try:
        result = TravelService(planner=planner).plan(QUERY)
        assert result.status == "error"
        assert result.errors == ["empty_or_refused_response"]
    finally:
        planner.client.close()


def test_connection_error_is_safe():
    handler = Mock(side_effect=httpx.ConnectError("private provider detail"))
    planner = sdk_planner(handler)
    try:
        result = TravelService(planner=planner).plan(QUERY)
        assert result.status == "error"
        assert result.errors == ["connection_error (retryable; no automatic retry)"]
        assert handler.call_count == 1
    finally:
        planner.client.close()


def test_model_warnings_survive_deterministic_tools():
    decision = DeterministicTestPlanner().plan(parse_requirements(QUERY))
    decision.warnings = ["Some constraints cannot be verified."]
    planner = Mock()
    planner.plan.return_value = decision
    result = TravelService(planner=planner).plan(QUERY)
    assert result.status == "success"
    assert decision.warnings[0] in result.warnings
