from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from app.agent.itinerary import Itinerary
from app.agent.requirements import RequirementStatus, TravelRequirements
from app.tools.contracts import BudgetSummary, ToolRequest, ToolResult


class TravelState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    requirements: TravelRequirements
    requirement_status: RequirementStatus
    missing_fields: list[str]
    tool_requests: list[ToolRequest]
    tool_results: list[ToolResult]
    itinerary: Itinerary | None
    budget_summary: BudgetSummary | None
    warnings: list[str]
    errors: list[str]
    clarification_question: str | None
    validation_status: str
