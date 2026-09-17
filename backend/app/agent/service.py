"""Application boundary: parse input, execute one graph, map structured state."""

from time import perf_counter
from typing import Literal

from langchain_core.messages import HumanMessage
from pydantic import BaseModel, ConfigDict, Field

from app.agent.execution import (
    ExecutionStage,
    PublicExecutionSummary,
    RepairChange,
    RepairSummary,
    SemanticExecutionSummary,
    project_candidate_groups,
    project_tools,
)
from app.agent.extractor import RequirementsExtractorProtocol, RuleBasedRequirementsExtractor
from app.agent.graph import ToolRunner, build_graph
from app.agent.itinerary import Itinerary
from app.agent.openai_planner import OpenAIPlanner
from app.agent.planner import DeterministicTestPlanner, PlannerProtocol
from app.agent.requirements import TravelRequirements
from app.agent.semantic_coverage import SemanticCoverageAnalyzer
from app.agent.semantic_extractor import (
    OpenAISemanticExtractor,
    SemanticExtractionError,
    SemanticExtractionResult,
)
from app.agent.semantic_merge import merge_requirements
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
        semantic_extractor: OpenAISemanticExtractor | None = None,
        semantic_augmentation_enabled: bool = False,
    ):
        self.planner = planner if planner is not None else DeterministicTestPlanner()
        self.extractor = extractor if extractor is not None else RuleBasedRequirementsExtractor()
        self.coverage_analyzer = SemanticCoverageAnalyzer()
        self.semantic_extractor = semantic_extractor
        self.semantic_augmentation_enabled = semantic_augmentation_enabled
        self.graph = build_graph(self.planner, tool_runner)

    def run(self, query: str):
        """Internal execution boundary for evaluation; trace is never part of PlanResponse."""
        started = perf_counter()
        query = PlanRequest(query=query).query
        requirements = self.extractor.extract(query)
        requirements = TravelRequirements.model_validate_json(requirements.model_dump_json())
        coverage = self.coverage_analyzer.analyze(query, requirements)
        llm_invoked = False
        llm_status = "not_requested"
        proposal: SemanticExtractionResult | None = None
        llm_error_code = None
        merge_attempted = False
        merge_decisions = []
        merge_conflicts = []
        final_requirements_source: Literal["deterministic", "hybrid"] = "deterministic"
        requires_clarification = False
        if coverage.needs_llm and self.semantic_augmentation_enabled:
            if self.semantic_extractor is None:
                llm_status = "unavailable"
            else:
                llm_invoked = True
                try:
                    proposal = self.semantic_extractor.extract(query)
                    llm_status = "proposed"
                except SemanticExtractionError as exc:
                    llm_status = "failed"
                    llm_error_code = exc.code
        if proposal is not None:
            merge_attempted = True
            try:
                merge_result = merge_requirements(requirements, proposal, query, coverage.reasons)
                changed = merge_result.requirements.model_dump(mode="json") != requirements.model_dump(mode="json")
                requirements = merge_result.requirements
                merge_decisions = merge_result.decisions
                merge_conflicts = merge_result.conflicts
                requires_clarification = merge_result.requires_clarification
                final_requirements_source = "hybrid" if changed else "deterministic"
            except Exception:
                llm_error_code = "merge_failed"
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
            semantic_coverage=coverage,
            llm_invoked=llm_invoked,
            llm_extraction_status=llm_status,
            llm_semantic_proposal=proposal,
            llm_error_code=llm_error_code,
            semantic_merge_attempted=merge_attempted,
            semantic_merge_decisions=merge_decisions,
            semantic_merge_conflicts=merge_conflicts,
            final_requirements_source=final_requirements_source,
            requires_clarification=requires_clarification,
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
        extractor_model = getattr(self.semantic_extractor, "model", None)
        extractor_prompt_version = getattr(self.semantic_extractor, "prompt_version", None)
        semantic = SemanticExecutionSummary(
            mode="hybrid" if self.semantic_augmentation_enabled else "deterministic",
            coverage_triggered=trace.semantic_coverage.needs_llm,
            coverage_reasons=[reason.value for reason in trace.semantic_coverage.reasons],
            llm_invoked=trace.llm_invoked,
            extraction_status=trace.llm_extraction_status,
            final_source=trace.final_requirements_source,
            requires_clarification=trace.requires_clarification,
            extractor_model=extractor_model if isinstance(extractor_model, str) else None,
            extractor_prompt_version=(
                extractor_prompt_version if isinstance(extractor_prompt_version, str) else None
            ),
        )
        repair = None
        replan_context = state.get("replan_context")
        if replan_context is not None:
            final_budget = state.get("budget_summary")
            if final_budget is None:
                final_budget = next(
                    (
                        result.data
                        for result in reversed(state["tool_results"])
                        if isinstance(result.data, BudgetSummary)
                    ),
                    None,
                )
            previous_by_category: dict = {}
            for day in replan_context.previous_itinerary.daily_plan:
                for activity in day.activities:
                    previous_by_category.setdefault(activity.category, [])
                    if activity.name not in previous_by_category[activity.category]:
                        previous_by_category[activity.category].append(activity.name)
            final_by_category: dict = {}
            if state.get("itinerary") is not None:
                for day in state["itinerary"].daily_plan:
                    for activity in day.activities:
                        final_by_category.setdefault(activity.category, [])
                        if activity.name not in final_by_category[activity.category]:
                            final_by_category[activity.category].append(activity.name)
            changes = [
                RepairChange(
                    category=category,
                    before=before,
                    after=final_by_category.get(category, []),
                )
                for category, before in previous_by_category.items()
                if final_by_category.get(category, []) != before
            ]
            final_total = final_budget.estimated_total_cost if final_budget is not None else None
            initial_total = replan_context.previous_itinerary.estimated_total_cost
            repair = RepairSummary(
                attempt=replan_context.attempt,
                trigger=replan_context.violations,
                initial_total=initial_total,
                final_total=final_total,
                savings=(
                    max(round(initial_total - final_total, 2), 0)
                    if final_total is not None
                    else None
                ),
                final_outcome=(
                    "passed" if state["public_validation"].outcome == "passed" else "failed"
                ),
                changes=changes,
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
                    "replan",
                    "finalization",
                )
                if name not in visited
            ],
            tools=project_tools(
                state["approved_tool_requests"], state["tool_requests"], state["tool_results"]
            ),
            validation=state["public_validation"],
            replan_attempts=state["replan_attempts"],
            semantic=semantic,
            repair=repair,
            candidate_groups=project_candidate_groups(
                state["tool_results"], state["selected_candidate_ids"]
            ),
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
