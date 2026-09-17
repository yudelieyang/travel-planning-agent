"""Small public projection of a completed run, not the internal evaluation trace."""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.agent.requirements import RequirementStatus
from app.tools.contracts import (
    BudgetInput,
    BudgetSummary,
    Category,
    SearchInput,
    SearchToolName,
    ToolRequest,
    ToolResult,
    TravelOption,
)

StageName = Literal[
    "preflight",
    "clarification",
    "planner",
    "tools",
    "validation",
    "replan",
    "finalization",
]
StageOutcome = Literal["completed", "failed", "skipped", "not_reached", "clarification"]
PlannerOutcome = Literal["not_invoked", "accepted", "failed"]


class PublicModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class ExecutionStage(PublicModel):
    name: StageName
    # One-based node-entry order; null means the node was never reached.
    sequence: int | None = Field(default=None, ge=1)
    outcome: StageOutcome


class ViolationCode(StrEnum):
    HARD_BUDGET_EXCEEDED = "HARD_BUDGET_EXCEEDED"
    HOTEL_BUDGET_EXCEEDED = "HOTEL_BUDGET_EXCEEDED"


class ValidationViolation(PublicModel):
    code: ViolationCode
    category: Literal["budget"]
    expected: float = Field(ge=0)
    actual: float = Field(ge=0)
    excess: float = Field(gt=0)
    message: str


class ValidationSummary(PublicModel):
    performed: bool = False
    outcome: Literal["passed", "failed", "not_performed"] = "not_performed"
    reason: Literal["not_reached", "prior_errors", "missing_artifacts"] | None = "not_reached"
    violations: list[ValidationViolation] = Field(default_factory=list)


class SemanticExecutionSummary(PublicModel):
    """Safe, read-only projection of the already-completed semantic path."""

    mode: Literal["deterministic", "hybrid"]
    coverage_triggered: bool
    coverage_reasons: list[str] = Field(default_factory=list)
    llm_invoked: bool
    extraction_status: Literal["not_requested", "proposed", "unavailable", "failed"]
    final_source: Literal["deterministic", "hybrid"]
    requires_clarification: bool
    extractor_model: str | None = None
    extractor_prompt_version: str | None = None


class RepairChange(PublicModel):
    category: Category
    before: list[str]
    after: list[str]


class RepairSummary(PublicModel):
    """One bounded repair attempt, projected from retained graph state."""

    attempt: int = Field(ge=1, le=1)
    maximum_attempts: int = Field(default=1, ge=1, le=1)
    trigger: list[ValidationViolation]
    initial_total: float = Field(ge=0)
    final_total: float | None = Field(default=None, ge=0)
    savings: float | None = Field(default=None, ge=0)
    final_outcome: Literal["passed", "failed"]
    changes: list[RepairChange] = Field(default_factory=list)


def is_replan_eligible(validation: ValidationSummary, errors: list[str]) -> bool:
    """Only a pure, typed semantic hard-budget failure can enter repair."""
    return (
        validation.performed
        and validation.outcome == "failed"
        and bool(validation.violations)
        and all(
            violation.code
            in {ViolationCode.HARD_BUDGET_EXCEEDED, ViolationCode.HOTEL_BUDGET_EXCEEDED}
            for violation in validation.violations
        )
        and errors == [violation.message for violation in validation.violations]
    )


class PublicToolRecord(PublicModel):
    tool_name: SearchToolName | Literal["calculate_budget"]
    selected: bool = True
    executed: bool
    execution_order: int | None = Field(default=None, ge=1)
    requested_arguments: SearchInput | BudgetInput | None
    runtime_arguments: SearchInput | BudgetInput | None
    status: Literal["SUCCESS", "NO_RESULTS", "ERROR", "SKIPPED"]
    data: list[TravelOption] | BudgetSummary | None = None
    source: Literal["mock", "snapshot", "deterministic"] | None = None
    error_code: Literal["tool_execution_failed", "UNSUPPORTED_CITY_DATA"] | None = None


class CandidateGroup(PublicModel):
    category: Category
    selected: list[TravelOption]
    alternatives: list[TravelOption]


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
    replan_attempts: int = Field(default=0, ge=0, le=1)
    semantic: SemanticExecutionSummary
    repair: RepairSummary | None = None
    candidate_groups: list[CandidateGroup] = Field(default_factory=list)


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
                    if result is not None and result.source in ("mock", "snapshot", "deterministic")
                    else None
                ),
                error_code=(
                    "UNSUPPORTED_CITY_DATA"
                    if result is not None and result.error == "UNSUPPORTED_CITY_DATA"
                    else "tool_execution_failed"
                    if result is not None and result.status == "ERROR"
                    else None
                ),
            )
        )
    return records


def project_candidate_groups(
    results: list[ToolResult], selected_ids: dict[Category, list[str]]
) -> list[CandidateGroup]:
    """Allowlisted final candidate view with explicit selection semantics."""
    groups = []
    for result in results:
        if not isinstance(result.data, list) or not result.data:
            continue
        options = [row for row in result.data if isinstance(row, TravelOption)]
        if not options:
            continue
        category = options[0].category
        if category is None:
            continue
        chosen = set(selected_ids.get(category, []))
        groups.append(
            CandidateGroup(
                category=category,
                selected=[row for row in options if row.id in chosen],
                alternatives=[row for row in options if row.id not in chosen],
            )
        )
    return groups
