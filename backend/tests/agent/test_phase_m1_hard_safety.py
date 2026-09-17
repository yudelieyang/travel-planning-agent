import json

import pytest

from app.agent.requirements import ConstraintScope, ConstraintStrength, parse_requirements
from app.core.config import PROJECT_ROOT

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


def _case_map():
    cases = json.loads(
        (PROJECT_ROOT / "evals/datasets/hybrid_semantics_200_v1.json").read_text("utf-8")
    )["cases"]
    return {case["id"]: case for case in cases}


@pytest.mark.parametrize("case_id", sorted(P0_IDS))
def test_phase_m1_p0_cases_never_reach_an_unsafe_executable_constraint(case_id):
    case = _case_map()[case_id]
    expected = case["expected"]
    requirements = parse_requirements(case["input"])
    actual = {(item.scope.value, item.value) for item in requirements.requirements_v2.constraints}
    gold = {(item["scope"], item["value"]) for item in expected.get("constraints", [])}

    assert actual == gold
    if expected.get("unsupported_scopes") or expected.get("ambiguity_levels"):
        assert any(
            item.level.value == "BLOCKING" for item in requirements.requirements_v2.ambiguities
        )


def test_hard_ceiling_variants_preserve_scope_without_global_last_money_wins():
    requirements = parse_requirements(
        "The full Boston trip cannot exceed $1,400, while lodging must stay below $550 total."
    )

    assert [(item.scope, item.value) for item in requirements.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 1400),
        (ConstraintScope.HOTEL_TOTAL, 550),
    ]


def test_correction_variants_supersede_only_the_explicit_scope_and_project_legacy_total():
    requirements = parse_requirements(
        "Trip cap is $1,500. Hotel max $650 total. No, use $1,250 for the trip."
    )

    assert {(item.scope, item.value) for item in requirements.requirements_v2.constraints} == {
        (ConstraintScope.TOTAL_TRIP, 1250),
        (ConstraintScope.HOTEL_TOTAL, 650),
    }
    assert requirements.budget_amount == 1250


@pytest.mark.parametrize(
    "query,marker",
    [
        ("My hotel budget: $460.", "Hotel budget does not specify"),
        ("Accommodation must stay under $180 per night.", "HOTEL_PER_NIGHT"),
        ("Restaurant costs cannot exceed $310.", "FOOD_TOTAL"),
    ],
)
def test_ambiguous_or_unsupported_hard_money_is_blocking_and_non_executable(query, marker):
    requirements = parse_requirements(query)

    assert requirements.requirements_v2.constraints == []
    assert requirements.requirements_v2.ambiguities[0].level.value == "BLOCKING"
    assert marker in requirements.requirements_v2.ambiguities[0].reason


def test_trailing_soft_intent_overrides_a_preceding_hard_word_but_explicit_hard_remains_hard():
    soft = parse_requirements("Trip under $1,200 would be ideal, though flexible.")
    hard = parse_requirements("Trip must stay under $1,200.")

    assert soft.requirements_v2.constraints == []
    assert soft.budget_constraint_strength == ConstraintStrength.SOFT
    assert [(item.scope, item.value) for item in hard.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 1200)
    ]
