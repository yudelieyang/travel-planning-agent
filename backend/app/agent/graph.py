"""Single planner graph with deterministic preflight, tools and validation."""

from collections.abc import Callable

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph

from app.agent.itinerary import Itinerary, compose_draft, validate_itinerary
from app.agent.planner import DeterministicTestPlanner, PlannerProtocol
from app.agent.requirements import RequirementStatus, assess_requirements
from app.agent.state import TravelState
from app.tools.contracts import BudgetRequest, BudgetSummary, ToolRequest, ToolResult, ToolStatus
from app.tools.mock import run_tool

ToolRunner = Callable[[ToolRequest], ToolResult]


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
            return {"tool_requests": planner.plan(state["requirements"])}
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
                result = tool_runner(request)
                if not isinstance(result, ToolResult) or result.tool_name != request.tool_name:
                    raise ValueError("Mismatched tool result")
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
        errors = [
            f"{r.tool_name}: {r.status.value}" for r in results if r.status != ToolStatus.SUCCESS
        ]
        if errors:
            return {"tool_results": results, "errors": errors}
        if any(not isinstance(result.data, list) for result in results):
            return {"tool_results": results, "errors": ["Search tools must return option lists"]}
        daily, budget_input, warnings = compose_draft(
            state["requirements"],
            {r.tool_name: r.data for r in results},
        )
        budget_request = BudgetRequest(arguments=budget_input)
        budget_result = invoke(budget_request)
        results.append(budget_result)
        update = {"tool_requests": searches + [budget_request], "tool_results": results}
        if budget_result.status != ToolStatus.SUCCESS or not isinstance(
            budget_result.data, BudgetSummary
        ):
            return {**update, "errors": ["Budget calculation failed"]}
        budget = budget_result.data
        warnings.extend(budget.warnings)
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
            return {}
        if state["itinerary"] is None or state["budget_summary"] is None:
            return {"errors": ["Planning did not produce an itinerary and budget"]}
        return {"errors": validate_itinerary(state["itinerary"], state["budget_summary"])}

    def finalize(state: TravelState) -> dict:
        if state["errors"]:
            return {
                "itinerary": None,
                "budget_summary": None,
                "messages": [
                    AIMessage(content="The offline mock planner could not produce a plan.")
                ],
            }
        return {
            "messages": [
                AIMessage(content="Offline mock itinerary prepared; review estimate warnings.")
            ]
        }

    graph = StateGraph(TravelState)
    for name, node in [
        ("preflight", preflight),
        ("clarification", clarification),
        ("planner", plan),
        ("tools", tools),
        ("validate", validate),
        ("finalize", finalize),
    ]:
        graph.add_node(name, node)
    graph.add_edge(START, "preflight")
    graph.add_conditional_edges(
        "preflight",
        lambda state: state["requirement_status"],
        {RequirementStatus.SUFFICIENT: "planner", RequirementStatus.INSUFFICIENT: "clarification"},
    )
    graph.add_edge("clarification", END)
    graph.add_edge("planner", "tools")
    graph.add_edge("tools", "validate")
    graph.add_edge("validate", "finalize")
    graph.add_edge("finalize", END)
    return graph.compile()
