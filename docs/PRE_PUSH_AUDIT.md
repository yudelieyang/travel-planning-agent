# Phase P2A pre-push repository audit

Audit date: 2026-09-16

Scope: working tree at `main` / `08d922ed06e38cc53d803a056a1d3fab57c495a7`

Action boundary: audit only; no add, commit, push, deletion, cleanup, history rewrite, or production change.

## 1. Repository state

- Branch: `main`.
- HEAD: `08d922ed06e38cc53d803a056a1d3fab57c495a7`.
- Upstream: `origin/main`, up to date before the uncommitted checkpoint.
- Index: empty; `git diff --cached --name-status` returned no entries.
- Expanded porcelain baseline before this report: 194 files, not the 107 directory-collapsed status lines.
- Breakdown: 45 modified, 4 deleted, 145 untracked, 0 renamed.
- Tracked diff: 49 files, 2,751 insertions and 1,115 deletions.
- This report adds one further untracked documentation file after the baseline capture.

## 2. Status-entry classification

The following disjoint path groups cover all 194 baseline entries. Counts were validated against
`git status --porcelain=v1 -uall`; no entry was left unclassified.

| Path/group | Git state | Count | Category | Reason |
|---|---:|---:|---|---|
| `backend/app/**` | 15 M, 6 ?? | 21 | A — MUST COMMIT | Current runtime imports these agent, semantic, provider, API, and configuration modules. |
| `frontend/src/**` | 14 M, 2 ?? | 16 | A — MUST COMMIT | Current recruiter UI, public types, and snapshot provenance presentation. |
| `data/travel/snapshots/openstreetmap/**` | 41 ?? | 41 | A — MUST COMMIT | Required by explicit snapshot mode and preflight. |
| `data/travel/us/cities.json` | ?? | 1 | A — MUST COMMIT | Safe mock default, city registry, estimates, aliases, and synthetic transport baseline. |
| `.env.example`, `.env.demo.example`, `.gitignore`, `README.md` | 3 M, 1 ?? | 4 | B — SHOULD COMMIT | Reproducible safe/default and recruiter-demo setup. |
| `backend/tests/**` | 9 M, 16 ?? | 25 | B — SHOULD COMMIT | Regression, provider, semantic, repair, migration, and preflight evidence. |
| `data/mock/*.json` | 4 D | 4 | B — SHOULD COMMIT | Intentional retirement of duplicate legacy fixtures. |
| `data/travel/sources/openstreetmap/osm_{austin,boston,columbus}_*/**` | 9 ?? | 9 | B — SHOULD COMMIT | Compact selected-source provenance without broad raw responses. |
| `docs/**`, excluding `docs/PROJECT_STATUS_FINAL.md` | 1 M, 19 ?? | 20 | B — SHOULD COMMIT | Architecture, migration, testing, recruiter, and handoff evidence. |
| `evals/datasets/**` | 2 M, 13 ?? | 15 | B — SHOULD COMMIT | Frozen deterministic/live-subset inputs used by tests and evaluation scripts. |
| `frontend/tests/**` | 1 M | 1 | B — SHOULD COMMIT | Recruiter UI and API contract regression coverage. |
| `scripts/**` | 9 ?? | 9 | B — SHOULD COMMIT | Reproducible evaluation, acquisition-development, reporting, replay, and preflight tooling. |
| O5 `data/travel/sources/openstreetmap/**` for the other nine cities | 27 ?? | 27 | C — REVIEW | Correct compact provenance, but each file records a machine-local temporary path. Sanitize before a public checkpoint. |
| `docs/PROJECT_STATUS_FINAL.md` | ?? | 1 | C — REVIEW | Calls itself final but still describes fixture-only data and the old 486/50 verification baseline. Update or omit. |

Category totals for the 194-file baseline: A 79, B 87, C 28, D 0. The new
`docs/PRE_PUSH_AUDIT.md` is an additional B file.

No current status entry is category D. Category-D material exists only among ignored/local files:

- `.env`;
- `.venv/`, `.pytest_cache/`, `.ruff_cache/`;
- `frontend/node_modules/`, `frontend/dist/`;
- `chroma_data/chroma.sqlite3`;
- the timestamped `evals/results/planner-live-*.json` run output.

## 3. Secrets audit

- High-confidence working-tree scan found zero OpenAI-style, GitHub, Hugging Face, AWS, bearer,
  private-key, or certificate credentials in candidate commit files.
- `.env.example` and `.env.demo.example` contain empty API-key fields and the explicit
  `change_me` database placeholder only.
- Local `.env` is present, ignored, untracked, and contains a set OpenAI-style credential. Its value
  was not printed. It MUST NOT be force-added or copied into documentation.
- High-confidence Git-history scans found no matching credential material in committed history.
- The `origin` remote is HTTPS GitHub with no embedded user information.

Conclusion: no secret is present in the proposed checkpoint, provided staging stays explicit and
does not force-add `.env`.

## 4. `.gitignore` audit

Present and effective: `.env`, `.env.*` with explicit example exceptions, `.venv/`, Python bytecode,
pytest/Ruff caches, `node_modules/`, `dist/`, `build/`, package metadata, IDE metadata, `.DS_Store`,
logs, Chroma local contents, and evaluation results by default.

Required project artifacts are not ignored: both OSM trees, `docs/`, recruiter preflight, and OSM
acquisition script are visible to Git. `.env.demo.example` is correctly unignored.

Gaps to address narrowly before the checkpoint:

- `venv/` (without the leading dot);
- `.coverage`, `coverage.xml`, `htmlcov/`;
- Vite cache directories;
- repository-local acquisition `raw/` or `tmp/` directories if they are ever introduced;
- generic local SQLite/database files outside the already-covered `chroma_data/` path.

Do not add an ignore rule covering `data/travel/snapshots/` or `data/travel/sources/`.

Important blocker: 39 files under `evals/results/` are currently ignored. Thirty-eight stable
`hybrid_semantics_*` / `phase_*` evidence files are needed by README links, tests, or replay/report
workflows. The timestamped `planner-live-*` file is the one local run artifact that should remain
ignored. Add narrow exceptions for the 38 frozen artifacts or explicitly force-add exactly those
files; changing `.gitignore` is clearer for future contributors.

## 5. Real-data artifact audit

- Manifest: exactly 36 unique routes.
- Cities: exactly 12.
- Categories: `attractions`, `hotel`, `food` only.
- Transport routes in manifest: 0.
- Every city has exactly three manifest routes.
- Snapshot tree: 41 files, 126,241 bytes total. This includes 36 route snapshots, three category
  maps, the manifest, and NOTICE.
- Selected-source tree: 36 files, 127,948 bytes total.
- No repository data file is 400 KiB or larger.
- No broad raw Overpass response is present in the repository.
- `data/travel/us/cities.json` is 26,172 bytes and intentionally remains the controlled mock,
  regression, alias, estimate, and synthetic-transport baseline.

All data is comfortably suitable for ordinary GitHub storage.

## 6. Attribution audit

`data/travel/snapshots/openstreetmap/NOTICE.md` exists and states:

- `© OpenStreetMap contributors`;
- Open Database License (ODbL);
- snapshot/acquisition provenance;
- absence of OSM-supplied planner prices, ratings, reviews, bookings, and live availability;
- planner estimates are project-generated.

README, migration documentation, and UI consistently distinguish frozen OSM POI facts, planner
estimates, and synthetic transport. No current recruiter surface claims that snapshots are live.

## 7. Legacy mock/deletion audit

The four deleted `data/mock/*.json` files are intentionally superseded by
`data/travel/us/cities.json`. Runtime imports now route through `candidate_data.py`; no runtime or
test reads the deleted paths. Remaining references are historical migration documents that explain
the replacement. Restoring the four files would create stale duplicate sources and is not advised.

## 8. Untracked critical-file audit

Fresh-clone-critical untracked groups include:

- `backend/app/tools/candidate_data.py` and `candidate_providers.py`;
- semantic coverage/extractor/merge and hybrid evaluation modules;
- `CandidateExplorer.vue` and `PerformanceSummary.vue`;
- the complete `data/travel/` runtime tree;
- recruiter preflight and demo configuration;
- tests and frozen datasets.

All are included in categories A/B or the explicit category-C remediation plan. A commit that omits
any category-A group will not reproduce the current working application.

## 9. Generated artifact audit

Local generated material is already ignored:

| Path | Approximate size | Action |
|---|---:|---|
| `.venv/` | 471 MiB | MUST NOT COMMIT |
| `frontend/node_modules/` | 73.5 MiB | MUST NOT COMMIT |
| `frontend/dist/` | 121 KiB | MUST NOT COMMIT |
| `.pytest_cache/` | 81 KiB | MUST NOT COMMIT |
| `.ruff_cache/` | 6 KiB | MUST NOT COMMIT |
| `chroma_data/chroma.sqlite3` | 184 KiB | MUST NOT COMMIT |
| `evals/results/planner-live-*.json` | 10 KiB | MUST NOT COMMIT |

Frozen semantic evaluation results are generated evidence, not disposable build output: current
tests and README depend on them. Commit the 38 stable named artifacts, not the timestamped planner
run.

## 10. Dependency audit

- Backend definitions: tracked `requirements.txt` plus `pyproject.toml`; Python is constrained to
  3.11 and versions are pinned.
- Frontend definitions: tracked `package.json` and `package-lock.json`; Node >=22.18 is declared.
- `pip check`: no broken requirements.
- `npm ls --depth=0`: Vue, Vite, TypeScript, vue-tsc, and the Vue Vite plugin match declared versions.
- No Phase O/P source relies on an undeclared local package.
- Candidate acquisition uses standard library plus project models.
- Recruiter candidate runtime does not import DuckDB, PyIceberg, pandas, pyarrow, a Hugging Face
  client, an FSQ SDK, or an Overpass SDK.
- Chroma and its Hugging Face-related transitive packages are part of the broader bootstrap
  dependency set, but are not used by the deterministic recruiter planning path.

## 11. Environment config audit

- `.env.example`: safe `mock` default; empty OpenAI fields.
- `.env.demo.example`: explicit `snapshot`, deterministic planner/semantics, empty OpenAI fields.
- Manifest path is project-relative:
  `data/travel/snapshots/openstreetmap/migration_manifest.json`.
- No example contains `C:\Users\...` or another machine-specific path.
- Running preflight from the documented repository root validates all 36 routes.

## 12. Absolute-path audit

No runtime, config, test, README startup command, or manifest route depends on a machine-specific
absolute path.

Twenty-seven O5 selected-source provenance files contain a `raw_temporary_path` value under
`C:\Users\<local-user>\AppData\Local\Temp\...`. These values are historical acquisition metadata;
runtime never reads them and the raw files are intentionally not retained. They will not break a
fresh clone, but should be replaced with a redacted/system-temp marker before a public push to avoid
publishing a local profile path.

## 13. Documentation consistency

Consistent current facts:

- 12 supported cities;
- 36 real POI snapshot routes;
- transport is synthetic;
- runtime provider acquisition calls are zero;
- Phase O historical baseline is correctly labeled 631 backend / 53 frontend;
- P1 current baseline is 633 backend / 55 frontend.

Inconsistency: `docs/PROJECT_STATUS_FINAL.md` still says 486 backend, 50 frontend, and describes
controlled-fixture rather than snapshot POIs. README links this file as current project status.
Update it to the P1 checkpoint or relabel it as historical before staging.

README's `631 / 53` table row is explicitly labeled the frozen Phase O baseline and is therefore not
a contradiction, but README/handoff should also state the current P1 `633 / 55` release result.

## 14. Fresh-clone readiness

README statically includes every operational step: clone, enter repository root, copy demo env,
create Python 3.11 venv, install requirements, run `npm ci`, run preflight, start Uvicorn, start Vite,
and open localhost. Docker is correctly described as optional for the planning path.

The runtime startup flow is ready. The repository as currently stageable is not yet clean-clone
ready because ignored evaluation files are direct test dependencies and README evidence links.

## 15. Large-file audit

The proposed checkpoint, including the 38 frozen evaluation artifacts and excluding local generated
material, is approximately 5.15 MiB across 232 baseline files before this audit report. There are no
files over 10 MiB and no Git LFS need.

Top intended files:

| KiB | Path |
|---:|---|
| 478.1 | `evals/results/hybrid_semantics_200_v1_phase_m2.json` |
| 474.2 | `evals/results/hybrid_semantics_200_v1_phase_m1.json` |
| 469.6 | `evals/results/hybrid_semantics_200_v1_offline.json` |
| 330.0 | `evals/results/hybrid_semantics_200_v1_audit.json` |
| 207.6 | `evals/results/hybrid_semantics_200_v1_audit.md` |
| 202.8 | `evals/results/hybrid_semantics_200_v1_offline.md` |
| 182.7 | `evals/results/hybrid_semantics_200_v1_phase_m2.md` |
| 161.8 | `evals/results/hybrid_semantics_200_live_m3.json` |
| 158.6 | `evals/results/hybrid_semantics_200_v1_phase_m1.md` |
| 132.1 | `evals/results/hybrid_semantics_200_m3_replay_m4.json` |
| 116.7 | `evals/results/hybrid_semantics_200_live_m4.json` |
| 104.7 | `evals/results/phase_m2_coverage_delta.json` |
| 96.1 | `evals/results/hybrid_semantics_v1_phase_j.json` |
| 93.4 | `evals/results/hybrid_semantics_v1_offline.json` |
| 92.3 | `evals/results/hybrid_semantics_v1_phase_i.json` |
| 90.8 | `evals/results/hybrid_semantics_200_m4_replay_m5.json` |
| 84.9 | `evals/results/hybrid_semantics_200_live_m3.md` |
| 67.9 | `evals/results/hybrid_semantics_live_m6.json` |
| 61.3 | `evals/results/phase_m2_coverage_delta.md` |
| 61.1 | `evals/datasets/hybrid_semantics_200_v1.json` |

## 16. Test and release-gate results

- Recruiter preflight: passed, 36 snapshot routes, deterministic planner, offline retrieval.
- Backend: 633 passed, 3 expected xfailed; one existing Starlette deprecation warning.
- Ruff: passed.
- Frontend: 55 passed.
- Vue/TypeScript: passed.
- Production build: passed, 49 modules transformed.
- `git diff --check`: passed; only Git's existing LF-to-CRLF notices were printed.
- Golden/O5 focused matrix: 12 passed.
  - Boston: USD 223, validator passed.
  - Austin: USD 394 to USD 317, one repair, validator passed.
  - Columbus: USD 343, preferences/hard constraints preserved, validator passed.
  - Nine O5 batch cities: API and source matrix passed.

## 17. Runtime-network audit

Production candidate modules and frontend contain no Overpass endpoint, OSM acquisition client,
`urllib.request`, requests/httpx provider fetch, or import of `scripts/acquire_osm_snapshots.py`.

`openai_planner.py` retains its intentional optional OpenAI HTTP client; `live_simulation.py` uses
an HTTPX mock transport. Neither is OSM/provider acquisition. Network acquisition exists only in the
development script and is not imported by runtime candidate paths.

Expected provider acquisition calls at runtime: zero.

## 18. Blockers

1. **Ignored required evaluation artifacts.** Current tests read ignored result JSON files and README
   links ignored result Markdown. A normal checkpoint made only from visible status entries would
   pass locally but fail/lose evidence on a clean clone.
2. **Outdated current-status document.** `docs/PROJECT_STATUS_FINAL.md` contradicts the current data
   mode and 633/55 baseline while README presents it as a current entry point.

Both must be resolved before the checkpoint is staged. No production-code or test failure was found.

## 19. Warnings

- Sanitize the 27 historical `raw_temporary_path` values before a public push.
- Local ignored `.env` contains a real credential; keep it local and never force-add it.
- Add narrow missing ignore coverage for conventional venv, coverage, Vite cache, raw/temp, and local
  database artifacts.
- Existing Starlette test-client deprecation warning is non-blocking.
- Git reports expected LF-to-CRLF conversion notices on this Windows checkout.

## 20. Exact staging and commit plan

### Required remediation before staging

1. Update `.gitignore` so these 38 stable files are visible while timestamped planner runs stay
   ignored:
   - `evals/results/hybrid_semantics_*`
   - `evals/results/phase_*`
2. Update `docs/PROJECT_STATUS_FINAL.md` to the snapshot architecture and 633/55 baseline, or remove
   it from the README current-entry-point list.
3. Replace the 27 O5 `raw_temporary_path` values with a non-machine-specific system-temp marker.
4. Add the narrow ignore gaps listed in section 4.
5. Rerun the release gates and verify `git status --porcelain=v1 -uall` against this classification.

### Explicit staging set

After remediation, stage exactly:

```text
.env.example
.env.demo.example
.gitignore
README.md
backend/app/
backend/tests/
data/mock/                    # records the four intentional deletions
data/travel/
docs/
evals/datasets/
evals/results/hybrid_semantics_*
evals/results/phase_*
frontend/src/
frontend/tests/
scripts/
```

Do not stage `.env`, `.venv`, caches, `node_modules`, `frontend/dist`, Chroma data, or
`evals/results/planner-live-*`.

### Commit structure

Use one coherent checkpoint. The runtime changes, new source modules, data migration, tests, UI, and
documentation are interdependent; splitting them would create intermediate commits that do not
reproduce the tested application. Do not manufacture phase-history commits retroactively.

Recommended message:

```text
feat: finalize recruiter-ready travel planning agent
```

At that boundary, rerun all section-16 gates. Only then push and perform the second-computer
fresh-clone test.

## 21. P2A-R remediation status — 2026-09-17

The findings above remain the original P2A audit record. The following remediation supersedes the
open status of sections 18–20.

### Blocker resolution

1. **RESOLVED — stable evaluation artifacts.** `.gitignore` now exposes exactly the existing
   `hybrid_semantics_*` and `phase_*` result groups. All 38 stable artifacts are visible to Git,
   parse where applicable, total 4,044,570 bytes, and remain below 490 KiB each. Timestamped
   `planner-live-*` outputs remain ignored.
2. **RESOLVED — current project status.** `docs/PROJECT_STATUS_FINAL.md` now describes 12 cities,
   36 OSM snapshot POI routes, synthetic transport, offline candidate retrieval, safe mock default,
   explicit recruiter snapshot mode, frozen semantics, bounded repair, the current presets, and the
   verified 633/3 + 55 test baseline. README now labels it Current Project Status and records the
   same current checkpoint numbers.

Remaining blockers: **0**.

### Exact stable evaluation artifacts

```text
hybrid_semantics_200_failure_clusters.md
hybrid_semantics_200_live_m3.json
hybrid_semantics_200_live_m3.md
hybrid_semantics_200_live_m4.json
hybrid_semantics_200_live_m4.md
hybrid_semantics_200_m3_replay_m4.json
hybrid_semantics_200_m3_replay_m4.md
hybrid_semantics_200_m4_replay_m5.json
hybrid_semantics_200_m4_replay_m5.md
hybrid_semantics_200_v1_audit.json
hybrid_semantics_200_v1_audit.md
hybrid_semantics_200_v1_offline.json
hybrid_semantics_200_v1_offline.md
hybrid_semantics_200_v1_phase_m1.json
hybrid_semantics_200_v1_phase_m1.md
hybrid_semantics_200_v1_phase_m2.json
hybrid_semantics_200_v1_phase_m2.md
hybrid_semantics_holdout_v1_offline.json
hybrid_semantics_holdout_v1_offline.md
hybrid_semantics_holdout_v1_phase_j.json
hybrid_semantics_holdout_v1_phase_j.md
hybrid_semantics_live_k1.json
hybrid_semantics_live_k1.md
hybrid_semantics_live_m5.json
hybrid_semantics_live_m5.md
hybrid_semantics_live_m6.json
hybrid_semantics_live_m6.md
hybrid_semantics_v1_offline.json
hybrid_semantics_v1_offline.md
hybrid_semantics_v1_phase_i.json
hybrid_semantics_v1_phase_i.md
hybrid_semantics_v1_phase_j.json
hybrid_semantics_v1_phase_j.md
phase_i_failure_clusters.md
phase_m1_hard_safety_delta.json
phase_m1_hard_safety_delta.md
phase_m2_coverage_delta.json
phase_m2_coverage_delta.md
```

Reference closure by group:

- M3/M4 live JSON is consumed by replay scripts and `test_hybrid_live_m3.py`; paired Markdown is
  the human-readable frozen evidence.
- M3→M4 and M4→M5 replay JSON/Markdown are the reproducible replay outputs of those scripts.
- 200-case offline/audit/M1/M2 JSON and reports are inputs or outputs of the audit and phase-report
  tools; `test_hybrid_semantics_audit.py` directly reads the offline JSON.
- Holdout, Phase I/J, K1, M5, and M6 pairs preserve the frozen evaluation lineage; M5 JSON is a
  direct replay-test input and M6 Markdown is linked from README.
- Phase I clusters and M1/M2 delta pairs are report evidence; README directly links the M2 report.

### Provenance and checksum verification

- Removed only the optional `raw_temporary_path` property from exactly 27 O5 selected-source JSON
  files. No replacement or fake repository path was introduced.
- All 111 JSON files under snapshot, selected-source, evaluation-dataset, and evaluation-result
  trees parse successfully.
- SHA-256 comparison of all 41 snapshot-tree files before and after remediation: 0 mismatches.
- Canonical hashes of all 27 provenance objects after excluding `raw_temporary_path`: 0 mismatches.
- Raw-response hashes, raw byte counts, timestamps, query metadata, selected elements, provider
  identities, and snapshot provenance are unchanged. No separate checksum of the selected-source
  container file was referenced elsewhere, so no recorded checksum needed updating.
- Candidate-tree absolute-path rescan: 0 machine-specific user/temp paths.

### Ignore and secret remediation

Added narrow ignores for `venv/`, coverage outputs, `.vite/`, local database files, and repository
local `data/travel/raw/` / `data/travel/tmp/`. No tracked database fixture exists, and required
`data/travel/` snapshot/source paths remain visible.

Secret rescan found zero high-confidence OpenAI, GitHub, Hugging Face, AWS, bearer, or private-key
credentials in candidate files. Local `.env` remains ignored, untracked, and unstaged; both example
environment files keep empty API-key values.

### Clean-clone closure

- Current-document local links: complete.
- Required dependency manifests, env example, preflight, mock fixture, manifest, NOTICE, handoff,
  and project-status files: present and trackable.
- Every exact `evals/results/*.json` or `*.md` path referenced by current source/tests/docs exists and
  is trackable.
- Runtime/config/test machine-specific absolute paths: 0.
- A proposed checkpoint contains everything required to create the venv, install both dependency
  sets, run preflight, start backend/frontend, run the deterministic snapshot demo, and execute the
  ordinary full test suite.

### Final release gates

- Recruiter preflight: passed; 36 routes, deterministic planner, offline retrieval.
- Backend: 633 passed, 3 expected xfailed; one existing Starlette deprecation warning.
- Frontend: 55 passed.
- Ruff: passed.
- Vue/TypeScript: passed.
- Vite production build: passed; 49 modules transformed.
- `git diff --check`: passed; Windows line-ending notices only.
- Golden/O5 matrix: 12 passed; Boston 223, Austin 394→317 with one repair, Columbus 343, and all
  nine O5 cities preserved.
- Runtime provider acquisition calls: 0; no Overpass acquisition or live model evaluation ran.

### Final classification

Expanded visible status after remediation: 233 paths — 45 modified, 4 deleted, 184 untracked, and 0
renamed. Category A MUST COMMIT: 79. Category B SHOULD COMMIT: 154. Category C REVIEW: 0.
Category D MUST NOT COMMIT remains limited to ignored local environment, dependency, cache, build,
coverage, database, raw/temp, and timestamped planner-live artifacts.

### P2B staging plan

Stage only the explicit set from section 20, now including the trackable
`evals/results/hybrid_semantics_*` and `evals/results/phase_*` groups. Continue to exclude `.env`,
both venv patterns, dependency/build directories, caches, coverage output, Chroma/local databases,
raw/tmp acquisition caches, and `evals/results/planner-live-*`.

One coherent checkpoint remains the recommended commit structure:

```text
feat: finalize recruiter-ready travel planning agent
```

No file was staged, committed, pushed, deleted, or acquired during P2A-R.
