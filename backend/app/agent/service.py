"""Application boundary: parse input, execute one graph, map structured state."""

from typing import Literal

from langchain_core.messages import HumanMessage
from pydantic import BaseModel, ConfigDict, Field

from app.agent.graph import ToolRunner, build_graph
from app.agent.itinerary import Itinerary
from app.agent.planner import PlannerProtocol
from app.agent.requirements import RequirementStatus, TravelRequirements, parse_requirements
from app.tools.contracts import BudgetSummary
from app.tools.mock import run_tool


class PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    query: str = Field(min_length=1, max_length=2000)


class PlanResponse(BaseModel):
    status: Literal["success", "needs_clarification", "error"]
    requirements: TravelRequirements
    itinerary: Itinerary | None = None
    budget: BudgetSummary | None = None
    missing_fields: list[str] = Field(default_factory=list)
    clarification_question: str | None = None
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class TravelService:
    def __init__(self, planner: PlannerProtocol | None = None, tool_runner: ToolRunner = run_tool):
        self.graph = build_graph(planner, tool_runner)

    def plan(self, query: str) -> PlanResponse:
        query = PlanRequest(query=query).query
        requirements = parse_requirements(query)
        state = self.graph.invoke(
            {"requirements": requirements, "messages": [HumanMessage(content=query)]},
            config={"recursion_limit": 16, "callbacks": []},
        )
        if state["requirement_status"] == RequirementStatus.INSUFFICIENT:
            status = "needs_clarification"
        else:
            status = "error" if state["errors"] else "success"
        return PlanResponse(
            status=status,
            requirements=requirements,
            itinerary=state["itinerary"],
            budget=state["budget_summary"],
            missing_fields=state["missing_fields"],
            clarification_question=state["clarification_question"],
            warnings=state["warnings"],
            errors=state["errors"],
        )
