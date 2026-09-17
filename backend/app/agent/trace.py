"""Allowlisted execution metadata, separate from the user-facing response."""

from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.agent.semantic_coverage import SemanticCoverageResult
from app.agent.semantic_extractor import SemanticExtractionResult
from app.agent.semantic_merge import MergeConflict, MergeDecision
from app.agent.state import TravelState


class ExecutionTrace(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str = Field(default_factory=lambda: uuid4().hex)
    planner_type: str
    prompt_version: str | None
    requirement_status: str
    selected_tools: list[str]
    tool_statuses: list[dict[str, str]]
    validation_status: Literal["passed", "failed", "not_reached"]
    final_status: Literal["success", "error", "needs_clarification"]
    latency_ms: float
    model: str | None = None
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    api_latency_ms: float | None = Field(default=None, ge=0)
    api_error_type: str | None = None
    semantic_coverage: SemanticCoverageResult
    llm_invoked: bool = False
    llm_extraction_status: Literal["not_requested", "proposed", "unavailable", "failed"] = "not_requested"
    llm_semantic_proposal: SemanticExtractionResult | None = None
    llm_error_code: str | None = None
    semantic_merge_attempted: bool = False
    semantic_merge_decisions: list[MergeDecision] = Field(default_factory=list)
    semantic_merge_conflicts: list[MergeConflict] = Field(default_factory=list)
    final_requirements_source: Literal["deterministic", "hybrid"] = "deterministic"
    requires_clarification: bool = False


def final_status(state: TravelState) -> str:
    if state["errors"]:
        return "error"
    if state["requirement_status"] == "INSUFFICIENT":
        return "needs_clarification"
    return "success"


def make_trace(
    state: TravelState,
    *,
    planner_type: str,
    prompt_version: str | None,
    latency_ms: float,
    semantic_coverage: SemanticCoverageResult,
    llm_invoked: bool = False,
    llm_extraction_status: Literal["not_requested", "proposed", "unavailable", "failed"] = "not_requested",
    llm_semantic_proposal: SemanticExtractionResult | None = None,
    llm_error_code: str | None = None,
    semantic_merge_attempted: bool = False,
    semantic_merge_decisions: list[MergeDecision] | None = None,
    semantic_merge_conflicts: list[MergeConflict] | None = None,
    final_requirements_source: Literal["deterministic", "hybrid"] = "deterministic",
    requires_clarification: bool = False,
) -> ExecutionTrace:
    status = final_status(state)
    return ExecutionTrace(
        planner_type=planner_type,
        prompt_version=prompt_version,
        requirement_status=state["requirement_status"].value,
        selected_tools=[r.tool_name for r in state["tool_requests"]],
        tool_statuses=[
            {"tool": r.tool_name, "status": r.status.value} for r in state["tool_results"]
        ],
        validation_status=state.get("validation_status", "not_reached"),
        final_status=status,
        latency_ms=round(latency_ms, 2),
        semantic_coverage=semantic_coverage,
        llm_invoked=llm_invoked,
        llm_extraction_status=llm_extraction_status,
        llm_semantic_proposal=llm_semantic_proposal,
        llm_error_code=llm_error_code,
        semantic_merge_attempted=semantic_merge_attempted,
        semantic_merge_decisions=semantic_merge_decisions or [],
        semantic_merge_conflicts=semantic_merge_conflicts or [],
        final_requirements_source=final_requirements_source,
        requires_clarification=requires_clarification,
    )
