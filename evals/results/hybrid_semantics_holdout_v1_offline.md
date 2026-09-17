# Hybrid Semantic Evaluation v1

Mode: `offline`<br>
Cases: 16<br>
Case pass rate: 81.2%

## Coverage gate

TP: 4 | TN: 11 | FP: 1 | FN: 0
Precision: 80.0% | Recall: 100.0% | F1: 88.9%

## Hard-constraint safety

Silent hard corruption: 0
Unsupported hard constraints silently dropped: 0

## Failed cases

### HOLDOUT-007 — PARSER_MISS
Input: The trip must stay below $1200, and the hotel must stay below $500 total.
Gold: `{"needs_llm": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`

### HOLDOUT-015 — COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Input: Hotel maximum is $600 total. Actually, make it $450.
Gold: `{"needs_llm": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Actually, make it $450"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`

### HOLDOUT-016 — PARSER_MISS
Input: I can stretch the hotel budget if the location is excellent, but the trip should stay under $1000.
Gold: `{"needs_llm": true, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1000.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Trade-off language with multiple monetary statements"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
