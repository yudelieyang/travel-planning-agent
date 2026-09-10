"""Offline extraction capability report. Known gaps are reported, not hidden as test skips."""

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.agent.extractor import RuleBasedRequirementsExtractor  # noqa: E402
from app.agent.requirements_evaluation import evaluate_requirements  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any capability case fails")
    args = parser.parse_args()
    path = ROOT / "evals/datasets/requirements_eval_v1.json"
    raw = path.read_bytes()
    report = evaluate_requirements(json.loads(raw), RuleBasedRequirementsExtractor())
    report.update(
        dataset="requirements_eval_v1",
        dataset_sha256=hashlib.sha256(raw).hexdigest(),
        extractor="RuleBasedRequirementsExtractor",
    )
    output = (
        ROOT
        / "evals/results"
        / ("requirements-" + datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
    )
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({name: report[name] for name in ("overall", "core", "robustness")}, indent=2))
    print("Failed cases: " + ", ".join(r["id"] for r in report["records"] if not r["full_match"]))
    print(f"Report: {output.relative_to(ROOT)}")
    return int(args.strict and report["overall"]["metrics"]["full_case"]["accuracy"] != 1)


if __name__ == "__main__":
    raise SystemExit(main())
