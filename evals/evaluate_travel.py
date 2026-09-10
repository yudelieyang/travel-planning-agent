"""Deterministic full-dataset regression. No live/provider mode."""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.agent.evaluation import evaluate_case, score_records  # noqa: E402
from app.agent.planner import DeterministicTestPlanner  # noqa: E402


def main():
    cases = json.loads((ROOT / "evals/datasets/travel_smoke_v1.json").read_text("utf-8"))
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
    report = {
        "planner": "deterministic",
        "dataset": "travel_smoke_v1",
        "prompt_version": "N/A",
        "metrics": scores,
        "records": records,
    }
    path = (
        ROOT
        / "evals/results"
        / ("baseline-" + datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
    )
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in scores.items() if k not in ("case_checks", "counts")}, indent=2
        )
    )
    print(f"Report: {path.relative_to(ROOT)}")
    return 0 if scores["case_pass_rate"] == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
