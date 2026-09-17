"""Controlled planner comparison. Network creation is owned by the opt-in CLI only."""

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path
from statistics import mean
from time import perf_counter

from pydantic import BaseModel, ConfigDict, Field

from app.agent.extractor import RuleBasedRequirementsExtractor
from app.agent.graph import build_graph
from app.agent.itinerary import validate_itinerary
from app.agent.planner import TOOL_ALLOWLIST, DeterministicTestPlanner, PlannerError
from app.agent.requirements import TravelRequirements, assess_requirements
from app.agent.semantic_coverage import SemanticCoverageAnalyzer
from app.agent.trace import make_trace
from app.tools.contracts import BudgetRequest, BudgetSummary, ToolStatus
from app.tools.mock import calculate_budget, money

DEFAULT_MAX_CASES = 3
HARD_MAX_CASES = 8


class GoldenCase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    label: str
    query: str
    expected_status: str
    required_tools: list[str]
    optional_tools: list[str]
    forbidden_tools: list[str]
    expected_destination: str
    budget_constraint: dict
    expected_preferences: dict[str, list[str]]
    frozen_requirements: TravelRequirements


class LiveDataset(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    cases: list[GoldenCase] = Field(min_length=1, max_length=HARD_MAX_CASES)


def prepare_cases(path: Path, max_cases: int) -> tuple[LiveDataset, list[GoldenCase]]:
    if not 1 <= max_cases <= HARD_MAX_CASES:
        raise ValueError("max_cases must be between 1 and 8")
    dataset = LiveDataset.model_validate_json(path.read_text("utf-8"))
    if len({case.case_id for case in dataset.cases}) != len(dataset.cases):
        raise ValueError("Duplicate dataset case IDs")
    selected = dataset.cases[:max_cases]
    extractor = RuleBasedRequirementsExtractor()
    for case in selected:
        actual = extractor.extract(case.query)
        if (
            actual.model_dump(exclude={"requirements_v2"})
            != case.frozen_requirements.model_dump(exclude={"requirements_v2"})
            or assess_requirements(actual).status != "SUFFICIENT"
        ):
            raise ValueError("Frozen requirements changed or preflight is insufficient")
        if actual.destination != case.expected_destination:
            raise ValueError("Golden destination disagrees with frozen requirements")
        if any(
            getattr(actual, field) != values for field, values in case.expected_preferences.items()
        ):
            raise ValueError("Golden preferences disagree with frozen requirements")
        if (
            case.budget_constraint.get("amount") != actual.budget_amount
            or case.budget_constraint.get("scope") != actual.budget_scope.value
        ):
            raise ValueError("Golden budget disagrees with frozen requirements")
        capabilities = set(case.required_tools + case.optional_tools)
        if not capabilities <= TOOL_ALLOWLIST or capabilities & set(case.forbidden_tools):
            raise ValueError("Invalid golden tool capabilities")
    return dataset, selected


def provenance(root: Path, dataset_path: Path) -> dict:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    files = list((root / "backend/app").rglob("*.py")) + list(
        (root / "data/travel/us").glob("*.json")
    )
    files += [
        root / "requirements.txt",
        root / "pyproject.toml",
        root / "evals/evaluate_planner_live.py",
    ]
    digest = hashlib.sha256()
    for path in sorted(files):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(path.read_bytes())
    return {
        "git_commit": commit,
        "working_tree_dirty": bool(dirty),
        "code_sha256": digest.hexdigest(),
        "dataset_sha256": hashlib.sha256(dataset_path.read_bytes()).hexdigest(),
        "extractor_type": "rule_based",
        "extractor_git_commit": commit,
        "extractor_sha256": hashlib.sha256(
            (root / "backend/app/agent/requirements.py").read_bytes()
        ).hexdigest(),
    }


class RecordingPlanner:
    def __init__(self, planner, limit):
        if not 1 <= limit <= HARD_MAX_CASES:
            raise ValueError("Invalid planner call limit")
        self.planner, self.limit, self.calls = planner, limit, 0
        self.decision = None
        self.observation = None

    def plan(self, requirements):
        self.decision = None
        self.observation = None
        if self.calls >= self.limit:
            raise PlannerError("evaluation_call_limit")
        self.calls += 1
        try:
            self.decision = self.planner.plan(requirements)
            return self.decision
        finally:
            reader = getattr(self.planner, "get_observation", None)
            if callable(reader):
                self.observation = reader()


def factual_provenance(state) -> bool | None:
    itinerary, budget = state["itinerary"], state["budget_summary"]
    if itinerary is None:
        return None
    req = state["requirements"]
    if (
        budget is None
        or itinerary.destination != req.destination
        or itinerary.days != req.trip_days
        or itinerary.currency != "USD"
        or not validate_itinerary(itinerary, budget, req).is_valid
    ):
        return False
    categories = {
        "attractions": "search_attractions",
        "hotel": "search_hotels",
        "food": "search_restaurants",
        "transport": "search_transport",
    }
    options = {
        result.tool_name: result.data
        for result in state["tool_results"]
        if result.status == ToolStatus.SUCCESS and isinstance(result.data, list)
    }
    multiplier = req.travelers if req.travelers is not None else 1
    for day in itinerary.daily_plan:
        for activity in day.activities:
            candidates = options.get(categories[activity.category], [])

            def matches(row):
                names = (
                    [row.name]
                    if activity.category != "food"
                    else [f"{row.name} ({meal})" for meal in ("breakfast", "lunch", "dinner")]
                )
                return (
                    row.destination == req.destination
                    and row.currency == itinerary.currency
                    and activity.name in names
                    and activity.estimated_cost == money(Decimal(str(row.price)) * multiplier)
                )

            if not any(matches(row) for row in candidates):
                return False
    return True


def budget_integrity(state) -> bool | None:
    budget = state["budget_summary"] or next(
        (
            result.data
            for result in state["tool_results"]
            if result.tool_name == "calculate_budget" and result.status == ToolStatus.SUCCESS
        ),
        None,
    )
    if budget is None:
        return False if state["itinerary"] is not None else None
    requests = [r for r in state["tool_requests"] if isinstance(r, BudgetRequest)]
    results = [r for r in state["tool_results"] if r.tool_name == "calculate_budget"]
    if len(requests) != 1 or requests[0].arguments is None or len(results) != 1:
        return False
    return (
        isinstance(budget, BudgetSummary)
        and results[0].source == "deterministic"
        and results[0] == calculate_budget(requests[0].arguments)
        and budget == results[0].data
    )


def run_case(
    case: GoldenCase,
    recorder: RecordingPlanner,
    *,
    planner_name,
    model,
    prompt_version,
    metadata: dict,
) -> dict:
    started = perf_counter()
    # Both arms receive deep copies of the same rule-extracted, verified snapshot.
    state = build_graph(planner=recorder).invoke(
        {"requirements": case.frozen_requirements.model_copy(deep=True), "messages": []},
        config={"recursion_limit": 16, "callbacks": []},
    )
    trace = make_trace(
        state,
        planner_type=planner_name,
        prompt_version=prompt_version,
        latency_ms=(perf_counter() - started) * 1000,
        semantic_coverage=SemanticCoverageAnalyzer().analyze(
            case.query, case.frozen_requirements
        ),
    )
    observation = recorder.observation
    diagnostics = dict.fromkeys(
        ("invalid_tool", "invalid_arguments", "duplicate_tool"),
        False if recorder.decision is not None else None,
    )
    if observation:
        trace = trace.model_copy(update=observation["metadata"])
        diagnostics = observation["diagnostics"]
    decision = recorder.decision
    selected = [r.tool_name for r in decision.tool_requests] if decision else []
    executed = [r.tool_name for r in state["tool_results"]]
    searches = (
        [r for r in decision.tool_requests if not isinstance(r, BudgetRequest)] if decision else []
    )
    destination_ok = (
        all(r.arguments.destination == case.expected_destination for r in searches)
        if searches
        else None
    )
    req = case.frozen_requirements
    expected_tags = {
        "search_attractions": [x for x in req.interests if x != "food"],
        "search_hotels": req.hotel_preferences,
        "search_restaurants": req.food_preferences,
        "search_transport": req.transport_preferences,
    }
    preferences_ok = (
        all(set(expected_tags[r.tool_name]) <= set(r.arguments.preferences) for r in searches)
        if searches
        else None
    )
    budget_ok = budget_integrity(state)
    facts_ok = factual_provenance(state)
    budget = state["budget_summary"] or next(
        (
            result.data
            for result in state["tool_results"]
            if result.tool_name == "calculate_budget" and result.status == ToolStatus.SUCCESS
        ),
        None,
    )
    budget_golden = (budget.within_budget if budget else None) == case.budget_constraint[
        "within_budget"
    ]
    forbidden = sorted(set(executed) & set(case.forbidden_tools))
    recall = len(set(case.required_tools) & set(executed))
    status_ok = trace.final_status == case.expected_status
    successful = (
        status_ok
        and recall == len(case.required_tools)
        and not forbidden
        and all(value is False for value in diagnostics.values())
        and destination_ok is True
        and preferences_ok is True
        and budget_ok is not False
        and facts_ok is not False
        and budget_golden
        and (trace.final_status != "success" or not state["errors"])
    )
    return {
        "case_id": case.case_id,
        "extractor": "rule_based",
        "planner": planner_name,
        "model": model,
        "prompt_version": prompt_version,
        "provenance": metadata,
        "requirements_sha256": hashlib.sha256(req.model_dump_json().encode()).hexdigest(),
        "expected_tools": {
            "required": case.required_tools,
            "optional": case.optional_tools,
            "forbidden": case.forbidden_tools,
        },
        "selected_tools": selected,
        "executed_tools": executed,
        "invalid_tools": ["<unregistered>"]
        if diagnostics["invalid_tool"]
        else []
        if diagnostics["invalid_tool"] is False
        else None,
        "tool_validation": diagnostics,
        "forbidden_violations": forbidden,
        "required_tool_hits": recall,
        "destination_integrity": destination_ok,
        "preference_integrity": preferences_ok,
        "budget_integrity": budget_ok,
        "factual_provenance": facts_ok,
        "budget_golden_match": budget_golden,
        "final_status": trace.final_status,
        "final_status_correct": status_ok,
        "case_success": bool(successful),
        "latency_ms": trace.latency_ms,
        "trace": trace.model_dump(),
        "error": state["errors"],
    }


def aggregate(records: list[dict]) -> dict:
    def rate(values):
        observed = [value for value in values if value is not None]
        return {
            "value": sum(observed) / len(observed) if observed else None,
            "numerator": sum(observed),
            "denominator": len(observed),
        }

    hits = sum(r["required_tool_hits"] for r in records)
    required = sum(len(r["expected_tools"]["required"]) for r in records)
    metrics = {
        "case_success_rate": rate(r["case_success"] for r in records),
        "required_tool_recall": {
            "value": hits / required if required else None,
            "numerator": hits,
            "denominator": required,
        },
        "forbidden_tool_violation_rate": rate(bool(r["forbidden_violations"]) for r in records),
        "final_status_accuracy": rate(r["final_status_correct"] for r in records),
    }
    for metric, field in (
        ("invalid_tool_rate", "invalid_tool"),
        ("invalid_argument_rate", "invalid_arguments"),
        ("duplicate_tool_rate", "duplicate_tool"),
    ):
        metrics[metric] = rate(r["tool_validation"][field] for r in records)
    for metric, field in (
        ("destination_preservation_rate", "destination_integrity"),
        ("preference_preservation_rate", "preference_integrity"),
        ("budget_integrity_rate", "budget_integrity"),
        ("factual_provenance_rate", "factual_provenance"),
    ):
        metrics[metric] = rate(r[field] for r in records)
    metrics["mean_latency_ms"] = mean(r["latency_ms"] for r in records) if records else None
    return metrics


def run_comparison(
    cases,
    *,
    metadata,
    mode="offline",
    planner_factory=None,
    model=None,
    prompt_version="planner_v1",
) -> dict:
    if mode not in ("offline", "mock", "live") or not 1 <= len(cases) <= HARD_MAX_CASES:
        raise ValueError("Invalid comparison mode or case limit")
    baseline = RecordingPlanner(DeterministicTestPlanner(), len(cases))
    records = [
        run_case(
            case,
            baseline,
            planner_name="deterministic",
            model=None,
            prompt_version=None,
            metadata=metadata,
        )
        for case in cases
    ]
    report = {
        "mode": mode,
        "provenance": metadata,
        "requested_cases": [c.case_id for c in cases],
        "records": records,
        "comparison": {"Deterministic": aggregate(records), "OpenAI": "NOT RUN"},
        "provider_requests": 0,
        "mock_requests": 0,
        "stopped_early": False,
    }
    if mode == "offline" or not all(r["case_success"] for r in records):
        report["stopped_early"] = mode != "offline"
        return report
    if planner_factory is None:
        raise ValueError("Explicit planner factory is required")
    planner = planner_factory()
    recorder = RecordingPlanner(planner, len(cases))
    other = []
    try:
        for case in cases:
            record = run_case(
                case,
                recorder,
                planner_name="openai_mock" if mode == "mock" else "openai",
                model=model,
                prompt_version=prompt_version,
                metadata=metadata,
            )
            other.append(record)
            if not record["case_success"]:
                report["stopped_early"] = True
                break
    finally:
        planner.client.close()
    report["records"].extend(other)
    report["comparison"]["OpenAI MOCK" if mode == "mock" else "OpenAI"] = aggregate(other)
    report["mock_requests" if mode == "mock" else "provider_requests"] = recorder.calls
    return report


def write_report(report: dict, path: Path):
    path.parent.mkdir(exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
