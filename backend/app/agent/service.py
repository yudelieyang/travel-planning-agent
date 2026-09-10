"""Application boundary: parse input, execute one graph, map structured state."""

from time import perf_counter
from typing import Literal

from langchain_core.messages import HumanMessage
from pydantic import BaseModel, ConfigDict, Field

from app.agent.extractor import RequirementsExtractorProtocol, RuleBasedRequirementsExtractor
from app.agent.graph import ToolRunner, build_graph
from app.agent.itinerary import Itinerary
from app.agent.planner import DeterministicTestPlanner, PlannerProtocol
from app.agent.requirements import TravelRequirements
from app.agent.trace import final_status, make_trace
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
    def __init__(
        self,
        planner: PlannerProtocol | None = None,
        tool_runner: ToolRunner = run_tool,
        extractor: RequirementsExtractorProtocol | None = None,
    ):
        self.planner = planner if planner is not None else DeterministicTestPlanner()
        self.extractor = extractor if extractor is not None else RuleBasedRequirementsExtractor()
        self.graph = build_graph(self.planner, tool_runner)

    def run(self, query: str):
        """Internal execution boundary for evaluation; trace is never part of PlanResponse."""
        started = perf_counter()
        query = PlanRequest(query=query).query
        requirements = self.extractor.extract(query)
        requirements = TravelRequirements.model_validate_json(requirements.model_dump_json())
        state = self.graph.invoke(
            {"requirements": requirements, "messages": [HumanMessage(content=query)]},
            config={"recursion_limit": 16, "callbacks": []},
        )
        prompt_version = getattr(self.planner, "prompt_version", None)
        trace = make_trace(
            state,
            planner_type=type(self.planner).__name__,
            prompt_version=prompt_version if isinstance(prompt_version, str) else None,
            latency_ms=(perf_counter() - started) * 1000,
        )
        return state, trace

    def plan(self, query: str) -> PlanResponse:
        state, _trace = self.run(query)
        return PlanResponse(
            status=final_status(state),
            requirements=state["requirements"],
            itinerary=state["itinerary"],
            budget=state["budget_summary"],
            missing_fields=state["missing_fields"],
            clarification_question=state["clarification_question"],
            warnings=state["warnings"],
            errors=state["errors"],
        )
