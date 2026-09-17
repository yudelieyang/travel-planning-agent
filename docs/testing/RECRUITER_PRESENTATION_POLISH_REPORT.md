# Recruiter Presentation Polish Report

## 1. Problems

- **Max price ambiguity:** Search tool cards displayed `Max price: Not supplied` even when the user provided a total trip budget, making an intentionally unset category ceiling look like lost budget data.
- **Demo scenario ambiguity:** Shortcut cards led with destination names, making five capability demonstrations look like the product's supported-destination menu.

## 2. Root Causes

`max_price` comes from each search tool's requested/runtime arguments and represents an optional tool-specific hard price ceiling. It is neither the overall budget nor a planner-created category allocation. The deterministic planner does not invent per-category ceilings, so the value is normally null and the generic money formatter rendered it as `Not supplied`.

The overall budget is already available to the frontend in `PlanResponse.requirements`. The preset panel is also entirely frontend-defined: clicking a card copies that preset's natural-language query into the normal request input; it does not select a destination through a separate backend path.

## 3. Changes

- Renamed `Max price` to `Search price ceiling` and render a missing ceiling as `Not set`.
- Added a compact explanation that overall budget enforcement happens during itinerary budgeting and validation, while candidate prices are compared during planning.
- Reused the existing requirements payload to show a known overall trip budget once above the tool cards. No amount is shown when no budget was supplied.
- Reframed the shortcut area as `Try a demo scenario`, described the cards as optional behavior demos, and made capability names the primary card text.
- Kept Boston, New York City, clarification, and tight-budget queries functionally unchanged.
- Replaced the fictional Atlantis shortcut with Nashville, Tennessee, a real U.S. city outside the current 12-city controlled fixture.

## 4. Explicit Non-Changes

- No category budget allocation or derived tool ceiling.
- No backend production changes.
- No planner, validator, graph, replan, candidate ranking, or retrieval changes.
- No API or shared schema changes.
- No new route, modal, workflow, or interaction model.

## 5. Tests

Frontend presentation coverage verifies the unset and set search-ceiling states, known and absent overall budgets, retained candidate prices, capability-first scenario copy, exact preset queries, Nashville replacement, and absence of Atlantis from the preset data. Existing component and composable tests continue to cover selection, keyboard-native button semantics, custom requests, and response presentation.

## 6. Regression Results

- Frontend tests: **PASS — 46 passed, 0 failed**.
- Typecheck: **PASS — `vue-tsc --noEmit`**.
- Production build: **PASS — Vite transformed 47 modules and produced the production bundle**.
- Candidate-data regression: **PASS — 27 passed**, including NYC + unmatched `fried chicken` fallback and the Nashville unsupported-city contract.

## 7. Remaining Limitations

The overall budget remains itinerary-level and is not pre-allocated across hotel, food, attraction, or transport searches. Candidate prices and all travel results remain deterministic controlled-demo data rather than live quotes.
