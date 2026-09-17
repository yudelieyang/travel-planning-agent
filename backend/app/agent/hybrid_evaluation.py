"""Offline-first measurements for the hybrid semantic pipeline."""

import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field

from app.agent.requirements import (
    AmbiguityLevel,
    ConstraintScope,
    ConstraintStrength,
    PreferenceCategory,
    TravelRequirements,
    parse_requirements,
)
from app.agent.semantic_coverage import SemanticCoverageAnalyzer
from app.agent.semantic_extractor import (
    SemanticExtractionError,
    SemanticExtractionResult,
)
from app.agent.semantic_merge import MergeDecisionCode, merge_requirements


class GoldConstraint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope: ConstraintScope
    value: float
    strength: ConstraintStrength = ConstraintStrength.HARD
    operator: Literal["LTE"] = "LTE"
    supported_for_execution: bool = True


class GoldPreference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: PreferenceCategory
    value: str


class GoldUnsupportedConstraint(BaseModel):
    """A retained-but-non-executable monetary requirement."""

    model_config = ConfigDict(extra="forbid")

    scope: Literal["FOOD_TOTAL", "TRANSPORT_TOTAL", "ATTRACTIONS_TOTAL", "HOTEL_PER_NIGHT"]
    value: float
    strength: ConstraintStrength = ConstraintStrength.HARD
    operator: Literal["LTE"] = "LTE"
    supported_for_execution: Literal[False] = False


class AllowedGroundedAdditions(BaseModel):
    """Opt-in open-world scoring for source-grounded, non-safety fields."""

    model_config = ConfigDict(extra="forbid")

    preferences: bool = False
    assumable_ambiguities: bool = False


class HybridExpected(BaseModel):
    model_config = ConfigDict(extra="forbid")

    needs_llm: bool
    expected_runtime_llm_need: bool | None = None
    allow_hybrid_gap: bool = False
    destination: str | None = None
    duration_days: int | None = None
    travelers: int | None = None
    constraints: list[GoldConstraint] = Field(default_factory=list)
    preferences: list[GoldPreference] = Field(default_factory=list)
    ambiguity_levels: list[AmbiguityLevel] = Field(default_factory=list)
    merge_decisions: list[MergeDecisionCode] = Field(default_factory=list)
    requires_clarification: bool = False
    unsupported_scopes: list[str] = Field(default_factory=list)
    unsupported_constraints: list[GoldUnsupportedConstraint] = Field(default_factory=list)
    unsupported_semantics: list[str] = Field(default_factory=list)
    forbidden_constraints: list[GoldConstraint] = Field(default_factory=list)
    forbidden_preferences: list[GoldPreference] = Field(default_factory=list)
    allowed_grounded_additions: AllowedGroundedAdditions = Field(default_factory=AllowedGroundedAdditions)


class HybridCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    category: str
    input: str = Field(min_length=1)
    expected: HybridExpected
    mock_proposal: SemanticExtractionResult | None = None


class HybridDataset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: Literal[
        "hybrid_semantics_v1",
        "hybrid_semantics_holdout_v1",
        "hybrid_semantics_200_v1",
        "hybrid_semantics_m5_correction_holdout_v1",
        "hybrid_semantics_m6_correction_holdout_v1",
    ]
    cases: list[HybridCase] = Field(min_length=10, max_length=200)


class SemanticExtractorProtocol(Protocol):
    model: str
    prompt_version: str

    def extract(self, query: str) -> SemanticExtractionResult: ...


def load_dataset(path: Path) -> HybridDataset:
    dataset = HybridDataset.model_validate_json(path.read_text("utf-8"))
    validate_dataset(dataset, path)
    if dataset.version == "hybrid_semantics_v1" and len(dataset.cases) < 40:
        raise ValueError("The V1 calibration dataset requires at least 40 cases")
    return dataset


SEM200_CATEGORY_COUNTS = {
    "A_simple_deterministic": 20,
    "B_total_trip_hard": 20,
    "C_hotel_total_hard": 15,
    "D_multi_scope": 20,
    "E_same_scope_correction": 15,
    "F_mixed_scope_correction": 10,
    "G_soft_approximate": 15,
    "H_ambiguous_scope": 15,
    "I_unsupported_hard_scope": 15,
    "J_preferences": 10,
    "K_negation_exclusion": 10,
    "L_tradeoff_objective": 10,
    "M_false_money": 10,
    "N_noisy_english": 10,
    "O_adversarial_boundary": 5,
}


def normalize_input(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


def validate_dataset(dataset: HybridDataset, path: Path | None = None) -> None:
    """Fail loudly on data defects before a benchmark is evaluated."""
    ids = [case.id for case in dataset.cases]
    inputs = [case.input for case in dataset.cases]
    normalized = [normalize_input(value) for value in inputs]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate hybrid evaluation case IDs")
    if dataset.version == "hybrid_semantics_200_v1" and len(set(inputs)) != len(inputs):
        raise ValueError("Duplicate exact hybrid evaluation inputs")
    if dataset.version == "hybrid_semantics_200_v1" and len(set(normalized)) != len(normalized):
        raise ValueError("Duplicate normalized hybrid evaluation inputs")
    if any(not case.category for case in dataset.cases):
        raise ValueError("Hybrid evaluation cases require a category")
    if dataset.version != "hybrid_semantics_200_v1":
        return
    if len(dataset.cases) != 200:
        raise ValueError("The SEM200 benchmark must contain exactly 200 cases")
    if Counter(case.category for case in dataset.cases) != Counter(SEM200_CATEGORY_COUNTS):
        raise ValueError("SEM200 category distribution does not match the published plan")
    expected_ids = [f"SEM200-{number:03d}" for number in range(1, 201)]
    if ids != expected_ids:
        raise ValueError("SEM200 IDs must be stable and sequential from SEM200-001 through SEM200-200")
    if any(case.expected.expected_runtime_llm_need is None for case in dataset.cases):
        raise ValueError("Every SEM200 case must declare expected_runtime_llm_need")
    for case in dataset.cases:
        expected = case.expected
        unsupported_scopes = {item.scope for item in expected.unsupported_constraints}
        if unsupported_scopes != set(expected.unsupported_scopes):
            raise ValueError(f"{case.id} unsupported scope gold must include a matching constraint")
        if any(not item.supported_for_execution for item in expected.constraints):
            raise ValueError(f"{case.id} executable constraints must be marked supported_for_execution")
    if path is not None:
        _validate_historical_duplicates(path, normalized)


def _validate_historical_duplicates(path: Path, normalized: list[str]) -> None:
    historical = (
        "hybrid_semantics_v1.json",
        "hybrid_semantics_holdout_v1.json",
        "semantic_coverage_v1.json",
    )
    known = set()
    for name in historical:
        candidate = path.parent / name
        if not candidate.exists() or candidate.resolve() == path.resolve():
            continue
        raw = json.loads(candidate.read_text("utf-8"))
        known.update(
            normalize_input(item[key])
            for item in raw.get("cases", [])
            for key in ("input", "query")
            if key in item
        )
    fixture = path.parents[2] / "backend/tests/agent/fixtures/semantic_requirements_v2.json"
    if fixture.exists():
        known.update(
            normalize_input(item["query"])
            for item in json.loads(fixture.read_text("utf-8"))
            if "query" in item
        )
    if known.intersection(normalized):
        raise ValueError("SEM200 contains normalized input duplicates from historical semantic datasets")


def evaluate_dataset(
    dataset: HybridDataset,
    *,
    mode: Literal["offline", "live"] = "offline",
    extractor: SemanticExtractorProtocol | None = None,
) -> dict:
    if mode == "live" and extractor is None:
        raise ValueError("A semantic extractor is required for live evaluation")
    return evaluate_cases(
        dataset.cases,
        dataset_version=dataset.version,
        mode=mode,
        extractor=extractor,
    )


def evaluate_cases(
    cases: list[HybridCase],
    *,
    dataset_version: str,
    mode: Literal["offline", "live"] = "offline",
    extractor: SemanticExtractorProtocol | None = None,
) -> dict:
    if mode == "live" and extractor is None:
        raise ValueError("A semantic extractor is required for live evaluation")
    records = [_evaluate_case(case, mode=mode, extractor=extractor) for case in cases]
    return {
        "dataset_version": dataset_version,
        "generated_at": datetime.now(UTC).isoformat(),
        "mode": mode,
        "model": getattr(extractor, "model", None),
        "prompt_version": getattr(extractor, "prompt_version", None),
        "case_count": len(records),
        "records": records,
        "metrics": _metrics(records),
    }


def _evaluate_case(
    case: HybridCase,
    *,
    mode: Literal["offline", "live"],
    extractor: SemanticExtractorProtocol | None,
) -> dict:
    deterministic = parse_requirements(case.input)
    coverage = SemanticCoverageAnalyzer().analyze(case.input, deterministic)
    proposal = case.mock_proposal
    extraction_error = None
    extractor_observation = None
    if mode == "live" and coverage.needs_llm:
        try:
            proposal = extractor.extract(case.input) if extractor is not None else None
        except SemanticExtractionError as exc:
            extraction_error = exc.code
        observer = getattr(extractor, "get_observation", None)
        extractor_observation = observer() if callable(observer) else None
    merge = (
        merge_requirements(deterministic, proposal, case.input, coverage.reasons)
        if proposal is not None
        else None
    )
    final = merge.requirements if merge is not None else deterministic
    failures = _failures(case, deterministic, coverage.needs_llm, merge, final)
    return {
        "case_id": case.id,
        "category": case.category,
        "input": case.input,
        "passed": not failures,
        "failure_categories": failures,
        "expected": case.expected.model_dump(mode="json"),
        "deterministic": _semantic_view(deterministic),
        "coverage": coverage.model_dump(mode="json"),
        "proposal": proposal.model_dump(mode="json") if proposal else None,
        "extraction_error": extraction_error,
        "extractor_observation": extractor_observation,
        "merge": (
            {
                "decisions": [decision.code.value for decision in merge.decisions],
                "conflicts": [conflict.code.value for conflict in merge.conflicts],
                "requires_clarification": merge.requires_clarification,
            }
            if merge
            else None
        ),
        "final": _semantic_view(final),
    }


def _semantic_view(requirements: TravelRequirements) -> dict:
    return {
        "destination": requirements.destination,
        "duration_days": requirements.duration_days,
        "travelers": requirements.travelers,
        "constraints": [
            {"scope": item.scope.value, "value": item.value, "strength": item.strength.value}
            for item in requirements.requirements_v2.constraints
        ],
        "preferences": [
            {"category": item.category.value, "value": item.value}
            for item in requirements.requirements_v2.preferences
        ],
        "ambiguity_levels": [item.level.value for item in requirements.requirements_v2.ambiguities],
        "unsupported_scopes": _unsupported_scopes(requirements),
        "unsupported_semantics": [],
        "requires_clarification": any(
            item.level == AmbiguityLevel.BLOCKING for item in requirements.requirements_v2.ambiguities
        ),
    }


def _failures(case: HybridCase, deterministic, actual_needs_llm, merge, final) -> list[str]:
    expected = case.expected
    failures = []
    if actual_needs_llm != _runtime_llm_need(expected):
        failures.append(
            "COVERAGE_FALSE_NEGATIVE" if _runtime_llm_need(expected) else "COVERAGE_FALSE_POSITIVE"
        )
    # Offline evaluation has no proposal to merge. For an explicitly hybrid
    # case, do not report deliberately deferred semantic fields as parser errors
    # once the coverage gate correctly requests augmentation.
    if expected.allow_hybrid_gap and _runtime_llm_need(expected) and merge is None:
        return failures
    actual = _semantic_view(final)
    for field in ("destination", "duration_days", "travelers"):
        if getattr(expected, field) is not None and actual[field] != getattr(expected, field):
            failures.append("PARSER_MISS")
    actual_constraints = _constraint_set(actual["constraints"])
    expected_constraints = _gold_constraint_set(expected.constraints)
    if actual_constraints != expected_constraints:
        failures.append(_constraint_failure(case.category, expected, actual_constraints, merge))
    actual_preferences = _preference_set(actual["preferences"])
    expected_preferences = _gold_preference_set(expected.preferences)
    if not expected_preferences.issubset(actual_preferences) or (
        not expected.allowed_grounded_additions.preferences and actual_preferences != expected_preferences
    ):
        failures.append("PREFERENCE_ERROR")
    if _gold_constraint_set(expected.forbidden_constraints).intersection(actual_constraints):
        failures.append("WRONG_SCOPE")
    if _gold_preference_set(expected.forbidden_preferences).intersection(actual_preferences):
        failures.append("PREFERENCE_ERROR")
    if set(actual["ambiguity_levels"]) != {level.value for level in expected.ambiguity_levels}:
        failures.append("AMBIGUITY_ERROR")
    if not set(expected.unsupported_scopes).issubset(actual["unsupported_scopes"]):
        failures.append("UNSUPPORTED_SCOPE_ERROR")
    if expected.unsupported_semantics and not actual["unsupported_semantics"]:
        failures.append("AMBIGUITY_ERROR")
    if expected.merge_decisions:
        actual_decisions = [] if merge is None else [item.code.value for item in merge.decisions]
        if not set(code.value for code in expected.merge_decisions).issubset(actual_decisions):
            failures.append("MERGE_CONFLICT_ERROR")
    if actual["requires_clarification"] != expected.requires_clarification:
        failures.append("AMBIGUITY_ERROR")
    return list(dict.fromkeys(failures))


def _constraint_set(items) -> set[tuple[str, float, str]]:
    return {(item["scope"], item["value"], item["strength"]) for item in items}


def _gold_constraint_set(items) -> set[tuple[str, float, str]]:
    return {(item.scope.value, item.value, item.strength.value) for item in items}


def _constraint_failure(category: str, expected, actual: set[tuple[str, float, str]], merge) -> str:
    if "correction" in category:
        return "CORRECTION_ERROR"
    gold = _gold_constraint_set(expected.constraints)
    expected_scopes = {scope for scope, _, _ in gold}
    actual_scopes = {scope for scope, _, _ in actual}
    if any(value in {candidate[1] for candidate in actual if candidate[0] != scope} for scope, value, _ in gold):
        return "WRONG_SCOPE"
    if expected_scopes.intersection(actual_scopes):
        if any(
            value not in {candidate[1] for candidate in actual if candidate[0] == scope}
            for scope, value, _ in gold
        ):
            return "WRONG_AMOUNT"
        return "WRONG_STRENGTH"
    return "PARSER_MISS" if merge is None else "MERGE_FALSE_REJECT"


def _preference_set(items) -> set[tuple[str, str]]:
    return {(item["category"], item["value"].casefold()) for item in items}


def _gold_preference_set(items) -> set[tuple[str, str]]:
    return {(item.category.value, item.value.casefold()) for item in items}


def _metrics(records: list[dict]) -> dict:
    expected_llm = [
        _runtime_llm_need(HybridExpected.model_validate(record["expected"])) for record in records
    ]
    actual_llm = [record["coverage"]["needs_llm"] for record in records]
    tp = sum(expected and actual for expected, actual in zip(expected_llm, actual_llm, strict=True))
    tn = sum(not expected and not actual for expected, actual in zip(expected_llm, actual_llm, strict=True))
    fp = sum(not expected and actual for expected, actual in zip(expected_llm, actual_llm, strict=True))
    fn = sum(expected and not actual for expected, actual in zip(expected_llm, actual_llm, strict=True))
    failures = Counter(failure for record in records for failure in record["failure_categories"])
    hard_expected = [
        _gold_constraint_set(HybridExpected.model_validate(record["expected"]).constraints)
        for record in records
    ]
    hard_actual = [_constraint_set(record["final"]["constraints"]) for record in records]
    category_metrics = {
        category: {
            "passed": sum(record["passed"] for record in records if record["category"] == category),
            "total": sum(record["category"] == category for record in records),
        }
        for category in dict.fromkeys(record["category"] for record in records)
    }
    for score in category_metrics.values():
        score["pass_rate"] = _rate(score["passed"], score["total"])
    return {
        "coverage_gate": {
            "TP": tp,
            "TN": tn,
            "FP": fp,
            "FN": fn,
            "precision": _rate(tp, tp + fp),
            "recall": _rate(tp, tp + fn),
            "f1": _f1(tp, fp, fn),
            "false_positive_rate": _rate(fp, fp + tn),
        },
        "semantic_field_accuracy": _field_accuracy(records),
        "deferred_hybrid_cases": sum(_is_deferred_hybrid(record) for record in records),
        "hard_constraint_safety": {
            "silent_hard_constraint_corruption": sum(
                bool(actual - expected)
                for expected, actual, record in zip(hard_expected, hard_actual, records, strict=True)
            ),
            "wrong_hard_scope": sum(
                any(value in {item[1] for item in actual if item[0] != scope} for scope, value, _ in expected)
                for expected, actual in zip(hard_expected, hard_actual, strict=True)
            ),
            "wrong_hard_amount": sum(
                any(scope in {item[0] for item in actual} and value not in {item[1] for item in actual if item[0] == scope} for scope, value, _ in expected)
                for expected, actual in zip(hard_expected, hard_actual, strict=True)
            ),
            "soft_to_hard_unsafe_promotion": sum(
                bool(record["final"]["constraints"])
                and any("around" in value or "about" in value or "roughly" in value for _, value in record["expected"]["preferences"])
                for record in records
            ),
            "hard_to_soft_unsafe_downgrade": sum(
                bool(expected - actual) and bool(record["final"]["preferences"])
                for expected, actual, record in zip(hard_expected, hard_actual, records, strict=True)
            ),
            # Retained for historical Phase-K report consumers.
            "hard_constraint_false_rejection": sum(
                bool(expected - actual) and record["merge"] is not None
                for expected, actual, record in zip(hard_expected, hard_actual, records, strict=True)
            ),
            "hard_constraint_false_acceptance": sum(
                bool(actual - expected) and record["merge"] is not None
                for expected, actual, record in zip(hard_expected, hard_actual, records, strict=True)
            ),
            "unsupported_hard_constraints_silently_dropped": sum(
                bool(record["expected"]["unsupported_scopes"])
                and not set(record["expected"]["unsupported_scopes"]).issubset(record["final"]["unsupported_scopes"])
                for record in records
            ),
        },
        "merge": {
            "attempted": sum(record["merge"] is not None for record in records),
            "accepted_augmentations": sum(
                "ADDED_FROM_LLM" in (record["merge"] or {}).get("decisions", []) for record in records
            ),
            "hallucination_rejections": sum(
                "LLM_REJECTED_UNGROUNDED" in (record["merge"] or {}).get("decisions", [])
                for record in records
            ),
            "conflict_detections": sum(bool((record["merge"] or {}).get("conflicts")) for record in records),
            "accepted_augmentation_precision": _rate(
                sum(
                    _accepted_items_match_gold(record)
                    for record in records
                    if "ADDED_FROM_LLM" in (record["merge"] or {}).get("decisions", [])
                ),
                sum(
                    "ADDED_FROM_LLM" in (record["merge"] or {}).get("decisions", [])
                    for record in records
                ),
            ),
        },
        "failure_counts": dict(failures),
        "category_pass_rates": category_metrics,
        "case_pass_rate": _rate(sum(record["passed"] for record in records), len(records)),
    }


def render_markdown(report: dict) -> str:
    metrics = report["metrics"]
    gate = metrics["coverage_gate"]
    lines = [
        f"# Hybrid Semantic Evaluation {report['dataset_version']}",
        "",
        f"Mode: `{report['mode']}`  ",
        f"Cases: {report['case_count']}  ",
        f"Case pass rate: {metrics['case_pass_rate']:.1%}",
        f"Offline-deferred hybrid cases: {metrics['deferred_hybrid_cases']}",
        "",
        "## Coverage gate",
        "",
        f"TP: {gate['TP']} | TN: {gate['TN']} | FP: {gate['FP']} | FN: {gate['FN']}",
        f"Precision: {gate['precision']:.1%} | Recall: {gate['recall']:.1%} | F1: {gate['f1']:.1%}",
        "",
        "## Hard-constraint safety",
        "",
        f"Silent hard corruption: {metrics['hard_constraint_safety']['silent_hard_constraint_corruption']}",
        f"Wrong hard scope: {metrics['hard_constraint_safety']['wrong_hard_scope']}",
        f"Wrong hard amount: {metrics['hard_constraint_safety']['wrong_hard_amount']}",
        f"Soft → hard unsafe promotion: {metrics['hard_constraint_safety']['soft_to_hard_unsafe_promotion']}",
        f"Hard → soft unsafe downgrade: {metrics['hard_constraint_safety']['hard_to_soft_unsafe_downgrade']}",
        f"Unsupported hard constraints silently dropped: {metrics['hard_constraint_safety']['unsupported_hard_constraints_silently_dropped']}",
        "",
        "## Category pass rates",
        "",
    ]
    lines.extend(
        f"- {category}: {score['passed']}/{score['total']} ({score['pass_rate']:.1%})"
        for category, score in metrics["category_pass_rates"].items()
    )
    lines += ["", "## Failed cases by category and root cause"]
    failed = [record for record in report["records"] if not record["passed"]]
    if not failed:
        lines.append("\nNone.")
    for category in dict.fromkeys(record["category"] for record in failed):
        lines += ["", f"### {category}"]
        for record in (record for record in failed if record["category"] == category):
            lines += [
                f"\n#### {record['case_id']} — {', '.join(record['failure_categories'])}",
                f"Input: {record['input']}",
                f"Gold: `{json.dumps(record['expected'], ensure_ascii=False)}`",
                f"Deterministic: `{json.dumps(record['deterministic'], ensure_ascii=False)}`",
                f"Coverage: `{json.dumps(record['coverage'], ensure_ascii=False)}`",
                f"Proposal: `{json.dumps(record['proposal'], ensure_ascii=False)}`",
                f"Merge: `{json.dumps(record['merge'], ensure_ascii=False)}`",
                f"Final: `{json.dumps(record['final'], ensure_ascii=False)}`",
            ]
    return "\n".join(lines) + "\n"


def write_report(report: dict, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")


def _rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 1.0


def _f1(tp: int, fp: int, fn: int) -> float:
    return _rate(2 * tp, 2 * tp + fp + fn)


def _runtime_llm_need(expected: HybridExpected) -> bool:
    return expected.needs_llm if expected.expected_runtime_llm_need is None else expected.expected_runtime_llm_need


def _unsupported_scopes(requirements: TravelRequirements) -> list[str]:
    scopes = set()
    for ambiguity in requirements.requirements_v2.ambiguities:
        text = f"{ambiguity.source_text} {ambiguity.reason}".casefold()
        if (re.search(r"\b(?:food|meal|restaurant)\b", text) or "food_total" in text) and "not supported" in text:
            scopes.add("FOOD_TOTAL")
        if "transport" in text and "not supported" in text:
            scopes.add("TRANSPORT_TOTAL")
        if ("activit" in text or "attractions_total" in text) and "not supported" in text:
            scopes.add("ATTRACTIONS_TOTAL")
        if "hotel_per_night" in text:
            scopes.add("HOTEL_PER_NIGHT")
    return sorted(scopes)


def _field_accuracy(records: list[dict]) -> dict:
    fields = ("destination", "duration_days", "travelers", "constraints", "preferences", "ambiguity_levels")
    scores = {}
    for field in fields:
        relevant = [
            record
            for record in records
            if not _is_deferred_hybrid(record)
            and (field in {"constraints", "preferences", "ambiguity_levels"} or record["expected"][field] is not None)
        ]
        if field == "constraints":
            scores[field] = _rate(
                sum(
                    _gold_constraint_set(HybridExpected.model_validate(record["expected"]).constraints)
                    == _constraint_set(record["final"]["constraints"])
                    for record in relevant
                ),
                len(relevant),
            )
        elif field == "preferences":
            scores[field] = _rate(
                sum(
                    _gold_preference_set(HybridExpected.model_validate(record["expected"]).preferences).issubset(
                        _preference_set(record["final"]["preferences"])
                    )
                    for record in relevant
                ),
                len(relevant),
            )
        else:
            scores[field] = _rate(
                sum(record["expected"][field] == record["final"][field] for record in relevant),
                len(relevant),
            )
    constraint_records = [record for record in records if not _is_deferred_hybrid(record)]
    gold_constraints = [
        _gold_constraint_set(HybridExpected.model_validate(record["expected"]).constraints)
        for record in constraint_records
    ]
    actual_constraints = [_constraint_set(record["final"]["constraints"]) for record in constraint_records]
    scores["constraint_scope"] = _rate(
        sum({item[0] for item in gold} == {item[0] for item in actual} for gold, actual in zip(gold_constraints, actual_constraints, strict=True)),
        len(constraint_records),
    )
    scores["constraint_amount"] = _rate(
        sum({item[:2] for item in gold} == {item[:2] for item in actual} for gold, actual in zip(gold_constraints, actual_constraints, strict=True)),
        len(constraint_records),
    )
    scores["constraint_strength"] = _rate(
        sum({(item[0], item[2]) for item in gold} == {(item[0], item[2]) for item in actual} for gold, actual in zip(gold_constraints, actual_constraints, strict=True)),
        len(constraint_records),
    )
    correction_records = [record for record in records if "correction" in record["category"]]
    scores["correction"] = _rate(sum(record["passed"] for record in correction_records), len(correction_records))
    return scores


def _is_deferred_hybrid(record: dict) -> bool:
    expected = HybridExpected.model_validate(record["expected"])
    return expected.allow_hybrid_gap and _runtime_llm_need(expected) and record["merge"] is None


def _accepted_items_match_gold(record: dict) -> bool:
    expected = HybridExpected.model_validate(record["expected"])
    return _gold_constraint_set(expected.constraints).issubset(_constraint_set(record["final"]["constraints"])) and _gold_preference_set(
        expected.preferences
    ).issubset(_preference_set(record["final"]["preferences"]))
