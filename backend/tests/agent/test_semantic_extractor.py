from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from pydantic import SecretStr

from app.agent.requirements import (
    BudgetConstraint,
    ConstraintScope,
    RequirementsV2,
    TravelRequirements,
)
from app.agent.semantic_coverage import CoverageReason
from app.agent.semantic_extractor import (
    SEMANTIC_EXTRACTOR_PROMPTS,
    OpenAISemanticExtractor,
    SemanticExtractionError,
    SemanticExtractionResult,
    SemanticProposalConstraint,
    SemanticProposalScope,
    SemanticProposalStrength,
    create_semantic_extractor,
)
from app.agent.semantic_merge import merge_requirements
from app.agent.service import TravelService
from app.core.config import Settings


def settings(**changes):
    return Settings(
        _env_file=None,
        postgres_db="test",
        postgres_user="test",
        postgres_password=SecretStr("test"),
        **{
            "openai_api_key": SecretStr("offline-test-placeholder"),
            "openai_model": "offline-model",
            "semantic_augmentation_mode": "hybrid",
            **changes,
        },
    )


def proposal():
    return SemanticExtractionResult(
        constraints=[
            SemanticProposalConstraint(
                scope=SemanticProposalScope.HOTEL_TOTAL,
                value=400,
                strength=SemanticProposalStrength.HARD,
                source_text="Hotel spending must not exceed $400.",
            )
        ]
    )


def test_openai_semantic_extractor_accepts_only_schema_valid_structured_output():
    client = Mock()
    client.responses.parse.return_value = SimpleNamespace(status="completed", output_parsed=proposal())
    extractor = OpenAISemanticExtractor(settings(), client=client)

    result = extractor.extract("Hotel spending must not exceed $400.")

    assert result == proposal()
    assert client.responses.parse.call_args.kwargs["text_format"] is SemanticExtractionResult
    assert client.responses.parse.call_args.kwargs["store"] is False
    assert extractor.get_observation()["error"] is None


def test_semantic_prompts_v1_and_v2_are_preserved_and_v3_is_selectable():
    assert SEMANTIC_EXTRACTOR_PROMPTS["semantic_extractor_v1"] == (
        "Extract travel requirements into the supplied JSON schema only.\n"
        "You are a semantic extractor, not a travel planner. Do not calculate costs, decide feasibility,\n"
        "choose candidates, validate budgets, or recommend a repair. Separate hard constraints, soft\n"
        "preferences, objectives, and ambiguities. Budget scopes may be TOTAL_TRIP, HOTEL_TOTAL,\n"
        "HOTEL_PER_NIGHT, FOOD_TOTAL, or UNSPECIFIED. Preserve ambiguity rather than inventing certainty."
    )
    v1 = OpenAISemanticExtractor(
        settings(semantic_extractor_prompt_version="semantic_extractor_v1"), client=Mock()
    )
    v2 = OpenAISemanticExtractor(
        settings(semantic_extractor_prompt_version="semantic_extractor_v2"), client=Mock()
    )
    v3 = OpenAISemanticExtractor(
        settings(semantic_extractor_prompt_version="semantic_extractor_v3"), client=Mock()
    )

    assert v1.prompt_version == "semantic_extractor_v1"
    assert v2.prompt_version == "semantic_extractor_v2"
    assert v3.prompt_version == "semantic_extractor_v3"
    assert "without an explicit total-stay or per-night basis" in v2.instructions
    assert v2.instructions in v3.instructions


@pytest.mark.parametrize(
    "instruction",
    [
        "actually make it",
        "make that",
        "change it to",
        "change that to",
        "use X instead",
        "no use X",
        "sorry I meant X",
        "actually use X",
        "make the hotel X",
        "make the total X",
        "nearest compatible prior requirement",
        "explicit target overrides pronoun inheritance",
        "preserve the prior scope, LTE operator, and HARD or SOFT strength",
        "approximate or preferential wording remains SOFT",
        "explicit must/cannot/maximum wording is HARD",
        "unrelated clause",
        "BLOCKING ambiguity instead of guessing",
    ],
)
def test_v3_prompt_covers_bounded_correction_matrix(instruction):
    assert instruction.casefold() in SEMANTIC_EXTRACTOR_PROMPTS["semantic_extractor_v3"].casefold()


@pytest.mark.parametrize(
    ("proposal_scope", "proposal_value", "expected_value"),
    [
        (SemanticProposalScope.HOTEL_TOTAL, 400, 400),
        (SemanticProposalScope.HOTEL_TOTAL, 500, None),
        (SemanticProposalScope.TOTAL_TRIP, 400, None),
    ],
)
def test_v3_proposal_contract_keeps_frozen_m5_merge_authoritative(
    proposal_scope, proposal_value, expected_value
):
    query = "Hotel spending for the whole trip must stay under $500. Actually make it $400."
    deterministic = TravelRequirements(
        requirements_v2=RequirementsV2(
            constraints=[BudgetConstraint(scope=ConstraintScope.HOTEL_TOTAL, value=500)]
        )
    )
    proposed = SemanticExtractionResult(
        constraints=[
            SemanticProposalConstraint(
                scope=proposal_scope,
                value=proposal_value,
                strength=SemanticProposalStrength.HARD,
                source_text=(
                    "Actually make it $400."
                    if proposal_value == 400
                    else "Hotel spending for the whole trip must stay under $500."
                ),
            )
        ]
    )

    result = merge_requirements(
        deterministic,
        proposed,
        query,
        [CoverageReason.CORRECTION_TARGET_UNRESOLVED],
    )
    hotel = next(
        (
            item.value
            for item in result.requirements.requirements_v2.constraints
            if item.scope == ConstraintScope.HOTEL_TOTAL
        ),
        None,
    )

    assert hotel == expected_value


def test_invalid_structured_output_becomes_a_safe_extractor_failure():
    client = Mock()
    client.responses.parse.return_value = SimpleNamespace(status="completed", output_parsed={})

    try:
        OpenAISemanticExtractor(settings(), client=client).extract("I want a $200 hotel.")
    except SemanticExtractionError as exc:
        assert exc.code == "invalid_structured_proposal"
    else:
        raise AssertionError("Invalid structured output must not be accepted")


def test_missing_key_leaves_hybrid_semantic_extraction_unavailable():
    assert create_semantic_extractor(settings(openai_api_key="")) is None
    _, trace = TravelService(semantic_augmentation_enabled=True).run(
        "Plan 2 days in Boston. I want a $200 hotel."
    )
    assert (trace.llm_invoked, trace.llm_extraction_status) == (False, "unavailable")


def test_complete_deterministic_request_does_not_invoke_the_semantic_extractor():
    extractor = Mock()
    _, trace = TravelService(
        semantic_extractor=extractor, semantic_augmentation_enabled=True
    ).run(
        "Plan a 3-day trip to Columbus for 1 traveler under $900 total. "
        "I like zoos and fried chicken. Hotel spending must not exceed $400."
    )

    extractor.extract.assert_not_called()
    assert trace.semantic_coverage.needs_llm is False
    assert trace.llm_extraction_status == "not_requested"


def test_ambiguous_request_invokes_once_but_never_mutates_canonical_requirements():
    extractor = Mock()
    extractor.extract.return_value = proposal()
    query = "Plan 2 days in Boston. I want a $200 hotel."

    state, trace = TravelService(
        semantic_extractor=extractor, semantic_augmentation_enabled=True
    ).run(query)

    extractor.extract.assert_called_once_with(query)
    assert trace.llm_extraction_status == "proposed"
    assert trace.llm_semantic_proposal == proposal()
    assert state["requirements"].requirements_v2.constraints == []
    assert state["requirements"].requirements_v2.ambiguities


def test_extractor_failure_preserves_deterministic_execution():
    extractor = Mock()
    extractor.extract.side_effect = SemanticExtractionError("connection_error")

    state, trace = TravelService(
        semantic_extractor=extractor, semantic_augmentation_enabled=True
    ).run("Plan 2 days in Boston. I want a $200 hotel.")

    assert trace.llm_extraction_status == "failed"
    assert trace.llm_error_code == "connection_error"
    assert state["requirements"].requirements_v2.constraints == []
