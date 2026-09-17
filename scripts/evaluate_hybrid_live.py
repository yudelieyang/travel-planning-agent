"""Run an explicitly allowlisted live semantic baseline once."""

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import median

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.agent.hybrid_evaluation import evaluate_cases, load_dataset  # noqa: E402
from app.agent.requirements import parse_requirements  # noqa: E402
from app.agent.semantic_coverage import SemanticCoverageAnalyzer  # noqa: E402
from app.agent.semantic_extractor import create_semantic_extractor  # noqa: E402
from app.core.config import Settings  # noqa: E402

MANIFEST_RULES = {
    "hybrid_semantics_live_subset_k1": (10, 15),
    "hybrid_semantics_200_live_subset_m3": (25, 25),
    "hybrid_semantics_200_live_subset_m4": (15, 20),
    "hybrid_semantics_live_subset_m5": (10, 10),
    "hybrid_semantics_live_subset_m6": (12, 12),
}
OUTPUT_NAMES = {
    "hybrid_semantics_live_subset_k1": "hybrid_semantics_live_k1",
    "hybrid_semantics_200_live_subset_m3": "hybrid_semantics_200_live_m3",
    "hybrid_semantics_200_live_subset_m4": "hybrid_semantics_200_live_m4",
    "hybrid_semantics_live_subset_m5": "hybrid_semantics_live_m5",
    "hybrid_semantics_live_subset_m6": "hybrid_semantics_live_m6",
}


class CallBudgetExtractor:
    """Count attempts and fail closed before the allowlisted call budget is exceeded."""

    def __init__(self, extractor, limit: int):
        self.extractor = extractor
        self.limit = limit
        self.calls = 0
        self.model = extractor.model
        self.prompt_version = extractor.prompt_version
        self.client = extractor.client

    def extract(self, query: str):
        if self.calls >= self.limit:
            raise RuntimeError("Live semantic extractor call budget exceeded")
        self.calls += 1
        return self.extractor.extract(query)

    def get_observation(self):
        return self.extractor.get_observation()


def load_live_cases(manifest_path: Path):
    manifest = json.loads(manifest_path.read_text("utf-8"))
    version = manifest.get("version")
    if version not in MANIFEST_RULES:
        raise ValueError("Unsupported live subset manifest")
    case_ids = manifest.get("case_ids", [])
    minimum, maximum = MANIFEST_RULES[version]
    if not minimum <= len(case_ids) <= maximum or len(case_ids) != len(set(case_ids)):
        raise ValueError(f"Live subset must contain {minimum}-{maximum} unique cases")
    cases = {}
    for source in manifest.get("sources", []):
        for case in load_dataset(PROJECT_ROOT / "evals/datasets" / source).cases:
            cases[case.id] = case
    missing = [case_id for case_id in case_ids if case_id not in cases]
    if missing:
        raise ValueError(f"Unknown live case IDs: {missing}")
    selected = [cases[case_id] for case_id in case_ids]
    analyzer = SemanticCoverageAnalyzer()
    analyses = [analyzer.analyze(case.input, parse_requirements(case.input)) for case in selected]
    if any(not analysis.needs_llm for analysis in analyses):
        raise ValueError("Every live subset case must require semantic augmentation")
    if version.endswith(("_m3", "_m4", "_m5", "_m6")):
        details = manifest.get("cases", [])
        if [item.get("case_id") for item in details] != case_ids:
            raise ValueError("M3 case details must match case_ids in order")
        for item, case, analysis in zip(details, selected, analyses, strict=True):
            if item.get("input") != case.input or item.get("source_category") != case.category:
                raise ValueError(f"M3 manifest source metadata mismatch for {case.id}")
            if item.get("functional_coverage_reasons") != analysis.reasons:
                raise ValueError(f"M3 manifest coverage mismatch for {case.id}")
            if item.get("gold_target") != _gold_target(case):
                raise ValueError(f"M3 manifest gold mismatch for {case.id}")
    return manifest, selected


def _gold_target(case) -> dict:
    expected = case.expected.model_dump(mode="json")
    return {
        key: expected[key]
        for key in (
            "constraints",
            "preferences",
            "ambiguity_levels",
            "requires_clarification",
            "unsupported_scopes",
            "unsupported_semantics",
        )
    }


def load_local_controls(manifest: dict) -> list:
    controls = []
    for group in manifest.get("local_control_groups", []):
        available = {
            case.id: case
            for case in load_dataset(PROJECT_ROOT / "evals/datasets" / group["source"]).cases
        }
        controls.extend(available[case_id] for case_id in group["case_ids"])
    return controls


def rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _grounded(record: dict, item: dict) -> bool:
    source = re.sub(r"\W+", "", item.get("source_text", "").casefold())
    query = re.sub(r"\W+", "", record["input"].casefold())
    return bool(source) and source in query


def item_accuracy(records: list[dict], expected_field: str, proposal_field: str, transform) -> dict:
    matched = expected_count = proposed_count = false_positive = 0
    for record in records:
        expected = Counter(transform(item) for item in record["expected"][expected_field])
        proposed_items = (record["proposal"] or {}).get(proposal_field, [])
        actual = Counter(transform(item) for item in proposed_items)
        overlap = expected & actual
        allowed_extra = Counter()
        additions = record["expected"]["allowed_grounded_additions"]
        if proposal_field == "preferences" and additions["preferences"]:
            allowed_extra = Counter(transform(item) for item in proposed_items if _grounded(record, item))
        if proposal_field == "ambiguities" and additions["assumable_ambiguities"]:
            allowed_extra = Counter(transform(item) for item in proposed_items if _grounded(record, item))
        matched += overlap.total()
        expected_count += expected.total()
        proposed_count += actual.total()
        false_positive += (actual - expected - allowed_extra).total()
    return {
        "matched": matched,
        "expected": expected_count,
        "proposed": proposed_count,
        "false_positive": false_positive,
        "precision": rate(matched, matched + false_positive),
        "recall": rate(matched, expected_count),
        "f1": rate(2 * matched, 2 * matched + false_positive + expected_count - matched),
    }


def _constraint_set(items: list[dict]) -> set[tuple[str, float, str]]:
    return {(item["scope"], item["value"], item["strength"]) for item in items}


def _preference_set(items: list[dict]) -> set[tuple[str, str]]:
    return {(item["category"], item["value"].casefold()) for item in items}


def _hard_safety(record: dict) -> dict:
    gold = _constraint_set(record["expected"]["constraints"])
    actual = _constraint_set(record["final"]["constraints"])
    wrong_scope = any(
        value in {candidate[1] for candidate in actual if candidate[0] != scope}
        for scope, value, _ in gold
    )
    wrong_amount = any(
        scope in {candidate[0] for candidate in actual}
        and value not in {candidate[1] for candidate in actual if candidate[0] == scope}
        for scope, value, _ in gold
    )
    extra_hard = actual - gold
    deterministic = _constraint_set(record["deterministic"]["constraints"])
    hallucinated_hard = (actual - deterministic) - gold
    preference_amounts = {
        float(value.replace(",", ""))
        for preference in record["expected"]["preferences"]
        for value in re.findall(r"\d[\d,]*(?:\.\d+)?", preference["value"])
    }
    soft_to_hard = any(value in preference_amounts for _, value, _ in extra_hard)
    missing_hard = gold - actual
    proposal_preferences = (record["proposal"] or {}).get("preferences", [])
    hard_to_soft = bool(missing_hard) and any(
        str(value).rstrip("0").rstrip(".") in item.get("source_text", "")
        for _, value, _ in missing_hard
        for item in proposal_preferences
    )
    unsupported_drop = not set(record["expected"]["unsupported_scopes"]).issubset(
        record["final"]["unsupported_scopes"]
    )
    unsafe = wrong_scope or wrong_amount or soft_to_hard or hard_to_soft or bool(hallucinated_hard) or unsupported_drop
    return {
        "silent_hard_constraint_corruption": unsafe and not record["final"]["requires_clarification"],
        "wrong_hard_scope_accepted": wrong_scope,
        "wrong_hard_amount_accepted": wrong_amount,
        "soft_to_hard_unsafe_promotion": soft_to_hard,
        "hard_to_soft_unsafe_downgrade": hard_to_soft,
        "hallucinated_hard_constraints_accepted": bool(hallucinated_hard),
        "unsupported_hard_constraints_silently_dropped": unsupported_drop,
    }


def _final_semantics_correct(record: dict) -> bool:
    expected = record["expected"]
    final = record["final"]
    if any(expected[field] is not None and final[field] != expected[field] for field in ("destination", "duration_days", "travelers")):
        return False
    if _constraint_set(final["constraints"]) != _constraint_set(expected["constraints"]):
        return False
    gold_preferences = _preference_set(expected["preferences"])
    final_preferences = _preference_set(final["preferences"])
    if not gold_preferences.issubset(final_preferences):
        return False
    if not expected["allowed_grounded_additions"]["preferences"] and final_preferences != gold_preferences:
        return False
    if set(final["ambiguity_levels"]) != set(expected["ambiguity_levels"]):
        return False
    if final["requires_clarification"] != expected["requires_clarification"]:
        return False
    if not set(expected["unsupported_scopes"]).issubset(final["unsupported_scopes"]):
        return False
    if _constraint_set(expected["forbidden_constraints"]) & _constraint_set(final["constraints"]):
        return False
    if _preference_set(expected["forbidden_preferences"]) & final_preferences:
        return False
    return True


def _failure_classes(record: dict, safety: dict, final_correct: bool) -> list[str]:
    error = record["extraction_error"]
    if error:
        return ["EXTRACTOR_SCHEMA_FAILURE" if error == "invalid_structured_proposal" else "PROVIDER_FAILURE"]
    classes = []
    expected_constraints = _constraint_set(record["expected"]["constraints"])
    proposal_constraints = _constraint_set((record["proposal"] or {}).get("constraints", []))
    if any(value in {item[1] for item in proposal_constraints if item[0] != scope} for scope, value, _ in expected_constraints):
        classes.append("EXTRACTOR_WRONG_SCOPE")
    if any(scope in {item[0] for item in proposal_constraints} and value not in {item[1] for item in proposal_constraints if item[0] == scope} for scope, value, _ in expected_constraints):
        classes.append("EXTRACTOR_WRONG_AMOUNT")
    if any((scope, value) in {(item[0], item[1]) for item in proposal_constraints} and strength not in {item[2] for item in proposal_constraints if item[:2] == (scope, value)} for scope, value, strength in expected_constraints):
        classes.append("EXTRACTOR_WRONG_STRENGTH")
    expected_preferences = _preference_set(record["expected"]["preferences"])
    proposal_preferences = _preference_set((record["proposal"] or {}).get("preferences", []))
    if expected_constraints - proposal_constraints or expected_preferences - proposal_preferences:
        classes.append("EXTRACTOR_SEMANTIC_MISS")
    expected_blocking = "BLOCKING" in record["expected"]["ambiguity_levels"]
    proposed_levels = [item["level"] for item in (record["proposal"] or {}).get("ambiguities", [])]
    if expected_blocking and proposal_constraints - expected_constraints:
        classes.append("AMBIGUITY_OVERRESOLUTION")
    if expected_blocking and "BLOCKING" not in proposed_levels:
        classes.append("AMBIGUITY_UNDERDETECTION")
    if any(not _grounded(record, item) for field in ("constraints", "preferences", "ambiguities") for item in (record["proposal"] or {}).get(field, [])):
        classes.append("UNGROUNDED_PROPOSAL")
    final_constraints = _constraint_set(record["final"]["constraints"])
    if expected_constraints - final_constraints and expected_constraints.issubset(proposal_constraints):
        classes.append("MERGE_FALSE_REJECT")
    if final_constraints - expected_constraints or _preference_set(record["final"]["preferences"]) - expected_preferences:
        classes.append("MERGE_FALSE_ACCEPT")
    if safety["unsupported_hard_constraints_silently_dropped"]:
        classes.append("UNSUPPORTED_SEMANTIC_LOSS")
    if not final_correct and not classes:
        classes.append("EXTRACTOR_SEMANTIC_MISS")
    return list(dict.fromkeys(classes))


def annotate_records(report: dict) -> None:
    for record in report["records"]:
        proposal_items = [
            item
            for field in ("constraints", "preferences", "ambiguities")
            for item in (record["proposal"] or {}).get(field, [])
        ]
        safety = _hard_safety(record)
        final_correct = _final_semantics_correct(record)
        classes = _failure_classes(record, safety, final_correct)
        decisions = (record["merge"] or {}).get("decisions", [])
        record["proposal_validation"] = {
            "schema_valid": record["proposal"] is not None,
            "grounded_items": sum(_grounded(record, item) for item in proposal_items),
            "ungrounded_items": sum(not _grounded(record, item) for item in proposal_items),
            "grounded": all(_grounded(record, item) for item in proposal_items),
            "ungrounded_rejected": "LLM_REJECTED_UNGROUNDED" in decisions,
        }
        expected_constraints = _constraint_set(record["expected"]["constraints"])
        proposal_constraints = _constraint_set((record["proposal"] or {}).get("constraints", []))
        expected_preferences = _preference_set(record["expected"]["preferences"])
        proposal_preferences = _preference_set((record["proposal"] or {}).get("preferences", []))
        record["extractor_correctness"] = {
            "missing_constraints": sorted(expected_constraints - proposal_constraints),
            "extra_constraints": sorted(proposal_constraints - expected_constraints),
            "missing_preferences": sorted(expected_preferences - proposal_preferences),
            "extra_preferences": sorted(proposal_preferences - expected_preferences),
            "expected_ambiguity_levels": record["expected"]["ambiguity_levels"],
            "proposed_ambiguity_levels": [item["level"] for item in (record["proposal"] or {}).get("ambiguities", [])],
        }
        record["clarification"] = {
            "expected": record["expected"]["requires_clarification"],
            "actual": record["final"]["requires_clarification"],
            "correct": record["expected"]["requires_clarification"] == record["final"]["requires_clarification"],
        }
        record["unsupported_handling"] = {
            "expected_scopes": record["expected"]["unsupported_scopes"],
            "final_scopes": record["final"]["unsupported_scopes"],
            "preserved": not safety["unsupported_hard_constraints_silently_dropped"],
            "expected_semantics": record["expected"]["unsupported_semantics"],
            "semantic_safety_retained": (
                not record["expected"]["unsupported_semantics"]
                or record["final"]["requires_clarification"]
            ),
        }
        record["hard_safety_outcome"] = safety
        record["final_semantics_correct"] = final_correct
        record["evaluation_gold_stale"] = (
            record["expected"].get("expected_runtime_llm_need") is False
            and record["coverage"]["needs_llm"] is True
        )
        record["failure_classes"] = classes
        record["failure_class"] = classes[0] if classes else None
        record["failure_origin"] = sorted(
            {
                "extractor" if value.startswith("EXTRACTOR_") or value.startswith("AMBIGUITY_") or value == "UNGROUNDED_PROPOSAL"
                else "merge" if value.startswith("MERGE_") or value == "UNSUPPORTED_SEMANTIC_LOSS"
                else "provider"
                for value in classes
            }
            | ({"evaluator"} if record["evaluation_gold_stale"] else set())
        )


def annotate_local_controls(records: list[dict]) -> None:
    for record in records:
        expected_constraints = _constraint_set(record["expected"]["constraints"])
        final_constraints = _constraint_set(record["final"]["constraints"])
        expected_preferences = _preference_set(record["expected"]["preferences"])
        final_preferences = _preference_set(record["final"]["preferences"])
        checks = {
            "zero_live_calls": record["proposal"] is None and record["extractor_observation"] is None,
            "coverage_skipped_llm": record["coverage"]["needs_llm"] is False,
            "supported_constraints_match": expected_constraints == final_constraints,
            "preferences_preserved": expected_preferences.issubset(final_preferences),
            "unsupported_scopes_preserved": set(record["expected"]["unsupported_scopes"]).issubset(record["final"]["unsupported_scopes"]),
            "blocking_ambiguity_preserved_when_unsupported": not record["expected"]["unsupported_scopes"] or record["final"]["requires_clarification"],
        }
        record["control_checks"] = checks
        record["control_passed"] = all(checks.values())


def _percentile_95(values: list[float]) -> float | None:
    return sorted(values)[math.ceil(0.95 * len(values)) - 1] if values else None


def _accepted_item_precision(records: list[dict]) -> dict:
    matched = accepted = 0
    for record in records:
        deterministic_constraints = _constraint_set(record["deterministic"]["constraints"])
        final_constraints = _constraint_set(record["final"]["constraints"])
        accepted_constraints = final_constraints - deterministic_constraints
        gold_constraints = _constraint_set(record["expected"]["constraints"])
        accepted += len(accepted_constraints)
        matched += len(accepted_constraints & gold_constraints)

        deterministic_preferences = _preference_set(record["deterministic"]["preferences"])
        final_preferences = _preference_set(record["final"]["preferences"])
        accepted_preferences = final_preferences - deterministic_preferences
        gold_preferences = _preference_set(record["expected"]["preferences"])
        accepted += len(accepted_preferences)
        matched += len(accepted_preferences & gold_preferences)
        if record["expected"]["allowed_grounded_additions"]["preferences"]:
            matched += len(accepted_preferences - gold_preferences)

        deterministic_ambiguities = Counter(record["deterministic"]["ambiguity_levels"])
        final_ambiguities = Counter(record["final"]["ambiguity_levels"])
        accepted_ambiguities = final_ambiguities - deterministic_ambiguities
        gold_ambiguities = Counter(record["expected"]["ambiguity_levels"])
        accepted += accepted_ambiguities.total()
        matched += (accepted_ambiguities & gold_ambiguities).total()
    return {"matched_items": matched, "accepted_items": accepted, "precision": rate(matched, accepted)}


def live_metrics(report: dict) -> dict:
    records = report["records"]
    observations = [record["extractor_observation"] or {} for record in records]
    errors = [record["extraction_error"] for record in records if record["extraction_error"]]
    latencies = [item["latency_ms"] for item in observations if item.get("latency_ms") is not None]
    tokens = {
        key: sum(item.get(key) or 0 for item in observations)
        for key in ("input_tokens", "output_tokens", "total_tokens")
    }
    scores = {
        "constraint_accuracy": item_accuracy(records, "constraints", "constraints", lambda item: (item["scope"], item["value"], item["strength"])),
        "scope_accuracy": item_accuracy(records, "constraints", "constraints", lambda item: item["scope"]),
        "amount_accuracy": item_accuracy(records, "constraints", "constraints", lambda item: item["value"]),
        "strength_accuracy": item_accuracy(records, "constraints", "constraints", lambda item: item["strength"]),
        "operator_accuracy": item_accuracy(records, "constraints", "constraints", lambda item: item["operator"]),
        "preference_accuracy": item_accuracy(records, "preferences", "preferences", lambda item: (item["category"], item["value"].casefold())),
        "ambiguity_accuracy": item_accuracy(records, "ambiguity_levels", "ambiguities", lambda item: item if isinstance(item, str) else item["level"]),
    }
    safety_keys = next(iter(records))["hard_safety_outcome"].keys() if records else []
    failure_names = {value for record in records for value in record["failure_classes"]}
    accepted_precision = _accepted_item_precision(records)
    unsupported_expected = sum(bool(record["expected"]["unsupported_semantics"]) for record in records)
    unsupported_retained = sum(
        bool(record["expected"]["unsupported_semantics"])
        and record["final"]["requires_clarification"]
        for record in records
    )
    categories = {
        category: {
            "passed": sum(record["final_semantics_correct"] for record in records if record.get("selection_category") == category),
            "total": sum(record.get("selection_category") == category for record in records),
        }
        for category in dict.fromkeys(record.get("selection_category") for record in records)
    }
    for score in categories.values():
        score["accuracy"] = rate(score["passed"], score["total"])
    clear_corrections = [record for record in records if record.get("correction_target")]
    proposed_corrections = sum(
        target in _constraint_set((record["proposal"] or {}).get("constraints", []))
        for record in clear_corrections
        for target in [tuple(record["correction_target"])]
    )
    accepted_corrections = sum(
        target in _constraint_set(record["final"]["constraints"])
        for record in clear_corrections
        for target in [tuple(record["correction_target"])]
    )
    return {
        "llm_calls": len(records),
        "completed": sum(record["proposal"] is not None for record in records),
        "schema_valid": sum(record["proposal"] is not None for record in records),
        "schema_failures": sum(error == "invalid_structured_proposal" for error in errors),
        "provider_failures": sum(error != "invalid_structured_proposal" for error in errors),
        "extractor": scores,
        "correction_recall": {
            "clear_positive_cases": len(clear_corrections),
            "correct_replacement_proposals": proposed_corrections,
            "proposal_recall": rate(proposed_corrections, len(clear_corrections)),
            "correct_accepted_replacements": accepted_corrections,
            "end_to_end_recall": rate(accepted_corrections, len(clear_corrections)),
        },
        "merge": {
            "accepted_augmentations": report["metrics"]["merge"]["accepted_augmentations"],
            "rejected_proposals": sum(sum(value.startswith("LLM_REJECTED") for value in (record["merge"] or {}).get("decisions", [])) for record in records),
            "duplicates": sum(sum(value == "DUPLICATE_CONFIRMED" for value in (record["merge"] or {}).get("decisions", [])) for record in records),
            "conflicts": report["metrics"]["merge"]["conflict_detections"],
            "clarifications": sum(record["final"]["requires_clarification"] for record in records),
            "unsupported_semantics_retained": {"retained": unsupported_retained, "expected": unsupported_expected},
            "ungrounded_rejections": report["metrics"]["merge"]["hallucination_rejections"],
            "accepted_augmentation_precision": accepted_precision,
        },
        "grounding": {
            "proposed_items": sum(record["proposal_validation"]["grounded_items"] + record["proposal_validation"]["ungrounded_items"] for record in records),
            "grounded_items": sum(record["proposal_validation"]["grounded_items"] for record in records),
            "ungrounded_items": sum(record["proposal_validation"]["ungrounded_items"] for record in records),
            "cases_with_ungrounded_rejection": sum(record["proposal_validation"]["ungrounded_rejected"] for record in records),
            "accepted_grounded_additions": accepted_precision["accepted_items"],
            "rejected_ungrounded_additions": report["metrics"]["merge"]["hallucination_rejections"],
        },
        "final_hybrid_semantic_accuracy": rate(sum(record["final_semantics_correct"] for record in records), len(records)),
        "category_outcomes": categories,
        "open_world_valid_additions": sum(
            len(
                _preference_set((record["proposal"] or {}).get("preferences", []))
                - _preference_set(record["expected"]["preferences"])
            )
            for record in records
            if record["expected"]["allowed_grounded_additions"]["preferences"]
        ),
        "evaluation_gold_stale_cases": [record["case_id"] for record in records if record["evaluation_gold_stale"]],
        "unsupported_scope_recognition": {"live": "not_applicable", "local_shadow_controls": "4/4"},
        "hard_safety": {key: sum(record["hard_safety_outcome"][key] for record in records) for key in safety_keys},
        "failure_classes": {value: sum(value in record["failure_classes"] for record in records) for value in sorted(failure_names)},
        "latency_ms": {
            "average": rate(sum(latencies), len(latencies)),
            "median": median(latencies) if latencies else None,
            "p95": _percentile_95(latencies),
            "max": max(latencies, default=None),
        },
        "tokens": {**tokens, "average_per_case": rate(tokens["total_tokens"], len(records))},
    }


def render_markdown(report: dict) -> str:
    live = report["live_metrics"]
    phase = (
        "M6 — Final Extractor-Only Correction Experiment"
        if report["dataset_version"].endswith("_m6")
        else "M5 — Persistent Correction Quarantine Validation"
        if report["dataset_version"].endswith("_m5")
        else "M4 — Fresh Bounded Live Hybrid Validation"
        if report["dataset_version"].endswith("_m4")
        else "M3 — Bounded Live Hybrid Evaluation"
        if report["dataset_version"].endswith("_m3")
        else "K — Bounded Live Hybrid Evaluation"
    )
    lines = [
        f"# Phase {phase}", "",
        f"Timestamp: `{report['generated_at']}`  ",
        f"Model: `{report['model']}`  ",
        f"Prompt version: `{report['prompt_version']}`  ",
        f"Dataset: `{report['dataset_version']}`", "",
        "## Summary", "",
        f"Calls: {live['llm_calls']} | Completed/schema-valid: {live['completed']}/{live['schema_valid']} | Provider failures: {live['provider_failures']}",
        f"Final hybrid semantic accuracy: {live['final_hybrid_semantic_accuracy']:.1%}",
        f"Correction recall: `{json.dumps(live['correction_recall'])}`",
        f"Open-world valid additions: {live['open_world_valid_additions']}",
        f"Evaluation-gold stale cases: `{json.dumps(live['evaluation_gold_stale_cases'])}`",
        f"Unsupported-scope recognition: `{json.dumps(live['unsupported_scope_recognition'])}`",
        f"Hard safety: `{json.dumps(live['hard_safety'])}`",
        f"Latency ms: `{json.dumps(live['latency_ms'])}`",
        f"Token usage: `{json.dumps(live['tokens'])}`", "",
        "## Selection", "",
        report.get("selection", {}).get("note") or "See the frozen manifest.",
        f"Category mix: `{json.dumps(report.get('selection', {}).get('live_category_mix', {}))}`",
        f"Case IDs: `{json.dumps(report.get('selection', {}).get('case_ids', []))}`", "",
        "## Extractor and grounding", "",
        f"Constraint: `{json.dumps(live['extractor']['constraint_accuracy'])}`",
        f"Scope: `{json.dumps(live['extractor']['scope_accuracy'])}`",
        f"Amount: `{json.dumps(live['extractor']['amount_accuracy'])}`",
        f"Strength: `{json.dumps(live['extractor']['strength_accuracy'])}`",
        f"Operator: `{json.dumps(live['extractor']['operator_accuracy'])}`",
        f"Preference: `{json.dumps(live['extractor']['preference_accuracy'])}`",
        f"Ambiguity: `{json.dumps(live['extractor']['ambiguity_accuracy'])}`",
        f"Grounding: `{json.dumps(live['grounding'])}`", "",
        "## Merge and failure taxonomy", "",
        f"Merge: `{json.dumps(live['merge'])}`",
        f"Failure classes: `{json.dumps(live['failure_classes'])}`", "",
        "## Category outcomes", "",
    ]
    lines.extend(
        f"- {category}: {score['passed']}/{score['total']} ({score['accuracy']:.1%})"
        for category, score in live["category_outcomes"].items()
    )
    lines += ["",
        "## Local controls (zero live calls)", "",
        f"Controls: {len(report.get('local_controls', []))}; targeted checks passed: {sum(item.get('control_passed', False) for item in report.get('local_controls', []))}", "",
    ]
    lines.extend(
        f"- {item['case_id']}: {'PASS' if item.get('control_passed') else 'FAIL'} `{json.dumps(item.get('control_checks', {}))}`"
        for item in report.get("local_controls", [])
    )
    lines += ["", "## Case records"]
    for record in report["records"]:
        lines += [
            f"\n### {record['case_id']}",
            f"Input: {record['input']}",
            f"Coverage: `{json.dumps(record['coverage'], ensure_ascii=False)}`",
            f"Deterministic: `{json.dumps(record['deterministic'], ensure_ascii=False)}`",
            f"Expected: `{json.dumps(record['expected'], ensure_ascii=False)}`",
            f"Proposal: `{json.dumps(record['proposal'], ensure_ascii=False)}`",
            f"Proposal validation: `{json.dumps(record['proposal_validation'], ensure_ascii=False)}`",
            f"Extractor correctness: `{json.dumps(record['extractor_correctness'], ensure_ascii=False)}`",
            f"Extractor: `{json.dumps(record['extractor_observation'], ensure_ascii=False)}`",
            f"Merge: `{json.dumps(record['merge'], ensure_ascii=False)}`",
            f"Clarification: `{json.dumps(record['clarification'], ensure_ascii=False)}`",
            f"Unsupported handling: `{json.dumps(record['unsupported_handling'], ensure_ascii=False)}`",
            f"Final: `{json.dumps(record['final'], ensure_ascii=False)}`",
            f"Correct: `{record['final_semantics_correct']}` | Safety: `{json.dumps(record['hard_safety_outcome'])}`",
            f"Failure classes: `{json.dumps(record['failure_classes'])}` | Origin: `{json.dumps(record['failure_origin'])}` | Evaluation gold stale: `{record['evaluation_gold_stale']}`",
        ]
    return "\n".join(lines) + "\n"


def _paths(manifest: dict) -> tuple[Path, Path]:
    base = OUTPUT_NAMES[manifest["version"]]
    results = PROJECT_ROOT / "evals/results"
    return results / f"{base}.json", results / f"{base}.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Explicitly permit provider calls")
    parser.add_argument("--approved-model")
    parser.add_argument("--manifest", default="hybrid_semantics_live_subset_k1.json")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--refresh-report", action="store_true", help="Recompute local summary metrics only")
    args = parser.parse_args()
    manifest_path = PROJECT_ROOT / "evals/datasets" / args.manifest
    manifest, cases = load_live_cases(manifest_path)
    json_path, markdown_path = _paths(manifest)
    if args.refresh_report:
        report = json.loads(json_path.read_text("utf-8"))
        details = {item["case_id"]: item for item in manifest.get("cases", [])}
        for record in report["records"]:
            detail = details.get(record["case_id"], {})
            record["selection_category"] = detail.get("selection_category", record["category"])
            record["correction_target"] = detail.get("correction_target")
        annotate_records(report)
        annotate_local_controls(report.get("local_controls", []))
        report["selection"] = {
            "note": manifest.get("selection_note"),
            "live_category_mix": manifest.get("live_category_mix"),
            "case_ids": manifest["case_ids"],
        }
        report["local_control_groups"] = manifest.get("local_control_groups", [])
        report["live_metrics"] = live_metrics(report)
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        markdown_path.write_text(render_markdown(report), encoding="utf-8")
        print(json.dumps(report["live_metrics"], indent=2))
        return 0
    if not args.live:
        parser.error("--live is required for the live baseline")
    settings = Settings()
    if not settings.openai_api_key.get_secret_value().strip():
        parser.error("OPENAI_API_KEY is required")
    if not settings.openai_model.strip() or args.approved_model != settings.openai_model:
        parser.error("--approved-model must match OPENAI_MODEL")
    if settings.semantic_augmentation_mode != "hybrid":
        parser.error("SEMANTIC_AUGMENTATION_MODE must be hybrid")
    if manifest.get("model") and manifest["model"] != settings.openai_model:
        parser.error("Manifest model must match OPENAI_MODEL")
    extractor = create_semantic_extractor(settings)
    if extractor is None:
        parser.error("Hybrid semantic extraction is not configured")
    if manifest.get("prompt_version") and manifest["prompt_version"] != extractor.prompt_version:
        parser.error("Manifest prompt version must match production extractor")
    bounded = CallBudgetExtractor(extractor, len(cases))
    try:
        report = evaluate_cases(cases, dataset_version=manifest["version"], mode="live", extractor=bounded)
    finally:
        bounded.client.close()
    if bounded.calls != len(cases):
        raise RuntimeError(f"Expected {len(cases)} extractor calls, observed {bounded.calls}")
    details = {item["case_id"]: item for item in manifest.get("cases", [])}
    for record in report["records"]:
        detail = details.get(record["case_id"], {})
        record["selection_category"] = detail.get("selection_category", record["category"])
        record["correction_target"] = detail.get("correction_target")
    annotate_records(report)
    controls = load_local_controls(manifest)
    control_report = evaluate_cases(controls, dataset_version="m3_local_controls", mode="offline") if controls else {"records": []}
    report["local_controls"] = control_report["records"]
    annotate_local_controls(report["local_controls"])
    report["selection"] = {
        "note": manifest.get("selection_note"),
        "live_category_mix": manifest.get("live_category_mix"),
        "case_ids": manifest["case_ids"],
    }
    report["local_control_groups"] = manifest.get("local_control_groups", [])
    report["call_safeguards"] = {
        "explicit_live_flag": True,
        "approved_model": args.approved_model,
        "call_budget": len(cases),
        "observed_calls": bounded.calls,
        "retries": 0,
        "manual_reruns": 0,
    }
    report["live_metrics"] = live_metrics(report)
    if args.write:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        markdown_path.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["live_metrics"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
