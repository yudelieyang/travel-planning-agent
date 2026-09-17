"""Replay the frozen M3 proposals through the current deterministic merge policy."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from scripts.evaluate_hybrid_live import annotate_records, live_metrics  # noqa: E402

from app.agent.hybrid_evaluation import evaluate_cases, load_dataset  # noqa: E402
from app.agent.semantic_extractor import SemanticExtractionResult  # noqa: E402

M3_PATH = PROJECT_ROOT / "evals/results/hybrid_semantics_200_live_m3.json"
OUTPUT_PATH = PROJECT_ROOT / "evals/results/hybrid_semantics_200_m3_replay_m4.json"
MARKDOWN_PATH = PROJECT_ROOT / "evals/results/hybrid_semantics_200_m3_replay_m4.md"
SEM200_DATASET_PATH = PROJECT_ROOT / "evals/datasets/hybrid_semantics_200_v1.json"


def replay_recorded(
    source_path: Path,
    dataset_version: str,
    dataset_path: Path = SEM200_DATASET_PATH,
) -> dict:
    original = json.loads(source_path.read_text("utf-8"))
    available = {
        case.id: case
        for case in load_dataset(dataset_path).cases
    }
    cases = []
    for record in original["records"]:
        proposal = SemanticExtractionResult.model_validate(record["proposal"])
        cases.append(available[record["case_id"]].model_copy(update={"mock_proposal": proposal}))
    report = evaluate_cases(cases, dataset_version=dataset_version)
    categories = {
        record["case_id"]: record.get("selection_category", record["category"])
        for record in original["records"]
    }
    for record in report["records"]:
        record["selection_category"] = categories[record["case_id"]]
    annotate_records(report)
    replay_metrics = live_metrics(report)
    report["replay_summary"] = {
        "api_calls": 0,
        "original_canonical_accuracy": original["live_metrics"]["final_hybrid_semantic_accuracy"],
        "new_canonical_accuracy": replay_metrics["final_hybrid_semantic_accuracy"],
        "original_accepted_precision": original["live_metrics"]["merge"]["accepted_augmentation_precision"],
        "new_accepted_precision": replay_metrics["merge"]["accepted_augmentation_precision"],
        "original_hard_safety": original["live_metrics"]["hard_safety"],
        "new_hard_safety": replay_metrics["hard_safety"],
    }
    report["replay_metrics"] = replay_metrics
    return report


def replay() -> dict:
    return replay_recorded(M3_PATH, "hybrid_semantics_200_m3_replay_m4")


def render_markdown(report: dict, title: str = "Phase M4 — M3 Recorded-Proposal Replay") -> str:
    summary = report["replay_summary"]
    return "\n".join(
        [
            f"# {title}",
            "",
            "API calls: 0",
            f"Original canonical accuracy: {summary['original_canonical_accuracy']:.1%}",
            f"New canonical accuracy: {summary['new_canonical_accuracy']:.1%}",
            f"Original accepted precision: `{json.dumps(summary['original_accepted_precision'])}`",
            f"New accepted precision: `{json.dumps(summary['new_accepted_precision'])}`",
            f"Original hard safety: `{json.dumps(summary['original_hard_safety'])}`",
            f"New hard safety: `{json.dumps(summary['new_hard_safety'])}`",
            "",
        ]
    )


def main() -> int:
    report = replay()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MARKDOWN_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["replay_summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
