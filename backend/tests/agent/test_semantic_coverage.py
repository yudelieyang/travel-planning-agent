import json
from pathlib import Path

import pytest

from app.agent.requirements import parse_requirements
from app.agent.semantic_coverage import SemanticCoverageAnalyzer


def test_semantic_coverage_dataset():
    cases = json.loads(
        (Path(__file__).parents[3] / "evals/datasets/semantic_coverage_v1.json").read_text()
    )["cases"]
    analyzer = SemanticCoverageAnalyzer()

    for case in cases:
        result = analyzer.analyze(case["query"], parse_requirements(case["query"]))
        assert result.needs_llm is case["needs_llm"], case["id"]
        assert [reason.value for reason in result.reasons] == case["reasons"], case["id"]


def test_coverage_is_deterministic_for_the_same_input():
    query = "I want a $200 hotel."
    requirements = parse_requirements(query)
    analyzer = SemanticCoverageAnalyzer()

    assert analyzer.analyze(query, requirements) == analyzer.analyze(query, requirements)


def test_bare_hotel_budget_remains_a_blocking_scope_ambiguity():
    query = "My hotel budget is $300."
    result = SemanticCoverageAnalyzer().analyze(query, parse_requirements(query))

    assert result.needs_llm is True
    assert [reason.value for reason in result.reasons] == ["AMBIGUOUS_SCOPE"]


@pytest.mark.parametrize(
    "query,needs_llm",
    [
        ("Trip under $900 total. Dining must stay below $200.", True),
        ("whole Chicago trip cost less 1180 pls", True),
        ("Trip under $900 total. Hotel under $400 total.", False),
        ("Plan two days in Boston under $800.", False),
    ],
)
def test_unrepresented_hard_money_requires_augmentation_without_penalizing_complete_cases(
    query, needs_llm
):
    result = SemanticCoverageAnalyzer().analyze(query, parse_requirements(query))

    assert result.needs_llm is needs_llm
    assert ("MONETARY_SEMANTIC_GAP" in result.reasons) is needs_llm


def test_retained_unsupported_hard_scope_is_semantically_complete():
    requirements = parse_requirements("Spend no more than $300 on food.")
    result = SemanticCoverageAnalyzer().analyze("Spend no more than $300 on food.", requirements)

    assert requirements.requirements_v2.ambiguities[0].level.value == "BLOCKING"
    assert result.needs_llm is False


@pytest.mark.parametrize(
    "query,needs_llm",
    [
        ("Hotel max is $580 total. Actually, $530.", True),
        ("Trip max $1,800; hotel max $750 total; sorry, make the trip $1,600.", True),
        ("My total budget is $1,000. Actually make it $700.", False),
        ("The total is $1,000. Actually, museums close early.", False),
    ],
)
def test_only_unresolved_monetary_corrections_require_augmentation(query, needs_llm):
    result = SemanticCoverageAnalyzer().analyze(query, parse_requirements(query))

    assert result.needs_llm is needs_llm
    assert ("CORRECTION_TARGET_UNRESOLVED" in result.reasons) is needs_llm


@pytest.mark.parametrize(
    "query,needs_llm",
    [
        ("A $700 place to stay in New York City is okay.", True),
        ("Hotel spending must stay below $400 total.", False),
        ("A four-star place to stay is okay.", False),
    ],
)
def test_unrepresented_hotel_money_remains_ambiguous(query, needs_llm):
    result = SemanticCoverageAnalyzer().analyze(query, parse_requirements(query))

    assert result.needs_llm is needs_llm
    assert ("AMBIGUOUS_SCOPE" in result.reasons) is needs_llm


@pytest.mark.parametrize(
    "query,needs_llm",
    [
        ("Boston is fine, but do not include zoos.", True),
        ("San Francisco without tourist-trap restaurants.", True),
        ("Do not let the total go over $900.", False),
        ("No more than $300 for food.", False),
    ],
)
def test_only_travel_exclusions_create_an_unrepresented_negation_gap(query, needs_llm):
    result = SemanticCoverageAnalyzer().analyze(query, parse_requirements(query))

    assert result.needs_llm is needs_llm
    assert ("UNREPRESENTED_NEGATION" in result.reasons) is needs_llm


@pytest.mark.parametrize(
    "query,needs_llm",
    [
        ("Save on food so we can spend more on activities.", True),
        ("Prioritize hotel quality over restaurants.", True),
        ("Pay extra for a quiet hotel if it cuts commute time.", True),
        ("Hotel under $400 total, but trip under $900 total.", False),
    ],
)
def test_two_sided_tradeoffs_require_augmentation_without_matching_plain_conjunctions(
    query, needs_llm
):
    result = SemanticCoverageAnalyzer().analyze(query, parse_requirements(query))

    assert result.needs_llm is needs_llm
    assert ("TRADEOFF_LANGUAGE" in result.reasons) is needs_llm


@pytest.mark.parametrize(
    "query,needs_llm",
    [
        ("I enjoy seafood in Boston.", True),
        ("Museums please.", True),
        (
            "Plan a 3-day trip to Columbus for 1 traveler under $900 total. "
            "I like zoos and fried chicken. Hotel spending must not exceed $400.",
            False,
        ),
        ("I want to spend no more than $900 total.", False),
        ("Austin for 4 days; I want 5 attractions.", False),
    ],
)
def test_explicit_unrepresented_preferences_use_a_bounded_requirement_gap(query, needs_llm):
    result = SemanticCoverageAnalyzer().analyze(query, parse_requirements(query))

    assert result.needs_llm is needs_llm
    assert ("UNRESOLVED_REQUIREMENT_CLAUSE" in result.reasons) is needs_llm


@pytest.mark.parametrize(
    "query",
    [
        "Hotel under $600 total. Make it a 4-day trip.",
        "Hotel total max $900; actually make the trip 4 days, not $900.",
    ],
)
def test_non_monetary_corrections_do_not_create_a_correction_gap(query):
    result = SemanticCoverageAnalyzer().analyze(query, parse_requirements(query))

    assert "CORRECTION_TARGET_UNRESOLVED" not in result.reasons


def test_mixed_soft_hotel_and_hard_total_requests_preserve_the_hybrid_boundary():
    hybrid = "Seattle hotel around $600 total, but the whole trip cannot exceed $1,500."
    soft_only = "Hotel around $600 total."

    assert SemanticCoverageAnalyzer().analyze(hybrid, parse_requirements(hybrid)).needs_llm is True
    assert (
        SemanticCoverageAnalyzer().analyze(soft_only, parse_requirements(soft_only)).needs_llm
        is False
    )
