"""Write the Phase-M1 P0 safety delta against the frozen SEM200 corpus."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.agent.requirements import parse_requirements

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "evals/datasets/hybrid_semantics_200_v1.json"
RESULT_PATH = ROOT / "evals/results/hybrid_semantics_200_v1_phase_m1.json"
OUTPUT_JSON = ROOT / "evals/results/phase_m1_hard_safety_delta.json"
OUTPUT_MD = ROOT / "evals/results/phase_m1_hard_safety_delta.md"

P0_IDS = {
    "SEM200-024",
    "SEM200-026",
    "SEM200-027",
    "SEM200-028",
    "SEM200-030",
    "SEM200-032",
    "SEM200-057",
    "SEM200-061",
    "SEM200-064",
    "SEM200-066",
    "SEM200-068",
    "SEM200-075",
    "SEM200-080",
    "SEM200-082",
    "SEM200-085",
    "SEM200-091",
    "SEM200-097",
    "SEM200-099",
    "SEM200-115",
    "SEM200-120",
    "SEM200-134",
    "SEM200-135",
    "SEM200-136",
    "SEM200-138",
    "SEM200-141",
    "SEM200-142",
}

BEFORE = {
    "silent_hard_constraint_corruption": 8,
    "wrong_hard_scope": 1,
    "wrong_hard_amount": 5,
    "soft_to_hard_unsafe_promotion": 1,
    "hard_to_soft_unsafe_downgrade": 0,
    "unsupported_hard_constraints_silently_dropped": 6,
}


def constraint_set(items: list) -> set[tuple[str, float]]:
    return {(item["scope"], item["value"]) for item in items}


def build_report() -> dict:
    cases = {
        case["id"]: case
        for case in json.loads(DATASET_PATH.read_text(encoding="utf-8"))["cases"]
        if case["id"] in P0_IDS
    }
    evaluation = {
        item["case_id"]: item
        for item in json.loads(RESULT_PATH.read_text(encoding="utf-8"))["records"]
    }
    records = []
    after = {key: 0 for key in BEFORE}

    for case_id in sorted(P0_IDS):
        case = cases[case_id]
        expected = case["expected"]
        requirements = parse_requirements(case["input"])
        actual = {
            (item.scope.value, item.value) for item in requirements.requirements_v2.constraints
        }
        gold = constraint_set(expected.get("constraints", []))
        blocking = any(
            item.level.value == "BLOCKING" for item in requirements.requirements_v2.ambiguities
        )
        unsupported = expected.get("unsupported_scopes", [])

        if actual - gold:
            after["silent_hard_constraint_corruption"] += 1
        if any(
            value in {candidate[1] for candidate in actual if candidate[0] != scope}
            for scope, value in gold
        ):
            after["wrong_hard_scope"] += 1
        if any(
            scope in {candidate[0] for candidate in actual}
            and value not in {candidate[1] for candidate in actual if candidate[0] == scope}
            for scope, value in gold
        ):
            after["wrong_hard_amount"] += 1
        if case_id == "SEM200-115" and actual:
            after["soft_to_hard_unsafe_promotion"] += 1
        if gold and not gold.issubset(actual) and not blocking:
            after["hard_to_soft_unsafe_downgrade"] += 1
        if unsupported and not blocking:
            after["unsupported_hard_constraints_silently_dropped"] += 1

        records.append(
            {
                "case_id": case_id,
                "gold_constraints": sorted(gold),
                "actual_constraints": sorted(actual),
                "blocking": blocking,
                "unsupported_scopes": unsupported,
                "generic_evaluator_failures": evaluation[case_id]["failure_categories"],
                "p0_safe": actual == gold
                and (not unsupported or blocking)
                and (not expected.get("ambiguity_levels") or blocking),
            }
        )

    return {
        "version": "phase_m1_hard_safety_delta_v1",
        "dataset": DATASET_PATH.name,
        "source_result": RESULT_PATH.name,
        "p0_case_ids": sorted(P0_IDS),
        "before": BEFORE,
        "after": after,
        "remaining_p0_cases": [item["case_id"] for item in records if not item["p0_safe"]],
        "records": records,
    }


def render(report: dict) -> str:
    lines = [
        "# Phase M1 — Hard-Safety Delta",
        "",
        "Scope: the 26 P0 cases manually audited in Phase L. This does not reinterpret unrelated SEM200 coverage or preference failures.",
        "",
        "## Audited P0 result",
        "",
        f"P0 cases safe: {len(report['p0_case_ids']) - len(report['remaining_p0_cases'])}/{len(report['p0_case_ids'])}",
        f"Remaining P0 hard-safety cases: {report['remaining_p0_cases'] or 'none'}",
        "",
        "| Metric | Phase L baseline | Phase M1 |",
        "| --- | ---: | ---: |",
    ]
    lines.extend(
        f"| {metric.replace('_', ' ')} | {report['before'][metric]} | {report['after'][metric]} |"
        for metric in report["before"]
    )
    lines += [
        "",
        "## Residual generic-evaluator observations",
        "",
        "These are not retained P0 hard-safety defects:",
    ]
    for item in report["records"]:
        if item["generic_evaluator_failures"]:
            lines.append(f"- {item['case_id']}: {', '.join(item['generic_evaluator_failures'])}")
    lines += [
        "",
        "`PARSER_MISS` records above are unrelated destination parsing misses; `SEM200-120` is the Phase L evaluator-contract ambiguity observation. The P0 semantic oracle confirms their money safety state.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    report = build_report()
    OUTPUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render(report), encoding="utf-8")
    if report["remaining_p0_cases"]:
        raise SystemExit(f"P0 safety residue: {report['remaining_p0_cases']}")
    print("P0 hard-safety residue: none")


if __name__ == "__main__":
    main()
