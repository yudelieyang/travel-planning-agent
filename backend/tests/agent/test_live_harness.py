import importlib.util
import json
from contextvars import Context
from copy import deepcopy
from unittest.mock import Mock

import httpx
import pytest

from app.agent.graph import build_graph
from app.agent.live_evaluation import (
    RecordingPlanner,
    aggregate,
    budget_integrity,
    factual_provenance,
    prepare_cases,
    run_comparison,
    write_report,
)
from app.agent.live_simulation import MOCK_MODEL, response_body, simulated_planner
from app.agent.planner import DeterministicTestPlanner, PlannerError
from app.core.config import PROJECT_ROOT, Settings

DATASET = PROJECT_ROOT / "evals/datasets/planner_live_smoke_v1.json"


def configured(**values):
    return Settings(openai_api_key="", openai_model="", **values)


def cli_module():
    spec = importlib.util.spec_from_file_location(
        "planner_live_cli", PROJECT_ROOT / "evals/evaluate_planner_live.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_flag_and_dry_run_cannot_create_provider(monkeypatch, capsys):
    monkeypatch.setenv("AGENT_PLANNER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "offline-canary")
    monkeypatch.setenv("OPENAI_MODEL", "configured-model")
    cli = cli_module()
    provider = Mock(side_effect=AssertionError("Provider must not be constructed"))
    monkeypatch.setattr(cli, "OpenAIPlanner", provider)
    for args in ([], ["--dry-run"]):
        assert cli.main(args) == 0
        result = json.loads(capsys.readouterr().out)
        assert result["actual_api_requests"] == 0
        assert result["number_of_live_cases"] == 3
        assert result["expected_api_requests_if_later_authorized"] == 3
        assert "offline-canary" not in json.dumps(result)
    provider.assert_not_called()


@pytest.mark.parametrize(
    "args,values,error",
    [
        (["--live"], {}, "OPENAI_API_KEY"),
        (["--live"], {"openai_api_key": "offline-placeholder"}, "OPENAI_MODEL"),
        (
            ["--live", "--approved-model", "different"],
            {"openai_api_key": "offline-placeholder", "openai_model": "configured-model"},
            "approved-model",
        ),
        (["--dry-run", "--max-cases", "9"], {}, "max_cases"),
        (["--dry-run", "--max-cases", "0"], {}, "max_cases"),
    ],
)
def test_guards_fail_before_provider_construction(args, values, error, monkeypatch, capsys):
    cli = cli_module()
    settings = Settings(**{"openai_api_key": "", "openai_model": "", **values})
    monkeypatch.setattr(cli, "Settings", lambda: settings)
    provider = Mock(side_effect=AssertionError("Provider must not be constructed"))
    monkeypatch.setattr(cli, "OpenAIPlanner", provider)
    with pytest.raises(SystemExit) as exc:
        cli.main(args)
    assert exc.value.code == 2
    assert error in capsys.readouterr().err
    provider.assert_not_called()


def test_frozen_requirements_are_checked_before_execution(tmp_path):
    data = json.loads(DATASET.read_text("utf-8"))
    data["cases"][0]["frozen_requirements"]["travelers"] = 7
    changed = tmp_path / "dataset.json"
    changed.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="Frozen requirements"):
        prepare_cases(changed, 3)


def test_full_mock_pipeline_serializes_and_ignores_search_order(tmp_path):
    dataset, cases = prepare_cases(DATASET, 8)
    report = run_comparison(
        cases,
        metadata={"dataset_version": dataset.version, "git_commit": "offline-test"},
        mode="mock",
        planner_factory=lambda: simulated_planner(configured()),
        model=MOCK_MODEL,
    )
    assert report["provider_requests"] == 0
    assert report["mock_requests"] == 8
    assert report["comparison"]["OpenAI"] == "NOT RUN"
    assert report["comparison"]["OpenAI MOCK"]["case_success_rate"]["value"] == 1
    assert report["comparison"]["OpenAI MOCK"]["required_tool_recall"]["value"] == 1
    assert report["comparison"]["OpenAI MOCK"]["budget_integrity_rate"]["denominator"] == 7
    a, b = report["records"][:8], report["records"][8:]
    for first, second in zip(a, b, strict=True):
        assert first["requirements_sha256"] == second["requirements_sha256"]
        assert first["selected_tools"] != second["selected_tools"]
        assert set(first["selected_tools"]) == set(second["selected_tools"])
        assert first["final_status"] == second["final_status"]
    path = tmp_path / "mock.json"
    write_report(report, path)
    restored = json.loads(path.read_text("utf-8"))
    assert restored == report
    assert "offline-placeholder" not in path.read_text("utf-8")
    assert not report["stopped_early"]


@pytest.mark.parametrize(
    "fault,metric",
    [
        ("unknown", "invalid_tool_rate"),
        ("duplicate", "duplicate_tool_rate"),
        ("arguments", "invalid_argument_rate"),
    ],
)
def test_invalid_decision_metrics_are_observed_without_storing_raw_output(fault, metric):
    _, cases = prepare_cases(DATASET, 3)

    def handler(request):
        data = DeterministicTestPlanner().plan(cases[0].frozen_requirements).model_dump(mode="json")
        if fault == "unknown":
            data["tool_requests"][0]["tool_name"] = "untrusted-secret-canary"
        elif fault == "duplicate":
            data["tool_requests"][1] = data["tool_requests"][0]
        else:
            data["tool_requests"][0]["arguments"]["max_price"] = -1
        return httpx.Response(200, json=response_body(json.dumps(data)))

    report = run_comparison(
        cases,
        metadata={},
        mode="mock",
        planner_factory=lambda: simulated_planner(configured(), handler),
        model=MOCK_MODEL,
    )
    assert report["comparison"]["OpenAI MOCK"][metric]["value"] == 1
    assert report["comparison"]["OpenAI MOCK"][metric]["denominator"] == 1
    assert report["stopped_early"] and report["mock_requests"] == 1
    assert report["records"][-1]["final_status"] == "error"
    assert "untrusted-secret-canary" not in json.dumps(report)


@pytest.mark.parametrize(
    "status,error", [(401, "authentication_error"), (429, "rate_limit"), (500, "provider_error")]
)
def test_provider_failures_stop_after_one_mock_request(status, error):
    _, cases = prepare_cases(DATASET, 3)
    handler = Mock(
        return_value=httpx.Response(status, json={"error": {"message": "private-canary"}})
    )
    report = run_comparison(
        cases,
        metadata={},
        mode="mock",
        planner_factory=lambda: simulated_planner(configured(), handler),
        model=MOCK_MODEL,
    )
    assert handler.call_count == 1
    assert report["stopped_early"]
    assert report["records"][-1]["trace"]["api_error_type"] == error
    assert report["comparison"]["OpenAI MOCK"]["invalid_tool_rate"]["value"] is None
    assert "private-canary" not in json.dumps(report)


def test_call_limit_prevents_extra_requests_and_resets_observation():
    _, cases = prepare_cases(DATASET, 1)
    planner = simulated_planner(configured())
    limited = RecordingPlanner(planner, 1)
    try:
        limited.plan(cases[0].frozen_requirements)
        with pytest.raises(PlannerError, match="evaluation_call_limit"):
            limited.plan(cases[0].frozen_requirements)
        assert limited.calls == 1
        assert limited.observation is None
    finally:
        planner.client.close()


def test_usage_and_observation_are_per_call_and_per_context():
    _, cases = prepare_cases(DATASET, 1)
    req = cases[0].frozen_requirements
    body = response_body(DeterministicTestPlanner().plan(req).model_dump_json())
    body["usage"] = {
        "input_tokens": 12,
        "output_tokens": 8,
        "total_tokens": 20,
        "input_tokens_details": {"cached_tokens": 0},
        "output_tokens_details": {"reasoning_tokens": 0},
    }
    handler = Mock(
        side_effect=[httpx.Response(200, json=body), httpx.ReadTimeout("private-canary")]
    )
    planner = simulated_planner(configured(), handler)
    try:
        assert Context().run(planner.get_observation) is None
        planner.plan(req)
        info = planner.get_observation()["metadata"]
        assert (info["input_tokens"], info["output_tokens"], info["total_tokens"]) == (12, 8, 20)
        assert info["api_latency_ms"] >= 0
        assert Context().run(planner.get_observation) is None
        with pytest.raises(PlannerError):
            planner.plan(req)
        info = planner.get_observation()["metadata"]
        assert info["api_error_type"] == "timeout"
        assert info["total_tokens"] is None
    finally:
        planner.client.close()


@pytest.mark.parametrize("field,value", [("name", "Invented Hotel"), ("estimated_cost", 999)])
def test_provenance_rejects_invented_final_facts(field, value):
    _, cases = prepare_cases(DATASET, 1)
    state = build_graph().invoke({"requirements": cases[0].frozen_requirements, "messages": []})
    assert factual_provenance(state) is True and budget_integrity(state) is True
    setattr(state["itinerary"].daily_plan[0].activities[0], field, value)
    assert factual_provenance(state) is False


def test_negative_controls_change_all_integrity_metrics():
    _, cases = prepare_cases(DATASET, 1)
    baseline = run_comparison(cases, metadata={})["records"]
    broken = deepcopy(baseline)
    row = broken[0]
    row.update(
        case_success=False,
        required_tool_hits=0,
        forbidden_violations=["book_flight"],
        destination_integrity=False,
        preference_integrity=False,
        budget_integrity=False,
        factual_provenance=False,
        final_status_correct=False,
    )
    scores = aggregate(broken)
    for name in (
        "case_success_rate",
        "required_tool_recall",
        "destination_preservation_rate",
        "preference_preservation_rate",
        "budget_integrity_rate",
        "factual_provenance_rate",
        "final_status_accuracy",
    ):
        assert scores[name]["value"] == 0
    assert scores["forbidden_tool_violation_rate"]["value"] == 1


def test_failed_deterministic_baseline_prevents_provider_factory():
    _, cases = prepare_cases(DATASET, 1)
    changed = cases[0].model_copy(update={"expected_status": "error"})
    factory = Mock(side_effect=AssertionError("Do not run provider after bad baseline"))
    report = run_comparison([changed], metadata={}, mode="mock", planner_factory=factory)
    factory.assert_not_called()
    assert report["stopped_early"]
    assert report["comparison"]["OpenAI"] == "NOT RUN"


@pytest.mark.parametrize(
    "status,code,expected",
    [
        (429, "insufficient_quota", "insufficient_quota"),
        (402, "billing_required", "billing_required"),
        (404, "model_not_found", "model_not_available"),
        (403, "permission_denied", "permission_denied"),
    ],
)
def test_live_infrastructure_errors_are_distinct_and_not_retried(status, code, expected):
    _, cases = prepare_cases(DATASET, 3)
    handler = Mock(
        return_value=httpx.Response(
            status, json={"error": {"message": "private-canary", "code": code, "type": code}}
        )
    )
    report = run_comparison(
        cases,
        metadata={},
        mode="mock",
        planner_factory=lambda: simulated_planner(configured(), handler),
        model=MOCK_MODEL,
    )
    assert report["mock_requests"] == handler.call_count == 1
    assert report["stopped_early"]
    assert report["records"][-1]["trace"]["api_error_type"] == expected
    assert report["records"][-1]["error"] == [expected]
    assert "private-canary" not in json.dumps(report)
