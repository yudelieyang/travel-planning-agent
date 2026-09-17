# Project status — recruiter demo checkpoint

## Current state

The project is ready for a deterministic, API-key-free recruiter walkthrough. It supports 12 U.S.
cities. In explicit recruiter snapshot mode, attractions, hotels, and restaurants come from 36
checked-in OpenStreetMap snapshot routes; transport remains a controlled synthetic planning
allowance. Runtime candidate retrieval is local and makes zero provider-network calls.

The safe application default remains `mock`. Copying `.env.demo.example` to `.env` deliberately
selects the real-world snapshot manifest. “Real-world snapshot” does not mean live availability or
live provider access: POI facts are frozen, and displayed costs are deterministic project-generated
planner estimates rather than OSM or commercial prices.

## Demo-ready capabilities

- Five-stage request-to-result narrative with visible requirements and candidate provenance.
- Real POIs, selected candidates, alternatives, validation, budget, and itinerary evidence.
- Typed hard constraints, soft preferences, objectives, and ambiguity boundaries.
- Exactly one eligible bounded repair followed by deterministic revalidation.
- Offline presets: Boston real snapshot trip, Austin bounded repair, and Columbus preference match.
- Optional hybrid semantic presets kept separate from the primary deterministic demo.

## Frozen architecture

- Candidate provider routing and the 36-route migration manifest are frozen.
- The semantic subsystem, planner contracts, validator, repair behavior, and budget formulas are
  unchanged by recruiter-demo finalization.
- Coverage gate: 94.9% recall and 100% precision on the frozen 200-case audit.
- Extractor v3 correction proposal recall: 100%; accepted clear corrections: 87.5%.
- Recorded live hard-safety violations: 0.

## Verification record

- Backend: `633 passed, 3 xfailed`.
- Frontend: `55 passed`.
- Ruff: passed.
- Vue/TypeScript: passed.
- Vite production build: passed.
- Recruiter preflight: 36 snapshot routes, deterministic planner, offline retrieval.
- Boston: USD 223, validator passed.
- Austin: USD 394 → USD 317, repair attempt 1 of 1, validator passed.
- Columbus: USD 343, preference and hard-constraint behavior preserved.
- Runtime provider-network acquisition calls: 0.

## Scope boundaries

- No live prices, booking, availability, maps, routing, opening hours, or ratings enrichment.
- Planner estimates are not provider quotes.
- Transport is a synthetic per-person/day allowance, not an OSM POI.
- English-only bounded request patterns and one repair attempt maximum.
- Optional hybrid semantic extraction requires credentials and provider connectivity.

## Second-computer checklist

- [ ] Install standard CPython 3.11 x64, Node.js 22.18+, and npm.
- [ ] Clone the repository and open PowerShell at the repository root.
- [ ] Copy `.env.demo.example` to `.env`; do not commit local credentials.
- [ ] Create `.venv` and install `requirements.txt`.
- [ ] Run `npm.cmd ci` in `frontend`.
- [ ] Run `scripts/preflight_recruiter_demo.py` and require all 36 routes to pass.
- [ ] Start Uvicorn and Vite using the README commands.
- [ ] Run the backend, frontend, Ruff, typecheck, and production-build gates.

## Recommended entry points

- `README.md` for setup, architecture, evidence, and limitations.
- `docs/RECRUITER_DEMO_HANDOFF.md` for operational handoff.
- `docs/RECRUITER_DEMO_SCRIPT.md` for the walkthrough.
- `docs/REAL_DATA_BATCH_MIGRATION_REPORT.md` for snapshot migration evidence.
- `evals/results/phase_m2_coverage_delta.md` and
  `evals/results/hybrid_semantics_live_m6.md` for semantic evaluation evidence.
