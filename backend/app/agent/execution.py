"""Small public projection of a completed run, not the internal evaluation trace."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.agent.requirements import RequirementStatus
from app.tools.contracts import (
    BudgetInput,
    BudgetSummary,
    SearchInput,
    SearchToolName,
    ToolRequest,
    ToolResult,
    TravelOption,
)

StageName = Literal["preflight", "clarification", "planner", "tools", "validation", "finalization"]
StageOutcome = Literal["completed", "failed", "skipped", "not_reached", "clarification"]
PlannerOutcome = Literal["not_invoked", "accepted", "failed"]


class PublicModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class ExecutionStage(PublicModel):
    name: StageName
    # One-based node-entry order; null means the node was never reached.
    sequence: int | None = Field(default=None, ge=1)
    outcome: StageOutcome


class ValidationSummary(PublicModel):
    performed: bool = False
    outcome: Literal["passed", "failed", "not_performed"] = "not_performed"
    reason: Literal["not_reached", "prior_errors", "missing_artifacts"] | None = "not_reached"


class PublicToolRecord(PublicModel):
    tool_name: SearchToolName | Literal["calculate_budget"]
    selected: bool = True
    executed: bool
    execution_order: int | None = Field(default=None, ge=1)
    requested_arguments: SearchInput | BudgetInput | None
    runtime_arguments: SearchInput | BudgetInput | None
    status: Literal["SUCCESS", "NO_RESULTS", "ERROR", "SKIPPED"]
    data: list[TravelOption] | BudgetSummary | None = None
    source: Literal["mock", "deterministic"] | None = None
    error_code: Literal["tool_execution_failed"] | None = None


class PublicExecutionSummary(PublicModel):
    run_id: str
    # Injected protocol implementations must not be mislabeled as demo or live.
    mode: Literal["demo", "live", "custom"]
    planner_type: str
    planner_invoked: bool
    prompt_version: str | None
    latency_ms: float = Field(ge=0)
    requirement_status: RequirementStatus
    planner_outcome: PlannerOutcome
    stages: list[ExecutionStage]
    tools: list[PublicToolRecord]
    validation: ValidationSummary


def project_tools(
    requested: list[ToolRequest], runtime: list[ToolRequest], results: list[ToolResult]
) -> list[PublicToolRecord]:
    """Explicit allowlist: never serialize ToolResult.error or arbitrary metadata."""
    inputs = {request.tool_name: request.arguments for request in runtime}
    outputs = {result.tool_name: (i, result) for i, result in enumerate(results, 1)}
    records = []
    for request in requested:
        observed = outputs.get(request.tool_name)
        order, result = observed if observed else (None, None)
        records.append(
            PublicToolRecord(
                tool_name=request.tool_name,
                executed=result is not None,
                execution_order=order,
                requested_arguments=request.arguments,
                runtime_arguments=inputs[request.tool_name] if result is not None else None,
                status=result.status.value if result is not None else "SKIPPED",
                data=result.data if result is not None else None,
                source=(
                    result.source
                    if result is not None and result.source in ("mock", "deterministic")
                    else None
                ),
                error_code=(
                    "tool_execution_failed"
                    if result is not None and result.status == "ERROR"
                    else None
                ),
            )
        )
    return records
