# Natural-Language Input Hardening Report

## 1. Root Causes

### Preference connectors

The preference extractor recognized an initial discourse prefix such as `I like` and captured the remainder of that sentence. It then split the captured text only on commas or the bare word `and`.

This worked for:

```text
I like zoos and fried chicken.
→ zoos
→ fried chicken
```

It did not normalize a repeated introducer:

```text
I like zoos and I love fried chicken.
→ zoos
→ I love fried chicken
```

`fried chicken` already had a correct FOOD classification, and `zoo`/`zoos` already had the required activity normalization. The failure occurred earlier: the second segment retained `I love`, `I prefer`, or `I also like`, so category detection saw a discourse phrase instead of the preference value.

The live API and test parser use the same rule-based extractor path. Runtime checks confirmed this was a parser behavior, not a separate test-only parser or frontend endpoint mismatch.

### Budget phrases

The existing amount pattern recognized values carrying `$`, `€`, `£`, ISO currency codes, or a short list of directly adjacent budget prefixes. It did not recognize currency words such as `dollars`, so `I only want to spend 1300 dollars about it` had neither a recognized prefix immediately beside the number nor recognized currency metadata.

Because strength came mainly from the old amount regex's captured prefix, phrases such as `no more than $1300` and `spending limit is $1300` could yield an amount via `$` without receiving HARD semantics.

The parser already avoided treating ordinary `3-day` and `2 travelers` numbers as budgets. That protection was retained.

## 2. Parser Changes

The hardening remains bounded, deterministic, and dependency-free.

Preference handling now has three small stages:

1. find a supported preference introducer, including `I also like`;
2. split its value span on commas and common `and`/`but` connectors;
3. strip a repeated `I like`, `I love`, `I prefer`, `I enjoy`, `I need`, or `also` prefix from each segment before classification.

This is connector normalization, not a full-sentence special case. The existing generic fields and typed `SpecificPreference` records remain unchanged. A single small taxonomy addition treats `coffee` as food; no general food ontology was introduced.

Budget handling keeps the existing amount parser and adds orthogonal helpers for:

- currency-word recognition (`dollar(s)`, `euro(s)`, `pound(s)`);
- sentence-bounded budget-intent detection for otherwise unmarked numeric amounts;
- scope detection around the chosen amount;
- strength detection from the nearest explicit HARD or SOFT marker;
- currency normalization to USD/EUR/GBP.

Later explicit budget statements still override earlier statements. The implementation does not treat every number as money and does not change budget calculation, validation, planning, graph topology, or replan behavior.

## 3. Supported Budget Examples

| Pattern family | Example | Amount | Scope | Strength |
|---|---|---:|---|---|
| Conservative spend | `I only want to spend $1300.` | 1300 USD | UNKNOWN | UNSPECIFIED |
| Currency word | `I only want to spend 1300 dollars.` | 1300 USD | UNKNOWN | UNSPECIFIED |
| Capacity | `I can spend $1300.` | 1300 USD | UNKNOWN | UNSPECIFIED |
| Trip allocation | `I have $1300 for the trip.` | 1300 USD | TOTAL_TRIP | UNSPECIFIED |
| Explicit limit | `My spending limit is $1300.` | 1300 USD | UNKNOWN | HARD |
| Upper bound | `Keep the trip under $1300.` | 1300 USD | UNKNOWN | HARD |
| Upper bound | `I want to spend no more than $1300.` | 1300 USD | UNKNOWN | HARD |
| Approximation | `I'd like to keep the trip around $1300.` | 1300 USD | UNKNOWN | SOFT |
| Approximate total | `I can spend about $1300 total.` | 1300 USD | TOTAL_TRIP | SOFT |
| Explicit total budget | `My total budget is $1300.` | 1300 USD | TOTAL_TRIP | HARD |
| Screenshot wording | `I only want to spend 1300 dollars about it.` | 1300 USD | UNKNOWN | UNSPECIFIED |

Existing forms such as `under $1000`, `max $1000`, `max 1k`, `don't spend more than $1000`, and `budget USD 1000` continue to work.

## 4. Ambiguous Language Policy

Amount extraction and constraint semantics are intentionally separate:

- `under`, `up to`, `max`, `at most`, `no more than`, `don't spend more than`, `spending limit`, and the existing explicit budget forms are HARD.
- `around` and `about` before the selected amount are SOFT and retain the `approximate budget` constraint marker.
- `can spend`, `have`, and `only want to spend` capture capacity/intent but remain UNSPECIFIED unless an explicit bound or approximation marker is present.
- `total`, `total budget`, `for the trip`, `on the trip`, `whole trip`, and `entire trip` provide TOTAL_TRIP scope.
- `per person`, `per traveler`, and `each` provide PER_PERSON scope.
- `about it` after a currency amount does not mean approximate amount and does not establish total-trip scope.
- Unmapped scope language remains UNKNOWN rather than being guessed.
- A duration number, traveler count, date, or rating-like number is not accepted merely because it is numeric.

This is a controlled grammar, not a claim of arbitrary-English understanding.

## 5. UI Guidance Changes

`TravelRequestPanel.vue` now includes a compact, always-visible `aside` titled `Tips for a better request` next to the textarea. It tells users that they may include destination, duration/dates, travelers, total budget, interests, and food/hotel/transport preferences.

It provides this concrete example:

```text
Plan a 3-day trip to Columbus for 1 traveler under $1300 total.
I like zoos and fried chicken.
```

It also suggests clear budget wording: `total budget of $1300`, `under $1300 total`, or `around $1300`. The text explicitly says optional details may be omitted and that the agent may ask for clarification when required information is missing.

The textarea placeholder was aligned with the example, but the independent helper remains visible after typing. `aria-describedby` connects the textarea to both the guidance panel and existing maximum-length/help text. The implementation is static HTML plus three small CSS rules: no modal, wizard, router, state, or dependency was added.

## 6. Tests Added

Backend regression coverage adds 19 passing cases across the existing requirements and scenario-semantic suites:

- `I like zoos and fried chicken`
- `I like zoos and I love fried chicken`
- `I enjoy museums and I prefer seafood`
- `I enjoy parks and I also like coffee`
- `I like walking, but I prefer public transit`
- eleven budget grammar/strength/scope combinations
- `3-day` budget false-positive protection
- `2 travelers` budget false-positive protection
- full Columbus graph/API-domain scenario with repeated preference introducer and `$1300 on the trip`

The Columbus scenario verifies destination, duration, both preference channels, amount/currency/scope/strength, five successful tools, a complete itinerary, and passed validation.

One frontend SSR test verifies that the helper title, recommended fields, Columbus example, budget wording, optional-detail disclosure, textarea description linkage, preset buttons, Plan Trip, and Reset are rendered. Existing composable tests continue to verify custom input, submit, reset, duplicate-submit blocking, and response lifecycle behavior without a brittle page snapshot.

## 7. Regression Results

| Check | Result |
|---|---|
| Targeted requirements/parser/scenario tests | PASS — 113 passed, 3 expected xfailed, 0 failed |
| Full backend suite | PASS — 313 passed, 3 expected xfailed, 0 failed |
| Full frontend suite | PASS — 43 passed, 0 failed |
| TypeScript/Vue typecheck | PASS |
| Vite production build | PASS — 47 modules transformed |
| Ruff | PASS |
| Diff whitespace check | PASS; only Git's existing LF/CRLF notices were emitted |

Direct FastAPI-path acceptance result:

```text
Plan a 3-day trip to Columbus.
I like zoos and I love fried chicken.
I only want to spend $1300 on the trip.
```

- status: `success`
- destination/duration: `Columbus`, 3
- interests: `zoo`, `food`
- food preferences: `fried chicken`
- budget: 1300 USD, TOTAL_TRIP, UNSPECIFIED strength
- attraction/hotel/restaurant/transport/budget tools: all SUCCESS
- itinerary: present
- validation: passed

Boston and NYC requests still succeed. The Wave 3 USD 400 Boston case still performs exactly one replan and passes at USD 392. Four candidate groups remain available, confirming Candidate Explorer compatibility.

No live API or external network source was used.

## 8. Remaining Known Limitations

- Preference parsing supports a bounded family of first-person English introducers and connectors, not arbitrary grammar or languages.
- Coordinated noun phrases that legitimately contain `and` can still be split conservatively.
- Generic terms such as `museums` and `seafood` continue to populate their established generic fields instead of being duplicated as `SpecificPreference` records.
- The taxonomy remains intentionally small; unknown preferences are preserved as UNSPECIFIED rather than guessed.
- A currency-marked amount continues to be treated as budget-compatible under the existing product behavior, even when the surrounding prose is sparse.
- `per day` has no dedicated value in the existing `BudgetScope` contract and therefore remains UNKNOWN.
- Ambiguous corrections without punctuation or a recognizable intent marker may remain outside the grammar.
- The UI offers guidance, not a guarantee that every phrasing is supported, and does not claim coverage of every U.S. city or live inventory.
