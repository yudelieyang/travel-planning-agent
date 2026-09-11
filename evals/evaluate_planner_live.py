"""Controlled planner A/B harness. Default dry-run; live needs explicit approval and flags."""

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
# This experiment does not use external tracing, regardless of ambient shell settings.
os.environ["LANGSMITH_TRACING"] = "false"
os.environ["LANGCHAIN_TRACING_V2"] = "false"

from app.agent.live_evaluation import (  # noqa: E402
    DEFAULT_MAX_CASES,
    prepare_cases,
    provenance,
    run_comparison,
    write_report,
)
from app.agent.live_simulation import MOCK_MODEL, simulated_planner  # noqa: E402
from app.agent.openai_planner import OpenAIPlanner, PlannerConfigurationError  # noqa: E402
from app.core.config import Settings  # noqa: E402


def check_live_configuration(settings, approved_model):
    if not settings.openai_api_key.get_secret_value().strip():
        raise PlannerConfigurationError("OPENAI_API_KEY is required; live was not started")
    if not settings.openai_model.strip():
        raise PlannerConfigurationError("OPENAI_MODEL is required; live was not started")
    if approved_model != settings.openai_model.strip():
        raise PlannerConfigurationError("--approved-model must match OPENAI_MODEL")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true")
    modes.add_argument(
        "--simulate", action="store_true", help="MockTransport only; no provider calls"
    )
    modes.add_argument(
        "--live", action="store_true", help="Paid requests; obtain user approval first"
    )
    parser.add_argument("--max-cases", type=int, default=DEFAULT_MAX_CASES)
    parser.add_argument("--approved-model")
    args = parser.parse_args(argv)
    path = ROOT / "evals/datasets/planner_live_smoke_v1.json"
    try:
        settings = Settings()
        if args.live:
            check_live_configuration(settings, args.approved_model)
        dataset, selected = prepare_cases(path, args.max_cases)
        metadata = provenance(ROOT, path)
        metadata.update(
            dataset_version=dataset.version, prompt_version=settings.planner_prompt_version
        )
    except ValueError as exc:
        parser.error(str(exc))
    if not args.live and not args.simulate:
        print(
            json.dumps(
                {
                    "mode": "DRY RUN",
                    "dataset": dataset.version,
                    "dataset_cases": len(dataset.cases),
                    "selected_cases": [c.case_id for c in selected],
                    "number_of_live_cases": len(selected),
                    "planner": "OpenAIPlanner (NOT RUN)",
                    "extractor": "RuleBasedRequirementsExtractor",
                    "model_configuration": "configured"
                    if settings.openai_model.strip()
                    else "not configured",
                    "expected_api_requests_if_later_authorized": len(selected),
                    "actual_api_requests": 0,
                    "provenance": metadata,
                },
                indent=2,
            )
        )
        return 0
    mode = "live" if args.live else "mock"
    factory = (
        (lambda: OpenAIPlanner(settings)) if args.live else (lambda: simulated_planner(settings))
    )
    report = run_comparison(
        selected,
        metadata=metadata,
        mode=mode,
        planner_factory=factory,
        model=settings.openai_model.strip() if args.live else MOCK_MODEL,
        prompt_version=settings.planner_prompt_version,
    )
    output = (
        ROOT
        / "evals/results"
        / ("planner-" + mode + "-" + datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
    )
    write_report(report, output)
    print(
        json.dumps(
            {
                "mode": mode,
                "comparison": report["comparison"],
                "provider_requests": report["provider_requests"],
                "mock_requests": report["mock_requests"],
                "stopped_early": report["stopped_early"],
            },
            indent=2,
        )
    )
    print(f"Report: {output.relative_to(ROOT)}")
    return int(report["stopped_early"] or not all(r["case_success"] for r in report["records"]))


if __name__ == "__main__":
    raise SystemExit(main())
