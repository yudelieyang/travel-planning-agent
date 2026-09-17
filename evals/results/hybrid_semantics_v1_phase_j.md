# Hybrid Semantic Evaluation v1

Mode: `offline`<br>
Cases: 50<br>
Case pass rate: 90.0%
Offline-deferred hybrid cases: 0

## Coverage gate

TP: 13 | TN: 37 | FP: 0 | FN: 0
Precision: 100.0% | Recall: 100.0% | F1: 100.0%

## Hard-constraint safety

Silent hard corruption: 0
Unsupported hard constraints silently dropped: 0

## Failed cases

### HYBRID-001 — PARSER_MISS
Input: Plan a 2-day trip to Boston under $800.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Deterministic: `{"destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`

### HYBRID-009 — PARSER_MISS
Input: Keep it below $1200. Sorry, I meant no more than $950.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 950.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`

### HYBRID-031 — PARSER_MISS
Input: Plan 2 days in Boston under 900 dollars.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Deterministic: `{"destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`

### HYBRID-032 — PARSER_MISS
Input: Plan 2 days in Boston. My budget is USD 900.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Deterministic: `{"destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`

### HYBRID-033 — PARSER_MISS
Input: Plan 2 days in Boston. My budget is €900.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Deterministic: `{"destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": 2, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
