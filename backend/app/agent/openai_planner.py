"""Opt-in provider adapter. Construction does not make a network request."""

import json
from contextvars import ContextVar
from time import perf_counter

import httpx
from openai import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)
from pydantic import ValidationError

from app.agent.planner import DeterministicTestPlanner, PlannerDecision, PlannerError, ReplanContext
from app.agent.prompts import PROMPTS
from app.agent.requirements import TravelRequirements
from app.core.config import Settings


class PlannerConfigurationError(ValueError):
    pass


def create_openai_client(settings: Settings):
    return OpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        base_url="https://api.openai.com/v1",
        timeout=30.0,
        max_retries=0,
        http_client=httpx.Client(timeout=30.0, trust_env=False),
    )


def infrastructure_error(exc, fallback):
    """Persist only known error categories, never raw provider text."""
    code = getattr(exc, "code", None)
    known = {
        "insufficient_quota": "insufficient_quota",
        "billing_required": "billing_required",
        "model_not_found": "model_not_available",
        "model_not_available": "model_not_available",
        "permission_denied": "permission_denied",
    }
    if isinstance(code, str) and code in known:
        return known[code]
    if getattr(exc, "status_code", None) == 403:
        return "permission_denied"
    return fallback


class OpenAIPlanner:
    def __init__(self, settings: Settings, *, client=None):
        if not settings.openai_api_key.get_secret_value().strip():
            raise PlannerConfigurationError("OPENAI_API_KEY is required for the OpenAI planner")
        if not settings.openai_model.strip():
            raise PlannerConfigurationError("OPENAI_MODEL is required for the OpenAI planner")
        self.model = settings.openai_model.strip()
        self.max_output_tokens = settings.openai_max_output_tokens
        self.reasoning_effort = settings.openai_reasoning_effort
        self._observation = ContextVar("planner_observation", default=None)
        self.prompt_version = settings.planner_prompt_version
        if self.prompt_version not in PROMPTS:
            raise PlannerConfigurationError("Unsupported planner prompt version")
        self.client = (
            client
            if client is not None
            else create_openai_client(settings)
        )

    def plan(
        self, requirements: TravelRequirements, feedback: ReplanContext | None = None
    ) -> PlannerDecision:
        metadata = {
            "model": self.model,
            "input_tokens": None,
            "output_tokens": None,
            "total_tokens": None,
            "api_latency_ms": None,
            "api_error_type": None,
        }
        diagnostics = {"invalid_tool": None, "invalid_arguments": None, "duplicate_tool": None}
        started = perf_counter()
        try:
            instructions = PROMPTS[self.prompt_version]
            if feedback is not None:
                instructions += (
                    "\nThe input includes a typed hard-budget failure and previous itinerary. "
                    "Return a materially lower-cost matching plan and set budget_repair to true."
                )
            response = self.client.responses.parse(
                model=self.model,
                instructions=instructions,
                input=(
                    requirements.model_dump_json()
                    if feedback is None
                    else json.dumps(
                        {
                            "requirements": requirements.model_dump(mode="json"),
                            "replan_context": feedback.model_dump(mode="json"),
                        }
                    )
                ),
                text_format=PlannerDecision,
                max_output_tokens=self.max_output_tokens,
                reasoning={"effort": self.reasoning_effort},
                store=False,
            )
            usage = getattr(response, "usage", None)
            for name in ("input_tokens", "output_tokens", "total_tokens"):
                value = getattr(usage, name, None)
                metadata[name] = value if type(value) is int and value >= 0 else None
            if response.status != "completed":
                raise PlannerError("incomplete_response")
            decision = response.output_parsed
            if decision is None:
                raise PlannerError("empty_or_refused_response")
            # Revalidate even if a mocked/constructed model bypassed Pydantic validation.
            validated = PlannerDecision.model_validate_json(decision.model_dump_json(), strict=True)
            diagnostics = dict.fromkeys(diagnostics, False)
            return validated
        except APITimeoutError:
            metadata["api_error_type"] = "timeout"
            raise PlannerError("timeout", retryable=True) from None
        except AuthenticationError:
            metadata["api_error_type"] = "authentication_error"
            raise PlannerError("authentication_error") from None
        except RateLimitError as exc:
            code = infrastructure_error(exc, "rate_limit")
            metadata["api_error_type"] = code
            raise PlannerError(code, retryable=code == "rate_limit") from None
        except APIConnectionError:
            metadata["api_error_type"] = "connection_error"
            raise PlannerError("connection_error", retryable=True) from None
        except ValidationError as exc:
            # Error type only. Never copy ValidationError.input, message, or provider bodies.
            kinds = {
                error["type"] for error in exc.errors(include_input=False, include_context=False)
            }
            for index, kind in enumerate(("invalid_tool", "duplicate_tool", "invalid_arguments")):
                if kind in kinds:
                    diagnostics[kind] = True
                    for passed in ("invalid_tool", "duplicate_tool", "invalid_arguments")[:index]:
                        diagnostics[passed] = False
                    break
            metadata["api_error_type"] = "invalid_structured_decision"
            raise PlannerError("invalid_structured_decision") from None
        except (ValueError, TypeError, AttributeError):
            metadata["api_error_type"] = "invalid_structured_decision"
            raise PlannerError("invalid_structured_decision") from None
        except APIError as exc:
            code = infrastructure_error(exc, "provider_error")
            metadata["api_error_type"] = code
            raise PlannerError(code) from None
        except PlannerError as exc:
            metadata["api_error_type"] = exc.code
            raise
        finally:
            metadata["api_latency_ms"] = round((perf_counter() - started) * 1000, 2)
            self._observation.set({"metadata": metadata, "diagnostics": diagnostics})

    def get_observation(self):
        """Per-context metadata; no mutable process-wide last-response state."""
        observation = self._observation.get()
        return (
            {
                "metadata": dict(observation["metadata"]),
                "diagnostics": dict(observation["diagnostics"]),
            }
            if observation
            else None
        )


def create_planner(settings: Settings):
    if settings.agent_planner == "deterministic":
        return DeterministicTestPlanner()
    return OpenAIPlanner(settings)
