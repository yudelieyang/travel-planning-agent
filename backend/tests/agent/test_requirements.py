import json
from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.agent.requirements import (
    BudgetConstraint,
    ConstraintOperator,
    ConstraintScope,
    ConstraintStrength,
    OptimizationObjective,
    PreferenceCategory,
    RequirementsV2,
    TravelRequirements,
    parse_requirements,
)
from app.core.budget import BudgetScope

QUERY = "Plan a 3-day trip to New York City under $1000. I like museums and food."


def test_parse_vertical_slice_without_inventing_travelers():
    requirements = parse_requirements(QUERY)
    assert requirements.destination == "New York City"
    assert requirements.duration_days == 3
    assert requirements.budget_amount == 1000
    assert requirements.currency == "USD"
    assert requirements.interests == ["museums", "food"]
    assert requirements.travelers is None
    assert requirements.origin is None
    assert requirements.start_date is None


def test_no_invented_requirements():
    requirements = parse_requirements("Plan a trip for me.")
    assert requirements.destination is None
    assert requirements.duration_days is None
    assert requirements.budget_amount is None
    assert requirements.travelers is None


def test_dates_origin_preferences_and_travelers():
    r = parse_requirements(
        "Travel from Boston to NYC from 2026-10-01 to 2026-10-03 "
        "for 2 travelers under USD 1,000. Vegetarian food and quiet hotels."
    )
    assert r.origin == "Boston"
    assert r.destination == "New York City"
    assert r.start_date == date(2026, 10, 1)
    assert r.trip_days == 3
    assert r.travelers == 2
    assert r.food_preferences == ["vegetarian"]
    assert r.hotel_preferences == ["quiet"]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"duration_days": 0},
        {"travelers": 0},
        {"budget_amount": -1},
        {"budget_amount": float("nan")},
        {"start_date": "2026-10-03", "end_date": "2026-10-01"},
        {"start_date": "2026-10-01", "end_date": "2026-10-03", "duration_days": 2},
    ],
)
def test_invalid_requirements(kwargs):
    with pytest.raises(ValidationError):
        TravelRequirements(**kwargs)


def test_preserves_specific_preferences_with_a_category_and_raw_value():
    requirements = parse_requirements(
        "Plan a 3-day trip to New York City. I enjoy city walking and fried chicken."
    )

    assert requirements.interests == ["city walking", "food"]
    assert requirements.food_preferences == ["fried chicken"]
    assert [preference.model_dump() for preference in requirements.specific_preferences] == [
        {"category": PreferenceCategory.ACTIVITY, "value": "city walking"},
        {"category": PreferenceCategory.FOOD, "value": "fried chicken"},
    ]
    assert TravelRequirements.model_validate_json(requirements.model_dump_json()) == requirements


@pytest.mark.parametrize(
    "phrase",
    [
        "under $1000",
        "max $1000",
        "don't spend more than $1000",
        "my budget is $1000",
        "maximum budget is $1000",
    ],
)
def test_budget_limit_variants_have_one_hard_constraint_representation(phrase):
    requirements = parse_requirements(f"Plan a 3-day trip to Boston. {phrase}.")

    assert requirements.budget_amount == 1000
    assert requirements.budget_constraint_strength == ConstraintStrength.HARD


def test_represents_soft_budget_and_optimization_objective_without_enforcing_them():
    soft = parse_requirements("Plan a 3-day trip to Boston. I would prefer to stay around $800.")
    objective = parse_requirements(
        "Plan a 3-day trip to Boston under $1000. Spend as much of the budget as reasonably possible."
    )

    assert soft.budget_constraint_strength == ConstraintStrength.SOFT
    assert objective.budget_constraint_strength == ConstraintStrength.HARD
    assert objective.objective == OptimizationObjective.MAXIMIZE_BUDGET_UTILIZATION


@pytest.mark.parametrize(
    "phrase,interests,food,transport,specifics",
    [
        (
            "I like zoos and fried chicken.",
            ["zoo", "food"],
            ["fried chicken"],
            [],
            [(PreferenceCategory.ACTIVITY, "zoo"), (PreferenceCategory.FOOD, "fried chicken")],
        ),
        (
            "I like zoos and I love fried chicken.",
            ["zoo", "food"],
            ["fried chicken"],
            [],
            [(PreferenceCategory.ACTIVITY, "zoo"), (PreferenceCategory.FOOD, "fried chicken")],
        ),
        ("I enjoy museums and I prefer seafood.", ["museums"], ["seafood"], [], []),
        (
            "I enjoy parks and I also like coffee.",
            ["parks", "food"],
            ["coffee"],
            [],
            [(PreferenceCategory.FOOD, "coffee")],
        ),
        (
            "I like walking, but I prefer public transit.",
            [],
            [],
            ["walking", "public transit"],
            [],
        ),
    ],
)
def test_preference_connectors_do_not_leak_discourse_prefixes(
    phrase, interests, food, transport, specifics
):
    requirements = parse_requirements(phrase)
    assert requirements.interests == interests
    assert requirements.food_preferences == food
    assert requirements.transport_preferences == transport
    assert [(item.category, item.value) for item in requirements.specific_preferences] == specifics


@pytest.mark.parametrize(
    "phrase,strength,scope",
    [
        ("I only want to spend $1300.", ConstraintStrength.UNSPECIFIED, BudgetScope.UNKNOWN),
        (
            "I only want to spend 1300 dollars.",
            ConstraintStrength.UNSPECIFIED,
            BudgetScope.UNKNOWN,
        ),
        ("I can spend $1300.", ConstraintStrength.UNSPECIFIED, BudgetScope.UNKNOWN),
        ("I have $1300 for the trip.", ConstraintStrength.UNSPECIFIED, BudgetScope.TOTAL_TRIP),
        ("My spending limit is $1300.", ConstraintStrength.HARD, BudgetScope.UNKNOWN),
        ("Keep the trip under $1300.", ConstraintStrength.HARD, BudgetScope.TOTAL_TRIP),
        ("I want to spend no more than $1300.", ConstraintStrength.HARD, BudgetScope.UNKNOWN),
        ("I'd like to keep the trip around $1300.", ConstraintStrength.SOFT, BudgetScope.UNKNOWN),
        ("I can spend about $1300 total.", ConstraintStrength.SOFT, BudgetScope.TOTAL_TRIP),
        ("My total budget is $1300.", ConstraintStrength.HARD, BudgetScope.TOTAL_TRIP),
        (
            "I only want to spend 1300 dollars about it.",
            ConstraintStrength.UNSPECIFIED,
            BudgetScope.UNKNOWN,
        ),
    ],
)
def test_budget_intent_grammar_preserves_conservative_semantics(phrase, strength, scope):
    requirements = parse_requirements(phrase)
    assert requirements.budget_amount == 1300
    assert requirements.currency == "USD"
    assert requirements.budget_constraint_strength == strength
    assert requirements.budget_scope == scope


@pytest.mark.parametrize("phrase", ["Plan a 3-day trip.", "Plan a trip for 2 travelers."])
def test_non_money_numbers_are_not_budget_false_positives(phrase):
    requirements = parse_requirements(phrase)
    assert requirements.budget_amount is None
    assert requirements.budget_constraint_strength == ConstraintStrength.UNSPECIFIED
    assert requirements.budget_scope == BudgetScope.UNKNOWN


def test_requirements_v2_preserves_independent_budget_scopes_and_legacy_total_projection():
    requirements = TravelRequirements(
        requirements_v2=RequirementsV2(
            constraints=[
                BudgetConstraint(
                    scope=ConstraintScope.TOTAL_TRIP,
                    operator=ConstraintOperator.LTE,
                    value=900,
                    source_text="under $900 total",
                ),
                BudgetConstraint(
                    scope=ConstraintScope.HOTEL_TOTAL,
                    value=400,
                    source_text="hotel spending must not exceed $400",
                ),
            ]
        )
    )

    assert [(item.scope, item.value) for item in requirements.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 900),
        (ConstraintScope.HOTEL_TOTAL, 400),
    ]
    assert requirements.budget_amount == 900
    assert requirements.budget_scope == BudgetScope.TOTAL_TRIP
    assert requirements.budget_constraint_strength == ConstraintStrength.HARD
    assert TravelRequirements.model_validate_json(requirements.model_dump_json()) == requirements


def test_legacy_hard_total_budget_is_projected_to_requirements_v2():
    requirements = TravelRequirements(
        budget_amount=900,
        budget_scope=BudgetScope.TOTAL_TRIP,
        budget_constraint_strength=ConstraintStrength.HARD,
    )

    assert requirements.requirements_v2.constraints[0].scope == ConstraintScope.TOTAL_TRIP
    assert requirements.requirements_v2.constraints[0].value == 900


def test_semantic_requirements_v2_dataset():
    cases = json.loads((Path(__file__).parent / "fixtures/semantic_requirements_v2.json").read_text())

    for case in cases:
        requirements = parse_requirements(case["query"])
        assert [(item.scope.value, item.value) for item in requirements.requirements_v2.constraints] == [
            tuple(item) for item in case["constraints"]
        ], case["id"]
        assert requirements.budget_amount == case["legacy_budget"], case["id"]
        assert [(item.category.value, item.value) for item in requirements.requirements_v2.preferences] == [
            tuple(item) for item in case["preferences"]
        ], case["id"]


def test_unsupported_hard_food_budget_is_retained_as_blocking_ambiguity():
    requirements = parse_requirements("My total budget is $1500. Spend no more than $300 on food.")

    assert [(item.scope, item.value) for item in requirements.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 1500)
    ]
    assert requirements.requirements_v2.ambiguities[0].level == "BLOCKING"


def test_unspecified_hotel_amount_is_blocking_not_a_hard_constraint():
    requirements = parse_requirements("I want a $200 hotel.")

    assert requirements.requirements_v2.constraints == []
    assert requirements.requirements_v2.ambiguities[0].level == "BLOCKING"


@pytest.mark.parametrize(
    "query,scope,value",
    [
        ("Don't let the total go over $900.", ConstraintScope.TOTAL_TRIP, 900),
        ("Hotel must stay below $400 total.", ConstraintScope.HOTEL_TOTAL, 400),
    ],
)
def test_common_hard_ceiling_paraphrases_keep_their_scope(query, scope, value):
    requirements = parse_requirements(query)

    assert [(item.scope, item.value) for item in requirements.requirements_v2.constraints] == [
        (scope, value)
    ]


def test_scope_aware_correction_inherits_only_an_explicitly_corrected_scope():
    requirements = parse_requirements(
        "My total budget is $1200 and the hotel can cost at most $500 total. "
        "Actually make the total budget $1000."
    )

    assert [(item.scope, item.value) for item in requirements.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 1000),
        (ConstraintScope.HOTEL_TOTAL, 500),
    ]


@pytest.mark.parametrize(
    "query,expected",
    [
        (
            "My total budget is $1000. Make it $800.",
            [(ConstraintScope.TOTAL_TRIP, 800)],
        ),
        (
            "Hotel spending must stay under $500. Actually make it $400.",
            [(ConstraintScope.HOTEL_TOTAL, 400)],
        ),
        (
            "Trip under $900. Hotel under $400.",
            [(ConstraintScope.TOTAL_TRIP, 900), (ConstraintScope.HOTEL_TOTAL, 400)],
        ),
        (
            "The whole trip must stay under $1000. The hotel must stay under $400.",
            [(ConstraintScope.TOTAL_TRIP, 1000), (ConstraintScope.HOTEL_TOTAL, 400)],
        ),
    ],
)
def test_phase_j_explicit_scope_and_immediate_correction_rules(query, expected):
    requirements = parse_requirements(query)

    assert [(item.scope, item.value) for item in requirements.requirements_v2.constraints] == expected


def test_phase_j_scope_free_amount_after_unrelated_clause_does_not_inherit_scope():
    requirements = parse_requirements("Trip budget is $1000. I like museums. $400 would be nice.")

    assert [(item.scope, item.value) for item in requirements.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 1000)
    ]


def test_phase_j_soft_and_ambiguous_budget_forms_preserve_existing_safety_policy():
    soft = parse_requirements("I'd like the trip to stay around $1000.")
    hotel = parse_requirements("My hotel budget is $300.")
    scope_free = parse_requirements("I have $900.")

    assert soft.requirements_v2.constraints == []
    assert soft.budget_constraint_strength == ConstraintStrength.SOFT
    assert hotel.requirements_v2.constraints == []
    assert hotel.requirements_v2.ambiguities[0].level == "BLOCKING"
    assert scope_free.requirements_v2.constraints == []
    assert scope_free.budget_amount == 900
    assert scope_free.budget_scope == BudgetScope.UNKNOWN


def test_phase_j_false_correction_and_scope_inheritance_guards():
    unchanged = parse_requirements("My total budget is $1000. Actually, I like museums.")
    distant = parse_requirements("My total budget is $1000. I like museums. Actually make it $800.")
    non_budget = parse_requirements("Make it a 3-day trip. I'd rather stay near downtown.")
    unsupported = parse_requirements("Hotel max $400. Dinner around $100.")
    rating = parse_requirements("Trip max $900. Hotel rating 4 stars.")

    assert [(item.scope, item.value) for item in unchanged.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 1000)
    ]
    assert [(item.scope, item.value) for item in distant.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 1000)
    ]
    assert non_budget.requirements_v2.constraints == []
    assert [(item.scope, item.value) for item in unsupported.requirements_v2.constraints] == [
        (ConstraintScope.HOTEL_TOTAL, 400)
    ]
    assert [(item.scope, item.value) for item in rating.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 900)
    ]


def test_unsupported_transport_and_activity_caps_remain_blocking_non_executable_semantics():
    for query in ("Keep transportation below $100.", "Activities must stay under $150."):
        requirements = parse_requirements(query)
        assert requirements.requirements_v2.constraints == []
        assert requirements.requirements_v2.ambiguities[0].level == "BLOCKING"


def test_visit_activity_and_false_money_numbers_are_not_confused():
    visit = parse_requirements("I want to visit zoos in Columbus.")
    numbers = parse_requirements("Visit 2 museums. Take Route 66 at 9 AM.")

    assert visit.destination == "Columbus"
    assert (PreferenceCategory.ACTIVITY, "zoo") in {
        (item.category, item.value) for item in visit.requirements_v2.preferences
    }
    assert numbers.requirements_v2.constraints == []
