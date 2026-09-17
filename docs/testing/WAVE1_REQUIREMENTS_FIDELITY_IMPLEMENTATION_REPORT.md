# Wave 1 — Requirements Fidelity & Constraint Semantics

## 1. Objective

Wave 1 implements only the semantic foundation: user language is preserved as typed requirements. It does not change plan selection, budget validation policy, graph topology, retry/replan, tool recovery, geography, multi-turn state, or the frontend experience.

## 2. Repository Baseline

| Item | Before Wave 1 |
|---|---|
| Branch | `main` |
| HEAD | `08d922ed06e38cc53d803a056a1d3fab57c495a7` |
| Working tree | Prior untracked scenario/audit/docs files were present |
| Relevant offline tests | 92 passed, 13 xfailed |
| Full backend suite | 246 passed, 13 xfailed |

No live provider, travel, maps, or other network API was called.

## 3. Wave 1 XFAIL Inventory

| Test | Root cause | Result |
|---|---|---|
| `test_preserves_specific_food_preference_in_recruiter_golden_case` | Fixed parser vocabulary dropped a specific food phrase | PASS |
| `test_preserves_budget_utilization_objective_in_recruiter_golden_case` | Requirements schema had no objective field | PASS |
| `test_invalid_textual_budget_is_not_silently_dropped` | Malformed optional budget was ignored | PASS, now invalid at the API boundary |
| `test_transport_preferences_and_rental_car_avoidance_are_preserved_for_planner` | Singular-only rental-car negation pattern | PASS |
| `test_preserves_halal_restriction_as_a_food_requirement` | Specific dietary phrase had no preservation path | PASS |
| `test_parser_accepts_equivalent_casual_trip_request` | `just me` and `max 1k` were outside bounded grammar | PASS |
| `test_parser_ignores_irrelevant_context_and_extracts_trip_fields` | Mid-sentence `<duration> <Destination> trip` had no bounded pattern | PASS |
| `test_later_budget_constraint_overrides_earlier_statement` | Parser stopped at the first budget match | PASS |

These eight conversions are genuine assertions without their former `xfail` markers. The malformed-budget assertion was corrected to the existing API contract: parser `ValueError` maps to HTTP 422, rather than creating a new clarification flow for an otherwise optional field.

## 4. Root Causes

`TravelRequirements`, `TravelState`, and the planner copy/serialization boundary already retain populated requirement fields. The original loss occurred in `parse_requirements`, which only emitted a tiny fixed preference vocabulary. The mock restaurant fixture may still have no matching result for a newly preserved preference; Wave 1 intentionally preserves meaning without inventing data or adding a fallback strategy.

Budget arithmetic was already correct. The missing layer was representation: `budget_amount` and an untyped string constraint could not distinguish a hard limit, a soft approximation, a correction, or an optimization objective.

## 5. Production Changes

| File | Change | Why |
|---|---|---|
| `backend/app/agent/requirements.py` | Added typed preference, constraint-strength, and objective models; extended bounded parsing and normalization | Preserve user meaning in the existing requirements object without changing downstream control flow |

No state, planner, graph, validator, tool, API-route, frontend, retry, or replan module was modified. `TravelState` already carries `TravelRequirements`, and the service's JSON validation preserves the additive fields automatically.

## 6. Schema / Contract Changes

Before:

```text
budget_amount, budget_scope, interests, food_preferences,
hotel_preferences, transport_preferences, constraints: list[str]
```

Backward-compatible additions:

```text
budget_constraint_strength: UNSPECIFIED | HARD | SOFT
objective: null | maximize_budget_utilization
specific_preferences: [{ category, value }]
```

All old fields retain their names and behavior. New fields have safe defaults, are Pydantic typed and JSON serializable, and therefore appear additively in the API/OpenAPI requirements model. Existing static frontend responses remain valid; the frontend was intentionally not changed to render the new metadata in Wave 1.

## 7. Preference Preservation

The parser now captures concise preference clauses (`I like`, `I enjoy`, `I prefer`, `I love`, `I need`) into typed `specific_preferences`. It keeps the normal category fields for existing tool routing:

```text
I enjoy city walking and fried chicken
  -> interests: [city walking, food]
  -> food_preferences: [fried chicken]
  -> specific_preferences:
       [{ACTIVITY, city walking}, {FOOD, fried chicken}]
```

Values are normalized for whitespace/case rather than storing duplicate full prompts. Generic already-supported terms remain in their existing fields instead of becoming redundant specifics. Food category detection uses bounded semantic cues (for example `fried …` and `… food`) rather than a growing list of dishes.

## 8. Constraint Semantics

- `under`, `up to`, `max`, `maximum`, `at most`, and `don't spend more than` create `HARD` budget strength.
- `around` creates `SOFT` strength and preserves the pre-existing `approximate budget` compatibility string.
- “Spend as much … budget as reasonably possible” creates `maximize_budget_utilization`.

This is representation only. The deterministic planner does not optimize the objective, and the validator does not change pass/fail behavior for an over-budget hard constraint.

## 9. Conflict Precedence

The deterministic rule is **the last recognized explicit budget statement wins**. For example, `$1,000. Actually, don't spend more than $700.` produces 700. The parser collects recognized monetary matches before selecting the last one; it does not use minimum, maximum, or nondeterministic selection.

## 10. Invalid Input Behavior

| Input | Behavior |
|---|---|
| Negative budget | Rejected by existing Pydantic `ge=0` requirements validation |
| Zero budget | Valid explicit limit; budget calculator may report over budget |
| `budget abc` | Parser raises `ValueError`; existing FastAPI route maps it to HTTP 422 |
| No budget stated | Remains valid; budget is optional and no amount is invented |

No new clarification branch was introduced.

## 11. Tests Changed / Added

| File | Coverage |
|---|---|
| `backend/tests/agent/test_scenario_semantics.py` | Removed markers only for the eight genuinely implemented Wave 1 cases; malformed budget now asserts the actual invalid-input contract |
| `backend/tests/agent/test_requirements.py` | Specific preference category/value, JSON round-trip, limit phrasing variants, hard/soft strength, objective representation |
| `backend/tests/agent/test_requirements_hardening.py` | API-level malformed-budget HTTP 422 contract |
| `evals/datasets/planner_live_smoke_v1.json` | Added default/new semantic requirement fields to frozen offline snapshots; hard limits are labelled HARD |

## 12. XFAIL Conversion

| Metric | Result |
|---|---:|
| Before | 13 xfailed |
| Converted to PASS | 8 |
| Remaining | 5 xfailed |
| XPASS | 0 |

Remaining xfails are deliberately outside Wave 1: geographic feasibility, semantic hard-budget enforcement, validation-to-replan, multi-turn revision, and attraction-only tool selection.

## 13. Full Regression

```text
Relevant parser/scenario suite: 108 passed, 5 xfailed
Backend:                       262 passed, 5 xfailed, 0 failed
Frontend:                      41 passed
Typecheck:                     passed
Build:                         passed
Ruff:                          passed
```

The only backend warning is the existing Starlette/AnyIO deprecation warning.

## 14. Scope Compliance

| Boundary | Changed? |
|---|---:|
| Validator semantics | NO |
| Replan implemented | NO |
| Tool recovery implemented | NO |
| Geographic logic modified | NO |
| Multi-turn implemented | NO |
| Planner strategy modified | NO |
| Graph control flow modified | NO |

## 15. Remaining Gaps

- A hard budget is represented but not semantically enforced by validation.
- No typed validation feedback or bounded repair/replan loop exists.
- A required tool failure/no-results still ends the full-trip run; there is no partial-result or fallback policy.
- Geography/time feasibility and durable conversation state remain absent.
- The parser remains deliberately bounded English grammar, not general NLU.
- Newly preserved specific preferences can still produce `NO_RESULTS` when the controlled mock fixture lacks corresponding tags; Wave 1 does not invent data.

## 16. Recommended Wave 2 Entry Conditions

The architecture is ready to begin **Semantic Hard-Budget Validation** once the team chooses a product policy for hard-limit violation: terminal error, clarification, or successful-but-explicitly-best-effort response. Wave 2 should then consume `budget_constraint_strength`, `budget_amount`, `budget_scope`, and calculator output to return stable structured violation reasons. It should not add replan until that policy and feedback contract are tested.
