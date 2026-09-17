from pathlib import Path

import pytest
from scripts.evaluate_hybrid_live import CallBudgetExtractor, load_live_cases
from scripts.replay_hybrid_m3 import replay, replay_recorded
from scripts.replay_hybrid_m4 import replay as replay_m4

from app.agent.hybrid_evaluation import evaluate_cases, load_dataset
from app.agent.semantic_extractor import SemanticExtractionResult

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_200_live_subset_m3.json"
M4_MANIFEST_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_200_live_subset_m4.json"
M5_MANIFEST_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_live_subset_m5.json"
M6_MANIFEST_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_live_subset_m6.json"
DATASET_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_200_v1.json"
M5_DATASET_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_m5_correction_holdout_v1.json"
M5_RESULT_PATH = PROJECT_ROOT / "evals/results/hybrid_semantics_live_m5.json"


class FakeExtractor:
    model = "gpt-5.6-luna"
    prompt_version = "semantic_extractor_v1"

    def __init__(self):
        self.calls = 0
        self.client = object()

    def extract(self, _query):
        self.calls += 1
        return SemanticExtractionResult()

    def get_observation(self):
        return {"latency_ms": 1, "input_tokens": 1, "output_tokens": 1, "total_tokens": 2}


def test_m3_manifest_is_exactly_bounded_and_functionally_gate_positive():
    manifest, cases = load_live_cases(MANIFEST_PATH)

    assert manifest["model"] == "gpt-5.6-luna"
    assert manifest["prompt_version"] == "semantic_extractor_v1"
    assert len(cases) == 25
    assert len({case.id for case in cases}) == 25
    assert [case.id for case in cases] == manifest["case_ids"]


def test_live_evaluation_calls_on_functional_gate_not_stale_dataset_flag():
    case = next(case for case in load_dataset(DATASET_PATH).cases if case.id == "SEM200-081")
    extractor = FakeExtractor()

    report = evaluate_cases([case], dataset_version="test", mode="live", extractor=extractor)

    assert case.expected.needs_llm is False
    assert report["records"][0]["coverage"]["needs_llm"] is True
    assert extractor.calls == 1


def test_call_budget_fails_closed_before_an_extra_attempt():
    extractor = FakeExtractor()
    bounded = CallBudgetExtractor(extractor, 1)

    bounded.extract("first")
    with pytest.raises(RuntimeError, match="budget exceeded"):
        bounded.extract("second")

    assert bounded.calls == 1
    assert extractor.calls == 1


def test_m4_recorded_proposal_replay_contains_m3_failures_and_clears_hard_safety():
    report = replay()
    required = {
        f"SEM200-{number:03d}"
        for number in (81, 93, 95, 116, 122, 125, 156, 158, 163, 166, 169, 172, 175, 186, 189, 192, 194, 199)
    }

    assert required.issubset({record["case_id"] for record in report["records"]})
    assert set(report["replay_summary"]["new_hard_safety"].values()) == {0}
    assert report["replay_summary"]["api_calls"] == 0


def test_m4_live_manifest_is_fresh_bounded_and_uses_v2():
    m3, _ = load_live_cases(MANIFEST_PATH)
    m4, cases = load_live_cases(M4_MANIFEST_PATH)

    assert len(cases) == 18
    assert not set(m4["case_ids"]) & set(m3["case_ids"])
    assert m4["model"] == "gpt-5.6-luna"
    assert m4["prompt_version"] == "semantic_extractor_v2"


def test_m5_m4_replay_quarantines_both_recorded_stale_corrections():
    report = replay_m4()
    records = {record["case_id"]: record for record in report["records"]}

    assert report["replay_summary"]["api_calls"] == 0
    assert report["replay_summary"]["new_hard_safety"]["wrong_hard_amount_accepted"] == 0
    assert all(
        not any(
            item["scope"] == "HOTEL_TOTAL" and item["value"] == stale
            for item in records[case_id]["final"]["constraints"]
        )
        for case_id, stale in (("SEM200-096", 420), ("SEM200-098", 460))
    )
    assert all(records[case_id]["final"]["requires_clarification"] for case_id in ("SEM200-096", "SEM200-098"))


def test_m5_live_manifest_is_frozen_exactly_bounded_and_uses_v2():
    manifest, cases = load_live_cases(M5_MANIFEST_PATH)

    assert len(cases) == 10
    assert len({case.id for case in cases}) == 10
    assert [case.id for case in cases] == manifest["case_ids"]
    assert sum(manifest["live_category_mix"].values()) == 10
    assert manifest["model"] == "gpt-5.6-luna"
    assert manifest["prompt_version"] == "semantic_extractor_v2"


def test_m6_m5_recorded_proposals_replay_with_frozen_hard_safety():
    report = replay_recorded(
        M5_RESULT_PATH,
        "hybrid_semantics_live_m5_replay_m6",
        M5_DATASET_PATH,
    )

    assert report["replay_summary"]["api_calls"] == 0
    assert set(report["replay_summary"]["new_hard_safety"].values()) == {0}
    assert report["replay_summary"]["new_canonical_accuracy"] == pytest.approx(0.7)


def test_m6_live_manifest_is_frozen_exactly_bounded_and_uses_v3():
    manifest, cases = load_live_cases(M6_MANIFEST_PATH)

    assert len(cases) == 12
    assert len({case.id for case in cases}) == 12
    assert [case.id for case in cases] == manifest["case_ids"]
    assert sum(manifest["live_category_mix"].values()) == 12
    assert sum(item.get("correction_target") is not None for item in manifest["cases"]) == 8
    assert manifest["model"] == "gpt-5.6-luna"
    assert manifest["prompt_version"] == "semantic_extractor_v3"
