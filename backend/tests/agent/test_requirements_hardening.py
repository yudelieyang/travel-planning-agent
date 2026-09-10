import json
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.agent.extractor import RuleBasedRequirementsExtractor
from app.agent.requirements import TravelRequirements, assess_requirements
from app.agent.requirements_evaluation import evaluate_requirements, failure_type
from app.agent.service import TravelService
from app.core.config import PROJECT_ROOT
from app.main import app


@pytest.mark.parametrize("amount", ["3", "three", "THREE"])
@pytest.mark.parametrize(
    "template",
    [
        "Plan a {n}-day trip to Boston.",
        "I'll be in Boston for {n} days!",
        "Give me {n} days in Boston;",
    ],
)
def test_duration_phrasings(amount, template):
    req = RuleBasedRequirementsExtractor().extract(template.format(n=amount))
    assert req.destination == "Boston"
    assert req.duration_days == 3
    assert req.travelers is None


@pytest.mark.parametrize(
    "query", ["nyc for 3 days pls", "  NYC   for  3 DAYS  pls ", "NYC, 3 days."]
)
def test_surface_normalization(query):
    req = RuleBasedRequirementsExtractor().extract(query)
    assert (req.destination, req.duration_days) == ("New York City", 3)


@pytest.mark.parametrize(
    "negative", ["I don't like museums", "Do not include museums", "No museums", "Avoid museums"]
)
def test_negative_interest_is_not_positive(negative):
    req = RuleBasedRequirementsExtractor().extract("Plan a 2-day trip to Boston. " + negative)
    assert req.interests == []
    assert "avoid museums" in req.constraints


def test_positive_and_negative_preferences_are_separate():
    req = RuleBasedRequirementsExtractor().extract(
        "Plan a 2-day trip to Boston. I don't want museums but I like parks."
    )
    assert req.interests == ["parks"]
    assert req.constraints == ["avoid museums"]


@pytest.mark.parametrize(
    "text,travelers",
    [
        ("I'm traveling alone", 1),
        ("for two", 2),
        ("for me and my partner", 2),
        ("for a family of four", 4),
        ("for three adults", 3),
        ("We are traveling", None),
    ],
)
def test_party_expressions(text, travelers):
    req = RuleBasedRequirementsExtractor().extract(f"Plan a 2-day trip to Boston. {text}.")
    assert req.travelers == travelers


@pytest.mark.parametrize(
    "query",
    [
        "Plan a 3-day trip to New York or Boston.",
        "Boston or NYC, three days.",
        "Go to somewhere warm for 3 days.",
    ],
)
def test_ambiguous_destination_requires_clarification(query):
    planner = Mock()
    result = TravelService(planner=planner).plan(query)
    assert result.status == "needs_clarification"
    assert result.requirements.destination is None
    assert "destination" in result.missing_fields
    planner.plan.assert_not_called()


@pytest.mark.parametrize(
    "query", ["Tell me a joke.", "What's the weather today?", "Book me a flight right now."]
)
def test_unrelated_requests_do_not_invent_trip(query):
    req = RuleBasedRequirementsExtractor().extract(query)
    assert req.destination is None and req.duration_days is None
    assert assess_requirements(req).status == "INSUFFICIENT"


def test_budget_and_conflict_facts_are_preserved_without_resolution():
    req = RuleBasedRequirementsExtractor().extract(
        "I want a luxury hotel in Boston but my total budget is $150 for three days."
    )
    assert req.hotel_preferences == ["luxury"]
    assert req.budget_amount == 150
    assert req.budget_scope == "TOTAL_TRIP"
    assert req.duration_days == 3


@pytest.mark.parametrize("phrase", ["Keep it cheap", "Make it affordable", "I have no budget"])
def test_qualitative_budget_never_becomes_a_dollar_amount(phrase):
    assert RuleBasedRequirementsExtractor().extract(phrase).budget_amount is None


@pytest.mark.parametrize(
    "query,status",
    [
        ("Plan a three-day trip to Boston.", "success"),
        ("Plan a trip.", "needs_clarification"),
        ("Plan a 2-day trip to Boston. I don't want museums.", "success"),
        ("Plan a 2-day trip to New York or Boston.", "needs_clarification"),
    ],
)
def test_api_extraction_paths(query, status):
    with TestClient(app) as client:
        result = client.post("/api/v1/travel/plan", json={"query": query})
    assert result.status_code == 200
    assert result.json()["status"] == status
    if "don't" in query:
        assert result.json()["requirements"]["interests"] == []
        assert "avoid museums" in result.json()["requirements"]["constraints"]
        assert any("not verified" in w for w in result.json()["warnings"])


@pytest.mark.parametrize(
    "field,actual,expected,tags,category",
    [
        ("travelers", None, 2, [], "MISSING_EXTRACTION"),
        ("travelers", 2, None, [], "FALSE_POSITIVE"),
        ("travelers", 3, 2, [], "WRONG_VALUE"),
        ("interests", ["museums"], [], ["negation"], "NEGATION_ERROR"),
        ("destination", "Boston", None, ["ambiguity"], "AMBIGUITY_ERROR"),
        ("destination", "boston", "Boston", [], "NORMALIZATION_ERROR"),
    ],
)
def test_deterministic_taxonomy(field, actual, expected, tags, category):
    assert failure_type(field, actual, expected, tags) == category


def test_evaluator_passes_only_query_and_scores_partial_fields():
    extractor = Mock()
    extractor.extract.return_value = TravelRequirements(destination="Boston", duration_days=3)
    case = {
        "id": "unseen-id",
        "query": "arbitrary input",
        "split": "core",
        "language": "en",
        "tags": [],
        "expected_fields": {"destination": "Boston", "duration_days": 4},
        "expected_status": "SUFFICIENT",
    }
    report = evaluate_requirements([case], extractor)
    extractor.extract.assert_called_once_with("arbitrary input")
    assert report["overall"]["metrics"]["full_case"]["accuracy"] == 0
    assert report["overall"]["metrics"]["field_level"]["accuracy"] == 0.5
    assert report["overall"]["metrics"]["travelers"]["accuracy"] is None


def test_capability_dataset_reports_gaps_without_asserting_perfect_accuracy():
    cases = json.loads(
        (PROJECT_ROOT / "evals/datasets/requirements_eval_v1.json").read_text("utf-8")
    )
    assert len(cases) == len({case["id"] for case in cases}) == 44
    report = evaluate_requirements(cases, RuleBasedRequirementsExtractor())
    assert report["core"]["case_count"] == 28
    assert report["robustness"]["case_count"] == 16
    failures = [r for r in report["records"] if not r["full_match"]]
    # Capability gaps are measured, not xfailed/skipped or supplied to the extractor.
    assert all(r["failures"] for r in failures)
    assert len(report["records"]) == 44
