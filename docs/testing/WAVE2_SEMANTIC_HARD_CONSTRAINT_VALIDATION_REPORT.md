# Wave 2 — Semantic Hard-Constraint Validation

## 1. Objective

Wave 2 adds deterministic semantic validation for an explicit hard budget. It detects and reports a violation; it does not repair an itinerary, replan, retry, or change tool behavior.

## 2. Repository Baseline

| Item | Before Wave 2 |
|---|---|
| Branch | `main` |
| HEAD | `08d922ed06e38cc53d803a056a1d3fab57c495a7` |
| Working tree | Wave 1 tracked edits plus prior untracked scenario/audit/documentation files were present; they were preserved |
| Relevant baseline | 113 passed, 5 xfailed, 0 failed |
| Wave 1 full backend baseline | 262 passed, 5 xfailed, 0 failed |

All validation and tests in this wave use local deterministic fixtures only. No provider or travel API was called.

## 3. Remaining XFAIL Inventory

| Test | Capability family | Wave 2 result |
|---|---|---|
| `test_rejects_geographically_impossible_daily_schedule` | Geographic feasibility | Later wave; remains XFAIL |
| `test_validator_rejects_over_budget_plan_directly` | Semantic hard-budget validation | Converted to PASS as `test_validator_rejects_hard_budget_violation_directly` |
| `test_validation_failure_triggers_a_second_planner_attempt` | Replan/retry | Later wave; remains XFAIL |
| `test_multiturn_revision_preserves_unchanged_days` | Durable multi-turn revision | Deferred; remains XFAIL |
| `test_attraction_only_request_selects_no_unneeded_trip_tools` | Tool-selection mode | Deferred; remains XFAIL |

## 4. Current Validator Audit

Before this wave, `validate_itinerary` verified day numbering, daily activity arithmetic, and agreement among itinerary and budget totals. The calculator already derived `within_budget`, `comparison_cost`, and `remaining_budget` with the existing Decimal two-decimal convention, but the validator did not consume those fields or the Wave 1 constraint strength. An over-budget hard request therefore passed validation.

## 5. Root Cause

The calculation layer was correct: it could deterministically compute that a comparable USD budget was exceeded. The missing layer was semantic policy: no rule converted `HARD` + `within_budget=false` into validation failure. This wave connects the existing typed requirement and calculated comparison without rewriting arithmetic.

## 6. Validation Contract

| Requirement semantics | Deterministic outcome |
|---|---|
| `HARD` budget, comparable cost above limit | Validation fails with `HARD_BUDGET_EXCEEDED` |
| `HARD` budget, cost at or below limit | Validation passes |
| `SOFT` budget overage | Does not hard-fail validation |
| `UNSPECIFIED` strength / legacy request | Does not acquire a new hard failure |
| `maximize_budget_utilization` objective | Not evaluated and never creates a failure |

The validator requires an actual comparison (`within_budget is False` and `comparison_cost` available), so ambiguous scope/currency cases remain non-failing rather than being guessed.

## 7. Production Changes

| File | Change | Reason |
|---|---|---|
| `backend/app/agent/execution.py` | Added typed violation code/model and public validation `violations` list | Stable serializable business-failure contract |
| `backend/app/agent/itinerary.py` | Added `ItineraryValidationResult` and hard-budget rule using existing money rounding | Keep structural and semantic validation deterministic |
| `backend/app/agent/graph.py` | Projects validation result into state errors and public summary | Expose normal validation failure without an exception or new edge |
| `backend/app/agent/evaluation.py` and `live_evaluation.py` | Read an already-executed budget tool result when finalization clears failed response artifacts | Preserve offline evaluation observability |
| `frontend/src/types/travel.ts` | Added additive violation response types | Keep frontend contract typed; no UI behavior changed |
| `docs/phase-a-execution.md` | Updated validation contract documentation | Prevent stale success-on-hard-overage guidance |

The planner, budget calculator, tool implementations, API route, and graph topology were not changed.

## 8. Structured Violation Model

`ValidationSummary.violations` is an additive list of `ValidationViolation` values. The current model contains:

```text
code: HARD_BUDGET_EXCEEDED
category: budget
expected: budget limit
actual: comparable computed cost
excess: actual - expected
message: human-readable explanation
```

For a performed semantic failure, the public summary is `performed=true`, `outcome=failed`, `reason=null`, and contains the violation. This is distinct from prior execution errors, which retain `reason=prior_errors` and no fabricated violation. The top-level response remains the existing terminal `error` status and does not produce a replacement itinerary.

## 9. Hard Budget Behavior

The existing `money()` Decimal two-decimal convention is used before comparison context is emitted.

| Cost vs. hard limit | Result |
|---|---|
| Below (`799.99` vs. `800`) | PASS |
| Equal (`800` vs. `800`) | PASS |
| Above (`800.01` vs. `800`) | FAIL with `HARD_BUDGET_EXCEEDED` and excess `0.01` |

## 10. Soft Budget Behavior

`SOFT` retains the Wave 1 interpretation of an approximate preference. An overage has no hard semantic violation and no validator failure solely for that reason. No generic preference validator was introduced.

## 11. Objective Behavior

`maximize_budget_utilization` remains represented in requirements only. Wave 2 adds no score, threshold, plan mutation, or failure for under-utilization.

## 12. Backward Compatibility

`budget_constraint_strength` defaults to `UNSPECIFIED`. Direct legacy callers may still call `validate_itinerary(itinerary, budget)` without requirements; they receive structural validation only. Existing typed API fields remain additive. No unspecified budget is silently promoted to `HARD`.

## 13. Tests Added / Changed

| File | Coverage |
|---|---|
| `backend/tests/agent/test_semantic_validation.py` | Below/equal/above boundaries, typed serialization, soft, objective, and legacy strength behavior |
| `backend/tests/agent/test_scenario_semantics.py` | Genuine XFAIL conversion and terminal hard-budget scenario behavior |
| `backend/tests/agent/test_public_execution.py` | Public violation serialization and semantic business failure versus prior error behavior |
| `backend/tests/agent/test_graph.py` | New validation result contract |
| Evaluation/API/invariant/live-harness tests and datasets | Expected hard-overage terminal status while retaining calculator observability |

The targeted acceptance suite passed: **71 passed, 4 xfailed**.

## 14. XFAIL Conversion

| Metric | Result |
|---|---:|
| Before | 5 xfailed |
| Converted to PASS | 1 |
| After | 4 xfailed |
| XPASS | 0 |

The converted test now asserts the typed failure context instead of lowering or skipping its assertion. Replan remains separately XFAIL.

## 15. Regression Results

```text
Backend:   269 passed, 4 xfailed, 0 failed
Frontend:  41 passed
Typecheck: passed
Build:     passed
Ruff:      passed
```

The backend run reports one pre-existing Starlette/AnyIO deprecation warning. The frontend commands were run from `frontend/`, the directory containing its `package.json`.

## 16. Scope Compliance

| Boundary | Changed? |
|---|---:|
| Planner strategy modified | NO |
| Graph topology modified | NO |
| Replan implemented | NO |
| Tool recovery implemented | NO |
| Geographic logic implemented | NO |
| Multi-turn implemented | NO |
| Optimization execution implemented | NO |
| Live/network validation added | NO |

## 17. Wave 3 Readiness

The validation output supplies a stable code, category, expected limit, actual comparable cost, and excess. That is sufficient input for a future validation-feedback-to-replan contract. Wave 2 intentionally provides no retry counter, replan prompt, conditional graph edge, or repair method.

## 18. Remaining Capability Gaps

- No constrained replan after `HARD_BUDGET_EXCEEDED`.
- No geographic/time-feasibility validation.
- No tool fallback or partial-plan recovery.
- No durable multi-turn itinerary revision.
- No attraction-only tool-selection mode.
- Preference fulfillment and objective quality are not evaluated.
