"""Allowlisted execution metadata, separate from the user-facing response."""

from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

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


def final_status(state: TravelState) -> str:
    if state["errors"]:
        return "error"
    if state["requirement_status"] == "INSUFFICIENT":
        return "needs_clarification"
    return "success"


def make_trace(
    state: TravelState, *, planner_type: str, prompt_version: str | None, latency_ms: float
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
    )
