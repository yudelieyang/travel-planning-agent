"""Stable local fixtures, no provider SDKs, model calls or network access."""

from decimal import Decimal
from typing import TYPE_CHECKING

from app.core.budget import BudgetScope
from app.tools.candidate_data import candidates_for
from app.tools.contracts import (
    BudgetInput,
    BudgetRequest,
    BudgetSummary,
    Category,
    SearchInput,
    ToolRequest,
    ToolResult,
    ToolStatus,
)

if TYPE_CHECKING:
    from app.tools.candidate_providers import CandidateProvider


def money(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01")))


def _search(
    tool_name: str,
    category: Category,
    arguments: SearchInput,
    provider: "CandidateProvider | None" = None,
) -> ToolResult:
    source = provider.source_for(arguments.destination, category) if provider is not None else "mock"
    try:
        selected = candidates_for(
            arguments.destination,
            category,
            max_price=arguments.max_price,
            preferences=arguments.preferences,
            provider=provider,
        )
        if selected is None:
            return ToolResult(
                tool_name=tool_name,
                status=ToolStatus.NO_RESULTS,
                data=[],
                source=source,
                error="UNSUPPORTED_CITY_DATA",
                metadata={"count": 0, "currency": "USD"},
            )
        return ToolResult(
            tool_name=tool_name,
            status=ToolStatus.SUCCESS if selected else ToolStatus.NO_RESULTS,
            data=selected,
            source=source,
            metadata={"count": len(selected), "currency": "USD"},
        )
    except (OSError, ValueError, TypeError):
        return ToolResult(
            tool_name=tool_name,
            status=ToolStatus.ERROR,
            source=source,
            error=(
                "Mock fixture unavailable or invalid"
                if source == "mock"
                else "Candidate snapshot unavailable or invalid"
            ),
        )


def search_attractions(
    arguments: SearchInput, provider: "CandidateProvider | None" = None
) -> ToolResult:
    return _search("search_attractions", "attractions", arguments, provider)


def search_hotels(
    arguments: SearchInput, provider: "CandidateProvider | None" = None
) -> ToolResult:
    return _search("search_hotels", "hotel", arguments, provider)


def search_restaurants(
    arguments: SearchInput, provider: "CandidateProvider | None" = None
) -> ToolResult:
    return _search("search_restaurants", "food", arguments, provider)


def search_transport(
    arguments: SearchInput, provider: "CandidateProvider | None" = None
) -> ToolResult:
    return _search("search_transport", "transport", arguments, provider)


def calculate_budget(arguments: BudgetInput) -> ToolResult:
    breakdown = {
        category: Decimal("0") for category in ("hotel", "food", "transport", "attractions")
    }
    for item in arguments.items:
        breakdown[item.category] += Decimal(str(item.amount))
    per_person = sum(breakdown.values(), Decimal("0"))
    # A unit quote is not an assertion that the party has one traveler.
    multiplier = arguments.travelers if arguments.travelers is not None else 1
    total = per_person * multiplier
    warnings = []
    within = None
    comparison = None
    if arguments.travelers is None:
        warnings.append("Traveler count is unspecified: costs are per traveler, not a group total.")
    if arguments.limit is not None:
        if arguments.limit_currency != "USD":
            warnings.append(
                "Mock prices are USD; no currency conversion or budget comparison was made."
            )
        elif arguments.budget_scope == BudgetScope.UNKNOWN:
            warnings.append("Budget scope is unknown; no budget comparison was made.")
        elif arguments.budget_scope == BudgetScope.PER_PERSON:
            comparison = per_person
            within = per_person <= Decimal(str(arguments.limit))
            if not within:
                warnings.append("Estimated per-person cost exceeds the supplied budget.")
        elif arguments.travelers is None:
            warnings.append("Group budget cannot be verified without a traveler count.")
            if total > Decimal(str(arguments.limit)):
                warnings.append("Even the per-traveler reference cost exceeds the supplied budget.")
        else:
            comparison = total
            within = total <= Decimal(str(arguments.limit))
            if not within:
                warnings.append("Estimated group cost exceeds the supplied budget.")
    summary = BudgetSummary(
        basis="group" if arguments.travelers is not None else "per_traveler",
        travelers=arguments.travelers,
        per_traveler_cost=money(per_person),
        estimated_total_cost=money(total),
        breakdown={key: money(value * multiplier) for key, value in breakdown.items()},
        provided_limit=arguments.limit,
        limit_currency=arguments.limit_currency,
        budget_scope=arguments.budget_scope,
        within_budget=within,
        comparison_cost=money(comparison) if comparison is not None else None,
        remaining_budget=(
            money(Decimal(str(arguments.limit)) - comparison) if comparison is not None else None
        ),
        warnings=warnings,
    )
    return ToolResult(
        tool_name="calculate_budget",
        status=ToolStatus.SUCCESS,
        data=summary,
        source="deterministic",
    )


def run_tool(
    request: ToolRequest, *, provider: "CandidateProvider | None" = None
) -> ToolResult:
    if isinstance(request, BudgetRequest):
        if request.arguments is None:
            return ToolResult(
                tool_name=request.tool_name,
                status=ToolStatus.ERROR,
                source="deterministic",
                error="Budget inputs are unresolved",
            )
        return calculate_budget(request.arguments)
    functions = {
        "search_attractions": search_attractions,
        "search_hotels": search_hotels,
        "search_restaurants": search_restaurants,
        "search_transport": search_transport,
    }
    return functions[request.tool_name](request.arguments, provider)
