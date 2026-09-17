"""Optional structured semantic proposals. Phase G owns any merge into requirements."""

from contextvars import ContextVar
from enum import StrEnum
from time import perf_counter

from openai import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.agent.openai_planner import create_openai_client, infrastructure_error
from app.agent.requirements import AmbiguityLevel, OptimizationObjective, PreferenceCategory
from app.core.config import Settings


class SemanticProposalScope(StrEnum):
    TOTAL_TRIP = "TOTAL_TRIP"
    HOTEL_TOTAL = "HOTEL_TOTAL"
    HOTEL_PER_NIGHT = "HOTEL_PER_NIGHT"
    FOOD_TOTAL = "FOOD_TOTAL"
    UNSPECIFIED = "UNSPECIFIED"


class SemanticProposalStrength(StrEnum):
    HARD = "HARD"
    SOFT = "SOFT"


class SemanticProposalConstraint(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    kind: str = Field(default="BUDGET", pattern=r"^BUDGET$")
    scope: SemanticProposalScope
    operator: str = Field(default="LTE", pattern=r"^LTE$")
    value: float = Field(ge=0)
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    strength: SemanticProposalStrength
    source_text: str = Field(min_length=1, max_length=500)
    extractor_source: str = Field(default="llm", pattern=r"^llm$")


class SemanticProposalPreference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: PreferenceCategory
    value: str = Field(min_length=1, max_length=100)
    source_text: str = Field(min_length=1, max_length=500)


class SemanticProposalAmbiguity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    level: AmbiguityLevel
    source_text: str = Field(min_length=1, max_length=500)
    reason: str = Field(min_length=1, max_length=200)


class SemanticExtractionResult(BaseModel):
    """Untrusted semantic proposal; deliberately distinct from RequirementsV2."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    constraints: list[SemanticProposalConstraint] = Field(default_factory=list)
    preferences: list[SemanticProposalPreference] = Field(default_factory=list)
    objectives: list[OptimizationObjective] = Field(default_factory=list)
    ambiguities: list[SemanticProposalAmbiguity] = Field(default_factory=list)


class SemanticExtractionError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


SEMANTIC_EXTRACTOR_PROMPTS = {
    "semantic_extractor_v1": """Extract travel requirements into the supplied JSON schema only.
You are a semantic extractor, not a travel planner. Do not calculate costs, decide feasibility,
choose candidates, validate budgets, or recommend a repair. Separate hard constraints, soft
preferences, objectives, and ambiguities. Budget scopes may be TOTAL_TRIP, HOTEL_TOTAL,
HOTEL_PER_NIGHT, FOOD_TOTAL, or UNSPECIFIED. Preserve ambiguity rather than inventing certainty.""",
    "semantic_extractor_v2": """Extract travel requirements into the supplied JSON schema only.
Be conservative: source grounding does not justify an inferred scope, strength, or polarity.
For hotel/lodging money without an explicit total-stay or per-night basis, return a BLOCKING
ambiguity and no constraint. '$300 hotel' is ambiguous; '$300 total hotel spend' is HOTEL_TOTAL;
'$300 per night' is HOTEL_PER_NIGHT. Treat must/cannot/maximum/no-more-than as HARD and
prefer/around/ideally/would-like as SOFT; mixed meaning stays ambiguous. Never convert avoid,
exclude, do-not, without, or no-X language into a positive preference: return a BLOCKING
ambiguity because exclusion is not executable. Preserve conditional or priority tradeoffs as a
BLOCKING ambiguity; do not reduce them to independent preferences that imply completeness.
Do not calculate costs, choose candidates, validate budgets, or recommend repairs.""",
    "semantic_extractor_v3": """Extract travel requirements into the supplied JSON schema only.
Be conservative: source grounding does not justify an inferred scope, strength, or polarity.
For hotel/lodging money without an explicit total-stay or per-night basis, return a BLOCKING
ambiguity and no constraint. '$300 hotel' is ambiguous; '$300 total hotel spend' is HOTEL_TOTAL;
'$300 per night' is HOTEL_PER_NIGHT. Treat must/cannot/maximum/no-more-than as HARD and
prefer/around/ideally/would-like as SOFT; mixed meaning stays ambiguous. Never convert avoid,
exclude, do-not, without, or no-X language into a positive preference: return a BLOCKING
ambiguity because exclusion is not executable. Preserve conditional or priority tradeoffs as a
BLOCKING ambiguity; do not reduce them to independent preferences that imply completeness.
Do not calculate costs, choose candidates, validate budgets, or recommend repairs.
For an explicit monetary correction, extract the corrected requirement, not the superseded one.
Correction forms include actually make it, make that, change it to, change that to, use X instead,
no use X, sorry I meant X, actually use X, adjust X, make the hotel X, and make the total X.
Use only the nearest compatible prior requirement in the same local context; never use a global
last amount, scope, or constraint. An explicit target overrides pronoun inheritance. If only the
amount changes, preserve the prior scope, LTE operator, and HARD or SOFT strength. Explicit new
approximate or preferential wording remains SOFT; explicit must/cannot/maximum wording is HARD.
Use the correction clause as source_text. If target or amount is unclear, or an unrelated clause
breaks the local context, return a BLOCKING ambiguity instead of guessing. Unrelated uses of
correction words are not monetary corrections.""",
}


class OpenAISemanticExtractor:
    prompt_version = "semantic_extractor_v3"

    def __init__(self, settings: Settings, *, client=None):
        if not settings.openai_api_key.get_secret_value().strip() or not settings.openai_model.strip():
            raise SemanticExtractionError("not_configured")
        self.model = settings.openai_model.strip()
        self.max_output_tokens = settings.openai_max_output_tokens
        self.reasoning_effort = settings.openai_reasoning_effort
        self.prompt_version = settings.semantic_extractor_prompt_version
        self.instructions = SEMANTIC_EXTRACTOR_PROMPTS[self.prompt_version]
        self.client = client if client is not None else create_openai_client(settings)
        self._observation = ContextVar("semantic_extractor_observation", default=None)

    def extract(self, query: str) -> SemanticExtractionResult:
        metadata = {"input_tokens": None, "output_tokens": None, "total_tokens": None, "latency_ms": None, "error": None}
        started = perf_counter()
        try:
            response = self.client.responses.parse(
                model=self.model,
                instructions=self.instructions,
                input=query,
                text_format=SemanticExtractionResult,
                max_output_tokens=self.max_output_tokens,
                reasoning={"effort": self.reasoning_effort},
                store=False,
            )
            if response.status != "completed" or response.output_parsed is None:
                raise SemanticExtractionError("empty_or_refused_response")
            usage = getattr(response, "usage", None)
            for name in ("input_tokens", "output_tokens", "total_tokens"):
                value = getattr(usage, name, None)
                metadata[name] = value if type(value) is int and value >= 0 else None
            proposal = response.output_parsed
            return SemanticExtractionResult.model_validate_json(proposal.model_dump_json(), strict=True)
        except APITimeoutError:
            metadata["error"] = "timeout"
            raise SemanticExtractionError("timeout") from None
        except AuthenticationError:
            metadata["error"] = "authentication_error"
            raise SemanticExtractionError("authentication_error") from None
        except RateLimitError as exc:
            metadata["error"] = infrastructure_error(exc, "rate_limit")
            raise SemanticExtractionError(metadata["error"]) from None
        except APIConnectionError:
            metadata["error"] = "connection_error"
            raise SemanticExtractionError("connection_error") from None
        except ValidationError:
            metadata["error"] = "invalid_structured_proposal"
            raise SemanticExtractionError("invalid_structured_proposal") from None
        except (ValueError, TypeError, AttributeError):
            metadata["error"] = "invalid_structured_proposal"
            raise SemanticExtractionError("invalid_structured_proposal") from None
        except APIError as exc:
            metadata["error"] = infrastructure_error(exc, "provider_error")
            raise SemanticExtractionError(metadata["error"]) from None
        finally:
            metadata["latency_ms"] = round((perf_counter() - started) * 1000, 2)
            self._observation.set(metadata)

    def get_observation(self):
        observation = self._observation.get()
        return dict(observation) if observation is not None else None


def create_semantic_extractor(settings: Settings) -> OpenAISemanticExtractor | None:
    if settings.semantic_augmentation_mode != "hybrid":
        return None
    try:
        return OpenAISemanticExtractor(settings)
    except SemanticExtractionError as exc:
        if exc.code == "not_configured":
            return None
        raise
