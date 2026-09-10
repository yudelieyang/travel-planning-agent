"""Opt-in provider adapter. Construction does not make a network request."""

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

from app.agent.planner import DeterministicTestPlanner, PlannerDecision, PlannerError
from app.agent.prompts import PROMPTS
from app.agent.requirements import TravelRequirements
from app.core.config import Settings


class PlannerConfigurationError(ValueError):
    pass


class OpenAIPlanner:
    def __init__(self, settings: Settings, *, client=None):
        if not settings.openai_api_key.get_secret_value().strip():
            raise PlannerConfigurationError("OPENAI_API_KEY is required for the OpenAI planner")
        if not settings.openai_model.strip():
            raise PlannerConfigurationError("OPENAI_MODEL is required for the OpenAI planner")
        self.model = settings.openai_model.strip()
        self.prompt_version = settings.planner_prompt_version
        if self.prompt_version not in PROMPTS:
            raise PlannerConfigurationError("Unsupported planner prompt version")
        self.client = (
            client
            if client is not None
            else OpenAI(
                api_key=settings.openai_api_key.get_secret_value(),
                base_url="https://api.openai.com/v1",
                timeout=30.0,
                max_retries=0,
                http_client=httpx.Client(timeout=30.0, trust_env=False),
            )
        )

    def plan(self, requirements: TravelRequirements) -> PlannerDecision:
        try:
            response = self.client.responses.parse(
                model=self.model,
                instructions=PROMPTS[self.prompt_version],
                input=requirements.model_dump_json(),
                text_format=PlannerDecision,
                max_output_tokens=2000,
                store=False,
            )
            if response.status != "completed":
                raise PlannerError("incomplete_response")
            decision = response.output_parsed
            if decision is None:
                raise PlannerError("empty_or_refused_response")
            # Revalidate even if a mocked/constructed model bypassed Pydantic validation.
            return PlannerDecision.model_validate_json(decision.model_dump_json(), strict=True)
        except APITimeoutError:
            raise PlannerError("timeout", retryable=True) from None
        except AuthenticationError:
            raise PlannerError("authentication_error") from None
        except RateLimitError:
            raise PlannerError("rate_limit", retryable=True) from None
        except APIConnectionError:
            raise PlannerError("connection_error", retryable=True) from None
        except (ValidationError, ValueError, TypeError, AttributeError):
            raise PlannerError("invalid_structured_decision") from None
        except APIError:
            raise PlannerError("provider_error") from None


def create_planner(settings: Settings):
    if settings.agent_planner == "deterministic":
        return DeterministicTestPlanner()
    return OpenAIPlanner(settings)
