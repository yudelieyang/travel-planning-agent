"""Stable local fixtures, no provider SDKs, model calls or network access."""

import json
from decimal import Decimal
from pathlib import Path

from app.tools.contracts import (
    BudgetInput,
    BudgetRequest,
    BudgetSummary,
    SearchInput,
    ToolRequest,
    ToolResult,
    ToolStatus,
    TravelOption,
)

MOCK_ROOT = Path(__file__).resolve().parents[3] / "data" / "mock"


def money(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01")))


def _search(tool_name: str, filename: str, arguments: SearchInput) -> ToolResult:
    try:
        raw = json.loads((MOCK_ROOT / filename).read_text(encoding="utf-8"))
        rows = [TravelOption.model_validate(row) for row in raw]
        aliases = {"nyc": "new york city", "new york": "new york city"}
        destination = aliases.get(
            arguments.destination.casefold(), arguments.destination.casefold()
        )
        preferences = {p.strip().casefold() for p in arguments.preferences}
        selected = [
            row
            for row in rows
            if row.destination.casefold() == destination
            and (arguments.max_price is None or row.price <= arguments.max_price)
            and (not preferences or preferences.issubset(set(row.tags)))
        ]
        selected.sort(key=lambda row: (row.price, row.id))
        return ToolResult(
            tool_name=tool_name,
            status=ToolStatus.SUCCESS if selected else ToolStatus.NO_RESULTS,
            data=selected,
            source="mock",
            metadata={"count": len(selected), "currency": "USD"},
        )
    except (OSError, ValueError, TypeError):
        return ToolResult(
            tool_name=tool_name,
            status=ToolStatus.ERROR,
            source="mock",
            error="Mock fixture unavailable or invalid",
        )


def search_attractions(arguments: SearchInput) -> ToolResult:
    return _search("search_attractions", "attractions.json", arguments)


def search_hotels(arguments: SearchInput) -> ToolResult:
    return _search("search_hotels", "hotels.json", arguments)


def search_restaurants(arguments: SearchInput) -> ToolResult:
    return _search("search_restaurants", "restaurants.json", arguments)


def search_transport(arguments: SearchInput) -> ToolResult:
    return _search("search_transport", "transport.json", arguments)


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
    if arguments.travelers is None:
        warnings.append("Traveler count is unspecified: costs are per traveler, not a group total.")
    if arguments.limit is not None:
        if arguments.limit_currency != "USD":
            warnings.append(
                "Mock prices are USD; no currency conversion or budget comparison was made."
            )
        elif arguments.travelers is None:
            warnings.append("Group budget cannot be verified without a traveler count.")
            if total > Decimal(str(arguments.limit)):
                warnings.append("Even the per-traveler reference cost exceeds the supplied budget.")
        else:
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
        within_budget=within,
        warnings=warnings,
    )
    return ToolResult(
        tool_name="calculate_budget",
        status=ToolStatus.SUCCESS,
        data=summary,
        source="deterministic",
    )


def run_tool(request: ToolRequest) -> ToolResult:
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
    return functions[request.tool_name](request.arguments)
