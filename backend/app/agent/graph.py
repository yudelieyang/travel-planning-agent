"""Single planner graph with deterministic preflight, tools and validation."""

from collections.abc import Callable

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph

from app.agent.execution import ExecutionStage, ValidationSummary, is_replan_eligible
from app.agent.itinerary import Itinerary, compose_draft, validate_itinerary
from app.agent.planner import (
    DeterministicTestPlanner,
    PlannerDecision,
    PlannerError,
    PlannerProtocol,
    ReplanContext,
)
from app.agent.requirements import RequirementStatus, assess_requirements
from app.agent.state import TravelState
from app.tools.contracts import BudgetRequest, BudgetSummary, ToolRequest, ToolResult, ToolStatus
from app.tools.mock import calculate_budget, run_tool

ToolRunner = Callable[[ToolRequest], ToolResult]
MAX_REPLAN_ATTEMPTS = 1


def build_graph(planner: PlannerProtocol | None = None, tool_runner: ToolRunner = run_tool):
    planner = planner if planner is not None else DeterministicTestPlanner()

    def preflight(state: TravelState) -> dict:
        assessment = assess_requirements(state["requirements"])
        return {
            "requirement_status": assessment.status,
            "missing_fields": assessment.missing_fields,
            "tool_requests": [],
            "tool_results": [],
            "itinerary": None,
            "budget_summary": None,
            "warnings": [],
            "errors": [],
            "clarification_question": None,
            "validation_status": "not_reached",
            "approved_tool_requests": [],
            "public_validation": ValidationSummary(),
            "replan_attempts": 0,
            "replan_context": None,
            "budget_repair": False,
            "selected_candidate_ids": {},
        }

    def clarification(state: TravelState) -> dict:
        questions = {
            "destination": "Where would you like to travel?",
            "duration": "For how many days, or on which start and end dates?",
        }
        question = " ".join(questions[field] for field in state["missing_fields"])
        return {"clarification_question": question, "messages": [AIMessage(content=question)]}

    def plan(state: TravelState) -> dict:
        try:
            # An untrusted implementation receives a private copy, never graph-owned state.
            snapshot = state["requirements"].model_dump(mode="json")
            supplied = state["requirements"].model_copy(deep=True)
            feedback = state["replan_context"]
            decision = planner.plan(supplied) if feedback is None else planner.plan(supplied, feedback)
            if supplied.model_dump(mode="json") != snapshot:
                return {"errors": ["planner_modified_requirements"]}
            decision = PlannerDecision.model_validate_json(decision.model_dump_json(), strict=True)
            if not decision.can_proceed:
                return {"errors": ["planner_cannot_proceed"], "warnings": decision.warnings}
            if feedback is not None and not decision.budget_repair:
                return {"errors": ["planner_did_not_apply_budget_repair"]}
            for request in decision.tool_requests:
                if not isinstance(request, BudgetRequest) and (
                    request.arguments.destination.casefold()
                    != state["requirements"].destination.casefold()
                ):
                    return {"errors": ["planner_destination_mismatch"]}
                if not isinstance(request, BudgetRequest):
                    expected = {
                        "search_attractions": [
                            x for x in state["requirements"].interests if x != "food"
                        ],
                        "search_hotels": state["requirements"].hotel_preferences,
                        "search_restaurants": state["requirements"].food_preferences,
                        "search_transport": state["requirements"].transport_preferences,
                    }[request.tool_name]
                    if not set(expected).issubset(request.arguments.preferences):
                        return {"errors": ["planner_dropped_preferences"]}
            return {
                "tool_requests": decision.tool_requests,
                "approved_tool_requests": [r.model_copy(deep=True) for r in decision.tool_requests],
                "warnings": decision.warnings,
                "budget_repair": decision.budget_repair,
            }
        except PlannerError as exc:
            suffix = " (retryable; no automatic retry)" if exc.retryable else ""
            return {"errors": [exc.code + suffix]}
        except Exception as exc:
            return {"errors": [f"Planner failed ({type(exc).__name__})"]}

    def tools(state: TravelState) -> dict:
        if state["errors"]:
            return {}
        requests = state["tool_requests"]
        required = {
            "search_attractions",
            "search_hotels",
            "search_restaurants",
            "search_transport",
            "calculate_budget",
        }
        if len(requests) != len(required) or {r.tool_name for r in requests} != required:
            return {"errors": ["Mock slice requires four searches and one budget calculation"]}
        results = []

        def invoke(request: ToolRequest) -> ToolResult:
            try:
                result = tool_runner(request.model_copy(deep=True))
                if not isinstance(result, ToolResult) or result.tool_name != request.tool_name:
                    raise ValueError("Mismatched tool result")
                result = ToolResult.model_validate_json(result.model_dump_json())
                if isinstance(request, BudgetRequest):
                    expected = calculate_budget(request.arguments)
                    if result != expected:
                        raise ValueError("Budget must match the deterministic calculator")
                return result
            except Exception as exc:
                return ToolResult(
                    tool_name=request.tool_name,
                    status=ToolStatus.ERROR,
                    source="mock",
                    error=f"Tool execution failed ({type(exc).__name__})",
                )

        searches = [r for r in requests if not isinstance(r, BudgetRequest)]
        for request in searches:
            results.append(invoke(request))
        errors = (
            ["UNSUPPORTED_CITY_DATA"]
            if any(result.error == "UNSUPPORTED_CITY_DATA" for result in results)
            else [
                f"{result.tool_name}: {result.status.value}"
                for result in results
                if result.status != ToolStatus.SUCCESS
            ]
        )
        if errors:
            return {"tool_results": results, "errors": errors}
        if any(not isinstance(result.data, list) for result in results):
            return {"tool_results": results, "errors": ["Search tools must return option lists"]}
        daily, budget_input, warnings, selected_candidate_ids = compose_draft(
            state["requirements"],
            {r.tool_name: r.data for r in results},
            use_low_cost_options=state["budget_repair"],
        )
        budget_request = BudgetRequest(arguments=budget_input)
        budget_result = invoke(budget_request)
        results.append(budget_result)
        update = {
            "tool_requests": searches + [budget_request],
            "tool_results": results,
            "selected_candidate_ids": selected_candidate_ids,
        }
        if budget_result.status != ToolStatus.SUCCESS or not isinstance(
            budget_result.data, BudgetSummary
        ):
            return {**update, "errors": ["Budget calculation failed"]}
        budget = budget_result.data
        warnings = state["warnings"] + warnings + budget.warnings
        itinerary = Itinerary(
            destination=state["requirements"].destination,
            days=state["requirements"].trip_days,
            daily_plan=daily,
            estimated_total_cost=budget.estimated_total_cost,
            warnings=warnings,
        )
        return {**update, "itinerary": itinerary, "budget_summary": budget, "warnings": warnings}

    def validate(state: TravelState) -> dict:
        if state["errors"]:
            return {
                "validation_status": "failed",
                "public_validation": ValidationSummary(reason="prior_errors"),
            }
        if state["itinerary"] is None or state["budget_summary"] is None:
            return {
                "errors": ["Planning did not produce an itinerary and budget"],
                "validation_status": "failed",
                "public_validation": ValidationSummary(reason="missing_artifacts"),
            }
        result = validate_itinerary(
            state["itinerary"], state["budget_summary"], state["requirements"]
        )
        outcome = "passed" if result.is_valid else "failed"
        return {
            "errors": result.errors,
            "validation_status": outcome,
            "public_validation": ValidationSummary(
                performed=True,
                outcome=outcome,
                reason=None,
                violations=result.violations,
            ),
        }

    def replan(state: TravelState) -> dict:
        attempt = state["replan_attempts"] + 1
        return {
            "errors": [],
            "replan_attempts": attempt,
            "replan_context": ReplanContext(
                violations=[violation.model_copy(deep=True) for violation in state["public_validation"].violations],
                previous_itinerary=state["itinerary"].model_copy(deep=True),
                attempt=attempt,
            ),
            "budget_repair": False,
        }

    def finalize(state: TravelState) -> dict:
        if state["errors"]:
            return {
                "itinerary": None,
                "budget_summary": None,
                "messages": [
                    AIMessage(content="The planner could not produce a validated mock itinerary.")
                ],
            }
        return {
            "messages": [
                AIMessage(content="Offline mock itinerary prepared; review estimate warnings.")
            ]
        }

    def observed(name, node):
        """Record node completion without changing node outputs or routing."""

        def execute(state):
            update = node(state)
            previous = [] if name == "preflight" else state["execution_stages"]
            outcome = "completed"
            if (
                name == "preflight"
                and update["requirement_status"] == RequirementStatus.INSUFFICIENT
            ):
                outcome = "clarification"
            elif name == "tools" and state["errors"]:
                outcome = "skipped"
            elif name == "validation" and update["public_validation"].reason == "prior_errors":
                outcome = "skipped"
            elif name in ("planner", "tools", "validation") and update.get("errors"):
                outcome = "failed"
            return {
                **update,
                "execution_stages": previous
                + [ExecutionStage(name=name, sequence=len(previous) + 1, outcome=outcome)],
            }

        return execute

    graph = StateGraph(TravelState)
    for name, node in [
        ("preflight", preflight),
        ("clarification", clarification),
        ("planner", plan),
        ("tools", tools),
        ("validate", validate),
        ("replan", replan),
        ("finalize", finalize),
    ]:
        public_name = {"validate": "validation", "finalize": "finalization"}.get(name, name)
        graph.add_node(name, observed(public_name, node))
    graph.add_edge(START, "preflight")
    graph.add_conditional_edges(
        "preflight",
        lambda state: state["requirement_status"],
        {RequirementStatus.SUFFICIENT: "planner", RequirementStatus.INSUFFICIENT: "clarification"},
    )
    graph.add_edge("clarification", END)
    graph.add_edge("planner", "tools")
    graph.add_edge("tools", "validate")
    graph.add_conditional_edges(
        "validate",
        lambda state: (
            "replan"
            if state["replan_attempts"] < MAX_REPLAN_ATTEMPTS
            and is_replan_eligible(state["public_validation"], state["errors"])
            else "finalize"
        ),
        {"replan": "replan", "finalize": "finalize"},
    )
    graph.add_edge("replan", "planner")
    graph.add_edge("finalize", END)
    return graph.compile()
