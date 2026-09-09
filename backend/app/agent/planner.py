"""One replaceable planner boundary. The current implementation is NOT an AI model."""

from typing import Protocol

from app.agent.requirements import TravelRequirements
from app.tools.contracts import BudgetRequest, SearchInput, SearchRequest, ToolRequest


class PlannerProtocol(Protocol):
    def plan(self, requirements: TravelRequirements) -> list[ToolRequest]: ...


class DeterministicTestPlanner:
    def plan(self, requirements: TravelRequirements) -> list[ToolRequest]:
        if not requirements.destination or requirements.trip_days is None:
            raise ValueError("Preflight must succeed before planning")
        preferences = {
            "search_attractions": [x for x in requirements.interests if x != "food"],
            "search_hotels": requirements.hotel_preferences,
            "search_restaurants": requirements.food_preferences,
            "search_transport": requirements.transport_preferences,
        }
        return [
            SearchRequest(
                tool_name=name,
                arguments=SearchInput(
                    destination=requirements.destination,
                    preferences=tags,
                ),
            )
            for name, tags in preferences.items()
        ] + [BudgetRequest()]
