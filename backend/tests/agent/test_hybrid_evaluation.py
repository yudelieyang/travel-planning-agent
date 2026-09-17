import json

import pytest

from app.agent.hybrid_evaluation import (
    SEM200_CATEGORY_COUNTS,
    HybridDataset,
    evaluate_dataset,
    load_dataset,
    render_markdown,
)
from app.core.config import PROJECT_ROOT

DATASET_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_v1.json"
HOLDOUT_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_holdout_v1.json"
LIVE_SUBSET_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_live_subset_k1.json"
SEM200_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_200_v1.json"
SEM200_LIVE_CANDIDATES_PATH = (
    PROJECT_ROOT / "evals/datasets/hybrid_semantics_200_live_candidates_v1.json"
)


def test_hybrid_dataset_is_versioned_and_manually_bounded():
    dataset = load_dataset(DATASET_PATH)

    assert dataset.version == "hybrid_semantics_v1"
    assert len(dataset.cases) == 50
    assert len({case.id for case in dataset.cases}) == 50


def test_dataset_rejects_duplicate_case_identifiers(tmp_path):
    raw = json.loads(DATASET_PATH.read_text("utf-8"))
    raw["cases"][1]["id"] = raw["cases"][0]["id"]
    path = tmp_path / "duplicate.json"
    path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate hybrid evaluation case IDs"):
        load_dataset(path)


def test_offline_evaluation_reports_coverage_confusion_and_merge_safety():
    report = evaluate_dataset(load_dataset(DATASET_PATH))
    metrics = report["metrics"]

    assert report["mode"] == "offline"
    assert metrics["coverage_gate"] == {
        "TP": 6,
        "TN": 26,
        "FP": 11,
        "FN": 7,
        "precision": 6 / 17,
        "recall": 6 / 13,
        "f1": 0.4,
        "false_positive_rate": 11 / 37,
    }
    assert metrics["hard_constraint_safety"]["silent_hard_constraint_corruption"] == 0
    assert metrics["merge"]["hallucination_rejections"] == 1


def test_offline_mock_cases_exercise_merge_outcomes_and_failure_reporting():
    report = evaluate_dataset(HybridDataset.model_validate_json(DATASET_PATH.read_text("utf-8")))
    records = {record["case_id"]: record for record in report["records"]}

    assert "ADDED_FROM_LLM" in records["HYBRID-040"]["merge"]["decisions"]
    assert "LLM_REJECTED_UNGROUNDED" in records["HYBRID-041"]["merge"]["decisions"]
    assert "UNSUPPORTED_RETAINED" in records["HYBRID-042"]["merge"]["decisions"]
    markdown = render_markdown(report)
    assert "HYBRID-001" in markdown
    assert "Coverage gate" in markdown


def test_holdout_allows_an_explicitly_deferred_hybrid_gap_after_coverage_requests_llm():
    report = evaluate_dataset(load_dataset(HOLDOUT_PATH))
    records = {record["case_id"]: record for record in report["records"]}

    assert report["metrics"]["case_pass_rate"] == 0.875
    assert report["metrics"]["deferred_hybrid_cases"] == 1
    assert report["metrics"]["coverage_gate"] == {
        "TP": 2,
        "TN": 12,
        "FP": 0,
        "FN": 2,
        "precision": 1.0,
        "recall": 0.5,
        "f1": 2 / 3,
        "false_positive_rate": 0.0,
    }
    assert records["HOLDOUT-016"]["coverage"]["needs_llm"] is True
    assert records["HOLDOUT-016"]["failure_categories"] == []


def test_live_mode_requires_an_explicit_extractor():
    with pytest.raises(ValueError, match="semantic extractor"):
        evaluate_dataset(load_dataset(DATASET_PATH), mode="live")


def test_phase_k_live_subset_is_bounded_and_contains_only_coverage_gate_cases():
    manifest = json.loads(LIVE_SUBSET_PATH.read_text("utf-8"))
    available = {}
    for path in (DATASET_PATH, HOLDOUT_PATH):
        available.update({case.id: case for case in load_dataset(path).cases})

    assert manifest["version"] == "hybrid_semantics_live_subset_k1"
    assert 10 <= len(manifest["case_ids"]) <= 15
    assert len(manifest["case_ids"]) == len(set(manifest["case_ids"]))
    assert "HOLDOUT-016" in manifest["case_ids"]
    assert all(available[case_id].expected.needs_llm for case_id in manifest["case_ids"])


def test_sem200_dataset_is_exactly_sized_and_schema_validated():
    dataset = load_dataset(SEM200_PATH)

    assert dataset.version == "hybrid_semantics_200_v1"
    assert len(dataset.cases) == 200
    assert [case.id for case in dataset.cases] == [
        f"SEM200-{number:03d}" for number in range(1, 201)
    ]
    assert {case.category for case in dataset.cases} == set(SEM200_CATEGORY_COUNTS)
    assert {
        category: sum(case.category == category for case in dataset.cases)
        for category in SEM200_CATEGORY_COUNTS
    } == SEM200_CATEGORY_COUNTS
    assert len({case.input for case in dataset.cases}) == 200
    assert all(case.expected.expected_runtime_llm_need is not None for case in dataset.cases)


def test_sem200_rejects_invalid_gold_and_duplicate_normalized_input(tmp_path):
    raw = json.loads(SEM200_PATH.read_text("utf-8"))
    raw["cases"][1]["input"] = raw["cases"][0]["input"].upper()
    path = tmp_path / "duplicate-normalized.json"
    path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate normalized"):
        load_dataset(path)

    raw = json.loads(SEM200_PATH.read_text("utf-8"))
    raw["cases"][0]["expected"]["constraints"] = [{"scope": "NOT_A_SCOPE", "value": 10}]
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError):
        load_dataset(path)


def test_sem200_live_candidates_are_bounded_and_semantically_eligible():
    dataset = load_dataset(SEM200_PATH)
    eligible = {case.id for case in dataset.cases if case.expected.expected_runtime_llm_need}
    manifest = json.loads(SEM200_LIVE_CANDIDATES_PATH.read_text("utf-8"))
    candidate_ids = [item["case_id"] for item in manifest["candidates"]]

    assert manifest["version"] == "hybrid_semantics_200_live_candidates_v1"
    assert 20 <= len(candidate_ids) <= 30
    assert len(candidate_ids) == len(set(candidate_ids))
    assert set(candidate_ids).issubset(eligible)
    assert {item["priority"] for item in manifest["candidates"]} == {"high", "medium"}
