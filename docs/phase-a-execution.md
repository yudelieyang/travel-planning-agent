# Public execution contract — Phase A

`POST /api/v1/travel/plan` still accepts only `{"query": "..."}`. All existing
response fields and domain status semantics are preserved. Two additive changes:

- `execution: PublicExecutionSummary | null` (populated for completed service runs).
- `budget.comparison_cost` and `budget.remaining_budget`, nullable numbers.

The Pydantic contract is defined in `backend/app/agent/execution.py`. FastAPI's
OpenAPI response schema includes these models. Existing HTTP 422 and 503 responses
are unchanged and do not contain an execution summary.

## Completed-request semantics

This is a synchronous snapshot, not streaming or live stage progress.

`stages` lists reached nodes in execution order, followed by unvisited nodes.
`sequence` is one-based node-entry order; null identifies `not_reached` nodes.
All seven semantic stages are represented: preflight, clarification, planner, tools,
validation, replan, finalization. `skipped` with a sequence means the node was reached but
its work was bypassed because of prior errors. It is distinct from `not_reached`.

- Success: preflight, planner, tools, validation, finalization complete;
  clarification is not reached.
- Missing requirements: preflight reports `clarification`; clarification completes;
  planner, tools, validation, finalization are not reached.
- Planner failure: planner is failed; tools and validation are skipped;
  finalization completes. No rejected raw decision or tool arguments are exposed.
- Search failure: tools fails; selected budget calculation is skipped; validation
  is skipped; finalization completes even though the domain response is an error.
- A typed hard-budget failure can enter one `replan` stage, then planner, tools,
  and validation run once more. It either passes with the repaired itinerary or
  terminates after the second validation.

`planner_outcome` is `not_invoked`, `accepted`, or `failed`. The last includes blocked,
rejected, and exceptional planner outcomes. Existing response errors retain their
existing classifications. No planner rationale or hidden reasoning is added.

## Tools

`tools` retains the order of graph-approved planner selections. Each selected tool
has `selected=true`. `execution_order` is the actual one-based invocation order,
or null for skipped tools. The graph always executes searches before the calculator,
even if a planner listed the calculator first.

- `requested_arguments`: a copy of the approved planner arguments. The calculator
  has null here because the planner is forbidden to supply budget inputs.
- `runtime_arguments`: the inputs passed to the runner, or null when not executed.
  An executed calculator exposes its resolved typed costs and comparison inputs.
- `status`: SUCCESS, NO_RESULTS, ERROR, or SKIPPED. A skipped tool is not executed.
- `data`: existing typed travel options or budget summary, without a raw tool object.
- `source`: only mock/deterministic sources are public; other strings become null.
- `error_code`: tool_execution_failed for ERROR, otherwise null. Arbitrary result
  error text and metadata are not copied into this public contract.

Options remain small local fixture lists. Data and arguments are structured; no
provider response bodies, messages, prompts, settings, or clients are serialized.
Existing domain fields (including validated warnings) remain unchanged.

## Validation and internal trace

`validation.performed` means `validate_itinerary` actually ran. Its outcome is
passed, failed, or not_performed. A non-performed check has reason not_reached,
prior_errors, or missing_artifacts. Performed checks have reason null.
`violations` is an additive structured list. A deterministic hard-budget failure
uses `HARD_BUDGET_EXCEEDED` with its budget limit, comparison cost, and excess;
soft budgets and optimization objectives do not fail validation.

The old internal `ExecutionTrace.validation_status` remains unchanged: it records
failed for earlier execution errors. The public summary makes the additional
distinction that consistency checks did not run. Finalization completion is not
a claim that the itinerary succeeded. The top-level `status` remains authoritative.

Internal evaluation traces remain separate and are not serialized. The service
reuses their run ID, planner identity, prompt version, and total latency instead
of generating conflicting metadata. No per-stage timings or persistence are added.

## Mode

Mode comes from the instantiated planner: demo for DeterministicTestPlanner, live
for OpenAIPlanner, custom for other injected protocol implementations. The ordinary
configured API factory uses demo/live. `planner_type` identifies the implementation.
`prompt_version` is null when unavailable. A live-configured clarification response
still has `planner_invoked=false`: no provider call occurred. Live mode still uses
mock travel data and deterministic itinerary composition.

## Budget

The calculator computes the new fields using its existing Decimal arithmetic and
two-decimal money convention, without changing totals, warnings, or within_budget.

| Comparison | comparison_cost | remaining_budget |
|---|---|---|
| USD TOTAL_TRIP with a supplied limit and traveler count | Group cost | Limit minus group cost |
| USD PER_PERSON with a supplied limit | Per-traveler cost | Limit minus per-traveler cost |
| Unknown scope, missing limit, incompatible currency, or TOTAL_TRIP without travelers | null | null |

In the final row within_budget remains null. Negative remaining_budget is valid.
When the parsed budget strength is HARD and the comparison is deterministically
over budget, validation fails with `HARD_BUDGET_EXCEEDED`. The graph may make one
bounded repair using least-cost matching fixture options, then validates again;
an unspecified or SOFT strength remains compatible with the existing non-failing
behavior. `execution.replan_attempts` records zero or one attempts.

## Verified presets

- `Plan a 2-day trip to Boston for 1 traveler under $500 total.` — success,
  comparison 223, remaining 277, within_budget true.
- `Plan a trip for me.` — needs_clarification; no planner or tool execution.
- `Plan a 2-day trip to Atlantis.` — error; four NO_RESULTS searches, calculator skipped.
- `Plan a 2-day trip to Boston for 2 travelers under $50 total.` — error,
  one repair attempt produces comparison 392, then validation remains
  `HARD_BUDGET_EXCEEDED`.

No frontend, planner selector, new endpoint, storage, or external call is added.
