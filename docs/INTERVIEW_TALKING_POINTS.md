# Interview Talking Points

## Thirty-second summary

I built a single-agent travel planner around a typed state machine. It separates hard constraints from preferences, retrieves transparent controlled candidates, validates final costs, and performs one structured repair when a hard budget fails. The default path is fully deterministic; an optional LLM extractor is gated and treated as an untrusted proposal.

## Design decisions worth discussing

- **Typed semantics over prompt-only policy.** Total-trip and hotel-total budgets are explicit contracts with scope, operator, strength, provenance, and confidence.
- **Selective model use.** A deterministic coverage gate decides whether hybrid extraction is warranted; straightforward requests never pay the latency or reliability cost.
- **Conservative merge.** LLM output cannot silently rewrite deterministic facts. Unsupported scopes, ambiguous targets, polarity problems, and conflicting corrections are rejected or clarification-bound.
- **Validation after composition.** The agent validates the actual itinerary and budget artifact, not merely the planner’s intended tool call.
- **Bounded recovery.** Only typed hard-budget violations can trigger repair, and the graph allows exactly one attempt before returning a safe terminal result.
- **Observable decisions.** The public response exposes allowlisted stages, runtime tool inputs, candidates, violations, semantic mode, and repair evidence without leaking prompts or raw model reasoning.
- **Reproducible portfolio path.** The recruiter demo needs no key, network, Docker service, or live provider.

## Evaluation story

- Built a 200-case semantic robustness set spanning hard/soft budgets, scopes, corrections, ambiguity, negation, unsupported requirements, and tradeoffs.
- The frozen coverage gate reached 94.9% recall and 100% precision.
- The one-time extractor-v3 correction experiment reached 100% proposal recall and 87.5% accepted correction recall.
- Across the bounded live calibration, hard-safety violations were zero.
- The reports retain failure classes and misses; the project does not hide model limitations behind an aggregate score.

## Tradeoffs

The system deliberately prefers a visible clarification over a plausible but unsafe interpretation. Controlled candidate data limits breadth, but it makes selection, validation, and repair reproducible. The public API exposes enough evidence for trust while keeping internal proposals, prompts, and private provider objects out of the response.

## What I would build next

1. Add provider adapters behind the same typed tool contracts, with freshness and availability metadata.
2. Add explicit multi-turn clarification state rather than asking users to resubmit a full request.
3. Calibrate hybrid thresholds on a larger, independently authored holdout set.
4. Add browser end-to-end screenshots and accessibility checks to CI.
5. Introduce persistence only when a real product workflow requires it; the current graph does not need a database.

## Honest limitations to volunteer

- The language surface is bounded and English-only.
- Candidate coverage is 12 controlled U.S. cities.
- Hotel-per-night and other unsupported scopes are not executed as hard constraints.
- Live LLM evidence came from bounded evaluation subsets and is model/version dependent.
- Ratings are visible metadata but are not always ranking inputs.
- This is planning and validation, not booking.

## Useful implementation details

- FastAPI, Pydantic, LangGraph, Vue 3, Vite, pytest, and Ruff.
- Public models use `extra="forbid"` and explicit allowlists.
- Search tools return typed options; the deterministic budget calculator is checked against resolved inputs.
- Repair feedback carries typed violations plus the prior itinerary.
- Frontend totals are never recomputed; displayed amounts come from backend artifacts.
