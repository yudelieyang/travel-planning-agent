import pytest

from app.agent.requirements import (
    AmbiguityLevel,
    BudgetConstraint,
    ConstraintScope,
    PreferenceCategory,
    RequirementAmbiguity,
    RequirementsV2,
    SpecificPreference,
    TravelRequirements,
    parse_requirements,
)
from app.agent.semantic_coverage import CoverageReason
from app.agent.semantic_extractor import (
    SemanticExtractionResult,
    SemanticProposalConstraint,
    SemanticProposalPreference,
    SemanticProposalScope,
    SemanticProposalStrength,
)
from app.agent.semantic_merge import MergeDecisionCode, merge_requirements
from app.agent.service import TravelService


def requirements(*constraints, preferences=(), ambiguities=()):
    return TravelRequirements(
        destination="Boston",
        duration_days=3,
        travelers=1,
        requirements_v2=RequirementsV2(
            constraints=list(constraints), preferences=list(preferences), ambiguities=list(ambiguities)
        ),
    )


def proposal_constraint(scope, value, source_text, strength=SemanticProposalStrength.HARD):
    return SemanticExtractionResult(
        constraints=[
            SemanticProposalConstraint(
                scope=scope, value=value, strength=strength, source_text=source_text
            )
        ]
    )


def test_duplicate_hard_constraint_is_collapsed():
    query = "Keep my total trip under $900."
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.TOTAL_TRIP, value=900)),
        proposal_constraint(SemanticProposalScope.TOTAL_TRIP, 900, "Keep my total trip under $900."),
        query,
    )

    assert len(result.requirements.requirements_v2.constraints) == 1
    assert result.conflicts == []
    assert result.decisions[0].code == MergeDecisionCode.DUPLICATE_CONFIRMED


def test_supported_grounded_missing_scope_is_augmented_and_projects_legacy_fields():
    query = "Keep my total trip under $900. Hotel spending for the whole trip must not exceed $400."
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.TOTAL_TRIP, value=900)),
        proposal_constraint(
            SemanticProposalScope.HOTEL_TOTAL,
            400,
            "Hotel spending for the whole trip must not exceed $400.",
        ),
        query,
    )

    assert [(item.scope, item.value) for item in result.requirements.requirements_v2.constraints] == [
        (ConstraintScope.TOTAL_TRIP, 900),
        (ConstraintScope.HOTEL_TOTAL, 400),
    ]
    assert result.requirements.budget_amount == 900
    assert result.decisions[0].code == MergeDecisionCode.ADDED_FROM_LLM


def test_explicit_amount_conflict_preserves_deterministic_hard_constraint():
    query = "Keep my total trip under $900, not $950."
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.TOTAL_TRIP, value=900)),
        proposal_constraint(SemanticProposalScope.TOTAL_TRIP, 950, "Keep my total trip under $900, not $950."),
        query,
    )

    assert result.requirements.requirements_v2.constraints[0].value == 900
    assert result.conflicts
    assert result.requires_clarification is True


def test_hard_proposal_does_not_upgrade_a_deterministic_soft_hotel_preference():
    query = "I'd prefer the hotel around $400."
    result = merge_requirements(
        requirements(preferences=[SpecificPreference(category=PreferenceCategory.HOTEL, value="around usd 400")]),
        proposal_constraint(SemanticProposalScope.HOTEL_TOTAL, 400, "I'd prefer the hotel around $400."),
        query,
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requires_clarification is True


def test_ambiguous_per_night_soft_proposal_never_becomes_an_executable_constraint():
    query = "I want a $200 hotel."
    result = merge_requirements(
        requirements(
            ambiguities=[
                RequirementAmbiguity(
                    level=AmbiguityLevel.BLOCKING,
                    source_text=query,
                    reason="Hotel amount has an ambiguous scope.",
                )
            ]
        ),
        proposal_constraint(
            SemanticProposalScope.HOTEL_PER_NIGHT,
            200,
            "I want a $200 hotel.",
            SemanticProposalStrength.SOFT,
        ),
        query,
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requirements.requirements_v2.ambiguities[0].level == AmbiguityLevel.BLOCKING
    assert result.decisions[-1].code == MergeDecisionCode.UNSUPPORTED_RETAINED


def test_unsupported_food_total_is_retained_as_non_executable_semantics():
    query = "Spend no more than $300 on food."
    result = merge_requirements(
        requirements(),
        proposal_constraint(SemanticProposalScope.FOOD_TOTAL, 300, query),
        query,
    )

    assert result.requirements.requirements_v2.constraints == []
    assert "FOOD_TOTAL <= 300 USD HARD" in result.requirements.requirements_v2.ambiguities[-1].reason
    assert result.requires_clarification is True


def test_preference_deduplication_and_grounded_augmentation():
    query = "I like fried chicken and art museums."
    result = merge_requirements(
        requirements(preferences=[SpecificPreference(category=PreferenceCategory.FOOD, value="fried chicken")]),
        SemanticExtractionResult(
            preferences=[
                SemanticProposalPreference(
                    category=PreferenceCategory.FOOD,
                    value="fried chicken",
                    source_text="I like fried chicken",
                ),
                SemanticProposalPreference(
                    category=PreferenceCategory.ACTIVITY,
                    value="art museums",
                    source_text="art museums",
                ),
            ]
        ),
        query,
    )

    assert [(item.category, item.value) for item in result.requirements.requirements_v2.preferences] == [
        (PreferenceCategory.FOOD, "fried chicken"),
        (PreferenceCategory.ACTIVITY, "art museums"),
    ]
    assert "art museums" in result.requirements.interests


def test_hallucinated_preference_is_rejected_without_source_grounding():
    result = merge_requirements(
        requirements(),
        SemanticExtractionResult(
            preferences=[
                SemanticProposalPreference(
                    category=PreferenceCategory.ACTIVITY, value="skiing", source_text="skiing"
                )
            ]
        ),
        "Plan 3 days in Boston.",
    )

    assert result.requirements.requirements_v2.preferences == []
    assert result.decisions[0].code == MergeDecisionCode.LLM_REJECTED_UNGROUNDED


class GapExtractor:
    def extract(self, _query):
        return requirements(
            BudgetConstraint(scope=ConstraintScope.TOTAL_TRIP, value=900),
            ambiguities=[
                RequirementAmbiguity(
                    level=AmbiguityLevel.BLOCKING,
                    source_text="If necessary",
                    reason="Unresolved trade-off language.",
                )
            ],
        )


class FixedSemanticExtractor:
    def extract(self, _query):
        return proposal_constraint(
            SemanticProposalScope.HOTEL_TOTAL,
            400,
            "hotel spending for the whole trip must not exceed $400.",
        )


def test_hybrid_service_merges_supported_gap_before_planner_and_validator():
    query = (
        "Plan 3 days in Boston for 1 traveler under $900 total. If necessary, "
        "hotel spending for the whole trip must not exceed $400."
    )
    state, trace = TravelService(
        extractor=GapExtractor(),
        semantic_extractor=FixedSemanticExtractor(),
        semantic_augmentation_enabled=True,
    ).run(query)

    hotel_request = next(item for item in state["tool_requests"] if item.tool_name == "search_hotels")
    assert trace.semantic_coverage.needs_llm is True
    assert trace.final_requirements_source == "hybrid"
    assert trace.requires_clarification is True
    assert hotel_request.arguments.max_price == 200
    assert state["validation_status"] == "passed"


@pytest.mark.parametrize(
    ("query", "proposal", "expected"),
    [
        (
            "Hotel spending cannot exceed $580 total. Actually, $530.",
            proposal_constraint(SemanticProposalScope.HOTEL_TOTAL, 530, "Actually, $530."),
            {ConstraintScope.HOTEL_TOTAL: 530},
        ),
        (
            "Trip ceiling $1,800 and lodging ceiling $750 total; sorry, make the trip $1,600.",
            SemanticExtractionResult(
                constraints=[
                    SemanticProposalConstraint(
                        scope=SemanticProposalScope.TOTAL_TRIP,
                        value=1600,
                        strength=SemanticProposalStrength.HARD,
                        source_text="sorry, make the trip $1,600.",
                    ),
                    SemanticProposalConstraint(
                        scope=SemanticProposalScope.HOTEL_TOTAL,
                        value=750,
                        strength=SemanticProposalStrength.HARD,
                        source_text="lodging ceiling $750 total",
                    ),
                ]
            ),
            {ConstraintScope.TOTAL_TRIP: 1600, ConstraintScope.HOTEL_TOTAL: 750},
        ),
        (
            "The total is capped at $1,350. Hotel total is capped at $500. Change total to $1,200 only.",
            SemanticExtractionResult(
                constraints=[
                    SemanticProposalConstraint(
                        scope=SemanticProposalScope.TOTAL_TRIP,
                        value=1200,
                        strength=SemanticProposalStrength.HARD,
                        source_text="Change total to $1,200 only.",
                    ),
                    SemanticProposalConstraint(
                        scope=SemanticProposalScope.HOTEL_TOTAL,
                        value=500,
                        strength=SemanticProposalStrength.HARD,
                        source_text="Hotel total is capped at $500.",
                    ),
                ]
            ),
            {ConstraintScope.TOTAL_TRIP: 1200, ConstraintScope.HOTEL_TOTAL: 500},
        ),
    ],
)
def test_correction_aware_merge_replaces_only_stale_scope(query, proposal, expected):
    result = merge_requirements(
        parse_requirements(query),
        proposal,
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert {item.scope: item.value for item in result.requirements.requirements_v2.constraints} == expected
    assert result.requires_clarification is False
    assert any(item.code == MergeDecisionCode.CORRECTION_APPLIED for item in result.decisions)
    if ConstraintScope.TOTAL_TRIP in expected:
        assert result.requirements.budget_amount == expected[ConstraintScope.TOTAL_TRIP]


def test_ambiguous_correction_removes_uncertain_hard_state_and_requires_clarification():
    query = "Trip total max $1,200. Hotel total max $500. Actually make it $900."
    result = merge_requirements(
        parse_requirements(query),
        proposal_constraint(SemanticProposalScope.TOTAL_TRIP, 900, "Actually make it $900."),
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requires_clarification is True
    assert result.requirements.requirements_v2.ambiguities[-1].level == AmbiguityLevel.BLOCKING


@pytest.mark.parametrize(
    "proposal",
    [
        proposal_constraint(SemanticProposalScope.TOTAL_TRIP, 850, "Change total to $900."),
        proposal_constraint(SemanticProposalScope.HOTEL_TOTAL, 900, "Change total to $900."),
    ],
)
def test_wrong_correction_amount_or_scope_is_rejected(proposal):
    query = "Trip total max $1,200. Change total to $900."
    result = merge_requirements(
        parse_requirements(query),
        proposal,
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requires_clarification is True
    assert all(item.code != MergeDecisionCode.CORRECTION_APPLIED for item in result.decisions)


def test_m5_stale_hotel_proposal_cannot_reenter_quarantined_scope():
    query = "Hotel spending for the whole trip must stay below $420. Actually make it $380."
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.HOTEL_TOTAL, value=420)),
        proposal_constraint(
            SemanticProposalScope.HOTEL_TOTAL,
            420,
            "Hotel spending for the whole trip must stay below $420.",
        ),
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requires_clarification is True
    assert MergeDecisionCode.STALE_PROPOSAL_REJECTED in {
        item.code for item in result.decisions
    }


def test_m5_valid_hotel_replacement_releases_quarantine():
    query = "Hotel spending for the whole trip must stay below $420. Actually make it $380."
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.HOTEL_TOTAL, value=420)),
        proposal_constraint(SemanticProposalScope.HOTEL_TOTAL, 380, "make it $380"),
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert [(item.scope, item.value) for item in result.requirements.requirements_v2.constraints] == [
        (ConstraintScope.HOTEL_TOTAL, 380)
    ]
    assert result.requires_clarification is False
    assert MergeDecisionCode.CORRECTION_APPLIED in {item.code for item in result.decisions}


def test_m5_wrong_hotel_replacement_amount_leaves_scope_unresolved():
    query = (
        "Hotel spending for the whole trip must stay below $420. "
        "Actually make it $380, not $400."
    )
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.HOTEL_TOTAL, value=420)),
        proposal_constraint(SemanticProposalScope.HOTEL_TOTAL, 400, "make it $380, not $400"),
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requires_clarification is True
    assert MergeDecisionCode.CORRECTION_REPLACEMENT_REJECTED in {
        item.code for item in result.decisions
    }


def test_m5_wrong_scope_cannot_resolve_hotel_quarantine():
    query = "Hotel spending for the whole trip must stay below $420. Actually make hotel $380."
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.HOTEL_TOTAL, value=420)),
        proposal_constraint(SemanticProposalScope.TOTAL_TRIP, 380, "make hotel $380"),
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requires_clarification is True
    assert all(item.scope != ConstraintScope.TOTAL_TRIP for item in result.requirements.requirements_v2.constraints)


def test_m5_unrelated_scope_is_preserved_and_normally_deduplicated():
    query = (
        "Keep the total trip under $1,000. Hotel spending for the whole trip must stay below $420. "
        "Actually make hotel $380."
    )
    result = merge_requirements(
        requirements(
            BudgetConstraint(scope=ConstraintScope.TOTAL_TRIP, value=1000),
            BudgetConstraint(scope=ConstraintScope.HOTEL_TOTAL, value=420),
        ),
        SemanticExtractionResult(
            constraints=[
                SemanticProposalConstraint(
                    scope=SemanticProposalScope.TOTAL_TRIP,
                    value=1000,
                    strength=SemanticProposalStrength.HARD,
                    source_text="Keep the total trip under $1,000.",
                ),
                SemanticProposalConstraint(
                    scope=SemanticProposalScope.HOTEL_TOTAL,
                    value=380,
                    strength=SemanticProposalStrength.HARD,
                    source_text="make hotel $380",
                ),
            ]
        ),
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert {item.scope: item.value for item in result.requirements.requirements_v2.constraints} == {
        ConstraintScope.TOTAL_TRIP: 1000,
        ConstraintScope.HOTEL_TOTAL: 380,
    }
    assert any(
        item.code == MergeDecisionCode.DUPLICATE_CONFIRMED and "TOTAL_TRIP" in item.subject
        for item in result.decisions
    )


def test_m5_missing_replacement_and_unknown_amount_keep_old_hotel_in_quarantine():
    query = "Hotel spending for the whole trip must stay below $420. Actually make the hotel cheaper."
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.HOTEL_TOTAL, value=420)),
        SemanticExtractionResult(),
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requires_clarification is True


def test_m5_total_trip_quarantine_clears_stale_canonical_and_legacy_values():
    query = "Keep the total trip under $1,200. Actually make it $1,000."
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.TOTAL_TRIP, value=1200)),
        proposal_constraint(
            SemanticProposalScope.TOTAL_TRIP,
            1200,
            "Keep the total trip under $1,200.",
        ),
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requirements.budget_amount is None
    assert result.requirements.budget_scope.value == "UNKNOWN"
    assert result.requires_clarification is True


@pytest.mark.parametrize(
    ("query", "old_amount", "new_amount"),
    [
        (
            "Keep the whole trip below $1,100 and accommodation below $420 total. "
            "Adjust hotel only: $380.",
            420,
            380,
        ),
        (
            "Lodging must not exceed $460 total; entire trip must not exceed $980. "
            "Make lodging $400 instead.",
            460,
            400,
        ),
    ],
)
def test_m5_recorded_m4_stale_hotel_proposals_are_quarantined(query, old_amount, new_amount):
    result = merge_requirements(
        parse_requirements(query),
        proposal_constraint(
            SemanticProposalScope.HOTEL_TOTAL,
            old_amount,
            query.split(";")[0].split(" and ")[-1].strip(),
        ),
        query,
        [CoverageReason.AMBIGUOUS_SCOPE, CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    hotel_values = {
        item.value
        for item in result.requirements.requirements_v2.constraints
        if item.scope == ConstraintScope.HOTEL_TOTAL
    }
    assert old_amount not in hotel_values
    assert new_amount not in hotel_values
    assert result.requires_clarification is True


def test_m5_latest_of_multiple_same_scope_corrections_wins_when_validated():
    query = "Hotel total max $500. Actually make it $450. No, make that $400."
    result = merge_requirements(
        requirements(BudgetConstraint(scope=ConstraintScope.HOTEL_TOTAL, value=500)),
        proposal_constraint(SemanticProposalScope.HOTEL_TOTAL, 400, "make that $400"),
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )

    assert [(item.scope, item.value) for item in result.requirements.requirements_v2.constraints] == [
        (ConstraintScope.HOTEL_TOTAL, 400)
    ]


def test_explicit_adjustment_can_reuse_ambiguous_scope_coverage_without_gate_change():
    query = (
        "Keep the whole trip below $1,100 and accommodation below $420 total. "
        "Adjust hotel only: $380."
    )
    proposal = SemanticExtractionResult(
        constraints=[
            SemanticProposalConstraint(
                scope=SemanticProposalScope.TOTAL_TRIP,
                value=1100,
                strength=SemanticProposalStrength.HARD,
                source_text="whole trip below $1,100",
            ),
            SemanticProposalConstraint(
                scope=SemanticProposalScope.HOTEL_TOTAL,
                value=380,
                strength=SemanticProposalStrength.HARD,
                source_text="Adjust hotel only: $380.",
            ),
        ]
    )

    result = merge_requirements(
        parse_requirements(query), proposal, query, [CoverageReason.AMBIGUOUS_SCOPE]
    )

    assert {item.scope: item.value for item in result.requirements.requirements_v2.constraints} == {
        ConstraintScope.TOTAL_TRIP: 1100,
        ConstraintScope.HOTEL_TOTAL: 380,
    }
    assert result.requires_clarification is False


@pytest.mark.parametrize(
    ("query", "amount"),
    [
        ("I want a $200 hotel.", 200),
        ("My hotel budget is $300.", 300),
        ("I can spend $700 on lodging.", 700),
    ],
)
def test_ambiguous_hotel_hard_proposal_is_firewalled(query, amount):
    result = merge_requirements(
        parse_requirements(query),
        proposal_constraint(SemanticProposalScope.HOTEL_TOTAL, amount, query),
        query,
        [CoverageReason.AMBIGUOUS_SCOPE],
    )

    assert result.requirements.requirements_v2.constraints == []
    assert result.requires_clarification is True
    assert any(item.code == MergeDecisionCode.LLM_REJECTED_UNSAFE for item in result.decisions)


def test_explicit_whole_trip_hotel_cap_may_be_promoted():
    query = "Hotel spending for the whole trip must stay below $300."
    result = merge_requirements(
        requirements(),
        proposal_constraint(SemanticProposalScope.HOTEL_TOTAL, 300, query),
        query,
    )

    assert [(item.scope, item.value) for item in result.requirements.requirements_v2.constraints] == [
        (ConstraintScope.HOTEL_TOTAL, 300)
    ]
    assert result.requires_clarification is False


def test_positive_preference_remains_supported():
    query = "I like zoos."
    result = merge_requirements(
        requirements(),
        SemanticExtractionResult(
            preferences=[
                SemanticProposalPreference(
                    category=PreferenceCategory.ACTIVITY,
                    value="zoo",
                    source_text=query,
                )
            ]
        ),
        query,
    )

    assert result.requirements.requirements_v2.preferences[0].value == "zoo"


@pytest.mark.parametrize(
    ("query", "category", "value"),
    [
        ("Do not include zoos.", PreferenceCategory.ACTIVITY, "zoo"),
        ("Avoid nightlife.", PreferenceCategory.ACTIVITY, "nightlife"),
        ("No luxury hotels.", PreferenceCategory.HOTEL, "luxury"),
    ],
)
def test_negative_preference_is_rejected_and_retained_as_blocking(query, category, value):
    result = merge_requirements(
        requirements(),
        SemanticExtractionResult(
            preferences=[
                SemanticProposalPreference(category=category, value=value, source_text=query)
            ]
        ),
        query,
        [CoverageReason.UNREPRESENTED_NEGATION],
    )

    assert result.requirements.requirements_v2.preferences == []
    assert result.requires_clarification is True
    assert any(item.code == MergeDecisionCode.LLM_REJECTED_UNSAFE for item in result.decisions)


def test_tradeoff_component_preference_is_not_detached_from_its_dependency():
    query = "Spend more on the hotel if it is downtown."
    result = merge_requirements(
        requirements(),
        SemanticExtractionResult(
            preferences=[
                SemanticProposalPreference(
                    category=PreferenceCategory.HOTEL,
                    value="downtown hotel",
                    source_text=query,
                )
            ]
        ),
        query,
        [CoverageReason.TRADEOFF_LANGUAGE],
    )

    assert result.requirements.requirements_v2.preferences == []
    assert result.requires_clarification is True
