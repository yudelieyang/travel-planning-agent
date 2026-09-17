"""Shared decision contract and an offline regression planner."""

from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator
from pydantic_core import PydanticCustomError

from app.agent.execution import ValidationViolation
from app.agent.itinerary import Itinerary
from app.agent.requirements import ConstraintScope, TravelRequirements
from app.tools.contracts import BudgetRequest, SearchInput, SearchRequest, ToolRequest

TOOL_ALLOWLIST = frozenset(
    {
        "search_attractions",
        "search_hotels",
        "search_restaurants",
        "search_transport",
        "calculate_budget",
    }
)


class PlannerError(RuntimeError):
    def __init__(self, code: str, *, retryable: bool = False):
        self.code = code
        self.retryable = retryable
        super().__init__(code)


class PlannerDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)
    can_proceed: bool
    tool_requests: list[ToolRequest] = Field(max_length=5)
    warnings: list[str] = Field(max_length=10)
    budget_repair: bool = False

    @model_validator(mode="before")
    @classmethod
    def classify_tool_contract(cls, value):
        """Safe error types for metrics; never persist the rejected provider payload."""
        if not isinstance(value, dict) or not isinstance(value.get("tool_requests"), list):
            return value
        requests = [
            r.model_dump(mode="json") if isinstance(r, (SearchRequest, BudgetRequest)) else r
            for r in value["tool_requests"]
        ]
        names = [r.get("tool_name") if isinstance(r, dict) else None for r in requests]
        if any(not isinstance(name, str) or name not in TOOL_ALLOWLIST for name in names):
            raise PydanticCustomError("invalid_tool", "Unregistered or missing tool name")
        if len(names) != len(set(names)):
            raise PydanticCustomError("duplicate_tool", "Duplicate tool request")
        for request in requests:
            try:
                if request["tool_name"] == "calculate_budget":
                    BudgetRequest.model_validate(request, strict=True)
                    if request.get("arguments") is not None:
                        raise ValueError("Budget arguments must be tool-derived")
                else:
                    SearchRequest.model_validate(request, strict=True)
            except (ValidationError, ValueError, TypeError):
                raise PydanticCustomError("invalid_arguments", "Invalid tool arguments") from None
        return value

    @model_validator(mode="after")
    def execution_contract(self):
        names = [request.tool_name for request in self.tool_requests]
        if any(name not in TOOL_ALLOWLIST for name in names) or len(names) != len(set(names)):
            raise ValueError("Unknown or duplicate tool")
        if self.can_proceed and set(names) != TOOL_ALLOWLIST:
            raise ValueError("This mock slice requires four searches and a budget calculation")
        if not self.can_proceed and self.tool_requests:
            raise ValueError("Blocked decisions cannot request tools")
        if any(
            isinstance(r, BudgetRequest) and r.arguments is not None for r in self.tool_requests
        ):
            raise ValueError("Budget arguments must be resolved from tool results")
        if any(len(warning) > 500 for warning in self.warnings):
            raise ValueError("Warnings must be brief")
        return self


class PlannerProtocol(Protocol):
    def plan(
        self, requirements: TravelRequirements, feedback: "ReplanContext | None" = None
    ) -> PlannerDecision: ...


class ReplanContext(BaseModel):
    violations: list[ValidationViolation] = Field(min_length=1)
    previous_itinerary: Itinerary
    attempt: int = Field(ge=1)


class DeterministicTestPlanner:
    def plan(
        self, requirements: TravelRequirements, feedback: ReplanContext | None = None
    ) -> PlannerDecision:
        if not requirements.destination or requirements.trip_days is None:
            raise ValueError("Preflight must succeed before planning")
        preferences = {
            "search_attractions": [x for x in requirements.interests if x != "food"],
            "search_hotels": requirements.hotel_preferences,
            "search_restaurants": requirements.food_preferences,
            "search_transport": requirements.transport_preferences,
        }
        requests = [
            SearchRequest(
                tool_name=name,
                arguments=SearchInput(
                    destination=requirements.destination,
                    preferences=tags,
                    max_price=hotel_price_ceiling(requirements) if name == "search_hotels" else None,
                ),
            )
            for name, tags in preferences.items()
        ] + [BudgetRequest()]
        return PlannerDecision(
            can_proceed=True,
            tool_requests=requests,
            warnings=[],
            budget_repair=feedback is not None,
        )


def hotel_price_ceiling(requirements: TravelRequirements) -> float | None:
    """Translate a supported group hotel cap into the fixture's per-person nightly price."""
    constraint = next(
        (
            item
            for item in requirements.requirements_v2.constraints
            if item.scope == ConstraintScope.HOTEL_TOTAL
        ),
        None,
    )
    nights = (requirements.trip_days or 0) - 1
    if constraint is None or constraint.currency != "USD" or requirements.travelers is None or nights < 1:
        return None
    return constraint.value / (requirements.travelers * nights)
