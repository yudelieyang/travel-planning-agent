# Real Candidate Data Migration Plan

## Scope

Phase O migrates candidate identity and provenance from controlled fixtures to versioned real-place
snapshots. It does not redesign requirements extraction, planner decisions, itinerary composition,
budget formulas, validation, or bounded repair. Normal execution and tests remain offline.

Phase O2 added the provider seam, local snapshot contract, provenance fields, configuration, and
validation. Phase O3A-OSM uses that seam for the first real-place pilot; there is still no live
runtime provider.

## Phase O3A-OSM Boston attractions pilot

The first real snapshot uses OpenStreetMap because the two FSQ attempts had no authorized credential
or official local slice. FSQ remains a possible future provider or enrichment source; its design work
was not removed.

One sequential POST was successfully sent to `https://overpass-api.de/api/interpreter` for one-time
acquisition at `2026-09-16T05:36:07.2890118Z` (OSM base timestamp
`2026-09-16T05:34:00Z`). The query first resolved the Boston admin-level 8 relation inside the
Massachusetts admin-level 4 area, then returned named museum, attraction, zoo, aquarium, park, and
selected historic objects with center coordinates and tags. It returned 713 elements. Overpass is
not called by application startup, request handling, or tests.

Three non-duplicate candidates with complete observed addresses and category diversity were selected:

| Internal ID | OpenStreetMap identity | Name | Observed category | Planner estimate |
|---|---|---|---|---|
| `bos-a1` | `way/29650851` | Isabella Stewart Gardner Museum | `tourism=museum` | USD 20/person/visit |
| `bos-a2` | `way/29660091` | New England Aquarium | `tourism=aquarium` | USD 15/person/visit |
| `bos-a3` | `way/23787885` | Boston Public Garden | `leisure=park` | USD 0/person/visit |

Observed `addr:*` components were joined without inventing missing values. Way center coordinates came
from Overpass `out center tags`. Ratings, review counts, images, and provider prices remain absent.
The retained source selection is
`data/travel/sources/openstreetmap/osm_boston_attractions_2026-09-16_v1/boston_attractions_selected.json`;
the runtime snapshot is
`data/travel/snapshots/openstreetmap/osm_boston_attractions_2026-09-16_v1/boston_attractions.json`.

The versioned category mapping is `data/travel/snapshots/openstreetmap/category_map_v1.json`
(`osm_attractions_v1`). The cost method is
`legacy_demo_cost_preserved_for_phase_o_migration`, version `phase_o_v1`. Prices are project planner
estimates, not OSM admission or ticket prices.

© OpenStreetMap contributors. The OSM-derived location data is available under the Open Database
License (ODbL); repository-specific acquisition and transformation details are in
`data/travel/snapshots/openstreetmap/NOTICE.md`.

Verification on 2026-09-16:

- focused provider/public-projection tests: 51 passed;
- full backend: 508 passed, 3 expected failures;
- Ruff: passed;
- frontend: 51 passed;
- Vue/TypeScript typecheck and production build: passed;
- local snapshot-mode API smoke: HTTP 200, total USD 223, validation passed, attractions from the
  OSM snapshot, and hotel/food/transport from controlled fixtures.

## Phase O3B Boston hotels pilot

One sequential POST to `https://overpass-api.de/api/interpreter` acquired the hotel source at
`2026-09-16T06:26:35.9245460Z` (OSM base timestamp `2026-09-16T06:23:21Z`). The query reused the
Massachusetts → Boston administrative-area resolution and returned named `tourism=hotel` nodes,
ways, and relations with center coordinates and tags. It returned 112 elements and deliberately
excluded hostel, motel, guest house, apartment, and bed-and-breakfast categories.

| Internal ID | OpenStreetMap identity | Name | Observed address | Planner estimate |
|---|---|---|---|---|
| `bos-h1` | `node/1325873780` | Boston Harbor Hotel | 70 Rowes Wharf, Boston, MA 02110 | USD 100/person/night |
| `bos-h2` | `node/2350330785` | The Eliot Hotel | 370 Commonwealth Avenue, Boston, MA 02115 | USD 130/person/night |
| `bos-h3` | `relation/63916` | Four Seasons Hotel Boston | 200 Boylston Street, Boston, MA 02116 | USD 220/person/night |

All three have `tourism=hotel`, usable provider addresses, and valid node or returned relation-center
coordinates. Inspection found no same-name object or other `tourism=hotel` object within the local
duplicate check radius, so no competing representation was retained. OSM `stars=*`, if present in a
future record, remains provider metadata and is never projected into the application's rating field.

The normalized snapshot is
`data/travel/snapshots/openstreetmap/osm_boston_hotels_2026-09-16_v1/boston_hotels.json`; selected
source records are retained under
`data/travel/sources/openstreetmap/osm_boston_hotels_2026-09-16_v1/boston_hotels_selected.json`.
The mapping is `osm_hotel_v1` in
`data/travel/snapshots/openstreetmap/category_map_hotel_v1.json`.

Legacy tags attached to `bos-h1/h2/h3` are retained solely as deterministic planner preference
metadata. They are not OSM claims. Prices likewise remain project estimates using
`legacy_demo_cost_preserved_for_phase_o_migration`, version `phase_o_v1`, with units unchanged at
USD per person per night.

O3B verification on 2026-09-16:

- focused provider/public-projection tests: 55 passed;
- candidate/tool/API/repair/invariant subset: 89 passed;
- full backend: 512 passed, 3 expected failures;
- Ruff: passed;
- frontend: 52 passed;
- Vue/TypeScript typecheck and production build: passed;
- established Boston smoke: HTTP 200, total USD 223, validation passed, zero repair attempts;
- hotel-ceiling smoke: USD 520 hotel total / 2 travelers / 2 nights produced a USD 130
  per-person/night ceiling and retained only `bos-h1` and `bos-h2`;
- runtime source sequence: snapshot, snapshot, mock, mock for attraction, hotel, food, transport.

## Phase O3C Boston restaurants pilot

One sequential POST to `https://overpass-api.de/api/interpreter` acquired the restaurant source at
`2026-09-16T12:07:21.4405410Z` (OSM base timestamp `2026-09-16T12:04:06Z`). The query reused the
Massachusetts → Boston administrative-area resolution and returned 868 named
`amenity=restaurant` nodes, ways, and relations with center coordinates and tags. There were no
request retries and application runtime remains fully offline.

| Internal ID | OpenStreetMap identity | Name | Observed address | Observed cuisine | Planner estimate |
|---|---|---|---|---|---|
| `bos-f1` | `node/12663666560` | Aceituna Grill | 267 Newbury Street, Boston, MA 02116 | `mediterranean` | USD 16/person/meal |
| `bos-f2` | `node/7775144117` | India Quality | 484 Commonwealth Avenue, Boston, MA 02215 | `indian` | USD 20/person/meal |
| `bos-f3` | `node/4418932490` | Atlantic Fish | 761 Boylston Street, Boston, MA 02116 | `seafood` | USD 30/person/meal |

All three records have complete observed addresses and valid node coordinates. Same-name and local
proximity inspection found India Quality and Atlantic Fish unique. Aceituna Grill has another Boston
branch, but it is a distinct place at different coordinates; the selected Newbury Street branch has
the complete address and cuisine/diet metadata. No duplicate representation was retained.
The retained coordinates are `42.3495341, -71.0834556` (Aceituna Grill),
`42.3485475, -71.0942315` (India Quality), and `42.3492931, -71.0811812` (Atlantic Fish).

The normalized snapshot is
`data/travel/snapshots/openstreetmap/osm_boston_food_2026-09-16_v1/boston_food.json`; selected source
records and the exact query are retained under
`data/travel/sources/openstreetmap/osm_boston_food_2026-09-16_v1/boston_food_selected.json`.
The mapping is `osm_food_v1` in
`data/travel/snapshots/openstreetmap/category_map_food_v1.json`. Semicolon-separated OSM cuisine
values are split, trimmed, lowercased, and de-duplicated while preserving order; a missing cuisine is
omitted rather than invented.

The snapshot version is `osm_boston_food_2026-09-16_v1` and its SHA-256 is
`59233fafa3a4aea4afa773aa40ac606ef2e99122fce86f37e173f9d77df1cdf8`. The existing migration
manifest now declares `(Boston, food)` against that file; no provider or router branch was added.

OSM cuisine/diet fields remain provider-observed metadata. Legacy `vegetarian`, `vegan`, and
`seafood` tags are retained separately and visibly labeled as deterministic planner preference
metadata. Prices are not observed menu prices: they preserve the legacy values and IDs through
`legacy_demo_cost_preserved_for_phase_o_migration`, version `phase_o_v1`. Ratings, review counts,
images, provider prices, menus, reservations, and live availability remain absent. Real restaurant
identity and location do not imply real menu pricing; a planner estimate is not an OpenStreetMap
price.

O3C verification on 2026-09-16:

- focused provider/public-projection tests: 62 passed;
- candidate/provider/tool/API/budget/repair/invariant subset: 167 passed;
- full backend: 519 passed, 3 expected failures;
- Ruff: passed;
- frontend: 53 passed;
- Vue/TypeScript typecheck and production build: passed;
- `git diff --check`: passed (existing line-ending warnings only);
- runtime source scan across `backend` and `frontend`: zero Overpass references;
- established Boston smoke: HTTP 200, total USD 223, validation passed, zero repair attempts;
- preference smoke (`vegetarian`): `bos-f1` and `bos-f2` retained their preference matches and
  selection order, with the same USD 223 total;
- runtime source sequence: snapshot, snapshot, snapshot, mock for attraction, hotel, food,
  transport.

## Phase O4A Austin POI migration and repair regression

### Controlled baseline

The authoritative pre-migration Austin fixture contained:

| Category | ID | Controlled name | Planner estimate / unit | Legacy planner tags |
|---|---|---|---|---|
| attractions | `aus-a1` | Mock Texas Art Hall | USD 19/person/visit | museums, art |
| attractions | `aus-a2` | Mock Music History Center | USD 17/person/visit | museums, history, music |
| attractions | `aus-a3` | Mock Springs Park | USD 5/person/visit | parks, outdoors |
| hotel | `aus-h1` | Mock Downtown Budget Lodge | USD 88/person/night | budget, central |
| hotel | `aus-h2` | Mock Hill Garden Inn | USD 120/person/night | quiet |
| hotel | `aus-h3` | Mock Live Music Hotel | USD 205/person/night | luxury, central |
| food | `aus-f1` | Mock Taco Yard | USD 14/person/meal | tacos, local |
| food | `aus-f2` | Mock Hill Country Greens | USD 18/person/meal | vegetarian, vegan |
| food | `aus-f3` | Mock Smokehouse Table | USD 27/person/meal | barbecue, local |
| transport | `aus-t1` | Mock Walking Allowance | USD 0/person/day | walking |
| transport | `aus-t2` | Mock Bus Day Allowance | USD 7/person/day | public transit |
| transport | `aus-t3` | Mock Rideshare Day Allowance | USD 40/person/day | taxi |

Stable search ordering was `a3,a2,a1`, `h1,h2,h3`, `f1,f2,f3`, and `t1,t2,t3`. The established
three-day, one-traveler USD 350 recruiter scenario initially rotated through all three attractions
and food candidates while using `h1` for two nights and `t1` each day. Its USD 394 total violated
`HARD_BUDGET_EXCEEDED` by USD 44. One bounded attempt replaced the rotations with `a3` and `f1`
throughout, producing USD 317, saving USD 77, and passing revalidation.

### One-time acquisition and selected POIs

Three sequential POST requests were sent to `https://overpass-api.de/api/interpreter`; application
runtime and tests never call Overpass. Each query resolved the Texas admin-level 4 area and Austin
admin-level 8 relation before using `nwr` plus `out center tags`.

| Category | Acquired at | OSM base | Query filter | Returned |
|---|---|---|---|---:|
| attractions | `2026-09-16T14:53:48.0538709Z` | `2026-09-16T14:51:00Z` | named museum/attraction/zoo/aquarium, park, historic | 910 |
| hotel | `2026-09-16T14:54:27.8734226Z` | `2026-09-16T14:52:01Z` | named `tourism=hotel` | 213 |
| food | `2026-09-16T14:55:27.4559314Z` | `2026-09-16T14:53:01Z` | named `amenity=restaurant` | 1,101 |

| Internal ID | OSM identity | Real name | Observed address | Coordinates | Planner estimate |
|---|---|---|---|---|---|
| `aus-a1` | `relation/20972967` | Blanton Museum of Art | 200 East Martin Luther King Jr Boulevard, Austin, TX 78705 | 30.2809842, -97.7374171 | USD 19/person/visit |
| `aus-a2` | `way/379207889` | Texas Music Museum | 1011 San Marcos Street, TX | 30.2694425, -97.7306205 | USD 17/person/visit |
| `aus-a3` | `way/946120954` | Zilker Park | Barton Springs Road, AUSTIN, TX 78746 | 30.2676819, -97.7666085 | USD 5/person/visit |
| `aus-h1` | `node/12577833089` | Hilton Austin | 500 East 4th Street, Austin, TX 78701 | 30.2652582, -97.7380600 | USD 88/person/night |
| `aus-h2` | `way/104137285` | Hyatt Regency Austin | 208 Barton Springs Road, Austin, TX 78704 | 30.2607066, -97.7467623 | USD 120/person/night |
| `aus-h3` | `way/134807221` | Four Seasons Hotel Austin | 98 San Jacinto Blvd, Austin, TX 78701 | 30.2616262, -97.7422786 | USD 205/person/night |
| `aus-f1` | `way/802335915` | Veracruz All Natural | 2505 Webberville Road, Austin, TX 78702 | 30.2630626, -97.7137458 | USD 14/person/meal |
| `aus-f2` | `way/382491308` | Bouldin Creek Cafe | 1900 South 1st Street, Austin, TX 78704 | 30.2464901, -97.7568002 | USD 18/person/meal |
| `aus-f3` | `way/382368408` | Franklin Barbecue | 900 East 11th Street, Austin, TX 78702 | 30.2701634, -97.7312704 | USD 27/person/meal |

Provider metadata remains separate from planner metadata. Attractions retain observed
`tourism=museum` or `leisure=park`; all hotels retain `tourism=hotel`; restaurants retain
`amenity=restaurant`, observed `cuisine=mexican` or `cuisine=barbecue`, and Bouldin Creek Cafe's
observed vegetarian/vegan diet tags. The legacy tags and all prices above remain deterministic
planner metadata by internal ID and are not attributed to OpenStreetMap.

Same-name and 0.0005-degree proximity inspection found no duplicate representation for eight
selected objects. Veracruz All Natural has another Austin branch, but the retained Webberville Road
way is a distinct, fully addressed branch with observed Mexican cuisine. Nearby food objects have
different names. The broader Zilker Metropolitan Park relation was excluded in favor of the richer,
addressed Zilker Park way. No selected object is marked closed or disused.

### Artifacts, routing, and repair result

The existing mappings are reused unchanged: `osm_attractions_v1`, `osm_hotel_v1`, and
`osm_food_v1`. No Austin-specific mapping or provider branch was added.

| Snapshot/version | SHA-256 |
|---|---|
| `osm_austin_attractions_2026-09-16_v1/austin_attractions.json` | `3e9b938b3bbe26306d1c450fa715bc4ce90d0ce281d49dab5fa2b6d98a836649` |
| `osm_austin_hotels_2026-09-16_v1/austin_hotels.json` | `873e0c7d5af9abedc98d356b0f5eceb393e4160d881d02d5a8c5fd91ae5007be` |
| `osm_austin_food_2026-09-16_v1/austin_food.json` | `5b53991ce3e09e97e022059ca618a85f1a18f740aadd6a8d8632ca792848aff8` |

The manifest version is now `osm_us_migrations_v1` and adds Austin attractions, hotel, and food.
Austin transport remains undeclared and routes to the controlled provider. Every declared Austin
route is eagerly validated and fails closed for missing, corrupt, empty, wrong-city, or
wrong-category snapshots.

| Repair evidence | Before migration | After migration |
|---|---|---|
| Initial selected identities | `a3,a2,a1`; `h1`; `f1,f2,f3`; `t1` | same internal IDs, real POI names |
| Initial total / hard limit | USD 394 / USD 350 | USD 394 / USD 350 |
| Violation | `HARD_BUDGET_EXCEEDED`, excess USD 44 | identical |
| Repair target | attractions and food | identical |
| Lower-cost result | `a3` and `f1` throughout | identical internal IDs |
| Repaired total / savings | USD 317 / USD 77 | USD 317 / USD 77 |
| Attempts / validation | 1 / passed | 1 / passed |

O4A verification on 2026-09-16:

- focused provider/public-projection tests: 69 passed;
- candidate/provider/tool/API/budget/repair/invariant subset: 174 passed;
- full backend: 526 passed, 3 expected failures;
- Ruff: passed;
- frontend: 53 passed;
- Vue/TypeScript typecheck and production build: passed;
- normal Austin snapshot smoke: HTTP 200, USD 394, validation passed, zero repair attempts;
- bounded-repair snapshot smoke: HTTP 200, USD 394 → USD 317, one attempt, validation passed;
- runtime source sequence for both smokes: snapshot, snapshot, snapshot, mock;
- Boston public regression retained its OSM routes and USD 223 budget;
- runtime source scan across `backend` and `frontend`: zero Overpass references;
- `git diff --check`: passed (existing line-ending warnings only).

## Phase O4B: Columbus real POIs and preference regression

O4B migrates Columbus attractions, hotels, and food to immutable OpenStreetMap snapshots. Transport
remains the controlled mock allowance. No candidate-provider, manifest-router, planner, semantic,
validator, budget, or bounded-repair implementation changed.

### Controlled baseline and behavioral contract

The authoritative pre-migration fixture contained five attractions (`cmh-a1`–`cmh-a5`, USD
22/28/18/20/0 per person/visit), four hotels (`cmh-h1`–`cmh-h4`, USD 82/105/135/190 per
person/night), six food rows (`cmh-f1`–`cmh-f6`, USD 14/17/20/18/26/16 per person/meal), and
three transport allowances (`cmh-t1`–`cmh-t3`, USD 0/8/38 per person/day). All attraction rows
carry the legacy `zoo` tag and all food rows carry the legacy `fried chicken` tag. Hotel tags remain
`budget/central`, `quiet/neighborhood`, `central`, and `luxury/quiet` by internal ID.

For the strongest request—three days, one traveler, USD 900 total, hotel total at most USD 400,
with zoo and fried-chicken preferences—the pre-migration contract was:

| Field | Controlled baseline |
|---|---|
| Parsed preferences | activity `zoo`; food `fried chicken` |
| Attraction order | `cmh-a5,a3,a4,a1,a2`; every row matched `zoo` |
| Attraction selected / alternatives | `a5,a3,a4` / `a1,a2` |
| Food order | `cmh-f1,f6,f2,f4,f3,f5`; every row matched `fried chicken` |
| Food selected / alternatives | `f1,f6,f2` / `f4,f3,f5` |
| Hotel ceiling / eligible order | USD 200 per person/night; `h1,h2,h3,h4` |
| Hotel selected / alternatives | `h1` / `h2,h3,h4` |
| Transport selected / alternatives | `t1` / `t2,t3` |
| Breakdown / total | hotel 164, food 141, attractions 38, transport 0; total USD 343 |
| Validator / repair | passed / 0 attempts |

The separate luxury-hotel repair baseline (USD 900 total and USD 300 hotel total, with the test
runner intentionally bypassing the search-time hotel ceiling) performed one bounded repair, changed
the final hotel to `cmh-h1`, produced hotel USD 164 and total USD 290, and passed validation.

### Acquisition and selection

The query first resolved the Ohio `admin_level=4` area, then the Columbus `admin_level=8` relation,
converted it to an area, selected named `nwr` objects, and returned centers and tags. An initial
attraction request with invalid `map_to_area` syntax returned HTTP 400 and wrote no data; the
corrected request is the only successful attraction acquisition. The hotel command did not return
tool output before an early file check, so a retry overlapped the still-running first request. Both
hotel requests succeeded with byte-identical content, the same OSM base timestamp, and the same
SHA-256; the artifact records the final write. Food used one successful request. Raw responses
remained temporary and the selected-source artifacts record their hashes.

| Category | Acquired UTC | OSM base UTC | Query filter | Returned | Raw SHA-256 |
|---|---|---|---|---:|---|
| attractions | 15:20:11 | 15:17:18 | museum, attraction, zoo, aquarium, park, historic | 482 | `7c4ab4122242b654fbf50315aa5f738cc789bb15270595a8bc62a3903bbee23b` |
| hotel | 15:22:28 final write | 15:18:20 | `tourism=hotel` | 140 | `0c9a08b44109c5ba1906713fa55deb2e80150e81118cd6eba4251a2058d6fb78` |
| food | 15:22:39 | 15:19:21 | `amenity=restaurant` | 797 | `cfc1bd1da517f5cffd6831efb457ff8da2523743cfc8097ad9f5cb6f04a4e6ca` |

| Internal ID | OSM identity | Selected name | Observed address | Coordinates | Preserved estimate |
|---|---|---|---|---|---|
| `cmh-a1` | `way/32873150` | COSI | 333 West Broad Street, Columbus, OH 43215 | 39.9596650, -83.0065950 | USD 22/person/visit |
| `cmh-a2` | `way/293476179` | Columbus Museum of Art | 480 East Broad Street, Columbus, OH 43215 | 39.9644285, -82.9877520 | USD 28/person/visit |
| `cmh-a3` | `way/835107792` | Ohio History Center | 800 E. 17th Avenue, Columbus, OH 43211 | 40.0050452, -82.9876307 | USD 18/person/visit |
| `cmh-a4` | `way/570391114` | National Veterans Memorial and Museum | 300 West Broad Street, Columbus, OH 43215 | 39.9619805, -83.0080526 | USD 20/person/visit |
| `cmh-a5` | `way/224492486` | Scioto Audubon Metro Park | 400 Whittier Street, Columbus, OH | 39.9470771, -83.0065835 | USD 0/person/visit |
| `cmh-h1` | `way/717324868` | Days Inn by Wyndham Columbus Fairgrounds | 1700 Clara Avenue, Columbus, OH 43211 | 39.9998016, -82.9857381 | USD 82/person/night |
| `cmh-h2` | `way/474605329` | Holiday Inn Express | 650 South High Street, Columbus, OH 43215 | 39.9488541, -82.9973137 | USD 105/person/night |
| `cmh-h3` | `node/4685223268` | Hampton Inn & Suites Columbus Downtown | 501 North High Street, Columbus, OH 43215 | 39.9724764, -83.0028760 | USD 135/person/night |
| `cmh-h4` | `node/1376126720` | The Westin Great Southern Columbus | 310 South High Street, Columbus, OH 43215 | 39.9558079, -82.9991240 | USD 190/person/night |
| `cmh-f1` | `node/8343623182` | Jerky's Jamaican Grill | 1247 North High Street, Columbus, OH 43201 | 39.9878053, -83.0058345 | USD 14/person/meal |
| `cmh-f2` | `node/8481484417` | Feed Me! Sandwich Kings! | 1053 East Main Street, Columbus, OH 43205 | 39.9577160, -82.9711763 | USD 17/person/meal |
| `cmh-f3` | `node/8561182617` | The Crispy Coop | 1717 Northwest Boulevard | 39.9932641, -83.0421042 | USD 20/person/meal |
| `cmh-f4` | `node/9993723530` | CM Chicken | 1132 West Henderson Road, Columbus, OH 43220 | 40.0535621, -83.0506175 | USD 18/person/meal |
| `cmh-f5` | `node/14093010165` | OX-B's | 7370P Sawmill Road, Columbus, OH 43235 | 40.1162563, -83.0900710 | USD 26/person/meal |
| `cmh-f6` | `way/512159964` | BonChon Chicken | 2973 North High Street, Columbus, OH 43202 | 40.0226892, -83.0141229 | USD 16/person/meal |

Selected identities are unique and have no same-object duplicate among the retained rows. Multiple
chain or same-theme restaurants in the returned pool were treated as distinct branches only when
their OSM identity and coordinates differed. No closed/disused object was selected. OSM names,
addresses, coordinates, `tourism`, `leisure`, `amenity`, and `cuisine` values are provider facts;
prices, units, and legacy tags are planner metadata.

The Columbus boundary returned no `tourism=zoo` object. Consequently, the attraction snapshot
truthfully exposes four `tourism=museum` facts and one `leisure=park` fact, while the `zoo` tags used
for deterministic matching remain separately labeled planner preference tags. For food, only
`cmh-f1` has observed `cuisine=fried_chicken`; the other five expose only their observed broader
values such as `chicken`, `american`, or `korean`. All six retain the separate legacy `fried chicken`
planner tag. Names were not used to invent cuisine.

The existing provider-global maps `osm_attractions_v1`, `osm_hotel_v1`, and `osm_food_v1` were
reused unchanged. No Columbus-specific mapping was added because the retained provider taxonomy was
already represented.

### Artifacts, routing, and regression result

| Artifact | SHA-256 |
|---|---|
| `osm_columbus_attractions_2026-09-16_v1/columbus_attractions.json` | `39c118b45fbc62b168e7eef29c8d85d2105faf26cfa44e74fd003c5c3bbbcdc9` |
| `osm_columbus_hotels_2026-09-16_v1/columbus_hotels.json` | `58c2c3fe84941eeb1d32a1b2f038c6f1952a39f204c482b63b71931c184cfcc2` |
| `osm_columbus_food_2026-09-16_v1/columbus_food.json` | `27cb785e81a9ccd9ebc5d1045b3dea4ec9f04c28221b6729ff415f6d68e58976` |
| selected attractions source | `cc6278a1c5d760959c7f134e664bb461c9012685a13f8b8f2de01303950de35d` |
| selected hotels source | `5dbbb2cf49ed3b088ea9e2e116dabbd52a41fbf44470cba31a81c84fd4a4344e` |
| selected food source | `080b05177735b030c30525eacd22dbd8fb2a99156ed80d407968818456df9c39` |

Manifest `osm_us_migrations_v2` adds exactly three Columbus routes. Columbus transport remains
undeclared and controlled. Missing, corrupt, empty, wrong-city, and wrong-category variants of each
declared Columbus route fail closed.

| Regression field | Before mock | After OSM snapshot |
|---|---|---|
| Parsed preferences and hard constraints | zoo, fried chicken; total 900; hotel total 400 | identical |
| Eligible/sorted internal IDs | attraction `a5,a3,a4,a1,a2`; hotel `h1,h2,h3,h4`; food `f1,f6,f2,f4,f3,f5` | identical |
| Selected and alternatives | as baseline table | identical internal IDs |
| Preference matches | every attraction `zoo`; every food row `fried chicken` | identical |
| Selected costs / three-meals rule | attractions 38; hotel 164; food 141 | identical |
| Total / validator / repairs | USD 343 / passed / 0 | identical |
| Luxury hotel repair | USD 290; `h1`; 1 attempt; passed | identical |

O4B verification on 2026-09-16:

- focused provider/public-projection tests: 87 passed;
- candidate/provider/tool/API/preference/budget/repair subset: 198 passed, 3 expected failures;
- full backend from repository root: 544 passed, 3 expected failures;
- Ruff: passed;
- frontend: 53 passed;
- Vue/TypeScript typecheck and production build: passed;
- normal and preference snapshot smokes: HTTP 200, USD 343, validation passed, zero repairs;
- both smoke source sequences: snapshot, snapshot, snapshot, mock;
- both smoke runs used real names/addresses/coordinates and made zero external network calls;
- luxury-hotel repair: USD 290, hotel USD 164, `cmh-h1`, one attempt, passed;
- Boston public regression and Austin USD 394 → USD 317 bounded repair regression passed;
- runtime OSM acquisition reference scan: zero;
- `git diff --check`: passed (existing line-ending warnings only).

Known limitations are that OSM is a point-of-interest source rather than an availability or pricing source, the selected
`cmh-f3` object has only the observed street address components, and the city-boundary query cannot
represent the Columbus Zoo outside that administrative boundary. Those limitations do not alter
planner behavior and are not filled with guessed facts.

## Current architecture

The current working-tree path is:

```text
data/travel/us/cities.json
  -> load_candidate_dataset()
  -> CandidateDataset / CityFixture / CandidateFixture
  -> resolve_city()
  -> candidates_for()
  -> TravelOption
  -> search tools
  -> compose_draft()
  -> candidate_groups
  -> CandidateExplorer.vue
```

`data/travel/us/cities.json` remains the authoritative controlled fixture and city/alias registry.
It contains 12 supported US cities and four candidate categories. `resolve_city()` and
`city_at_start()` remain compatible because frozen requirements code calls them directly.

`candidates_for()` remains the compatibility facade and sole owner of hard price filtering,
preference matching, and stable ordering by preference-match count, price, and ID. Providers supply
normalized candidates; they do not rank or select them.

Snapshot mode now loads `data/travel/snapshots/openstreetmap/migration_manifest.json`. The manifest
explicitly owns attractions, hotel, and food for Boston, Austin, and Columbus, each pointing to its
own `RealSnapshotProvider`. Transport for all three cities remains unlisted and therefore routes explicitly
to `MockFixtureProvider`. Every listed snapshot is eagerly validated; a missing, corrupt, empty, or
route-incompatible file fails service construction and never falls back to mock. Adding another city
or POI category requires a snapshot, a reusable or new mapping, and a manifest entry, not another
routing redesign.

## Cost semantics

Candidate price semantics remain unchanged:

| Category | Quote unit |
|---|---|
| `hotel` | USD per person per night |
| `food` | USD per person per meal |
| `transport` | USD per person per day allowance |
| `attractions` | USD per person per visit |

The composer still schedules three meals, one attraction, and one transport allowance per day, plus
`days - 1` hotel nights. The deterministic budget calculator still sums per-person items and applies
party size once. Phase O providers cannot change these formulas or claim a provider supplied a price
when it is a planner estimate.

## Frozen boundaries

The following behavior is frozen:

- `requirements.py`, `semantic_coverage.py`, `semantic_merge.py`, and `semantic_extractor.py`;
- `planner.py`, `prompts.py`, and `openai_planner.py`;
- `itinerary.py` and `graph.py`;
- semantic benchmarks, datasets, and results;
- candidate ranking and selection;
- budget formulas and validator semantics;
- bounded-repair triggers and the one-attempt limit;
- the signatures and behavior of `resolve_city()` and `city_at_start()`.

## Provider architecture

```text
search tool
  -> candidates_for()                 compatibility and search policy
      -> CandidateProvider.candidates()
          -> MockFixtureProvider      current controlled fixture
          -> RealSnapshotProvider     validated local JSON only
      -> TravelOption[]
```

`CandidateProvider` exposes one operation because that is all the existing path needs. The mock
provider wraps the current fixture without copying it. The snapshot provider eagerly reads and
validates one local file and performs no network operation. A live provider is intentionally absent;
when justified, it should be a separate snapshot-refresh path rather than a default request-time
dependency.

## Normalized candidate contract

Existing identity, selection, and cost fields remain intact. Phase O adds optional fields so mock rows
need no fake values:

- place: `address`, `latitude`, `longitude`;
- provider: `provider`, `provider_place_id`, provider category IDs/labels,
  `provider_refreshed_at`;
- snapshot: `snapshot_version`, `snapshot_fetched_at`;
- cost: `cost_origin`, `cost_method`, `cost_version`.

Optional Phase O fields are omitted from serialized mock candidates when null, preserving the current
mock response shape. A real snapshot candidate must carry provider identity, snapshot identity, and
cost provenance.

## Observed data versus estimates

Provider-observed fields are name, address, coordinates, provider identity, provider category
metadata, and provider refresh time. Snapshot version and fetch time describe the local artifact.

Price, currency, unit, preference tags, `cost_origin`, `cost_method`, and `cost_version` belong to the
planner/demo estimation layer. For Phase O snapshots `cost_origin` must be `planner_estimate`.
Provider-observed prices are not part of the O2 contract.

## Provenance semantics

The four provenance concepts remain distinct:

1. `ToolResult.source`: which execution data path served the search (`mock` or `snapshot`);
2. `TravelOption.source`: candidate data source (`controlled_mock_fixture` or `real_snapshot`);
3. provider/snapshot fields: external identity and local artifact version;
4. cost fields: origin and version of the planner estimate.

They must not be collapsed into one ambiguous source label.

## Snapshot strategy and format

Snapshots are immutable, versioned JSON artifacts stored under a future directory such as:

```text
data/travel/snapshots/<provider>/<snapshot-version>/<city>.json
```

Each artifact declares `snapshot_version`, timezone-aware `snapshot_fetched_at`, `provider`, source,
and one or more canonical registered cities. A city explicitly declares only its migrated categories;
every declared category must contain at least one candidate. Snapshot mode never downloads or
refreshes data.

## Validation and failure policy

Snapshot loading fails closed for:

- duplicate internal IDs;
- duplicate `(provider, provider_place_id)` identities;
- blank names or provider identifiers;
- missing, non-finite, out-of-range, or unpaired coordinates;
- unsupported categories or cities;
- malformed provider/source or snapshot versions;
- timestamps without timezone information;
- negative or non-finite prices;
- category/unit mismatches;
- missing or non-planner cost provenance;
- empty declared migrated categories.

A corrupt snapshot raises a provider-boundary error. The system never silently switches a declared
migrated category to mock data.

## Mode selection

`CANDIDATE_DATA_MODE` accepts `mock` or `snapshot` and defaults to `mock`. Snapshot mode requires
`CANDIDATE_SNAPSHOT_PATH`, which may identify the migration manifest or a legacy single snapshot.
The manifest and every listed snapshot are eagerly validated when the travel service is created.

The recruiter-demo acceptance target is `snapshot`; `mock` remains the deterministic CI and
regression fallback. Migrated category coverage is explicit and failures never fall back silently.

## Rollout order

1. Boston attractions (completed by Phase O3A-OSM).
2. Boston hotels (completed by Phase O3B with unchanged planner-estimated cost semantics).
3. Boston food (completed by Phase O3C with cuisine and planner tags kept distinct).
4. Austin (completed by Phase O4A with identical bounded-repair trajectory and totals).
5. Columbus (completed by Phase O4B with identical preference ranking and hard constraints).
6. Batch-migrate New York City and the remaining supported cities in reviewable groups.

Transport is an exception: walking, transit, taxi, and rideshare rows are planning allowances rather
than POIs. They remain synthetic estimated candidates and must not be presented as FSQ-observed
places.

## Testing strategy

- compare the explicit mock provider with the default `candidates_for()` facade;
- load a valid local snapshot and assert normalized provenance;
- reject each malformed identity, location, timestamp, category, cost, and city case;
- test default mock and explicit snapshot mode selection;
- prove corrupt snapshot mode does not fall back to mock;
- run existing candidate, tool, API, planner, validation, repair, and semantic regression tests;
- run Ruff without changing benchmark expectations;
- keep all ordinary tests free of external network calls.

## Rollback plan

Set `CANDIDATE_DATA_MODE=mock` and restart the service. Because planner, composer, budget, validation,
repair, and the authoritative mock fixture remain unchanged, rollback does not require code or data
conversion. A broken snapshot must be fixed or replaced rather than bypassed through implicit
fallback.

## Acceptance criteria

- Existing mock candidate values, ordering, selection, costs, validation, and repair are unchanged.
- `candidates_for()` remains compatible with all existing callers.
- Both provider implementations emit `TravelOption` objects through the same search policy.
- Real snapshots are local-only, versioned, provenance-complete, and strictly validated.
- Mock responses do not gain fake real-place fields.
- Default execution remains deterministic and offline.
- No frozen semantic, planner, validator, or repair behavior is modified.
- Phase O3 can insert Boston snapshot POIs without changing downstream planning contracts.

## Phase O5: multi-city batch migration

Phase O5 completed the frozen-architecture rollout for the nine remaining registered cities: New
York City, Chicago, Washington DC, Miami, Denver, Seattle, San Francisco, Los Angeles, and Las
Vegas. Attractions, hotels, and restaurants now route through 27 additional local OpenStreetMap
snapshots. Together with Boston, Austin, and Columbus, the manifest contains 36 real POI routes.
Transport remains deliberately synthetic and unlisted.

The development-only `scripts/acquire_osm_snapshots.py` workflow accepts one explicit city,
category, and acquisition version. It stores broad raw responses and per-unit checkpoints under the
system temporary directory, writes selected-source provenance beside each repository snapshot, and
validates the normalized temporary snapshot with `RealSnapshotProvider` before an fsync-backed
atomic replace. Completed units refuse another request by default; `--resume` reuses a non-empty raw
checkpoint, while `--force-refresh` is required to replace a completed unit. The script is not
imported by runtime code and is never invoked by application startup or tests.

Acquisition ran in three waves. Each wave passed focused provider/public execution regression and a
representative API smoke before the next began. Exact relation IDs, boundary names, and admin
levels were verified from each response. Area-index timeouts for Denver, Los Angeles, and Las Vegas
were handled with exact relation bounding boxes plus exact city-address filters; no loose name-only
city lookup was used. Public endpoint 429/504/timeouts were recorded as failed checkpoints and
resumed explicitly, without automatic retry loops or concurrent requests.

All existing internal IDs, planner prices, currency, quote units, preference tags, ordering,
selection, alternatives, budgets, validator outcomes, and repair semantics remain unchanged.
Provider facts are limited to observed OSM identity, name, address, coordinates, and category
metadata. Synthetic ratings/reviews were removed, OSM hotel stars were not converted to ratings,
and one missing San Francisco cuisine tag remains absent rather than inferred. The detailed
artifacts, checksums, selected POIs, quality warnings, and smoke matrix are in
`docs/REAL_DATA_BATCH_MIGRATION_REPORT.md`.
