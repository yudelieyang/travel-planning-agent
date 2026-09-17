# Hybrid Semantic Evaluation v1

Mode: `offline`<br>
Cases: 50<br>
Case pass rate: 98.0%

## Coverage gate

TP: 13 | TN: 36 | FP: 0 | FN: 1
Precision: 100.0% | Recall: 92.9% | F1: 96.3%

## Hard-constraint safety

Silent hard corruption: 0
Unsupported hard constraints silently dropped: 0

## Failed cases

### HYBRID-007 — COVERAGE_FALSE_NEGATIVE
Input: Keep the entire trip under $900. Hotel spending must stay below $400.
Gold: `{"needs_llm": true, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 900.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 400.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 900.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 400.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 900.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 400.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
