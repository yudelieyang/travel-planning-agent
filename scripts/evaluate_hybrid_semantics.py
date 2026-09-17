"""Evaluate hybrid semantics offline; pass --live only for explicit provider use."""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.agent.hybrid_evaluation import evaluate_dataset, load_dataset, write_report  # noqa: E402
from app.agent.semantic_extractor import create_semantic_extractor  # noqa: E402
from app.core.config import Settings  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Explicitly invoke the configured semantic extractor")
    parser.add_argument("--approved-model", help="Must match OPENAI_MODEL for live evaluation")
    parser.add_argument("--write", action="store_true", help="Write versioned JSON and Markdown reports")
    parser.add_argument("--dataset", default="hybrid_semantics_v1.json", help="Dataset filename")
    parser.add_argument("--label", help="Suffix for a non-baseline result artifact")
    args = parser.parse_args()
    dataset = load_dataset(PROJECT_ROOT / "evals/datasets" / args.dataset)
    mode = "live" if args.live else "offline"
    extractor = None
    if args.live:
        settings = Settings()
        if args.approved_model != settings.openai_model:
            parser.error("--approved-model must match OPENAI_MODEL")
        extractor = create_semantic_extractor(settings)
        if extractor is None:
            parser.error("Hybrid semantic extraction is not configured")
    try:
        report = evaluate_dataset(dataset, mode=mode, extractor=extractor)
    finally:
        if extractor is not None:
            extractor.client.close()
    print(f"Cases: {report['case_count']}")
    print(f"Coverage: {report['metrics']['coverage_gate']}")
    print(f"Hard safety: {report['metrics']['hard_constraint_safety']}")
    if args.write:
        results = PROJECT_ROOT / "evals/results"
        name = f"{dataset.version}_{args.label}" if args.label else f"{dataset.version}_{mode}"
        write_report(
            report,
            results / f"{name}.json",
            results / f"{name}.md",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
