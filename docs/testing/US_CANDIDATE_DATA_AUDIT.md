# US Travel Candidate Coverage & Transparency Audit

## Audit metadata

- Audit date: 2026-09-11
- Repository: `travel-planning-agent`
- Branch: `main`
- Audited HEAD: `08d922ed06e38cc53d803a056a1d3fab57c495a7`
- Working tree: dirty before this audit because the uncommitted Wave 1–3 implementation and reports are present; this audit did not reset, stash, or overwrite them.
- Scope: offline mock candidate fixtures, search-tool loading/filtering, planner-to-composer flow, public response serialization, and frontend visibility.

## Executive finding

The Columbus failure is primarily a data-coverage and registry problem, compounded by one narrow preference-routing gap. The current product has four category-specific JSON files containing only Boston and New York City. Search code reparses one file per tool call, owns a two-entry New York alias map, and reports an unknown city exactly like a supported city with no matches. The pipeline already preserves each tool's complete filtered result list in graph state and in `execution.tools[].data`, but it does not expose a stable selected-versus-alternative model. Candidate records also lack rating, review count, image metadata, description, city/state identity, category, and candidate-level source.

The implementation should therefore replace the four flat fixtures with one validated US demo dataset and one generic loader/registry, add typed optional metadata, preserve complete filtered pools, publish explicit selected and alternative groups, and add only the smallest preference normalization required for the Columbus acceptance query. It should not introduce live providers, scraping, LLM ranking, a database, or city-specific Python branches.

## 1. Where are candidate data and mock tools located?

Candidate fixtures are currently split across:

- `data/mock/attractions.json`
- `data/mock/hotels.json`
- `data/mock/restaurants.json`
- `data/mock/transport.json`

All four search implementations live in `backend/app/tools/mock.py`. The shared `_search()` helper maps each function to one filename, reads and parses the JSON on every invocation, validates rows as `TravelOption`, applies destination/price/preference filters, sorts by `(price, id)`, and returns a `ToolResult`. `run_tool()` is the common dispatcher. Budget calculation is deterministic and belongs in the same module but is independent of fixture loading.

The current candidate contract is `TravelOption` in `backend/app/tools/contracts.py`. It contains `id`, `destination`, `name`, `price`, `currency`, `unit`, and `tags`.

## 2. What cities are currently supported, and how many candidates exist per category?

Only two canonical destination strings are represented: Boston and New York City. Every category has six total rows and three rows per city.

| City | Attractions | Hotels | Restaurants | Transport | Total |
|---|---:|---:|---:|---:|---:|
| Boston | 3 | 3 | 3 | 3 | 12 |
| New York City | 3 | 3 | 3 | 3 | 12 |
| Total | 6 | 6 | 6 | 6 | 24 |

There are no Columbus, Chicago, Washington DC, Miami, Austin, Denver, Seattle, San Francisco, Los Angeles, or Las Vegas rows.

## 3. How are aliases such as NYC/New York/New York City handled?

Alias handling is duplicated and incomplete:

- `TravelRequirements.normalize_place()` canonicalizes `NYC`, `New York`, and `New York City` to `New York City`, and normalizes Boston capitalization.
- `_search()` independently maps only `nyc` and `new york` to `new york city`.
- There is no shared city registry, no state-aware identity, and no aliases for Washington DC or Columbus, OH.

This duplication can drift. Alias ownership should move to the fixture-backed candidate registry; requirements may keep lightweight display normalization, but search support must be resolved by one canonical registry.

## 4. Why does Columbus fail?

The normal API path was executed with `Plan a 3-day trip to Columbus. I like zoos and fried chicken.` The request is sufficient and the planner requests all four searches, but every category returns `NO_RESULTS`, so the budget tool is skipped and the final response is `error` with no itinerary.

The direct causes are:

1. No Columbus rows exist in any of the four fixtures.
2. No Columbus alias or canonical city record exists.
3. `fried chicken` is correctly classified as food, but `zoos` is recorded as an `UNSPECIFIED` specific preference and is not forwarded to attraction search.

A second observed wording, `I like viewing zoo and I love fried chicken`, exposes a broader bounded-parser limitation: it records `viewing zoo` and `i love fried chicken` as unspecified values. That parser behavior is distinct from candidate coverage and should not motivate an ontology or general NLP rewrite in this wave.

## 5. What fields exist on current attraction/hotel/restaurant/transport candidates?

All four fixture kinds use the same fields:

| Field | Present | Notes |
|---|---|---|
| `id` | Yes | Stable category-prefixed string |
| `destination` | Yes | Display city string only |
| `name` | Yes | Candidate label |
| `price` | Yes | Non-negative number |
| `currency` | Implicit | Contract defaults to USD; omitted from current JSON |
| `unit` | Yes | Typed per-person quote unit |
| `tags` | Yes | Exact-match preference tags |
| `rating` | No | Not modeled |
| `review_count` | No | Not modeled |
| `image_url` / image metadata | No | Not modeled |
| `source` | No | Only the enclosing tool result has `source="mock"` |
| `description` | No | Not modeled |
| canonical city/state/category | No | Inferred from file and destination text |

Category-specific duplicate price fields are not necessary: the existing `price` plus typed `unit` already distinguishes night, meal, visit, and day prices. Cuisine/type/mode can remain tags for this controlled dataset unless a later live-provider contract demonstrates a need for dedicated fields.

## 6. Do rating, review count, image, source, description, and tags already exist?

Only tags exist at candidate level. Source exists only at tool-result level and is currently `mock`. Rating, review count, image metadata, and description do not exist in the backend contract, fixture rows, public candidate shape, TypeScript type, or UI.

The existing UI does disclose that demo options and costs are mock estimates. The data itself does not falsely claim Google, Yelp, Booking.com, or any other third-party provider, and the implementation must preserve that policy.

## 7. How do tools filter candidates?

`_search()` currently performs:

1. case-folded exact destination equality after its small New York alias map;
2. optional `price <= max_price` filtering;
3. exact set containment requiring every requested preference to appear in the candidate's tag list;
4. deterministic ascending sort by `(price, id)`.

Consequences:

- Unknown city and known city/no preference match are indistinguishable.
- Plural/synonym variants such as `zoos` versus `zoo` do not match.
- Multi-preference requests use strict AND semantics and can collapse a pool to zero.
- No rating or review signals are available for ordering.

For a deterministic mock system, exact controlled tags plus a very small declared alias normalization is appropriate. Fuzzy matching, embeddings, web search, or LLM ranking would be disproportionate.

## 8. Does the planner receive all candidates, a filtered subset, or only a result?

The `PlannerProtocol.plan()` call happens before tools run. It receives `TravelRequirements` and, on the one allowed repair attempt, a typed `ReplanContext` containing validation violations and the previous itinerary. It emits search requests; it does not receive candidate records.

After tool execution, `compose_draft()` receives the complete filtered list returned by each of the four searches. It deterministically chooses from those arrays. In other words, the post-tool itinerary composer can see multiple candidates, while the pre-tool planner cannot. This separation is intentional in the current graph and should remain for this data-layer wave; provider/LLM candidate ranking is out of scope.

## 9. Where are alternatives lost?

Alternatives are not destroyed by the search layer:

- every filtered candidate remains in `TravelState.tool_results`;
- `project_tools()` includes each result list in `execution.tools[].data`;
- the frontend tool-call card renders every returned name and price.

What is lost is selection semantics. `compose_draft()` retains only candidate names and costs in itinerary activities, not candidate IDs. The public response has no category-level candidate group, no selected flag on options, and no explicit alternatives array. Consumers must guess which raw result was selected, and that guess is unsafe because normal planning rotates attractions/restaurants while hotel/transport take the first row and budget repair changes the strategy.

The correct fix is to retain selected candidate IDs during deterministic composition and project explicit selected/alternative groups without exposing internal graph state.

## 10. Can the public response express selected candidates and alternatives?

Not explicitly today. `PublicToolRecord.data` can serialize the filtered `TravelOption[]`, but it cannot say which options were used. `Itinerary.Activity` has no candidate ID and does not carry rating, review count, tags, image, or source. `PublicExecutionSummary` has no candidate collection.

An additive public model is needed, for example one group per category containing `selected` and `alternatives`, with each option carrying the unified metadata. This preserves compatibility because existing tool data and itinerary fields remain intact.

## 11. Does the frontend have a place to show candidate lists?

Partially. `ToolCallCard.vue` already renders raw search result names and prices under each tool, proving the response data reaches the UI. `ResultsShell.vue` has a stable sequence of panels and can host one compact Candidate Explorer panel without changing the workflow or overall page structure.

The current tool panel is diagnostic rather than decision-oriented: it omits rating, review count, tags, images, preference matches, and selected state. A dedicated compact component is justified once the backend provides stable candidate groups. It should remain display-only and must not introduce booking, maps, live availability, or a redesign.

## 12. What is the smallest clean implementation path?

1. Create one controlled `data/travel/us/cities.json` dataset containing a canonical city registry, aliases, state, and four candidate categories. Preserve all existing Boston/NYC IDs, names, prices, units, and tags; add ten cities through data only.
2. Add one small cached loader/registry that validates the dataset, resolves aliases generically, injects city/category/source context, and returns deterministic typed candidates.
3. Extend `TravelOption` additively with city, state, category, optional rating/review/image/description, candidate-level source, and preference matches. Optional values must remain safe to serialize and render.
4. Replace filename-specific search loading with category-based registry queries. Return the explicit stable error code `UNSUPPORTED_CITY_DATA` for any destination outside the controlled dataset while retaining ordinary `NO_RESULTS` for supported cities with no matching candidates.
5. Add only bounded normalization needed for the acceptance query (`zoo`/`zoos` as an activity preference). Record the broader repeated-introducer/parser limitation rather than expanding this wave into general language understanding.
6. During itinerary composition, retain unique selected candidate IDs. Add an allowlisted public `candidate_groups` projection with selected and alternative options; do not expose arbitrary metadata or the entire internal state.
7. Add a compact Candidate Explorer to the existing result flow, showing selected badge, price/unit, rating/review count when present, tags, preference matches, source, and image only when present.
8. Add focused backend and frontend tests, then rerun the complete existing suites plus typecheck, build, and Ruff. Keep Wave 3's one-attempt repair behavior unchanged.

This path uses no network, no new dependency, no database, no city-specific Python branch, and no planner rewrite. Adding a future city consists principally of adding one validated city record to the fixture.

## Explicit non-goals and residual limitations

- The dataset is controlled demo data, not live inventory or advice.
- Ratings and review counts are simulated display metadata and must be labeled as mock/demo, never attributed to a real provider.
- Images may be absent; the model and UI must tolerate that without placeholders that imply live listings.
- Search remains deterministic and tag-based.
- The bounded English extractor is not a general semantic parser. Phrases such as `viewing zoo and I love fried chicken` remain an independently documented parser limitation unless separately authorized.
- The existing pre-tool planner will continue to choose tools and filters; the deterministic post-tool composer will continue to choose candidates.
