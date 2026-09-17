# Travel Planning Agent Scenario Test Expansion

## 1. Repository State

- Branch: `main`
- HEAD: `08d922e06e38cc53d803a056a1d3fab57c495a7`
- Starting working tree: untracked `docs/architecture/` only. It was not changed.
- Production code modified: **NO**.

## 2. Existing Test Baseline

Before this change, `python -m pytest` collected **224** backend tests and passed
all of them. The configured runner is pytest (`pyproject.toml`, test root
`backend/tests`); no project-specific pytest markers are configured. Standard
parameterization and `xfail` are already used.

The baseline includes parser/model unit tests, budget-scope and mock-tool tests,
graph/service/API integration tests, execution-contract tests, deterministic
evaluation tests, and mocked OpenAI-planner/harness tests. The frontend has a
separate Node test suite using static fixture responses. Its five presets cover
Boston, NYC, clarification, tight budget, and Atlantis.

The default backend suite is offline: the deterministic planner and local JSON
data are used, and agent tests install a socket guard that fails any Internet
attempt. The live planner evaluator has an explicit `--live` gate and was not
run. There is no live pytest marker.

## 3. Test Coverage Audit

| Area | Existing coverage | Expansion |
|---|---|---|
| Requirements | Rule parser, dates, party counts, ambiguity, known evaluator cases | Semantic fixture, specific preference/objective gaps, noisy and conflicting input |
| Planner | Tool contract, mutation defenses, deterministic planner | Requirement-to-tool preservation and attraction-only scope gap |
| Tools | Mock filtering, tool contracts, full graph failures | Exception versus `NO_RESULTS` partial-data behavior |
| Budget | Scope and basic comparison | Exact ceiling boundaries, zero budget, traveler scaling, hotel-night convention |
| Validator | Structural itinerary/cost consistency | Direct over-budget semantic-validation gap |
| Clarification | Required destination/duration and no tool calls | Targeted single-field clarification cases |
| Recovery | Planner/tool failures safely terminate | Explicit xfail for absent validation-to-replan loop |
| End-to-end | Deterministic happy, Atlantis, API and frontend presets | Recruiter-quality happy fixture and repeated-run semantic contract |

Existing tests already use meaningful assertions for many contracts, but they did
not make the distinction between generic and specific preferences, optimization
goals, semantic budget enforcement, or recovery/multi-turn capabilities visible
as first-class scenarios.

## 4. New Scenario Matrix

| Scenario | Layer | Current result | Status |
|---|---|---|---|
| Happy path | End-to-end | Full itinerary, five tools, budget and validation | PASS |
| Specific preferences | Requirements | `fried chicken` is lost | XFAIL |
| Hard vs. soft budget | Requirements | `around` is marked approximate; no typed constraint role | PASS (partial) |
| Optimization objective | Requirements/planner | No objective field | XFAIL |
| Missing information | API/graph | Targeted destination/duration clarification | PASS |
| Conflicting luxury/low-budget input | End-to-end | Best-effort itinerary plus over-budget warning | PASS |
| Budget boundaries | Budget unit | Decimal ceiling, near-ceiling and zero cases | PASS |
| Traveler count | End-to-end | Group total doubles; per-traveler total stays stable | PASS |
| Duration/hotel nights | End-to-end | `days - 1` lodging-night convention | PASS |
| Food restrictions | Requirements | Vocabulary supports vegetarian; halal is unsupported | XFAIL (partial) |
| Transport preference | Requirements | Walking/transit parse; plural rental-car avoidance is missed | XFAIL (partial) |
| Geographic feasibility | Validation | No distance or travel-time model | XFAIL |
| Tool exception | Graph/service | Error, skipped budget, no fabricated itinerary | PASS |
| Partial data | Graph/service | `NO_RESULTS` differs from exception and still errors | PASS |
| Unsupported destination | End-to-end | No-results state; no fabricated plan | PASS |
| Semantic validation failure | Validator | Over-budget is not a validator failure | XFAIL |
| Validation to replan | Graph | No retry/replan edge | XFAIL |
| Multi-turn modification | Service | Stateless single-request service | XFAIL |
| Parser robustness | Requirements | Casual `max 1k` / `just me` form is unsupported | XFAIL |
| Noisy input | Requirements | Mid-sentence shorthand destination is unreliable | XFAIL |
| Contradictory input | Requirements | First budget match wins; precedence undefined | XFAIL |
| Invalid numerical input | Requirements | Typed invalid values reject; `budget abc` is silently absent | PASS / XFAIL |
| Tool selection | Planner | Only full-trip mode exists | XFAIL |
| Determinism | End-to-end | Stable domain and execution contract | PASS |
| Recruiter golden case | Fixture/requirements | Core fields parse; specific food/objective remain gaps | XFAIL (partial) |

## 5. Tests Added

- `backend/tests/agent/test_scenario_semantics.py` — 35 offline scenario tests.
- `evals/datasets/scenario_semantics_v1.json` — one passing happy-path fixture and
  one recruiter-quality semantic-golden fixture.
- This report.

The focused suite result was **22 passed, 13 xfailed, 0 failed, 0 skipped, 0
xpassed**. Each xfail is `strict=False` and documents an observable capability
gap rather than weakening an assertion.

## 6. Semantic Gaps Discovered

- The limited vocabulary does not preserve `fried chicken`; it also does not
  retain a `city walking` activity concept independently of transport walking.
- There is no optimization-objective field or objective-aware planner behavior.
- Soft budgets are only an `approximate budget` text constraint; constraints do
  not have a typed hard/soft semantic role and an over-budget total still returns
  a successful best-effort itinerary.
- `validate_itinerary` verifies structural cost consistency but deliberately does
  not reject a budget-ceiling breach.
- There is no validation-to-replan/retry edge or multi-turn itinerary state.
- A failed or empty required search is safely surfaced but aborts the itinerary;
  there is no recovery or partial-plan policy.
- Geographic feasibility, dietary restrictions outside the tiny fixture vocabulary,
  attraction-only requests, several casual/noisy forms, and conflicting-input
  precedence are not implemented.

## 7. Regression Results

Baseline before changes:

```text
python -m pytest
224 passed, 1 warning
```

Focused scenario command:

```text
python -m pytest backend/tests/agent/test_scenario_semantics.py -ra
22 passed, 13 xfailed
```

Full backend regression after the additions:

```text
python -m pytest -ra
246 passed, 13 xfailed, 1 warning
```

The pre-existing backend count increased from 224 to 259 collected cases; none
of the original cases regressed. The separate frontend verification also passed:

```text
npm.cmd test              41 passed
npm.cmd run typecheck     passed
npm.cmd run build         passed
```

## 8. Capability Matrix

| Capability | Supported | Tested | Notes |
|---|---:|---:|---|
| Destination/duration extraction | Yes | Yes | Bounded English grammar only |
| Budget comparison | Yes | Yes | Scope and traveler count affect comparability |
| Budget semantic enforcement | No | Yes | Best-effort success can be over budget |
| Specific food preference | Partial | Yes | Controlled vocabulary only |
| Optimization objective | No | Yes | XFAIL |
| Clarification | Yes | Yes | Destination and duration only required fields |
| Tool failure safety | Yes | Yes | Fails safely; no recovery |
| Geographic feasibility | No | Yes | XFAIL |
| Automatic replan | No | Yes | XFAIL |
| Multi-turn revision | No | Yes | XFAIL |

## 9. Recommended Next Test Priorities

1. Add fixtures for explicit hard-budget semantics versus best-effort behavior
   before any policy is changed.
2. Define a parser capability dataset for specific preferences, conflicts, and
   compact travel phrasing; keep unsupported entries as measured gaps.
3. Add controlled recovery-policy tests only after a product decision defines
   whether partial itineraries, clarification, or replan are expected.
4. If geographic data is introduced later, add itinerary distance/time invariants
   before enabling geographic claims in the demo.
