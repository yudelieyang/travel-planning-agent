"""Create the Phase-L manual triage for the fixed offline SEM200 result."""

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "evals/results/hybrid_semantics_200_v1_offline.json"
AUDIT_JSON = ROOT / "evals/results/hybrid_semantics_200_v1_audit.json"
AUDIT_MD = ROOT / "evals/results/hybrid_semantics_200_v1_audit.md"
CLUSTERS_MD = ROOT / "evals/results/hybrid_semantics_200_failure_clusters.md"

# These are manual policy decisions, not parser calibration rules.
EVALUATOR_IDS = {
    "SEM200-116",
    "SEM200-117",
    "SEM200-118",
    "SEM200-119",
    "SEM200-121",
    "SEM200-123",
    "SEM200-124",
    "SEM200-125",
    "SEM200-126",
    "SEM200-127",
    "SEM200-128",
    "SEM200-129",
    "SEM200-130",
}
GOLD_ERROR_IDS = {"SEM200-193", "SEM200-197", "SEM200-198", "SEM200-200"}
UNSUPPORTED_IDS = {f"SEM200-{number:03d}" for number in range(156, 166)}
INTENTIONAL_HYBRID_IDS = {f"SEM200-{number:03d}" for number in range(166, 176)}
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
P1_IDS = {
    "SEM200-132",
    "SEM200-137",
    *{f"SEM200-{number:03d}" for number in range(167, 176)},
    "SEM200-186",
    "SEM200-187",
    "SEM200-188",
    "SEM200-189",
    "SEM200-191",
    "SEM200-192",
    "SEM200-194",
    "SEM200-195",
    "SEM200-196",
}


def _raw_safety_ids(records: list[dict]) -> dict[str, list[str]]:
    corruption, drops, amounts, scopes, hard_to_soft = [], [], [], [], []
    for record in records:
        expected, actual = _constraint_set(record, "expected"), _constraint_set(record, "final")
        if actual - expected:
            corruption.append(record["case_id"])
        if set(record["expected"]["unsupported_scopes"]) - set(
            record["final"]["unsupported_scopes"]
        ):
            drops.append(record["case_id"])
        if any(
            scope in {item[0] for item in actual}
            and value not in {item[1] for item in actual if item[0] == scope}
            for scope, value, _ in expected
        ):
            amounts.append(record["case_id"])
        if any(
            value in {item[1] for item in actual if item[0] != scope}
            for scope, value, _ in expected
        ):
            scopes.append(record["case_id"])
        if expected - actual and record["final"]["preferences"]:
            hard_to_soft.append(record["case_id"])
    return {
        "silent_hard_corruption": corruption,
        "unsupported_hard_drops": drops,
        "wrong_hard_amount": amounts,
        "wrong_hard_scope": scopes,
        "hard_to_soft": hard_to_soft,
    }


def _constraint_set(record: dict, side: str) -> set[tuple[str, float, str]]:
    return {
        (item["scope"], item["value"], item["strength"]) for item in record[side]["constraints"]
    }


def classify(record: dict) -> tuple[str, str, str, str]:
    """Return classification, root cause, risk, and recommended disposition."""
    case_id, category = record["case_id"], record["category"]
    if case_id in EVALUATOR_IDS:
        return (
            "EVALUATOR_BUG",
            "Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.",
            "none",
            "Keep the case; revise only the evaluation contract after Phase L.",
        )
    if case_id in GOLD_ERROR_IDS:
        return (
            "GOLD_LABEL_ERROR",
            "Gold demands hybrid/ambiguity semantics that the established contract does not require for this input.",
            "none",
            "Correct gold in a later benchmark-only change.",
        )
    if case_id in UNSUPPORTED_IDS:
        return (
            "UNSUPPORTED_BY_DESIGN",
            "Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.",
            "P2",
            "Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.",
        )
    if case_id in INTENTIONAL_HYBRID_IDS:
        return (
            "INTENTIONAL_HYBRID_BOUNDARY",
            "Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.",
            "P1" if not record["coverage"]["needs_llm"] else "none",
            "Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.",
        )
    if case_id in P0_IDS:
        root = "explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value"
        if case_id in {
            "SEM200-134",
            "SEM200-135",
            "SEM200-136",
            "SEM200-138",
            "SEM200-141",
            "SEM200-142",
        }:
            root = "unsupported hard requirement disappeared without a blocking semantic record"
        if case_id == "SEM200-115":
            root = "soft total target was promoted to an executable hard total"
        if case_id == "SEM200-120":
            root = "ambiguous hotel amount was promoted to executable HOTEL_TOTAL"
        return (
            "REAL_SCOPE_BUG" if case_id in {"SEM200-057", "SEM200-120"} else "REAL_AMOUNT_BUG",
            root,
            "P0",
            "Phase-M hard-safety investigation.",
        )
    if case_id in P1_IDS:
        return (
            "REAL_COVERAGE_FALSE_NEGATIVE",
            "Deterministic output loses required semantics while the coverage gate does not request augmentation.",
            "P1",
            "Phase-M coverage investigation after P0 triage.",
        )
    if "correction" in category:
        return (
            "REAL_CORRECTION_BUG",
            "Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.",
            "P2",
            "Audit correction bridge/segmentation together, after P0 cases.",
        )
    if category == "J_preferences" or "PREFERENCE_ERROR" in record["failure_categories"]:
        return (
            "REAL_PREFERENCE_BUG",
            "Required grounded preference is missing or normalization includes unrelated location text.",
            "P3",
            "Defer until hard safety and coverage are resolved.",
        )
    if (
        category in {"C_hotel_total_hard", "D_multi_scope"}
        and record["final"]["requires_clarification"]
    ):
        return (
            "REAL_AMBIGUITY_BUG",
            "Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.",
            "P2",
            "Investigate scope anchors after P0 triage.",
        )
    return (
        "REAL_PARSER_BUG",
        "Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.",
        "P2",
        "Cluster with the relevant parser-family audit; do not calibrate in Phase L.",
    )


def functional_llm_need(record: dict, audit: dict) -> bool:
    """Functional sufficiency, independent of the benchmark's historical label."""
    case_id = record["case_id"]
    if case_id in UNSUPPORTED_IDS or case_id in GOLD_ERROR_IDS:
        return False
    if record["expected"]["expected_runtime_llm_need"]:
        return True
    return audit["classification"].startswith("REAL_")


def build_audit(raw: dict) -> dict:
    audited_records = []
    for record in raw["records"]:
        if record["passed"]:
            continue
        classification, root, risk, disposition = classify(record)
        audit = {
            "classification": classification,
            "root_cause": root,
            "production_risk": risk,
            "recommended_disposition": disposition,
        }
        audit["functional_llm_need"] = functional_llm_need(record, audit)
        audit["audited_semantic_pass"] = classification in {
            "EVALUATOR_BUG",
            "GOLD_LABEL_ERROR",
        } or (classification == "INTENTIONAL_HYBRID_BOUNDARY" and record["coverage"]["needs_llm"])
        audited_records.append(
            {
                "case_id": record["case_id"],
                "category": record["category"],
                "input": record["input"],
                "gold_semantics": record["expected"],
                "actual_deterministic_semantics": record["deterministic"],
                "coverage_decision": record["coverage"],
                "reported_failure_types": record["failure_categories"],
                "audit": audit,
            }
        )
    classifications = Counter(item["audit"]["classification"] for item in audited_records)
    all_records = {item["case_id"]: item for item in raw["records"]}
    functional = {
        case_id: next(
            (
                item["audit"]["functional_llm_need"]
                for item in audited_records
                if item["case_id"] == case_id
            ),
            record["expected"]["expected_runtime_llm_need"],
        )
        for case_id, record in all_records.items()
    }
    actual = {case_id: record["coverage"]["needs_llm"] for case_id, record in all_records.items()}
    tp = sum(functional[key] and actual[key] for key in all_records)
    tn = sum(not functional[key] and not actual[key] for key in all_records)
    fp = sum(not functional[key] and actual[key] for key in all_records)
    fn = sum(functional[key] and not actual[key] for key in all_records)
    audited_passes = sum(record["passed"] for record in raw["records"]) + sum(
        item["audit"]["audited_semantic_pass"] for item in audited_records
    )
    category_triage = {}
    for category, raw_score in raw["metrics"]["category_pass_rates"].items():
        entries = [item for item in audited_records if item["category"] == category]
        category_triage[category] = {
            "raw_pass_rate": raw_score["pass_rate"],
            "true_semantic_bugs": sum(
                item["audit"]["classification"].startswith("REAL_") for item in entries
            ),
            "evaluator_or_gold_issues": sum(
                item["audit"]["classification"] in {"EVALUATOR_BUG", "GOLD_LABEL_ERROR"}
                for item in entries
            ),
            "intentional_hybrid": sum(
                item["audit"]["classification"] == "INTENTIONAL_HYBRID_BOUNDARY" for item in entries
            ),
            "unsupported_by_design": sum(
                item["audit"]["classification"] == "UNSUPPORTED_BY_DESIGN" for item in entries
            ),
        }
    return {
        "version": "hybrid_semantics_200_v1_audit",
        "source_result": RAW_PATH.name,
        "raw_case_pass_rate": raw["metrics"]["case_pass_rate"],
        "raw_metrics": raw["metrics"],
        "failed_case_count": len(audited_records),
        "records": audited_records,
        "summary": {
            "classification_counts": dict(classifications),
            "raw_safety_case_ids": _raw_safety_ids(raw["records"]),
            "category_triage": category_triage,
            "true_p0_case_ids": sorted(P0_IDS),
            "true_p1_case_ids": sorted(P1_IDS),
            "true_silent_hard_corruption": [
                "SEM200-057",
                "SEM200-080",
                "SEM200-085",
                "SEM200-091",
                "SEM200-097",
                "SEM200-099",
                "SEM200-115",
                "SEM200-120",
            ],
            "true_unsupported_hard_drops": [
                "SEM200-134",
                "SEM200-135",
                "SEM200-136",
                "SEM200-138",
                "SEM200-141",
                "SEM200-142",
            ],
            "true_wrong_hard_amounts": [
                "SEM200-080",
                "SEM200-085",
                "SEM200-091",
                "SEM200-097",
                "SEM200-099",
            ],
            "true_wrong_hard_scopes": ["SEM200-057"],
            "true_hard_to_soft_downgrades": [],
            "true_soft_to_hard_promotions": ["SEM200-115"],
            "audited_semantic_pass_rate": audited_passes / len(raw["records"]),
            "functional_coverage": _coverage_metrics(tp, tn, fp, fn),
        },
    }


def _coverage_metrics(tp: int, tn: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    return {
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "precision": precision,
        "recall": recall,
        "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
    }


def render_audit(audit: dict) -> str:
    summary = audit["summary"]
    lines = [
        "# Phase L — 200-Case Failure Audit",
        "",
        f"Failed cases audited: {audit['failed_case_count']}",
        "",
        "## Corrected baseline",
        "",
        f"Audited semantic pass: {summary['audited_semantic_pass_rate']:.1%}",
        f"Functional coverage: `{json.dumps(summary['functional_coverage'])}`",
        "",
        "## Classification counts",
        "",
    ]
    lines.extend(
        f"- {name}: {count}" for name, count in sorted(summary["classification_counts"].items())
    )
    lines += ["", "## Hard-safety audit", ""]
    by_id = {item["case_id"]: item for item in audit["records"]}
    for label, case_ids in summary["raw_safety_case_ids"].items():
        lines += [
            f"### Raw {label}",
            "",
            "| Case | Gold hard constraints | Actual hard constraints | Blocking state | Audit |",
            "| --- | --- | --- | --- | --- |",
        ]
        for case_id in case_ids:
            raw = by_id[case_id]
            lines.append(
                f"| {case_id} | `{raw['gold_semantics']['constraints']}` | `{raw['actual_deterministic_semantics']['constraints']}` | {raw['actual_deterministic_semantics']['requires_clarification']} | {raw['audit']['classification']} |"
            )
        lines.append("")
    lines += [
        "## Category triage",
        "",
        "| Category | Raw pass | Real bugs | Evaluator/gold | Hybrid | Unsupported |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for category, score in summary["category_triage"].items():
        lines.append(
            f"| {category} | {score['raw_pass_rate']:.1%} | {score['true_semantic_bugs']} | {score['evaluator_or_gold_issues']} | {score['intentional_hybrid']} | {score['unsupported_by_design']} |"
        )
    lines += ["", "## Failed-case audit table", ""]
    for item in audit["records"]:
        lines += [
            f"### {item['case_id']} — {item['audit']['classification']}",
            f"Category: {item['category']}",
            f"Input: {item['input']}",
            f"Gold: `{json.dumps(item['gold_semantics'], ensure_ascii=False)}`",
            f"Actual: `{json.dumps(item['actual_deterministic_semantics'], ensure_ascii=False)}`",
            f"Coverage: `{json.dumps(item['coverage_decision'], ensure_ascii=False)}`",
            f"Reported: {', '.join(item['reported_failure_types'])}",
            f"Root cause: {item['audit']['root_cause']}",
            f"Risk: {item['audit']['production_risk']}",
            f"Disposition: {item['audit']['recommended_disposition']}",
            "",
        ]
    return "\n".join(lines)


def render_clusters(audit: dict) -> str:
    treatment = {
        "EVALUATOR_BUG": "Evaluation-only: model retained ambiguity details before comparing semantic views.",
        "GOLD_LABEL_ERROR": "Benchmark-only: align gold with the Phase-J executable/ambiguity contract.",
        "INTENTIONAL_HYBRID_BOUNDARY": "Keep hybrid; add coverage only where semantic augmentation is warranted.",
        "REAL_AMBIGUITY_BUG": "Phase M P2: review explicit scope-anchor recognition.",
        "REAL_AMOUNT_BUG": "Phase M: triage P0 hard drops/corrections before broad parser work.",
        "REAL_CORRECTION_BUG": "Phase M P2: investigate bounded correction bridges as one family.",
        "REAL_COVERAGE_FALSE_NEGATIVE": "Phase M P1: coverage must request augmentation when deterministic semantics are incomplete.",
        "REAL_PARSER_BUG": "Phase M P2: group by destination and hard-ceiling phrase family.",
        "REAL_PREFERENCE_BUG": "Defer as P3 until hard safety and coverage are stable.",
        "REAL_SCOPE_BUG": "Phase M P0: prevent executable scope corruption.",
        "UNSUPPORTED_BY_DESIGN": "Keep non-executable; decide later whether explicit exclusion representation is in scope.",
    }
    grouped = defaultdict(list)
    for item in audit["records"]:
        grouped[item["audit"]["classification"]].append(item["case_id"])
    lines = ["# SEM200 Failure Clusters", ""]
    for classification, ids in sorted(grouped.items()):
        lines += [
            f"## {classification}",
            "",
            f"Cases: {', '.join(ids)}",
            f"Count: {len(ids)}",
            f"Recommended treatment: {treatment[classification]}",
            "",
        ]
    return "\n".join(lines)


def main() -> None:
    audit = build_audit(json.loads(RAW_PATH.read_text(encoding="utf-8")))
    AUDIT_JSON.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    AUDIT_MD.write_text(render_audit(audit), encoding="utf-8")
    CLUSTERS_MD.write_text(render_clusters(audit), encoding="utf-8")
    print(f"Audited {audit['failed_case_count']} failed cases")
    print(audit["summary"]["functional_coverage"])


if __name__ == "__main__":
    main()
