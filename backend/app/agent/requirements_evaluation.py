"""Extractor-only evaluation with explicit denominators and deterministic failure labels."""

from collections import Counter

from app.agent.extractor import RequirementsExtractorProtocol
from app.agent.requirements import assess_requirements

GROUPS = {
    "destination": ("destination",),
    "duration": ("duration_days",),
    "dates": ("start_date", "end_date"),
    "travelers": ("travelers",),
    "budget_amount": ("budget_amount",),
    "budget_scope": ("budget_scope",),
    "preferences": ("interests", "hotel_preferences", "food_preferences", "transport_preferences"),
    "negation_constraints": ("constraints",),
}
FAILURE_TYPES = (
    "MISSING_EXTRACTION",
    "FALSE_POSITIVE",
    "WRONG_VALUE",
    "NEGATION_ERROR",
    "AMBIGUITY_ERROR",
    "NORMALIZATION_ERROR",
)


def equal(actual, expected):
    # Preference/constraint order has no semantics. Values themselves remain exact.
    if isinstance(actual, list) and isinstance(expected, list):
        return set(actual) == set(expected)
    return actual == expected


def failure_type(field: str, actual, expected, tags: list[str]) -> str:
    if "negation" in tags and field in (*GROUPS["preferences"], "constraints"):
        return "NEGATION_ERROR"
    if "ambiguity" in tags and field in ("destination", "duration_days", "constraints"):
        return "AMBIGUITY_ERROR"
    if isinstance(actual, str) and isinstance(expected, str):
        if " ".join(actual.casefold().split()) == " ".join(expected.casefold().split()):
            return "NORMALIZATION_ERROR"
    if actual in (None, [], "UNKNOWN") and expected not in (None, [], "UNKNOWN"):
        return "MISSING_EXTRACTION"
    if expected in (None, [], "UNKNOWN") and actual not in (None, [], "UNKNOWN"):
        return "FALSE_POSITIVE"
    return "WRONG_VALUE"


def evaluate_requirements(cases: list[dict], extractor: RequirementsExtractorProtocol) -> dict:
    records = []
    for case in cases:
        # No ID, expected fields, split, or tags are passed to the real extractor.
        try:
            requirements = extractor.extract(case["query"])
            actual = requirements.model_dump(mode="json")
            status = assess_requirements(requirements).status.value
            error = None
        except (ValueError, TypeError) as exc:
            actual, status, error = {}, "ERROR", type(exc).__name__
        expected = case["expected_fields"]
        matches = {
            field: field in actual and equal(actual[field], value)
            for field, value in expected.items()
        }
        failures = [
            {
                "field": field,
                "expected": expected[field],
                "actual": actual.get(field),
                "category": failure_type(field, actual.get(field), expected[field], case["tags"]),
            }
            for field, matched in matches.items()
            if not matched
        ]
        status_ok = status == case["expected_status"]
        if not status_ok:
            failures.append(
                {
                    "field": "preflight",
                    "expected": case["expected_status"],
                    "actual": status,
                    "category": "WRONG_VALUE",
                }
            )
        records.append(
            {
                "id": case["id"],
                "split": case["split"],
                "language": case["language"],
                "actual_fields": actual,
                "field_matches": matches,
                "nonempty_expected_groups": [
                    name
                    for name, fields in GROUPS.items()
                    if any(expected.get(field) not in (None, [], "UNKNOWN") for field in fields)
                ],
                "preflight_match": status_ok,
                "full_match": all(matches.values()) and status_ok,
                "failures": failures,
                "error": error,
            }
        )
    return {
        "overall": summarize(records),
        "core": summarize([r for r in records if r["split"] == "core"]),
        "robustness": summarize([r for r in records if r["split"] == "robustness"]),
        "records": records,
    }


def summarize(records: list[dict]) -> dict:
    def score(values):
        values = list(values)
        return {
            "correct": sum(values),
            "total": len(values),
            "accuracy": sum(values) / len(values) if values else None,
        }

    metrics = {
        "full_case": score(r["full_match"] for r in records),
        "field_level": score(v for r in records for v in r["field_matches"].values()),
        "preflight": score(r["preflight_match"] for r in records),
    }
    for name, fields in GROUPS.items():
        metrics[name] = score(
            all(r["field_matches"][f] for f in fields if f in r["field_matches"])
            for r in records
            if any(f in r["field_matches"] for f in fields)
        )
    counts = Counter(f["category"] for r in records for f in r["failures"])
    nonempty = {
        name: score(
            all(r["field_matches"][field] for field in fields if field in r["field_matches"])
            for r in records
            if name in r["nonempty_expected_groups"]
        )
        for name, fields in GROUPS.items()
    }
    return {
        "case_count": len(records),
        "metrics": metrics,
        "failure_taxonomy": {name: counts[name] for name in FAILURE_TYPES},
        "nonempty_target_metrics": nonempty,
    }
