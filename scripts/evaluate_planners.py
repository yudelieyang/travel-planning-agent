"""Offline by default. Run --live only after explicit approval of model and request budget."""

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.agent.evaluation import SMOKE_CASE_IDS, LimitedPlanner, evaluate_case  # noqa: E402
from app.agent.openai_planner import OpenAIPlanner, PlannerConfigurationError  # noqa: E402
from app.agent.planner import DeterministicTestPlanner  # noqa: E402
from app.core.config import Settings  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live", action="store_true", help="Explicitly enable up to 3 paid requests"
    )
    parser.add_argument("--approved-model", help="Must match the model approved before live use")
    args = parser.parse_args()
    settings = Settings()
    provider = None
    if args.live:
        if not args.approved_model or args.approved_model != settings.openai_model:
            parser.error("--approved-model must match OPENAI_MODEL; obtain approval first")
        try:
            provider = OpenAIPlanner(settings)
        except PlannerConfigurationError as exc:
            parser.error(str(exc))
    dataset = json.loads((PROJECT_ROOT / "evals/datasets/travel_smoke_v1.json").read_text("utf-8"))
    cases = [case for case in dataset if case["id"] in SMOKE_CASE_IDS]
    planners = [("deterministic", DeterministicTestPlanner(), None, None)]
    if provider:
        planners.append(
            (
                "openai",
                LimitedPlanner(provider, max_calls=3),
                settings.openai_model,
                settings.planner_prompt_version,
            )
        )
    results = PROJECT_ROOT / "evals/results"
    results.mkdir(exist_ok=True)
    output = results / (datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ") + ".jsonl")
    failed = False
    try:
        with output.open("x", encoding="utf-8") as stream:
            for name, planner, model, prompt in planners:
                for case in cases:
                    record = evaluate_case(
                        case, planner, planner_name=name, model=model, prompt_version=prompt
                    )
                    stream.write(json.dumps(record, ensure_ascii=False) + "\n")
                    stream.flush()
                    print(f"{case['id']} {name}: {record['final_status']}")
                    if record["final_status"] == "error":
                        failed = True
                        break  # Stop this run on the first failure; never retry automatically.
                if failed:
                    break
    finally:
        if provider:
            provider.client.close()
    print(f"Results: {output.relative_to(PROJECT_ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
