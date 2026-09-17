import json
from copy import deepcopy

from app.agent.evaluation import SMOKE_CASE_IDS, LimitedPlanner, evaluate_case, score_records
from app.agent.planner import DeterministicTestPlanner
from app.core.config import PROJECT_ROOT


def test_comparison_records_and_three_call_limit():
    cases = json.loads((PROJECT_ROOT / "evals/datasets/travel_smoke_v1.json").read_text("utf-8"))
    planner = LimitedPlanner(DeterministicTestPlanner(), max_calls=3)
    selected = [case for case in cases if case["id"] in SMOKE_CASE_IDS]
    records = [
        evaluate_case(case, planner, planner_name="test", model=None, prompt_version=None)
        for case in selected
    ]
    assert planner.calls == 3
    assert [record["final_status"] for record in records] == [
        "success",
        "needs_clarification",
        "error",
        "success",
    ]
    assert records[1]["tool_validation"] == "not_reached"
    assert records[2]["budget_handling"]["within_budget"] is False
    exhausted = evaluate_case(
        selected[0], planner, planner_name="test", model=None, prompt_version=None
    )
    assert exhausted["final_status"] == "error"
    assert exhausted["error"] == ["evaluation_call_limit"]
    assert planner.calls == 3


def test_full_dataset_metrics_and_negative_controls():
    cases = json.loads((PROJECT_ROOT / "evals/datasets/travel_smoke_v1.json").read_text("utf-8"))
    records = [
        evaluate_case(
            case,
            DeterministicTestPlanner(),
            planner_name="deterministic",
            model=None,
            prompt_version=None,
        )
        for case in cases
    ]
    scores = score_records(cases, records)
    assert scores["case_count"] == 18
    assert scores["case_pass_rate"] == 1
    assert scores["requirement_accuracy"] == 1
    assert scores["required_tool_hit_rate"] == 1
    assert scores["forbidden_tool_violations"] == 0
    assert scores["final_status_accuracy"] == 1
    broken = deepcopy(records)
    broken[0]["requirements"]["destination"] = "wrong"
    broken[0]["executed_tools"] = []
    broken[0]["final_status"] = "error"
    broken[1]["executed_tools"] = ["search_hotels"]
    broken[7]["warnings"] = []
    broken[8]["budget_handling"]["within_budget"] = False
    scores = score_records(cases, broken)
    assert scores["case_pass_rate"] < 1
    assert scores["requirement_accuracy"] < 1
    assert scores["required_tool_hit_rate"] < 1
    assert scores["forbidden_tool_violations"] == 1
    assert scores["final_status_accuracy"] < 1
