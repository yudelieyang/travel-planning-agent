"""Application boundary: parse input, execute one graph, map structured state."""

from time import perf_counter
from typing import Literal

from langchain_core.messages import HumanMessage
from pydantic import BaseModel, ConfigDict, Field

from app.agent.execution import ExecutionStage, PublicExecutionSummary, project_tools
from app.agent.extractor import RequirementsExtractorProtocol, RuleBasedRequirementsExtractor
from app.agent.graph import ToolRunner, build_graph
from app.agent.itinerary import Itinerary
from app.agent.openai_planner import OpenAIPlanner
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
    execution: PublicExecutionSummary | None = None


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
        state, trace = self.run(query)
        stages = state["execution_stages"]
        visited = {stage.name: stage for stage in stages}
        planner_stage = visited.get("planner")
        mode = (
            "demo"
            if isinstance(self.planner, DeterministicTestPlanner)
            else "live"
            if isinstance(self.planner, OpenAIPlanner)
            else "custom"
        )
        execution = PublicExecutionSummary(
            run_id=trace.run_id,
            mode=mode,
            planner_type=trace.planner_type,
            planner_invoked=planner_stage is not None,
            prompt_version=trace.prompt_version,
            latency_ms=trace.latency_ms,
            requirement_status=state["requirement_status"],
            planner_outcome=(
                "not_invoked"
                if planner_stage is None
                else "accepted"
                if planner_stage.outcome == "completed"
                else "failed"
            ),
            stages=stages
            + [
                ExecutionStage(name=name, outcome="not_reached")
                for name in (
                    "preflight",
                    "clarification",
                    "planner",
                    "tools",
                    "validation",
                    "finalization",
                )
                if name not in visited
            ],
            tools=project_tools(
                state["approved_tool_requests"], state["tool_requests"], state["tool_results"]
            ),
            validation=state["public_validation"],
        )
        return PlanResponse(
            status=final_status(state),
            requirements=state["requirements"],
            itinerary=state["itinerary"],
            budget=state["budget_summary"],
            missing_fields=state["missing_fields"],
            clarification_question=state["clarification_question"],
            warnings=state["warnings"],
            errors=state["errors"],
            execution=execution,
        )
