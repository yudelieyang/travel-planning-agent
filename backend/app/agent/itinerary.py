"""Deterministic mock itinerary composition and structural validation."""

from decimal import Decimal

from pydantic import BaseModel, Field

from app.agent.requirements import TravelRequirements
from app.tools.contracts import BudgetInput, BudgetSummary, Category, CostItem, TravelOption
from app.tools.mock import money


class Activity(BaseModel):
    name: str
    category: Category
    estimated_cost: float = Field(ge=0)


class DayPlan(BaseModel):
    day_number: int = Field(ge=1)
    activities: list[Activity]
    estimated_cost: float = Field(ge=0)


class Itinerary(BaseModel):
    destination: str
    days: int = Field(ge=1, le=30)
    currency: str = "USD"
    estimated_total_cost: float = Field(ge=0)
    daily_plan: list[DayPlan]
    warnings: list[str] = Field(default_factory=list)


def compose_draft(
    requirements: TravelRequirements,
    options: dict[str, list[TravelOption]],
) -> tuple[list[DayPlan], BudgetInput, list[str]]:
    days = requirements.trip_days
    if days is None:
        raise ValueError("Duration is required")
    multiplier = requirements.travelers if requirements.travelers is not None else 1
    daily = []
    costs = []
    for number in range(1, days + 1):
        attraction = options["search_attractions"][
            (number - 1) % len(options["search_attractions"])
        ]
        restaurant = options["search_restaurants"][
            (number - 1) % len(options["search_restaurants"])
        ]
        selected = [(attraction, "attractions", attraction.name)]
        selected += [
            (restaurant, "food", f"{restaurant.name} ({meal})")
            for meal in ("breakfast", "lunch", "dinner")
        ]
        transport = options["search_transport"][0]
        selected.append((transport, "transport", transport.name))
        if number < days:
            hotel = options["search_hotels"][0]
            selected.append((hotel, "hotel", hotel.name))
        activities = []
        for option, category, name in selected:
            costs.append(CostItem(category=category, amount=option.price))
            activities.append(
                Activity(
                    name=name,
                    category=category,
                    estimated_cost=money(Decimal(str(option.price)) * multiplier),
                )
            )
        subtotal = sum((Decimal(str(a.estimated_cost)) for a in activities), Decimal("0"))
        daily.append(
            DayPlan(day_number=number, activities=activities, estimated_cost=money(subtotal))
        )
    warnings = [
        "Offline mock estimates only; no live availability, tax, tips or intercity fares.",
        "Quote convention: three meals/day and days minus one lodging nights; prices per person.",
    ]
    if days > len(options["search_attractions"]):
        warnings.append("Small mock dataset: some attractions repeat across days.")
    if requirements.constraints:
        warnings.append(
            "Constraints are recorded but not verified by this mock planner: "
            + ", ".join(requirements.constraints)
        )
    if requirements.start_date or requirements.end_date:
        warnings.append(
            "Dates determine duration only; opening hours and dated availability are not checked."
        )
    return (
        daily,
        BudgetInput(
            items=costs,
            travelers=requirements.travelers,
            limit=requirements.budget_amount,
            budget_scope=requirements.budget_scope,
            limit_currency=requirements.currency,
        ),
        warnings,
    )


def validate_itinerary(itinerary: Itinerary, budget: BudgetSummary) -> list[str]:
    errors = []
    if [day.day_number for day in itinerary.daily_plan] != list(range(1, itinerary.days + 1)):
        errors.append("Itinerary day numbering or duration is inconsistent")
    for day in itinerary.daily_plan:
        subtotal = money(
            sum((Decimal(str(a.estimated_cost)) for a in day.activities), Decimal("0"))
        )
        if subtotal != day.estimated_cost:
            errors.append("Daily cost does not match activities")
    total = money(sum((Decimal(str(d.estimated_cost)) for d in itinerary.daily_plan), Decimal("0")))
    if total != budget.estimated_total_cost or total != itinerary.estimated_total_cost:
        errors.append("Itinerary cost does not match budget calculation")
    return errors
