"""Deterministic mock itinerary composition and structural validation."""

from decimal import Decimal

from pydantic import BaseModel, Field

from app.agent.execution import ValidationViolation, ViolationCode
from app.agent.requirements import ConstraintScope, TravelRequirements
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


class ItineraryValidationResult(BaseModel):
    errors: list[str] = Field(default_factory=list)
    violations: list[ValidationViolation] = Field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


def compose_draft(
    requirements: TravelRequirements,
    options: dict[str, list[TravelOption]],
    *,
    use_low_cost_options: bool = False,
) -> tuple[list[DayPlan], BudgetInput, list[str], dict[Category, list[str]]]:
    days = requirements.trip_days
    if days is None:
        raise ValueError("Duration is required")
    multiplier = requirements.travelers if requirements.travelers is not None else 1
    daily = []
    costs = []
    selected_ids: dict[Category, list[str]] = {
        "attractions": [],
        "hotel": [],
        "food": [],
        "transport": [],
    }
    for number in range(1, days + 1):
        attraction = select_option(options["search_attractions"], number, use_low_cost_options)
        restaurant = select_option(options["search_restaurants"], number, use_low_cost_options)
        selected = [(attraction, "attractions", attraction.name)]
        selected += [
            (restaurant, "food", f"{restaurant.name} ({meal})")
            for meal in ("breakfast", "lunch", "dinner")
        ]
        transport = select_option(options["search_transport"], 1, use_low_cost_options)
        selected.append((transport, "transport", transport.name))
        if number < days:
            hotel = select_option(options["search_hotels"], 1, use_low_cost_options)
            selected.append((hotel, "hotel", hotel.name))
        activities = []
        for option, category, name in selected:
            if option.id not in selected_ids[category]:
                selected_ids[category].append(option.id)
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
    if use_low_cost_options:
        warnings.append("Budget repair selected the least-cost matching options for each day.")
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
        selected_ids,
    )


def select_option(options: list[TravelOption], day: int, use_low_cost_options: bool) -> TravelOption:
    return min(options, key=lambda option: (option.price, option.id)) if use_low_cost_options else options[(day - 1) % len(options)]


def validate_itinerary(
    itinerary: Itinerary,
    budget: BudgetSummary,
    requirements: TravelRequirements | None = None,
) -> ItineraryValidationResult:
    errors = []
    violations = []
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
    if requirements is not None and budget.basis == "group":
        for constraint in requirements.requirements_v2.constraints:
            if constraint.currency != budget.currency:
                continue
            actual_value, code, message = {
                ConstraintScope.TOTAL_TRIP: (
                    budget.estimated_total_cost,
                    ViolationCode.HARD_BUDGET_EXCEEDED,
                    "Hard budget exceeded",
                ),
                ConstraintScope.HOTEL_TOTAL: (
                    budget.breakdown["hotel"],
                    ViolationCode.HOTEL_BUDGET_EXCEEDED,
                    "Hotel budget exceeded",
                ),
            }[constraint.scope]
            actual = money(Decimal(str(actual_value)))
            expected = money(Decimal(str(constraint.value)))
            excess = money(Decimal(str(actual)) - Decimal(str(expected)))
            if excess > 0:
                errors.append(message)
                violations.append(
                    ValidationViolation(
                        code=code,
                        category="budget",
                        expected=expected,
                        actual=actual,
                        excess=excess,
                        message=message,
                    )
                )
    return ItineraryValidationResult(errors=errors, violations=violations)
