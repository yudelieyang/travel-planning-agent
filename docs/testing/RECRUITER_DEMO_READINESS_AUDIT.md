# Recruiter Demo Readiness Audit

## 1. Executive Summary

**Verdict: NOT READY.** The controlled demo has credible backend capabilities—typed requirement semantics, deterministic hard-budget validation, one bounded repair attempt, candidate preservation, and safe terminal failure—but the current recruiter-facing page does not communicate those capabilities reliably enough for an unscripted 2–5 minute demo.

The decisive blocker is natural-language destination reliability. Two ordinary requests for supported cities were parsed as `spend three days in Seattle` and `keep the trip`, then reported as `UNSUPPORTED_CITY_DATA`. Four of eleven formal unfamiliar inputs ended unexpectedly. The strongest agent behavior did work: two Austin hard-budget requests produced an initial USD 394 plan, one repair, a USD 317 plan, and a passing second validation. However, the UI retained only the final cost and final candidates. It did not show the first cost, `HARD_BUDGET_EXCEEDED`, USD 44 excess, structured feedback, or before/after candidate changes.

The page is strongest at candidate metadata and data provenance. It is weakest at selection reasons, hard/soft semantics, validation detail, replan proof, failure wording, and information hierarchy. The weighted recruiter demo readiness score is **2.60 / 5.0**.

## 2. Repository / Runtime State

| Item | Observed state |
|---|---|
| Branch | `main` |
| HEAD | `08d922ed06e38cc53d803a056a1d3fab57c495a7` |
| Working tree | Dirty before this audit with known Wave 1–3, candidate-data, frontend, tests, evals, and documentation work; preserved without reset, restore, stash, clean, checkout, or commit |
| Backend | Current worktree started with `.venv` and deterministic planner on `http://127.0.0.1:8000`; `/health` returned `{"status":"ok","service":"travel-agent-backend"}` |
| Frontend | Current project Vite instance at `http://127.0.0.1:5173`; HTTP 200 |
| Browser console | No warnings or errors after the formal scenario run |
| Data mode | `demo`; deterministic planner; controlled mock travel data; no live availability |
| Docker | `docker compose ps` could not access the local Docker configuration/pipe. This did not block the running application path used by the demo. |
| Regression evidence | Latest pre-audit report: backend 313 passed / 3 expected xfailed; frontend 43 passed; typecheck, build, and Ruff passed. The suites were not used as a substitute for this browser audit. |
| Live APIs | None used |

Both requested ports were initially occupied. Read-only process inspection identified the frontend as this repository's Vite process and the backend as a Travel Agent uvicorn process. A direct current-source parser comparison proved that the backend process had stale loaded code. Only that confirmed stale backend PID was stopped; the current worktree backend was then started, health-checked, and all formal scenarios were rerun. Results produced by the stale process were excluded.

This audit adds only this report. Browser screenshots were captured and inspected inline through the available computer-use interface (happy/replan/failure/soft-budget states), but that interface did not return a repository filesystem path, so no screenshot files were persisted.

## 3. Audit Method

The audit used the actual local Vue page and submitted each request through its textarea and **Plan Trip** button. Eleven unfamiliar formal scenarios were run in the browser across Chicago, Seattle, Miami, Austin, Denver, Los Angeles, and Paris. Two current-runtime no-budget calibration calls established the pre-repair Austin and Denver costs without changing fixtures. Local API responses were then inspected only as supplemental evidence for fields the UI omitted, including `budget_constraint_strength`, `specific_preferences`, `replan_attempts`, and validation violations.

Functional correctness and recruiter understandability were scored separately. A safe `NO_RESULTS` response can therefore be functionally controlled while still being a poor recruiter demo outcome. Presets and existing golden sentences were not used as the main sample. No production code, tests, fixtures, or UI were changed.

**Browser-level audit: YES.** Formal scenario count: **11**. Outcome count: **4 success, 1 clarification, 2 expected terminal failures, 4 unexpected terminal failures**.

## 4. Scenario Matrix

| ID | Exact-input shorthand | City / parsed destination | Capability | Final status | Replan | Functional result | Recruiter clarity |
|---|---|---|---|---|---:|---|---|
| A | `Could you plan two days in Chicago... museums and pizza.` | Chicago | Happy path + preferences | Success | No | PARTIAL | PARTIAL |
| B | `I want to spend three days in Seattle... coffee... outdoor activities.` | `spend three days in Seattle` | Natural preference language | Error, unexpected | No | FAIL | FAIL |
| C | `Plan a 3-day Miami trip... keep the trip around $900...` | `keep the trip` | Soft budget + preferences | Error, unexpected | No | FAIL | FAIL |
| D | `...Austin... My total budget is $350.` | Austin | Hard budget, successful repair | Success | Yes | PASS | PARTIAL |
| E | `...Denver... My total budget is $40.` | Denver | Hard budget, unrecoverable repair | Error, expected | Yes | PASS | PARTIAL |
| F | `I want a relaxing trip with good food in Denver.` | Denver | Missing duration | Needs clarification | No | PASS | PASS |
| G | `...Los Angeles... outdoor attractions and Asian food.` | Los Angeles | Candidate diversity + strict preference | Error, unexpected | No | PARTIAL | PARTIAL |
| H | `...three-day getaway to Paris...` | Paris | Unsupported scope | Error, expected | No | PASS | PARTIAL |
| I | `...Austin... Do not spend more than $350 total.` | Austin | Hard-budget wording robustness | Success | Yes | PASS | PARTIAL |
| J | `...Seattle... coffee... parks.` | Seattle | Connector extraction + matched data | Error, unexpected | No | PARTIAL | PARTIAL |
| K | `...Miami... budget is around $900 total... seafood.` | Miami | Soft over-budget success | Success | No | PASS | PARTIAL |

`PASS` means the current bounded contract behaved correctly. `PARTIAL` means the run was safe but lost a requested preference, lacked controlled data, or did not explain the behavior adequately. `FAIL` means ordinary language corrupted a core requirement and caused the wrong outcome.

## 5. Scenario Findings

### A — Chicago happy path

- **Exact user input:** `Could you plan two days in Chicago for just me? I enjoy museums and pizza.`
- **Destination / capability:** Chicago; simple planning, traveler extraction, preferences, candidates, itinerary.
- **Extracted requirements:** destination Chicago, 2 days, 1 traveler, museums; no budget. Backend also preserved `pizza` as an `UNSPECIFIED` specific preference, but the requirements UI did not show it and restaurant search received no food preference.
- **Planner / tools:** deterministic planner accepted; attraction/hotel/restaurant/transport/budget tools all succeeded with result counts 2/3/3/3.
- **Selected candidates:** Mock City History Center, Mock Lakeside Art Hall, Mock Loop Budget Lodge, Mock Green Loop Cafe, Mock Deep Dish Kitchen, Mock Walking Allowance.
- **Alternatives:** two hotels, one restaurant, two transport options; no attraction alternative after both matching attractions were used.
- **Budget / validation:** USD 245 group total; no comparison; validation performed and passed.
- **Replan:** NO; no violation.
- **Final status / UI clarity:** success; selected/alternative metadata was readable, but pizza looked ignored even though Deep Dish Kitchen happened to be selected by rotation. Functional PARTIAL; recruiter clarity PARTIAL.
- **Unexpected behavior:** a concrete preference was preserved only in a backend field that the page does not render or route.

### B — Seattle natural preference sentence

- **Exact user input:** `I want to spend three days in Seattle. I love coffee and I also enjoy outdoor activities.`
- **Destination / capability:** intended Seattle; natural connector and preference extraction.
- **Extracted requirements:** destination incorrectly became `spend three days in Seattle`; 3 days; food/coffee was retained; outdoor activities remained an `UNSPECIFIED` specific preference.
- **Planner / tools:** planner accepted the malformed destination; all four searches returned zero with `UNSUPPORTED_CITY_DATA`; budget was skipped.
- **Candidate results / selection / alternatives:** none.
- **Budget / validation:** no budget result; validation not performed because of prior tool errors.
- **Replan:** NO; unsupported-data errors are not repair-eligible.
- **Final status / UI clarity:** unexpected domain error. The page exposed the bad destination, but the outcome used an internal code rather than explaining that parsing—not Seattle coverage—was the cause. Functional FAIL; recruiter clarity FAIL.
- **Unexpected behavior:** an ordinary `want to spend ... in Seattle` construction corrupted a supported destination.

### C — Miami soft budget, original natural wording

- **Exact user input:** `Plan a 3-day Miami trip for two people. I'd like to keep the trip around $900. I prefer beaches and seafood.`
- **Destination / capability:** intended Miami; soft budget and two preferences.
- **Extracted requirements:** destination incorrectly became `keep the trip`; 3 days; 2 travelers; USD 900, scope UNKNOWN, backend strength SOFT; seafood routed to food, beaches preserved only as an `UNSPECIFIED` specific preference; `approximate budget` constraint recorded.
- **Planner / tools:** planner accepted; all four searches returned `UNSUPPORTED_CITY_DATA`; budget skipped.
- **Candidate results / selection / alternatives:** none.
- **Budget / validation:** no result; validation not performed because of prior errors.
- **Replan:** NO; soft constraints and tool failures are not repair-eligible.
- **Final status / UI clarity:** unexpected domain error. Functional FAIL; recruiter clarity FAIL.
- **Unexpected behavior:** a later budget phrase overwrote a correctly stated supported destination.

### D — Austin hard budget, successful bounded repair

- **Exact user input:** `Please build a three-day trip to Austin for one traveler. My total budget is $350.`
- **Destination / capability:** Austin; Wave 2 hard validation and Wave 3 successful repair.
- **Extracted requirements:** Austin, 3 days, 1 traveler, USD 350 TOTAL_TRIP, backend strength HARD. The UI did not render HARD.
- **Planner / tools:** first deterministic plan used all four searches and budget calculation; the same tool categories ran after feedback. Current controlled pools contained 3 results per search.
- **First selection / cost:** all three attractions and all three restaurants rotated across days; budget lodge and walking; USD 394.
- **Violation / structured feedback:** `HARD_BUDGET_EXCEEDED`, expected 350, actual 394, excess 44; one typed feedback-driven repair attempt.
- **Final selected candidates:** Mock Springs Park, Mock Downtown Budget Lodge, Mock Taco Yard, Mock Walking Allowance. Alternatives were the other two candidates in every category.
- **Budget / validation:** repaired total USD 317, USD 33 remaining; second validation passed.
- **Replan:** YES; hard-budget violation.
- **Final status / UI clarity:** success. The pipeline clearly showed Validation FAILED → Budget repair → Planner → Tools → Validation completed, but the UI showed only the final USD 317 and final candidate set. Functional PASS; recruiter clarity PARTIAL.
- **Unexpected behavior:** no functional defect; the evidence needed to prove the repair was omitted.

The USD 350 threshold was not pre-hardcoded from a test. A current controlled-data calibration run produced a USD 394 initial Austin itinerary; the one-repair least-cost result was USD 317, making 350 a genuine feasible repair boundary.

### E — Denver hard budget, bounded terminal failure

- **Exact user input:** `Please arrange a two-day trip to Denver for one traveler. My total budget is $40.`
- **Destination / capability:** Denver; safe single repair followed by terminal failure.
- **Extracted requirements:** Denver, 2 days, 1 traveler, USD 40 TOTAL_TRIP, backend strength HARD; HARD was absent from the UI.
- **Planner / tools:** two planner/tool/validation passes in the pipeline; final search pools had 3 candidates in every category.
- **First selection / cost:** Mountain Park + Frontier History Hall, Mile High Cafe + Mountain Greens, Union Budget Lodge, walking; USD 211.
- **Final selected candidates:** least-cost Mountain Park, Mile High Cafe, Union Budget Lodge, walking. Two alternatives per category remained.
- **Budget / validation:** repaired cost USD 188; final typed violation expected 40, actual 188, excess 148; final validation failed.
- **Replan:** YES; first hard-budget violation; exactly one attempt, no loop.
- **Final status / UI clarity:** expected terminal domain error. The pipeline convincingly proved boundedness, but the banner only said `Hard budget exceeded`, Validation only said FAILED, and the Budget Summary said no result even though the tool card contained USD 188. Functional PASS; recruiter clarity PARTIAL.
- **Unexpected behavior:** final candidate cards remained labelled Selected even though no validated itinerary was returned; the error-level budget panel discarded the most useful failure numbers.

### F — Denver missing information

- **Exact user input:** `I want a relaxing trip with good food in Denver.`
- **Destination / capability:** Denver; preflight clarification for missing duration.
- **Extracted requirements:** Denver, duration `MISSING — required`, food interest; other optional fields not supplied. `relaxing` was not retained as a visible preference.
- **Planner / tools / candidates:** planner not invoked; no tools, candidates, or alternatives.
- **Budget / validation:** budget not reached; validation not performed with reason `Validation was not reached`.
- **Replan:** NO; clarification stops before planning.
- **Final status / UI clarity:** clear clarification question asking for days or dates, explicit `Missing: duration`, and independent-run guidance. Functional PASS; recruiter clarity PASS.
- **Unexpected behavior:** the qualitative `relaxing` preference disappeared, but it did not affect the appropriate clarification outcome.

### G — Los Angeles candidate-diversity request

- **Exact user input:** `Could you put together three days in Los Angeles for one person? I like outdoor attractions and Asian food.`
- **Destination / capability:** Los Angeles; preference routing, candidate diversity, and safe no-results.
- **Extracted requirements:** Los Angeles, 3 days, 1 traveler, food/asian; `outdoor attractions` survived only as an `UNSPECIFIED` specific preference and was not routed to attraction search.
- **Planner / tools:** attraction/hotel/transport returned 3 results each; restaurant returned zero for `asian`; budget skipped.
- **Candidate results / selection / alternatives:** Candidate Explorer rendered all 9 surviving options as alternatives and no selected candidates; the food group was absent.
- **Budget / validation:** none; validation not performed because of prior tool error.
- **Replan:** NO; `NO_RESULTS` is not a budget repair case.
- **Final status / UI clarity:** unexpected domain error `search_restaurants: NO_RESULTS`. Fail-closed behavior was safe, but the scenario did not demonstrate candidate selection and the all-alternative explorer was confusing. Functional PARTIAL; recruiter clarity PARTIAL.
- **Unexpected behavior:** a plausible preference for a supported flagship city had no fixture match, while the outdoor preference was not applied.

### H — Paris unsupported scope

- **Exact user input:** `Can you plan a three-day getaway to Paris for me?`
- **Destination / capability:** Paris; selected-U.S.-city boundary and non-hallucinating failure.
- **Extracted requirements:** Paris, 3 days; no traveler or budget.
- **Planner / tools:** planner accepted; all four searches returned zero with `UNSUPPORTED_CITY_DATA`; budget skipped.
- **Candidate results / selection / alternatives:** none.
- **Budget / validation:** none; validation not performed because of prior errors.
- **Replan:** NO; unsupported scope is terminal.
- **Final status / UI clarity:** expected domain error with no itinerary, no stack trace, and no console error. The result was safe, but `DOMAIN ERROR` and `UNSUPPORTED_CITY_DATA` do not explain the supported-city boundary or a next step. Functional PASS; recruiter clarity PARTIAL.
- **Unexpected behavior:** none functionally.

### I — Austin alternate hard-budget wording

- **Exact user input:** `Please build a three-day trip to Austin for one traveler. Do not spend more than $350 total.`
- **Destination / capability:** Austin; hard-budget language robustness plus repair.
- **Extracted requirements:** Austin, 3 days, 1 traveler, USD 350 TOTAL_TRIP, backend strength HARD.
- **Planner / tools / candidates:** same 3-per-category pools and repair path as D; final selected Springs Park, Downtown Budget Lodge, Taco Yard, and walking; two alternatives per category.
- **Budget / validation:** initial USD 394, repaired USD 317, final within budget and validation passed.
- **Replan:** YES; hard-budget excess.
- **Final status / UI clarity:** success. This phrasing correctly exercised the current hardening, but the UI still did not label the constraint HARD or show the initial failure details. Functional PASS; recruiter clarity PARTIAL.
- **Unexpected behavior:** none functionally.

### J — Seattle connector success but data failure

- **Exact user input:** `Please plan three days in Seattle for me. I love coffee and I also enjoy parks.`
- **Destination / capability:** Seattle; repeated preference introducer and controlled-data match.
- **Extracted requirements:** Seattle, 3 days, parks + food, coffee food preference; backend specific preference `FOOD:coffee`. This verifies connector hardening when the destination grammar is safe.
- **Planner / tools:** attraction returned Evergreen Park; hotel and transport returned 3 each; restaurant returned zero for coffee; budget skipped.
- **Candidate results / selection / alternatives:** Candidate Explorer displayed the park, hotels, and transport only as alternatives; no selected candidates and no food group.
- **Budget / validation:** none; validation not performed because of prior error.
- **Replan:** NO; no-results is terminal.
- **Final status / UI clarity:** unexpected domain error despite correct extraction. Functional PARTIAL because data could not fulfill the advertised preference; recruiter clarity PARTIAL.
- **Unexpected behavior:** the hardening report and parser recognize coffee, but the Seattle controlled fixture cannot satisfy it.

### K — Miami soft budget, safe wording control

- **Exact user input:** `Please plan three days in Miami for two people. My budget is around $900 total. I prefer beaches and seafood.`
- **Destination / capability:** Miami; successful soft-budget overage without repair.
- **Extracted requirements:** Miami, 3 days, 2 travelers, USD 900 TOTAL_TRIP, backend strength SOFT, seafood food preference, beaches as hidden `UNSPECIFIED` specific preference, and visible `approximate budget` constraint.
- **Planner / tools:** all five tools succeeded; search counts 3 attractions, 3 hotels, 1 seafood restaurant, 3 transport.
- **Selected candidates:** all three attractions, Downtown Budget Lodge, Ocean Table, and Walking Allowance. Alternatives: two hotels and two transport options; no attraction or food alternatives after filtered/used candidates.
- **Budget / validation:** USD 1,110 group total, USD 210 over the approximate budget; validation passed because the constraint is SOFT.
- **Replan:** NO; soft overage is not eligible.
- **Final status / UI clarity:** success. The page showed SUCCESS, OVER BUDGET, PASSED, and `approximate budget`, but never explicitly said SOFT or explained why over-budget still passes. Functional PASS; recruiter clarity PARTIAL.
- **Unexpected behavior:** beaches was not routed or displayed; the three status labels require developer explanation to reconcile.

## 6. Requirements Readiness

**Score: 3 / 5.** Destination, duration, travelers, budget amount/scope, currency, generic preferences, missing required fields, and optional absence are consistently placed in a readable grid. Scenario F is especially strong: `MISSING — required` and the clarification question agree.

The panel does not render `budget_constraint_strength`, `objective`, or `specific_preferences` even though the backend response contains them. This hides HARD in D/E/I, SOFT in C/K, pizza in A, beaches in C/K, outdoor wording in B/G, and coffee-specific evidence in J. `UNKNOWN`, `Not supplied`, and `None supplied` also occupy a large fraction of the panel. More seriously, B and C show that an incorrect destination can still be deemed sufficient and sent to tools.

Wave 1 exists in the backend, but the page only partially proves it.

## 7. Candidate Explorer Readiness

**Score: 4 / 5.** On successful runs, Selected versus Alternative is visually clear. Cards expose price/unit, rating, demo review count, tags, preference matches, source, and null-rating handling. No broken or misleading image placeholder appeared when `image_url` was null. Scenario A clearly connected `museums` to two selected attractions, and K connected `seafood` to Ocean Table.

The gaps are semantic rather than data transport. The explorer does not explain why selection favored a candidate, and on G/J it labels every surviving option Alternative even though no itinerary exists. On repaired runs it exposes only the final selection, not the previous selection that changed. With three days, repeated selected inputs are deduplicated, so a recruiter must inspect the itinerary to understand reuse.

## 8. Selection Explainability

**Score: 2 / 5.** `Preference match` is useful when populated, and prices/tags let a technical viewer infer some logic. That is not a selection reason. Most cards say `No explicit match`; there is no statement such as cheapest matching option, required preference match, rotation for diversity, higher rating, or retained because already cheapest.

The successful repair is the clearest missed opportunity. The final warnings eventually say that budget repair selected least-cost matching options, but the Candidate Explorer does not identify which choices changed or how much each change saved. Ratings and review counts are shown but are not ranking inputs, which can lead a recruiter to infer a selection policy that does not exist.

## 9. Budget & Constraint Readiness

**Score: 3 / 5.** The Budget Summary gives group/per-traveler basis, limit, scope, comparison cost, balance, and category breakdown. D/I and K demonstrate accurate group comparisons; no-budget A clearly says comparison unavailable.

Constraint semantics are not explicit. The requirements panel omits HARD/SOFT, and K presents `SUCCESS`, `OVER BUDGET`, and `PASSED` without a concise explanation that the USD 900 amount is an approximate preference. In terminal E, the top-level `budget` artifact is intentionally absent, so the main Budget Summary says no result even though the final budget-tool record contains USD 188, limit 40, and the overage. This makes the failure less understandable than the backend contract.

## 10. Validation Readiness

**Score: 2 / 5.** Recruiters can tell whether validation ran and whether its final outcome was PASSED, FAILED, or NOT PERFORMED. They cannot see any member of `validation.violations`. Scenario E's API exposed `HARD_BUDGET_EXCEEDED`, expected 40, actual 188, excess 148, and a message; the Validation panel exposed only Performed Yes / Outcome FAILED.

On D/I the final pass replaces the first violation in the public final summary, leaving only the pipeline's red first Validation box as evidence. On soft K, PASSED has no visible policy explanation. Wave 2 is operational but poorly demonstrated.

## 11. Replan Readiness

**Backend evidence: YES. UI evidence: PARTIAL.**

The two audited paths were:

```text
D / I: first plan USD 394
  -> HARD_BUDGET_EXCEEDED (limit 350, excess 44)
  -> structured feedback, attempt 1
  -> attractions changed from three rotating choices to Springs Park
  -> food changed from three rotating choices to Taco Yard
  -> new cost USD 317
  -> second validation PASS
  -> success

E: first plan USD 211
  -> hard-budget failure (limit 40)
  -> structured feedback, attempt 1
  -> least-cost candidates, new cost USD 188
  -> HARD_BUDGET_EXCEEDED (excess 148)
  -> second validation FAIL
  -> safe terminal error
```

The browser pipeline accurately represented two Planner, Tools, and Validation stages around one Budget repair, and the unrecoverable case proved there was no infinite loop. But the UI omitted the trigger code, first cost, first excess, structured feedback, `replan_attempts=1`, before/after candidate mapping, and savings. It also showed only one final tool snapshot. A recruiter can see that *something* called budget repair happened, but cannot independently verify what the agent changed or why it worked.

Wave 3 is therefore a real capability with weak recruiter evidence.

## 12. Failure / Clarification Readiness

Scenario F is demo-ready: it names the missing duration, asks an actionable question, shows that the planner was not invoked, and explains that the next run is independent.

Terminal failures are safe but not recruiter-friendly. There were no stack traces, blank screens, HTTP 500s, half-rendered itineraries, or console errors. However, `DOMAIN ERROR`, `UNSUPPORTED_CITY_DATA`, and `search_restaurants: NO_RESULTS` are internal terms. H does not say that the demo supports 12 selected U.S. cities; G/J do not say that the city is supported but no controlled candidate matched the requested preference; E does not show the limit, minimum repaired cost, or excess near the banner.

**Failure Clarity score: 2 / 5.**

## 13. Data Transparency

**Score: 4 / 5.** The header says local portfolio demo and Mock travel data; execution confirms DEMO MODE and `DeterministicTestPlanner`; candidate names are prefixed Mock; each card says Controlled mock fixture; costs/reviews are labelled as estimates/demo values; a result disclosure and footer repeat the limitation. Nothing implies Google, Yelp, Booking, live inventory, or current availability.

This is trustworthy, but the repetition can make the page feel more like a scripted fixture viewer than an agent demo. The best balance would retain one prominent disclosure and candidate provenance while reducing repeated source/no-live labels.

## 14. Information Hierarchy

**Score: 2 / 5.** At the audited desktop viewport, the first post-submit screen was dominated by presets, guidance, and the textarea; the outcome began below the initial viewport. A measured successful K page placed the request at document top 171 px with 771 px height, outcome at 1,082 px, Requirements at 1,239 px, Pipeline at 1,828 px, Tool Calls at 2,550 px with 1,844 px height, Candidate Explorer at 4,412 px, Validation at 5,774 px, Budget at 5,943 px, and Itinerary at 6,511 px. Engineering diagnostics began at 8,640 px.

The order prioritizes engineering trace before user result. Tool cards repeat destination, max price, preferences, result names, and prices already represented elsewhere; this pushes the most persuasive artifacts—repair proof, final budget, and itinerary—several screens down. Candidate Explorer is valuable but also long. The page currently behaves as an Engineering Debug View, not a concise Recruiter Demo View.

Internal language (`preflight`, `runtime inputs`, `execution order`, `domain error`, `budget repair`, validation codes) is acceptable for technical depth but needs short plain-language interpretation. The strongest information hierarchy would surface request understanding, outcome, key selections, budget/repair story, and itinerary first, with raw tool calls collapsed.

## 15. Scorecard

| Dimension | Score (1–5) | Weight | Weighted contribution | Evidence summary |
|---|---:|---:|---:|---|
| Requirement Clarity | 3 | 10% | 0.30 | Core grid is readable; semantic fields are hidden and two destinations were corrupted |
| Candidate Transparency | 4 | 15% | 0.60 | Strong selected/alternative metadata and provenance |
| Selection Explainability | 2 | 15% | 0.30 | Match tags exist; actual selection policy and change reasons do not |
| Budget Clarity | 3 | 10% | 0.30 | Strong arithmetic; hard/soft meaning and failure cost are unclear |
| Validation Clarity | 2 | 15% | 0.30 | Performed/outcome only; violations omitted |
| Replan Visibility | 2 | 15% | 0.30 | Loop visible; trigger, before/after, and savings missing |
| Failure Clarity | 2 | 5% | 0.10 | Safe rendering but internal codes and weak next steps |
| Data Transparency | 4 | 5% | 0.20 | Honest controlled/mock disclosure, slightly over-repeated |
| UI Information Hierarchy | 2 | 5% | 0.10 | Tool detail precedes validation, budget, and itinerary by several screens |
| Overall Recruiter Comprehension | 2 | 5% | 0.10 | Developer narration is required for the central capability |
| **Weighted total** |  | **100%** | **2.60 / 5.0** | **NOT READY** |

## 16. Findings by Severity

### BLOCKER

1. **Supported destinations can be replaced by ordinary later phrases.** Gap type: **Reliability Gap**. Evidence: B parsed Seattle as `spend three days in Seattle`; C parsed Miami as `keep the trip`; both became `UNSUPPORTED_CITY_DATA`. Affected: B, C. This makes an unscripted recruiter input look like the core system is broken.

### HIGH

1. **The UI cannot prove the successful repair decision.** Gap type: **Presentation Gap**. Evidence: D/I backend changed USD 394 to 317 and changed attraction/food choices, while UI retained only the final snapshot. Affected: D, I, E.
2. **Structured validation context is present but not rendered.** Gap type: **Presentation Gap**. Evidence: E contains code/limit/actual/excess in the API; Validation only says FAILED, and the main Budget panel says no result. Affected: D, E, I, K.
3. **Wave 1 semantic fields are absent from Extracted Requirements.** Gap type: **Presentation Gap**. Evidence: HARD/SOFT, objectives, and specific preferences are omitted. Affected: A, C, D, E, G, I, J, K.
4. **Advertised natural preferences exceed controlled fixture coverage/routing.** Gap type: **Data Gap / Capability Gap**. Evidence: Seattle coffee and Los Angeles Asian food produced `NO_RESULTS`; pizza, beaches, and outdoor attractions were preserved as unspecified but not routed. Affected: A, B, C, G, J, K.
5. **Engineering trace buries the recruiter result.** Gap type: **Presentation Gap**. Evidence: outcome below the initial viewport, 1,844 px of Tool Calls before Candidate/Validation/Budget, itinerary at 6,511 px in K. Affected: all successful and repair scenarios.

### MEDIUM

1. **Selected is a label, not an explanation.** Gap type: **Presentation Gap**. Evidence: no adjacent reason based on preference, price, rotation, or repair; ratings can be mistaken for ranking inputs. Affected: A, D, E, I, K.
2. **Failure terminology is implementation-facing.** Gap type: **Scope/Expectation Gap / Presentation Gap**. Evidence: `DOMAIN ERROR`, `UNSUPPORTED_CITY_DATA`, and `search_restaurants: NO_RESULTS` lack plain-language scope and recovery guidance. Affected: B, C, G, H, J.
3. **Candidate Explorer semantics are odd on failed runs.** Gap type: **Presentation Gap**. Evidence: G/J and E can display alternatives or selected repaired candidates without a validated itinerary. Affected: E, G, J.

### LOW

1. **Absent-field states create noise.** Gap type: **Presentation Gap**. Evidence: UNKNOWN, Not supplied, and None supplied dominate the requirements grid. Affected: most scenarios.
2. **Mock/provenance disclosure is repeated more than necessary.** Gap type: **Presentation Gap**. Evidence: header, source line on every candidate, result disclosure, limitations, and footer. Affected: successful scenarios.

Counts: **1 BLOCKER, 5 HIGH, 3 MEDIUM, 2 LOW**.

## 17. Capability vs Presentation Gap Matrix

| Finding | Backend capability | UI visibility | Gap type |
|---|---|---|---|
| Natural destination parsing | Incorrect for B/C | Incorrect value is visible only after failure | Reliability |
| Hard/soft semantics | Correct for D/E/I/K | Strength field omitted | Presentation |
| Specific preference preservation | Present for pizza, beaches, outdoor, coffee | Field omitted; some values not routed | Capability + Presentation |
| Candidate preservation | Selected and alternatives public | Strong on success; ambiguous on failure | Presentation |
| Preference match | Candidate-level matches public | Visible and helpful when matched | No material gap for matched terms |
| Selection policy | Deterministic rotation/least-cost repair | No normal or repair reason per selected card | Presentation |
| Hard-budget validator | Typed code, expected, actual, excess | Only final Performed/Outcome | Presentation |
| Bounded replan | One feedback attempt, recompute, revalidate | Pipeline only; no before/after evidence | Presentation |
| Unrecoverable failure | Safe terminal result after one attempt | Generic message; main budget missing | Presentation |
| Unsupported city | Safe, non-hallucinating terminal error | Internal code, no scope explanation | Scope/Expectation |
| Coffee/Asian data | Parser routes preferences | No matching Seattle/LA fixture candidates | Data |
| Final itinerary and budget | Complete and readable | Several screens below engineering trace | Presentation |

## 18. Recruiter Demo Value / Engineering Cost

| Finding / change candidate | Demo value (1–5) | Cost (1–5) | Risk | Priority |
|---|---:|---:|---|---|
| Bound destination extraction to known city spans and prevent later `trip`/budget phrases from overwriting a resolved city | 5 | 2 | Medium | P0 |
| Add a compact repair evidence block: initial cost/violation, changed candidates, savings, final validation | 5 | 3 | Low | P0 |
| Render HARD/SOFT and structured validation code/limit/actual/excess in plain language | 5 | 2 | Low | P0 |
| Put outcome, concise decision summary, budget/repair, and itinerary before collapsed raw tool details | 4 | 2 | Low | P1 |
| Align a small advertised preference set with each featured city's tags, or clearly guide supported preference vocabulary | 4 | 2 | Medium | P1 |
| Broaden to live providers or arbitrary-city coverage | 2 | 5 | High | DEFER |
| Add multi-turn editing or geographic routing | 2 | 5 | High | DEFER |

## 19. Recommended Final Polish

Only the following five changes are worth doing before a recruiter demo:

1. **Fix the destination-overwrite blocker.** Preserve a recognized supported city and reject/clarify implausible multiword destination captures instead of sending them to tools.
2. **Make Wave 2/3 visible in one compact story.** Show initial USD 394, `Hard budget exceeded by USD 44`, one repair, the exact attraction/food changes, final USD 317, and revalidation PASS.
3. **Show semantic requirements and violations.** Add hard/soft strength, specific preferences, objective when present, and violation code/limit/actual/excess with human wording.
4. **Reorder/collapse for a recruiter path.** Surface outcome, requirements, key candidates, repair/budget, and itinerary before collapsed Tool Calls and diagnostics.
5. **Make featured preference promises match controlled data.** Add or constrain a small documented vocabulary so coffee/Seattle and the chosen LA food example demonstrate selection rather than terminal no-results.

## 20. Deferred Work

Do not spend recruiter-MVP time on live travel providers, scraping, booking, maps, opening hours, geographic routing, arbitrary U.S./international city coverage, multi-turn memory, attraction-only tool modes, multi-agent orchestration, image sourcing, or broad LLM/embedding preference search. The audit shows that the existing deterministic capability is sufficient; the urgent problems are input reliability and evidence presentation.

Also defer aesthetic redesign. The visual system is coherent and accessible enough for this purpose. Reordering and concise explanation provide more demo value than new colors, animation, maps, or decorative imagery.

## 21. Suggested Recruiter Demo Script

Do not use an unscripted request until the destination blocker is fixed. With the current build, use this tested 2–3 minute sequence:

1. Submit D: `Please build a three-day trip to Austin for one traveler. My total budget is $350.`
2. Point out Austin / 3 days / 1 traveler / USD 350 total in Extracted Requirements, while verbally stating that this is a hard limit because the UI omits it.
3. Move directly to Execution Pipeline: first Validation failed, one Budget repair, second Planner/Tools/Validation, final success.
4. Explain the measured before/after verbally: USD 394 became USD 317; Springs Park and Taco Yard replaced rotating higher-cost daily choices.
5. Show Candidate Explorer's selected/alternative badges, price, tags, rating/demo review count, preference match, and controlled source.
6. Show final Budget Summary and Itinerary. Mention that all values are deterministic mock estimates and no live provider was called.
7. If time permits, submit F to demonstrate a safe clarification. Avoid B/C/G/J in a live demo until their reliability/data gaps are addressed.

This script is stable, but it currently requires presenter narration for the exact capability the UI should prove by itself.

## 22. Final Verdict

**NOT READY**

**Must fix before demo:**

- Natural destination overwrite for supported-city requests.
- Compact, explicit before/after replan and structured validation evidence.
- Visible hard/soft constraint semantics and recruiter-readable failure context.

**Nice to have:**

- Reorder/collapse the engineering trace.
- Align a small set of featured preferences with controlled city data.
- Reduce absent-field and repeated mock-source noise.

**Do not spend time on:**

- Live providers, more cities, booking/maps, multi-turn memory, geographic optimization, or visual redesign.

The project is technically credible and the strongest controlled Austin path works. It is not yet reliable or self-explanatory enough for a recruiter to type naturally and understand Wave 1–3 without developer narration.
