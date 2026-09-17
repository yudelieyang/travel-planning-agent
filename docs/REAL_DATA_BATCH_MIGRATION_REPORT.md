# Phase O5 real-data batch migration report

## Scope and outcome

The authoritative registry contains 12 supported cities. Boston, Austin, and Columbus were already
migrated before O5. O5 migrated New York City, Chicago, Washington DC, Miami, Denver, Seattle, San
Francisco, Los Angeles, and Las Vegas. The final manifest has 36 routes: attractions, hotel, and food
for every supported city. Transport is intentionally absent from the manifest and remains the
controlled mock planning allowance.

No runtime architecture changed. `CandidateProvider`, `RealSnapshotProvider`, routing, planner,
semantic processing, itinerary composition, budget calculation, validation, and bounded repair are
unchanged. All O5 work is acquisition data, normalized snapshots, manifest entries, tests, and
documentation.

## Repository safety record

- Branch: `main`.
- HEAD before and after: `08d922ed06e38cc53d803a056a1d3fab57c495a7`.
- `git status --short` line count: 97 before O5, 102 after O5. The repository was intentionally
  dirty; no reset, restore, checkout, clean, stash, rebase, or commit was performed. Git collapses
  the already-untracked `data/travel/` tree, so this count is not the number of O5 artifact files.
- Pre-change SHA-256: manifest
  `08d3239b5cd95a42158fd930e9567f1c0f9dc5ae95f8f76690b4437590b3dd35`, NOTICE
  `472ae3480991f680300dc609802a3b882e18c9f14681ceefc024ec47bcb57848`, migration plan
  `2b4b67a4fc073537c80af0f3cc2e735f87c933e4ac6e5837872cebaf2dfca32e`.

O5 created the acquisition script, baseline report, this report, two parameterized test modules, 27
normalized snapshots, and 27 selected-source artifacts. It modified only the existing migration
manifest, centralized OSM NOTICE, and migration plan within the O5 scope. Pre-existing unrelated
worktree changes were preserved.

## Development-only acquisition workflow

`scripts/acquire_osm_snapshots.py` executes exactly one explicit `(city, category, version)` unit.
It uses a verified administrative relation, provider-global category maps, a descriptive User-Agent,
one network request at a time, and no automatic retries. Broad responses and state files live under
`%TEMP%/travel-planning-agent-osm-o5/{raw,state}` and are not runtime data.

The state machine refuses a completed unit unless `--force-refresh` is explicit. `--resume` reuses a
non-empty raw checkpoint, but refetches a present-but-empty response. Fetch failures record `failed`
state and cannot create a final snapshot. Raw bytes, normalized snapshots, selected-source records,
and state are written to same-directory temporary files, flushed/fsynced, and atomically replaced.
Before the final replace, the normalized temporary snapshot is loaded through the existing
`RealSnapshotProvider` contract.

## Administrative boundaries

| City | OSM relation | Observed name | Admin level | Query strategy |
|---|---:|---|---:|---|
| New York City | 175905 | New York | 5 | relation area |
| Chicago | 122604 | Chicago | 8 | relation area |
| Washington DC | 162069 | District of Columbia | 4 | relation area |
| Miami | 1216769 | Miami | 8 | relation area |
| Denver | 1411339 | Denver | 6 | area for attractions; relation bbox + exact city for hotel/food |
| Seattle | 237385 | Seattle | 8 | relation area |
| San Francisco | 111968 | San Francisco | 6 | relation area |
| Los Angeles | 207359 | Los Angeles | 8 | relation bbox + exact city/full address |
| Las Vegas | 170117 | Las Vegas | 8 | area for attractions; relation bbox + exact city for hotel/food |

Washington DC deliberately uses the actual District of Columbia name and level instead of a generic
city/state assumption. Bbox use was an explicit response to overloaded area indexes; the same
response still had to contain the configured relation identity, and candidate queries required the
exact `addr:city` value.

## Wave execution

1. Wave 1: New York City, Chicago, Washington DC.
2. Wave 2: Miami, Denver, Seattle.
3. Wave 3: San Francisco, Los Angeles, Las Vegas.

After each wave, all new snapshots loaded through the manifest, focused provider/public tests passed,
generic city API smokes preserved baseline totals, and the Boston/Austin/Columbus golden tests stayed
green. Public endpoint 429, 504, DNS, and read-timeout failures were left as failed checkpoints and
resumed explicitly on another public instance. There were no concurrent requests and no automatic
retry loop.

## Data quality summary

All 27 O5 snapshots selected the expected three candidates. Address completeness and required
provider metadata completeness are 81/81. `Metadata` means OSM identity, coordinates, and at least
one provider category ID. Every snapshot uses `osm_attractions_v1`, `osm_hotel_v1`, or
`osm_food_v1`; no city-specific map was created.

| City | Category | Expected/selected | Address | Metadata | Snapshot version | Snapshot SHA-256 | Warning |
|---|---|---:|---:|---:|---|---|---|
| New York City | attractions | 3/3 | 3/3 | 3/3 | `osm_new_york_city_attractions_2026-09-16_v1` | `4caf819a75667a28987db7a9c25366a3fa5d21c51a0420c70bb4094cb955d43a` | none |
| New York City | hotel | 3/3 | 3/3 | 3/3 | `osm_new_york_city_hotels_2026-09-16_v1` | `f5b4ba2884c9eac77bdeb9a9b032ef0ed45c7b6e427fbe8dd4175d08a9e44cbf` | none |
| New York City | food | 3/3 | 3/3 | 3/3 | `osm_new_york_city_food_2026-09-16_v1` | `4a002efa5664dd3f1e71b6c5c7e77aef2a99d514342725e8dbe331657243b02e` | none |
| Chicago | attractions | 3/3 | 3/3 | 3/3 | `osm_chicago_attractions_2026-09-16_v1` | `1941f7a849ae8980f20927fbe02a32f445882dd5e596463e35709e17b78d1b02` | stale replica base timestamp |
| Chicago | hotel | 3/3 | 3/3 | 3/3 | `osm_chicago_hotels_2026-09-16_v1` | `5888ce380c7a91f79a3ccc7fbc0a13baf740ff1cf0f4e253aad125f23505c88e` | none |
| Chicago | food | 3/3 | 3/3 | 3/3 | `osm_chicago_food_2026-09-16_v1` | `33d3a020ccc4f2f6532c53d89167e23d9624863f8305db63dc58775e83c55cb2` | none |
| Washington DC | attractions | 3/3 | 3/3 | 3/3 | `osm_washington_dc_attractions_2026-09-16_v1` | `409f294540cc968f036f9e04eeca5170aca659fadb46009c825c29736b2ecbc1` | stale replica base timestamp |
| Washington DC | hotel | 3/3 | 3/3 | 3/3 | `osm_washington_dc_hotels_2026-09-16_v1` | `1875b6db1eec245d7583108d81d9bafca286128f994a08b12e6ee2bc4c04430d` | none |
| Washington DC | food | 3/3 | 3/3 | 3/3 | `osm_washington_dc_food_2026-09-16_v1` | `ebaa6cb69f8febe4718ad90ae30cd81efe1b14b6e850ca37e5222fb804d33aff` | none |
| Miami | attractions | 3/3 | 3/3 | 3/3 | `osm_miami_attractions_2026-09-16_v1` | `14160915f2e9bb476b7add8d50bf2f16da83a3c928926a1fbfebb275609016f4` | none |
| Miami | hotel | 3/3 | 3/3 | 3/3 | `osm_miami_hotels_2026-09-16_v1` | `60cada3ca2d79bcd0d8b12ec08d768917390787bb409ebce03ecfaf3faff01db` | stale replica base timestamp |
| Miami | food | 3/3 | 3/3 | 3/3 | `osm_miami_food_2026-09-16_v1` | `cb6f946eb6e9665153ba004ba8c84f637febd4071290c8277310e694823f7bcf` | stale replica base timestamp |
| Denver | attractions | 3/3 | 3/3 | 3/3 | `osm_denver_attractions_2026-09-16_v1` | `2e1c600579af68c3ee6ed33d51c462d0334b0553e68adedf36d1366d887f6717` | stale replica base timestamp |
| Denver | hotel | 3/3 | 3/3 | 3/3 | `osm_denver_hotels_2026-09-16_v1` | `0d465f639d52b96b413f25229e5a9d6eb5f2ac8fc2daef453cdadcca9f554fcb` | stale replica base timestamp; bbox fallback |
| Denver | food | 3/3 | 3/3 | 3/3 | `osm_denver_food_2026-09-16_v1` | `6a38fcac0a36a583a6265afdd1d29f32ce2cf83b1625b320d4a34dbc0fe1ff0b` | stale replica base timestamp; bbox fallback |
| Seattle | attractions | 3/3 | 3/3 | 3/3 | `osm_seattle_attractions_2026-09-16_v1` | `f0b39497733fb334c659305b7677b91a451dd5e11c743b8f7d21f93ea21e8235` | stale replica base timestamp |
| Seattle | hotel | 3/3 | 3/3 | 3/3 | `osm_seattle_hotels_2026-09-16_v1` | `d223c615748e5f9c803636e59ce1e359fbf1278b43f3e955265dbcb0735aa1a3` | stale replica base timestamp |
| Seattle | food | 3/3 | 3/3 | 3/3 | `osm_seattle_food_2026-09-16_v1` | `32b5246e7200b43b0d9e695ae655a94200d50dbd3ea16d1a83857b2eaa4574a0` | stale replica base timestamp |
| San Francisco | attractions | 3/3 | 3/3 | 3/3 | `osm_san_francisco_attractions_2026-09-16_v1` | `08868bbe66ca5c3d09ac0c96ff7de401e580c12bc215e8fe9a9bd12f7edcde1d` | stale replica base timestamp |
| San Francisco | hotel | 3/3 | 3/3 | 3/3 | `osm_san_francisco_hotels_2026-09-16_v1` | `333b34f8fc93a5fede77d42cdc7cb581eec8ed9cfdc97f8b293a784456c67713` | stale replica base timestamp |
| San Francisco | food | 3/3 | 3/3 | 3/3 | `osm_san_francisco_food_2026-09-16_v1` | `a2ea285e6ad4c1c80b472bbdc3d03585f204812529e81b07f93d4e805465b361` | one selected POI has no observed cuisine; stale replica |
| Los Angeles | attractions | 3/3 | 3/3 | 3/3 | `osm_los_angeles_attractions_2026-09-16_v1` | `af171ff1039afb5348088b3b7bf22fc40fb5f1222ea304750c77bfbd619fe0be` | stale replica base timestamp; bbox fallback |
| Los Angeles | hotel | 3/3 | 3/3 | 3/3 | `osm_los_angeles_hotels_2026-09-16_v1` | `48e35adb170b9bd6725646c227e0628bc2b17f13df70ead3e6528044c4dd12f1` | stale replica base timestamp; bbox fallback |
| Los Angeles | food | 3/3 | 3/3 | 3/3 | `osm_los_angeles_food_2026-09-16_v1` | `a499f5e23acc28bb72d7dd503f0f0033dc0e2518790d2a1d39d6a53472310841` | bbox fallback |
| Las Vegas | attractions | 3/3 | 3/3 | 3/3 | `osm_las_vegas_attractions_2026-09-16_v1` | `dc7040335694cfea2f91252dcc1468e6d74dbfb5cb6f71a9b833650f658ffad2` | stale replica base timestamp |
| Las Vegas | hotel | 3/3 | 3/3 | 3/3 | `osm_las_vegas_hotels_2026-09-16_v1` | `66006fbc28d75afd207482e44317eec03797ae54e341183f8e5c0744ee356802` | bbox fallback |
| Las Vegas | food | 3/3 | 3/3 | 3/3 | `osm_las_vegas_food_2026-09-16_v1` | `bab6f561e0d21ca2d341c05b8b9e95a6262a0635fa9579edba1fc918d469df27` | bbox fallback |

Snapshot files are under `data/travel/snapshots/openstreetmap/<snapshot-version>/<city>_<category>.json`.
The SHA-256 values above cover the exact committed-format snapshot bytes.

## Acquisition ledger

Selected-source artifacts are under `data/travel/sources/openstreetmap/<snapshot-version>/` with the
same file stem plus `_selected.json`. They contain the exact query, endpoint, boundary identity, raw
temporary path, timestamps, counts, full raw hash, raw byte size, selected source elements, and
duplicate decisions.

| City/category | Acquired UTC | OSM base UTC | Raw bytes | Raw response SHA-256 |
|---|---|---|---:|---|
| New York City/attractions | 2026-09-16T15:49:46Z | 2026-09-16T15:46:55Z | 766782 | `88e51df20e68df38905fcee41d230d2a2339d15aee1631e88921676d8cdcd209` |
| New York City/hotel | 2026-09-16T15:51:37Z | 2026-09-16T15:48:58Z | 372000 | `ba917897a46b734541d2a4ee84ca417dbf67276cd946228ea5428fa586264577` |
| New York City/food | 2026-09-16T15:53:05Z | 2026-09-16T15:49:59Z | 2692579 | `bc56423699f374acad038cd4678ba042f1778bbb8b2b4d54e2b1447e435f97a6` |
| Chicago/attractions | 2026-09-16T15:53:51Z | 2026-07-15T15:22:01Z | 496132 | `9fe314784b468cfcab74fd60dedfb76b5258cc6e62ac2f11c246d641aa0fbcd1` |
| Chicago/hotel | 2026-09-16T20:37:50Z | 2026-09-16T20:35:40Z | 124826 | `10b7f976ad8fa13dfc1a8068eee72b6718e1e27a7108bcfe1b034adc89a78682` |
| Chicago/food | 2026-09-16T20:39:57Z | 2026-09-16T20:37:42Z | 1038763 | `19661e06721f7fc4ff2591effb8cad021f9f7bfed63576e37b7f33826a8fa617` |
| Washington DC/attractions | 2026-09-16T20:41:30Z | 2026-05-06T03:25:00Z | 158159 | `395cd917b43db88dfdda1831545095c7d3ffa68d8005266fb03e76515047f915` |
| Washington DC/hotel | 2026-09-16T20:43:55Z | 2026-09-16T20:40:45Z | 110937 | `3aa64ab615d13b4757357fcdf7fda33d8d2684843a216da57e026fd586413235` |
| Washington DC/food | 2026-09-16T20:44:10Z | 2026-09-16T20:41:48Z | 582428 | `03357c4324f0fcf8cec6d6055d1801c7189cfe9d7ff85407f84f33d12158c917` |
| Miami/attractions | 2026-09-16T20:48:26Z | 2026-09-16T20:45:51Z | 48207 | `3cb52e01f7934659efde77892a64daf2f45a1287fda15b53bb59c249260acdd4` |
| Miami/hotel | 2026-09-16T20:49:27Z | 2026-07-24T11:04:51Z | 43128 | `d6dad17da5cfda01d93f5f5f8f91d1a5e9af7c3d68d0437f7b97d77c19872508` |
| Miami/food | 2026-09-16T20:53:44Z | 2026-05-06T03:25:00Z | 100669 | `f62797aacb2c1b6b30c08b9f5d51483a7caa915137758a59f1f1b6a9c6d48469` |
| Denver/attractions | 2026-09-16T20:54:14Z | 2026-07-15T15:22:01Z | 94102 | `5e597b760b11fb3060ad5a8c33a18268894a350e815304a11ab34f9c94237be0` |
| Denver/hotel | 2026-09-16T21:01:20Z | 2026-07-15T15:22:01Z | 70952 | `c5cd7d333a8cb299bd395f7da560502c90bbfce71a05c2c69c4d7d126bc3ecc0` |
| Denver/food | 2026-09-16T21:15:33Z | 2026-07-15T15:22:01Z | 395738 | `317ac34aab72671355381a7075718ec36691d2310532b47ba6215297bd71a64a` |
| Seattle/attractions | 2026-09-16T21:18:32Z | 2026-07-28T02:16:18Z | 197016 | `b7fa7bf0d4200823684243debc31eef6bcd79f3e70505dd9fa995b3e68732a00` |
| Seattle/hotel | 2026-09-16T21:20:21Z | 2026-07-24T11:04:51Z | 63405 | `2b4e702c7812ff727d35a2684892f95ba42d59a58a639c270bb3300acdc38399` |
| Seattle/food | 2026-09-16T21:20:47Z | 2026-05-31T22:37:44Z | 667623 | `17df094904a36e45b1d2f48f888109968624bce741cb931dc01bad80170f779f` |
| San Francisco/attractions | 2026-09-16T21:25:22Z | 2026-07-28T02:16:18Z | 135292 | `be82b42873d9542e04827f7c7a913a97237f84f8a8b4b3f775102b9ddfa6c95d` |
| San Francisco/hotel | 2026-09-16T21:26:59Z | 2026-07-28T02:16:18Z | 84356 | `543c2b80d0735935c890e525da0d3cea4acab17d95103eb1a7f6d0f45295454c` |
| San Francisco/food | 2026-09-16T21:29:14Z | 2026-06-01T08:52:28Z | 541742 | `a61ebf170a135b47fbf9fc53ad06211e0e3bfccc621dfb9739fdaffd04c2a996` |
| Los Angeles/attractions | 2026-09-16T21:34:48Z | 2026-07-24T11:04:51Z | 47052 | `73f6b07369029b8913a375e25fd1e32ec423a2c3e994e0beb6ebcce58f0f43d1` |
| Los Angeles/hotel | 2026-09-16T21:35:56Z | 2026-07-28T02:16:18Z | 78596 | `57da2500e3895ca8ca9f387f8c388fdf49224a0f18b3dd10ebcbce81ed392ad0` |
| Los Angeles/food | 2026-09-16T21:38:19Z | 2026-09-16T21:35:43Z | 437730 | `0f1082852759ba9cbb4e44288f705d15e94543ed89f56bea576a86d0ba18dac2` |
| Las Vegas/attractions | 2026-09-16T21:38:35Z | 2026-07-24T11:04:51Z | 52259 | `990333e90d960f44b90848e37682a986a6839e97525f39d1dbe539ad39169507` |
| Las Vegas/hotel | 2026-09-16T21:46:59Z | 2026-09-16T21:43:50Z | 33697 | `124a663673fbb6e27d45449b7560c7b1e1f40ea7f5420f45d733bba8f93a325b` |
| Las Vegas/food | 2026-09-16T21:47:28Z | 2026-09-16T21:44:44Z | 117603 | `796507eaaac9a137cd5ca049e458b68f7f294de2c13344344dfac1e232a93deb` |

## Selected POIs

| City | Attractions | Hotels | Restaurants |
|---|---|---|---|
| New York City | 9/11 Memorial & Museum; American Museum of Natural History; Asia Society | Arlo Soho; Arlo Williamsburg; EVEN Hotel | Anixi Mediterranean Vegan Restaurant; Aquavit; Atlantic Grill |
| Chicago | American Writers Museum; A. Philip Randolph Pullman Porter Museum; Balzekas Museum of Lithuanian Culture | Hotel Riu Plaza Chicago; Hyatt Regency Chicago; London House Chicago | Alinea; Calumet Fisheries; Frontera Grill |
| Washington DC | America's Islamic Heritage Museum; Arts and Industries Building; DAR Museum | Conrad Hotel Washington DC; Courtyard Washington, DC Dupont Circle; Grand Hyatt Washington | Bistrot du Coin; Blue Duck Tavern; Bresca |
| Miami | HistoryMiami Museum; Patricia and Phillip Frost Museum of Science; Pérez Art Museum Miami | Doubletree by Hilton Grand Hotel Biscayne Bay; Eurostars Langford; Four Seasons Hotel Miami | Versailles Restaurant; 305 Pizza; Amazonico |
| Denver | American Museum of Western Art; Children’s Museum of Denver at Marsico Campus; Clyfford Still Museum | Embassy Suites by Hilton Denver Downtown Convention Center; Hilton Denver City Center; Hyatt Regency Denver Tech Center | Buckhorn Exchange; La Diabla Pozole Y Mezcal; Acorn |
| Seattle | Burke Museum of Natural History and Culture; Center for Wooden Boats; Chihuly Garden and Glass | Crowne Plaza Seattle Downtown; Fairmont Olympic Hotel; Four Seasons Seattle | Alki Homestead; Annapurna Cafe; Café Campagne |
| San Francisco | Asian Art Museum of San Francisco; Cable Car Powerhouse and Barn; California Academy of Sciences | Four Seasons; Grand Hyatt San Francisco; Hilton San Francisco Financial District | A16; Greens Restaurant; John's Grill Live Jazz |
| Los Angeles | Academy Museum of Motion Pictures; Autry Museum of the American West; California Science Center | DoubleTree by Hilton Hotel Los Angeles Downtown; Fairmont Century Plaza; H Hotel Los Angeles, Curio Collection by Hilton | Astro Family Restaurant; Bavel; Bottega Louie |
| Las Vegas | Discovery Children's Museum; Las Vegas Natural History Museum; Neon Museum | La Quinta Inn & Suites; AC Hotel by Marriott Las Vegas Symphony Park; Best Western Plus Las Vegas West | Carson Kitchen; Heart Attack Grill; Weera Thai |

No selected-source artifact recorded a likely duplicate among the final candidates. The selector did
not need to discard a same-name near duplicate in these 27 units. Provider cuisine/diet metadata is
copied only from observed tags; the missing cuisine for John's Grill Live Jazz remains missing.

## Preserved planner behavior

- All 81 O5 internal IDs, prices, USD currency values, units, preference tags, and default order
  exactly match the pre-migration controlled fixture.
- Real names replace mock names, but selected IDs, alternatives, nine generic three-day budget
  totals, validation outcomes, and zero-repair behavior are unchanged.
- `cost_origin=planner_estimate`, the existing legacy cost method, and `phase_o_v1` are present on
  every migrated candidate. OSM is not represented as a price source.
- Ratings and review counts are absent/null for every migrated real candidate. Hotel stars remain
  provider metadata and are never converted into application ratings.
- Boston golden behavior, Austin's 394 → 317 one-attempt repair, and Columbus preference/hard
  constraint behavior remain dedicated golden regressions.

## Manifest and attribution

`migration_manifest.json` is version `osm_us_migrations_v5` and contains exactly 36 unique real
routes. Its eager loader validates every declared file, city, category, OSM identity, coordinate,
record count, unit, provenance field, and duplicate provider identity; a bad declared route fails
provider construction instead of falling back to mock. Attribution remains centralized in the
existing `NOTICE.md`: © OpenStreetMap contributors, ODbL.

## Known limitations and remaining risks

- Several public replicas returned an older OSM base timestamp than acquisition time. The exact base
  timestamp is preserved above; snapshots are frozen demonstrations, not current availability data.
- Public Overpass instances can return 429/504, DNS failures, or timeouts. The workflow is resumable,
  but refreshes remain an explicit developer operation.
- OSM does not provide application ratings, review counts, live prices, reservations, or guaranteed
  current opening status. Those fields are intentionally absent.
- Exact-city address filters improve boundary quality but can omit valid POIs with incomplete OSM
  address tags. Quality was preferred over famousness and the expected candidate count was still met.
- The acquisition cache is temporary and is not a long-term archival system; raw hashes and selected
  source records are retained for reproducibility.

## Final regression

- Focused Wave 3/provider/public/acquisition/batch suite: 137 passed.
- Final batch migration suite, including 36 per-route missing-file fail-closed cases: 83 passed.
- Full backend: 631 passed, 3 expected xfails, one existing Starlette deprecation warning.
- Ruff: passed.
- Frontend: 53 passed.
- Vue/TypeScript typecheck: passed.
- Production Vite build: passed.
- `git diff --check`: passed (Git emitted existing LF→CRLF working-copy notices only).
- Production runtime scan found no acquisition-script import, Overpass endpoint, or `urllib.request`
  acquisition client under `backend/app` or `frontend/src`.

## Final smoke matrix

Each request used the final `osm_us_migrations_v5` manifest explicitly. `real_ok` requires a real
OSM provider identity, usable address, valid coordinates, and planner-estimate cost provenance for
all selected and alternative POIs. Every row returned HTTP 200, validation `passed`,
`snapshot/snapshot/snapshot/mock`, and `real_ok=true`.

| City/scenario | Total USD | Repair attempts | Selected attraction / hotel / restaurant |
|---|---:|---:|---|
| New York City generic 3-day | 520 | 0 | Asia Society / Arlo Soho / Anixi Mediterranean Vegan Restaurant |
| Chicago generic 3-day | 433 | 0 | Balzekas Museum of Lithuanian Culture / Hotel Riu Plaza Chicago / Calumet Fisheries |
| Washington DC generic 3-day | 445 | 0 | America's Islamic Heritage Museum / Conrad Hotel Washington DC / Bistrot du Coin |
| Miami generic 3-day | 456 | 0 | Pérez Art Museum Miami / Doubletree by Hilton Grand Hotel Biscayne Bay / Versailles Restaurant |
| Denver generic 3-day | 411 | 0 | Clyfford Still Museum / Embassy Suites by Hilton Denver Downtown Convention Center / Buckhorn Exchange |
| Seattle generic 3-day | 466 | 0 | Chihuly Garden and Glass / Crowne Plaza Seattle Downtown / Alki Homestead |
| San Francisco generic 3-day | 536 | 0 | California Academy of Sciences / Four Seasons / A16 |
| Los Angeles generic 3-day | 495 | 0 | California Science Center / DoubleTree by Hilton Hotel Los Angeles Downtown / Astro Family Restaurant |
| Las Vegas generic 3-day | 415 | 0 | Neon Museum / La Quinta Inn & Suites / Carson Kitchen |
| Boston golden 2-day | 223 | 0 | Boston Public Garden / Boston Harbor Hotel / Aceituna Grill |
| Austin bounded repair | 317 | 1 | Zilker Park / Hilton Austin / Veracruz All Natural |
| Columbus preference/hard constraint | 343 | 0 | Scioto Audubon Metro Park / Days Inn by Wyndham Columbus Fairgrounds / Jerky's Jamaican Grill |

The Austin dedicated regression additionally confirms the unchanged 394 → 317 trajectory, one
repair attempt, and passed validator. The Columbus dedicated regression confirms the unchanged zoo
and fried-chicken planner tags, $400 hotel ceiling, ranking, budget, and zero repair attempts.
