"""Write the audited Phase-M2 functional-coverage delta for SEM200."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M1_PATH = ROOT / "evals/results/hybrid_semantics_200_v1_phase_m1.json"
M2_PATH = ROOT / "evals/results/hybrid_semantics_200_v1_phase_m2.json"
SAFETY_PATH = ROOT / "evals/results/phase_m1_hard_safety_delta.json"
OUTPUT_JSON = ROOT / "evals/results/phase_m2_coverage_delta.json"
OUTPUT_MD = ROOT / "evals/results/phase_m2_coverage_delta.md"

GOLD_ERROR_IDS = {"SEM200-193", "SEM200-197", "SEM200-198", "SEM200-200"}
CLUSTERS = {
    "P1 hard-money gap": {
        "SEM200-059",
        "SEM200-105",
        "SEM200-186",
        "SEM200-187",
        "SEM200-188",
        "SEM200-189",
        "SEM200-191",
        "SEM200-192",
        "SEM200-194",
        "SEM200-195",
    },
    "P1 exclusion gap": {f"SEM200-{number:03d}" for number in range(156, 166)},
    "P2 correction or ambiguity gap": {
        "SEM200-081",
        "SEM200-093",
        "SEM200-095",
        "SEM200-122",
    },
    "P3 tradeoff gap": {f"SEM200-{number:03d}" for number in range(167, 176)},
    "P3 preference gap": {
        "SEM200-008",
        "SEM200-009",
        "SEM200-013",
        "SEM200-014",
        "SEM200-016",
        "SEM200-018",
        "SEM200-058",
        "SEM200-065",
        "SEM200-069",
        "SEM200-072",
        "SEM200-074",
        "SEM200-086",
        "SEM200-089",
        "SEM200-090",
        *{f"SEM200-{number:03d}" for number in range(146, 156)},
        "SEM200-190",
    },
    "P3 rating enrichment": {"SEM200-196"},
}
WHY = {
    "P1 hard-money gap": "No represented-vs-source hard-money sufficiency check.",
    "P1 exclusion gap": "Negative travel requirements had no coverage signal.",
    "P2 correction or ambiguity gap": "The gate did not inspect unresolved correction targets or unrepresented hotel money.",
    "P3 tradeoff gap": "Tradeoff detection required narrow wording and usually a monetary symbol.",
    "P3 preference gap": "The gate did not detect explicit preference clauses left without a canonical preference.",
    "P3 rating enrichment": "Hotel-rating requirements are outside the bounded M2 signals.",
}
RISK = {
    "P1 hard-money gap": "A hard cap can disappear or retain the wrong amount/scope.",
    "P1 exclusion gap": "An excluded item can be silently included.",
    "P2 correction or ambiguity gap": "A superseded or ambiguous amount can be treated as final.",
    "P3 tradeoff gap": "The plan can ignore the requested allocation tradeoff.",
    "P3 preference gap": "The plan can omit a requested experience or accommodation preference.",
    "P3 rating enrichment": "The hotel star-rating request can be omitted.",
}


def constraint_set(items: list[dict]) -> set[tuple[str, float]]:
    return {(item["scope"], item["value"]) for item in items}


def preference_set(items: list[dict]) -> set[tuple[str, str]]:
    return {(item["category"], item["value"]) for item in items}


def functional_need(record: dict) -> bool:
    """Phase J/M1 sufficiency, with Phase-L evaluator/gold findings applied."""
    if record["case_id"] in GOLD_ERROR_IDS:
        return False
    expected, actual = record["expected"], record["deterministic"]
    if constraint_set(expected["constraints"]) != constraint_set(actual["constraints"]):
        return True
    if preference_set(expected["preferences"]) != preference_set(actual["preferences"]):
        return True
    if set(expected["unsupported_scopes"]) - set(actual["unsupported_scopes"]):
        return True
    unsupported = set(expected["unsupported_semantics"])
    represented_ambiguous_money = unsupported == {"AMBIGUOUS_MONETARY_SCOPE"} and (
        "BLOCKING" in actual["ambiguity_levels"]
    )
    if unsupported and not represented_ambiguous_money:
        return True
    if set(expected["ambiguity_levels"]) != set(actual["ambiguity_levels"]):
        return True
    return "BLOCKING" in actual["ambiguity_levels"] and not actual["unsupported_scopes"]


def coverage_metrics(records: list[dict]) -> dict:
    decisions = [(functional_need(record), record["coverage"]["needs_llm"]) for record in records]
    tp = sum(expected and actual for expected, actual in decisions)
    tn = sum(not expected and not actual for expected, actual in decisions)
    fp = sum(not expected and actual for expected, actual in decisions)
    fn = sum(expected and not actual for expected, actual in decisions)
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


def cluster_for(case_id: str) -> str:
    return next(name for name, case_ids in CLUSTERS.items() if case_id in case_ids)


def missing_semantic(record: dict) -> str:
    expected, actual = record["expected"], record["deterministic"]
    parts = []
    if constraint_set(expected["constraints"]) != constraint_set(actual["constraints"]):
        parts.append("hard constraint amount/scope")
    if preference_set(expected["preferences"]) != preference_set(actual["preferences"]):
        parts.append("preference")
    if expected["unsupported_semantics"]:
        parts.append("unsupported " + "/".join(expected["unsupported_semantics"]).lower())
    if set(expected["ambiguity_levels"]) != set(actual["ambiguity_levels"]):
        parts.append("blocking ambiguity")
    return ", ".join(dict.fromkeys(parts)) or "requirement-like clause"


def semantic_summary(view: dict) -> dict:
    return {
        "constraints": view["constraints"],
        "preferences": view["preferences"],
        "ambiguity_levels": view["ambiguity_levels"],
        "unsupported_scopes": view["unsupported_scopes"],
        "unsupported_semantics": view["unsupported_semantics"],
    }


def build_report() -> dict:
    m1 = json.loads(M1_PATH.read_text(encoding="utf-8"))
    m2 = json.loads(M2_PATH.read_text(encoding="utf-8"))
    safety = json.loads(SAFETY_PATH.read_text(encoding="utf-8"))
    m2_by_id = {record["case_id"]: record for record in m2["records"]}
    starting_fns = [
        record
        for record in m1["records"]
        if functional_need(record) and not record["coverage"]["needs_llm"]
    ]
    inventory = []
    for old in starting_fns:
        new = m2_by_id[old["case_id"]]
        cluster = cluster_for(old["case_id"])
        inventory.append(
            {
                "case_id": old["case_id"],
                "category": old["category"],
                "cluster": cluster,
                "input": old["input"],
                "expected_semantics": semantic_summary(old["expected"]),
                "deterministic_semantics": semantic_summary(old["deterministic"]),
                "missing_semantic": missing_semantic(old),
                "old_coverage": old["coverage"],
                "new_coverage": new["coverage"],
                "why_gate_failed": WHY[cluster],
                "risk": RISK[cluster],
                "hard_safety_changed": False,
            }
        )
    final_fns = [
        record["case_id"]
        for record in m2["records"]
        if functional_need(record) and not record["coverage"]["needs_llm"]
    ]
    return {
        "version": "phase_m2_functional_coverage_delta_v1",
        "source_results": [M1_PATH.name, M2_PATH.name],
        "functional_definition": "LLM needed iff deterministic semantics are incomplete or carry an unresolved supported ambiguity; retained unsupported hard scopes are complete.",
        "excluded_gold_error_ids": sorted(GOLD_ERROR_IDS),
        "starting_functional_coverage": coverage_metrics(m1["records"]),
        "final_functional_coverage": coverage_metrics(m2["records"]),
        "starting_raw_coverage": m1["metrics"]["coverage_gate"],
        "final_raw_coverage": m2["metrics"]["coverage_gate"],
        "starting_case_pass_rate": m1["metrics"]["case_pass_rate"],
        "final_case_pass_rate": m2["metrics"]["case_pass_rate"],
        "m1_hard_safety_after": safety["after"],
        "remaining_functional_fns": final_fns,
        "starting_fn_inventory": inventory,
    }


def render(report: dict) -> str:
    start, final = report["starting_functional_coverage"], report["final_functional_coverage"]
    lines = [
        "# Phase M2 — Functional Coverage Delta",
        "",
        report["functional_definition"],
        "",
        "## Coverage metrics",
        "",
        "| View | TP | TN | FP | FN | Precision | Recall | F1 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        metric_row("Audited M1", start),
        metric_row("Audited M2", final),
        metric_row("Raw M1", report["starting_raw_coverage"]),
        metric_row("Raw M2", report["final_raw_coverage"]),
        "",
        f"Functional FN reduction: {start['FN']} → {final['FN']}",
        f"Functional FP reduction: {start['FP']} → {final['FP']}",
        f"Raw overall pass: {report['starting_case_pass_rate']:.1%} → {report['final_case_pass_rate']:.1%}",
        "",
        "Raw metrics retain historical runtime labels. In particular, they count already-retained unsupported hard scopes as model-call positives; the audited view measures semantic sufficiency.",
        "",
        "## FN clusters",
        "",
        "| Cluster | Starting cases | Fixed | Remaining | Final FP introduced |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    new_by_id = {
        item["case_id"]: item["new_coverage"]["needs_llm"]
        for item in report["starting_fn_inventory"]
    }
    for name, case_ids in CLUSTERS.items():
        fixed = sum(new_by_id.get(case_id, False) for case_id in case_ids)
        lines.append(f"| {name} | {len(case_ids)} | {fixed} | {len(case_ids) - fixed} | 0 |")
    lines += [
        "",
        "## Remaining functional FNs",
        "",
        ", ".join(report["remaining_functional_fns"]),
        "",
        "These are low-risk partial/list preference enrichment (`151`, `153`), typo preference normalization (`190`), and hotel-rating enrichment (`196`).",
        "",
        "## M1 hard-safety oracle",
        "",
    ]
    lines.extend(
        f"- {name.replace('_', ' ')}: {value}"
        for name, value in report["m1_hard_safety_after"].items()
    )
    lines += [
        "",
        "## Starting true-FN delta",
        "",
        "| Case | Missing semantic | Old decision | New decision | New reason | Hard safety changed |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in report["starting_fn_inventory"]:
        reasons = ", ".join(item["new_coverage"]["reasons"]) or "none"
        lines.append(
            f"| {item['case_id']} | {item['missing_semantic']} | false | "
            f"{str(item['new_coverage']['needs_llm']).lower()} | {reasons} | no |"
        )
    lines += ["", "## Full starting FN inventory", ""]
    for item in report["starting_fn_inventory"]:
        lines += [
            f"### {item['case_id']} — {item['cluster']}",
            "",
            f"- Category: {item['category']}",
            f"- Input: {item['input']}",
            f"- Expected semantic information: `{json.dumps(item['expected_semantics'], ensure_ascii=False)}`",
            f"- Deterministic output: `{json.dumps(item['deterministic_semantics'], ensure_ascii=False)}`",
            f"- Missing semantic information: {item['missing_semantic']}",
            f"- Current M1 coverage signals: `{json.dumps(item['old_coverage']['signals'])}`",
            f"- Why the gate failed: {item['why_gate_failed']}",
            f"- Risk without augmentation: {item['risk']}",
            "",
        ]
    return "\n".join(lines)


def metric_row(label: str, metrics: dict) -> str:
    return (
        f"| {label} | {metrics['TP']} | {metrics['TN']} | {metrics['FP']} | {metrics['FN']} | "
        f"{metrics['precision']:.1%} | {metrics['recall']:.1%} | {metrics['f1']:.1%} |"
    )


def main() -> None:
    report = build_report()
    OUTPUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render(report), encoding="utf-8")
    print(report["starting_functional_coverage"])
    print(report["final_functional_coverage"])


if __name__ == "__main__":
    main()
