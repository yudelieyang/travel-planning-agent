"""Small comparative evaluations; no provider response bodies or secrets in records."""

from app.agent.planner import PlannerError, PlannerProtocol
from app.agent.service import TravelService
from app.tools.contracts import ToolResult, ToolStatus
from app.tools.mock import run_tool

SMOKE_CASE_IDS = ("TRAVEL-001", "TRAVEL-002", "TRAVEL-004", "TRAVEL-005")


class LimitedPlanner:
    """One shared budget across cases. The provider adapter itself has zero retries."""

    def __init__(self, planner: PlannerProtocol, max_calls: int = 3):
        self.planner = planner
        self.max_calls = max_calls
        self.calls = 0

    def plan(self, requirements):
        if self.calls >= self.max_calls:
            raise PlannerError("evaluation_call_limit")
        self.calls += 1
        return self.planner.plan(requirements)


def evaluate_case(
    case: dict,
    planner: PlannerProtocol,
    *,
    planner_name: str,
    model: str | None,
    prompt_version: str | None,
) -> dict:
    state, trace = TravelService(planner=planner, tool_runner=scenario_runner(case)).run(
        case["input"]
    )
    requirements = state["requirements"]
    selected = [r.tool_name for r in state["tool_requests"]]
    # Raw invalid provider output is deliberately discarded, so do not invent its tool names.
    validation = "valid" if selected else "not_reached"
    if state["errors"]:
        validation = "valid" if selected else "rejected_or_unavailable"
    budget = state["budget_summary"]
    return {
        "case_id": case["id"],
        "planner": planner_name,
        "model": model,
        "prompt_version": prompt_version,
        "status": state["requirement_status"].value,
        "selected_tools": selected,
        "invalid_tools": None if validation == "rejected_or_unavailable" else [],
        "tool_validation": validation,
        "final_status": trace.final_status,
        "requirements": requirements.model_dump(mode="json"),
        "executed_tools": [r.tool_name for r in state["tool_results"]],
        "warnings": state["warnings"],
        "trace": trace.model_dump(),
        "budget_handling": {
            "amount": requirements.budget_amount,
            "scope": requirements.budget_scope.value,
            "within_budget": budget.within_budget if budget else None,
            "cost_basis": budget.basis if budget else None,
            "estimated_total_cost": budget.estimated_total_cost if budget else None,
            "warnings": budget.warnings if budget else [],
        },
        "latency_ms": trace.latency_ms,
        "error": state["errors"],
    }


def scenario_runner(case: dict):
    """Explicit local fixture fault injection, never a planner-selectable capability."""
    fault = case.get("tool_fault")
    if fault is not None and fault != {"tool_name": "search_hotels", "status": "ERROR"}:
        raise ValueError("Unsupported evaluation fault fixture")

    def execute(request):
        if fault and request.tool_name == fault["tool_name"]:
            return ToolResult(
                tool_name=request.tool_name,
                status=ToolStatus.ERROR,
                source="mock",
                error="Injected offline fixture failure",
            )
        return run_tool(request)

    return execute


def score_records(cases: list[dict], records: list[dict]) -> dict:
    if not cases or len(cases) != len(records):
        raise ValueError("Expected one record per nonempty dataset case")
    totals = {
        "cases_passed": 0,
        "requirement_matches": 0,
        "requirement_checks": 0,
        "required_hits": 0,
        "required_checks": 0,
        "forbidden_violations": 0,
        "final_status_matches": 0,
    }
    checks = []
    for case, record in zip(cases, records, strict=True):
        if case["id"] != record["case_id"]:
            raise ValueError("Case/record order mismatch")
        fields = case["expected_requirement_fields"]
        matched = sum(
            set(record["requirements"].get(k, [])) == set(v)
            if isinstance(v, list)
            else record["requirements"].get(k) == v
            for k, v in fields.items()
        )
        totals["requirement_matches"] += matched
        totals["requirement_checks"] += len(fields)
        called = set(record["executed_tools"])
        required = set(case["required_tools"])
        hits = len(required & called)
        violations = len(set(case["forbidden_tools"]) & called)
        totals["required_hits"] += hits
        totals["required_checks"] += len(required)
        totals["forbidden_violations"] += violations
        status_ok = record["final_status"] == case["expected_api_status"]
        totals["final_status_matches"] += status_ok
        warning_ok = all(
            any(text in warning for warning in record["warnings"])
            for text in case.get("expected_warning", [])
        )
        budget_ok = True
        constraint = case.get("budget_constraint")
        budget = record["budget_handling"]
        if constraint:
            if "within_budget" in constraint:
                budget_ok &= budget["within_budget"] == constraint["within_budget"]
            if "scope" in constraint:
                budget_ok &= budget["scope"] == constraint["scope"]
            if "max_total" in constraint:
                total = budget["estimated_total_cost"]
                budget_ok &= total is not None and (
                    total > constraint["max_total"]
                    if constraint.get("must_exceed")
                    else total <= constraint["max_total"]
                )
        passed = (
            matched == len(fields)
            and hits == len(required)
            and not violations
            and status_ok
            and warning_ok
            and budget_ok
            and record["status"] == case["expected_status"]
        )
        totals["cases_passed"] += passed
        checks.append(
            {
                "case_id": case["id"],
                "passed": bool(passed),
                "requirements": matched == len(fields),
                "tools": hits == len(required) and not violations,
                "warnings": warning_ok,
                "budget": bool(budget_ok),
                "final_status": status_ok,
            }
        )

    def rate(numerator, denominator):
        return numerator / denominator if denominator else 1.0

    return {
        "case_count": len(cases),
        "case_pass_rate": rate(totals["cases_passed"], len(cases)),
        "requirement_accuracy": rate(totals["requirement_matches"], totals["requirement_checks"]),
        "required_tool_hit_rate": rate(totals["required_hits"], totals["required_checks"]),
        "forbidden_tool_violations": totals["forbidden_violations"],
        "final_status_accuracy": rate(totals["final_status_matches"], len(cases)),
        "counts": totals,
        "case_checks": checks,
    }
