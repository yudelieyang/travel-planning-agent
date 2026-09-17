# Recruiter Demo Script

Target: 3–5 minutes. Use deterministic mode so the walkthrough has no live dependency.

## Before the call

1. Copy `.env.example` to `.env` if needed; do not overwrite a configured `.env`.
2. Start the deterministic backend and frontend using the root README commands.
3. Confirm `http://127.0.0.1:8000/health` and open `http://127.0.0.1:5173`.
4. Click **Bounded Budget Repair**. Do not submit until the audience is ready.

## 0:00–0:40 — Frame the problem

“Travel requests combine hard limits, preferences, corrections, and ambiguous language. This agent keeps safety-critical constraints typed and validates the final plan rather than trusting fluent output.”

Point to the evaluation strip: 94.9% gate recall, 100% gate precision, and zero hard-safety violations in the bounded live evaluation.

## 0:40–1:20 — Submit the request

Use:

> Please build a three-day trip to Austin for one traveler. My total budget is $350.

Click **Plan Trip**. Point out that the page reports `DEMO MODE` and `SEMANTIC DETERMINISTIC`; the main path did not call a model or live travel provider.

## 1:20–2:05 — Show requirements understanding

In Stage 2, call out:

- Austin, 3 days, 1 traveler.
- `TOTAL TRIP ≤ USD 350.00`, explicitly labeled `HARD`.
- No unsupported or clarification-bound semantics.
- Coverage gate and model invocation are reported from the backend execution record.

## 2:05–2:50 — Show retrieval and selection

In Stage 3, explain that the planner selected four typed search tools. Each category shows selected candidates and preserved alternatives, with price units, tags, ratings, review counts, preference matches, and controlled-fixture provenance.

Be precise about filtering: the UI reports eligible returned candidates and the runtime price/preference filters. It does not invent a pre-filter total.

## 2:50–3:45 — Show the agentic decision

In Stages 4–5, narrate the evidence visible on screen:

- Initial plan: USD 394.
- Typed violation: `HARD_BUDGET_EXCEEDED`; limit USD 350, excess USD 44.
- Repair attempt 1 of 1.
- Lower-cost eligible attraction and food selections.
- Final plan: USD 317; USD 77 saved; USD 33 remaining.
- Revalidation: passed.

“The important part is not that it retried—it is that the retry was triggered by structured feedback, bounded to one attempt, and validated again.”

## 3:45–4:30 — Close

Show the final budget and itinerary, then mention that the raw planner/tool records are available under **Technical execution details** without dominating the main story.

Close with: “The default demo is reproducible. Hybrid mode is optional and only handles gaps; its proposals are grounded and conservatively merged rather than trusted.”

## Optional 30-second extension

Restart the backend in hybrid mode only if credentials and connectivity were verified beforehand. Use **Ambiguity Boundary** to show a coverage-triggered semantic proposal and clarification quarantine. If live mode is unavailable, do not improvise—stay with the deterministic demo and point to the checked-in evaluation artifacts.

## Recovery notes

- Backend unavailable: verify port 8000 and `/health`.
- Frontend unavailable: verify port 5173 and the Vite terminal.
- Mode badge unexpected: restart the backend after changing environment variables.
- Live extractor unavailable: return to deterministic mode; the primary demo remains complete.
