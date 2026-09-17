from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from app.agent.execution import ExecutionStage, ValidationSummary
from app.agent.itinerary import Itinerary
from app.agent.planner import ReplanContext
from app.agent.requirements import RequirementStatus, TravelRequirements
from app.tools.contracts import BudgetSummary, Category, ToolRequest, ToolResult


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
    execution_stages: list[ExecutionStage]
    approved_tool_requests: list[ToolRequest]
    public_validation: ValidationSummary
    replan_attempts: int
    replan_context: ReplanContext | None
    budget_repair: bool
    selected_candidate_ids: dict[Category, list[str]]
