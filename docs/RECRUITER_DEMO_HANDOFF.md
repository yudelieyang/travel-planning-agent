# Recruiter demo handoff

## 1. Current project state

Phase O is frozen. All 12 supported cities use local OpenStreetMap snapshots for attractions,
hotels, and restaurants; transport remains a controlled synthetic cost model. The primary recruiter
demo is deterministic, API-key-free, and performs no provider-network request.

Current verified release gates: 633 backend tests passed with 3 expected xfails, and all 55
frontend tests passed. Ruff, Vue/TypeScript, and the production build also pass.

## 2. Architecture summary

```text
request → requirements → offline snapshot candidates → filtering/ranking
        → planner estimates → validation → at most one bounded repair → itinerary
```

- Real POI facts: frozen OpenStreetMap snapshots.
- Runtime candidate retrieval: local and offline.
- Prices: deterministic planner estimates, not OSM or commercial prices.
- Transport: synthetic per-person/day planning allowances.
- Semantic subsystem: existing frozen deterministic/hybrid system.

See `docs/REAL_DATA_BATCH_MIGRATION_REPORT.md` for snapshot checksums and migration evidence. Do not
refresh or edit snapshots as part of demo setup.

## 3. Startup steps

Prerequisites are CPython 3.11 x64, Node.js 22.18+, npm, and Windows PowerShell. Docker Desktop is
optional because Postgres and Redis are not called by the planning workflow.

Fresh clone setup:

```powershell
Copy-Item .env.demo.example .env
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd frontend
npm.cmd ci
cd ..
.\.venv\Scripts\python.exe scripts\preflight_recruiter_demo.py
```

Terminal 1:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Terminal 2:

```powershell
cd frontend
npm.cmd run dev
```

Open <http://127.0.0.1:5173>. Backend health is at <http://127.0.0.1:8000/health>.

## 4. Environment variables

The primary demo uses `.env.demo.example`:

| Variable | Value | Purpose |
|---|---|---|
| `CANDIDATE_DATA_MODE` | `snapshot` | Deliberately selects real local POIs |
| `CANDIDATE_SNAPSHOT_PATH` | `data/travel/snapshots/openstreetmap/migration_manifest.json` | Final 36-route manifest |
| `AGENT_PLANNER` | `deterministic` | Stable offline planner |
| `SEMANTIC_AUGMENTATION_MODE` | `deterministic` | Stable offline semantic path |
| `OPENAI_API_KEY` / `OPENAI_MODEL` | blank | Not required for the primary demo |

The application default and `.env.example` remain `mock` for safety. Optional hybrid semantics
require an approved OpenAI key/model and `SEMANTIC_AUGMENTATION_MODE=hybrid`; this is a separate,
network-dependent demo and is not needed for the primary walkthrough.

## 5. Demo presets

- **Real Snapshot Trip** — Boston normal flow with real POIs and passing validation.
- **Bounded Budget Repair** — Austin hard-budget violation, one repair, revalidation.
- **Preference Matching** — Columbus zoo/fried-chicken preferences and hotel ceiling.
- **Ambiguity Boundary**, **Correction Safety**, **Tradeoff Boundary** — optional-live semantic
  examples; use only when hybrid mode and a key are deliberately configured.

## 6. Recommended order

1. Real Snapshot Trip.
2. Bounded Budget Repair.
3. Preference Matching.
4. At most one optional-live semantic boundary if network/model variability is acceptable.

## 7. What the scenarios demonstrate

The UI exposes the submitted request, parsed requirements, candidate source, selected options and
alternatives, filtering evidence, validation, bounded repair when applicable, budget, and itinerary.
No preset auto-submits, and each run is independent.

## 8. Real-data architecture

Snapshot mode eagerly loads the migration manifest through the existing provider system. Every
declared route must validate; missing, corrupt, empty, wrong-city, wrong-category, duplicate, or
invalid-coordinate data fails closed. Runtime never contacts OSM or Overpass.

## 9. Snapshot versus live

“Real-world snapshot” means the POI name, address, coordinates, identity, and category metadata came
from OSM and were frozen locally. It does not mean live availability, live opening status, or a live
provider call. The UI intentionally never labels snapshot data as “LIVE”.

## 10. Cost distinction

OSM is not a pricing provider. Admission, hotel, food, and transport values are preserved planner
estimates used for deterministic comparison. The UI labels these values as planner estimates.
Transport is a synthetic planning allowance rather than a POI.

## 11. Golden values

- Boston normal scenario: USD 223, validator passed.
- Austin repair: USD 394 → USD 317, one attempt, validator passed.
- Columbus preference scenario: USD 343, ranking/hard constraints preserved, validator passed.

## 12. Known limitations

- No live prices, bookings, availability, maps, routing, or ratings enrichment.
- Snapshot freshness is fixed at the recorded acquisition/base timestamps.
- English-only bounded request patterns and exactly one eligible repair attempt.
- Optional hybrid behavior depends on the configured external model and network.

## 13. Troubleshooting

- **Preflight says mode is mock:** copy `.env.demo.example` to `.env`, or set the two candidate
  variables explicitly before rerunning it.
- **Manifest/snapshot failure:** confirm the repository contains `data/travel/snapshots/openstreetmap`
  and do not bypass validation with mock fallback.
- **Backend configuration failure:** compare `.env` with `.env.demo.example`; do not add an API key
  for the deterministic demo.
- **Port in use:** stop the existing process using 8000 or 5173, then restart. Vite uses a strict port.
- **Docker unavailable:** skip Compose; it is optional. If demonstrating scaffolding, start Docker
  Desktop, run `docker compose up -d`, then `docker compose ps` and require healthy services.
- **Frontend dependencies missing:** run `npm.cmd ci` inside `frontend`.

## 14. Test commands

```powershell
.\.venv\Scripts\python.exe scripts\preflight_recruiter_demo.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\ruff.exe check backend scripts
cd frontend
npm.cmd test
npm.cmd run typecheck
npm.cmd run build
```

From the repository root, finish with `git diff --check`.

## 15. Safe reset and restart

Stop backend/frontend with `Ctrl+C`. Optional Compose services can be stopped with
`docker compose stop` without deleting volumes. Restart the two commands above; there is no runtime
snapshot cache to clear. To return to the safe fixture mode, set `CANDIDATE_DATA_MODE=mock`, remove or
ignore `CANDIDATE_SNAPSHOT_PATH`, and restart the backend. Never use reset/clean commands to prepare
the demo, and never commit `.env` or API keys.
