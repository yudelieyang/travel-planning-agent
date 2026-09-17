# Phase K — Bounded Live Hybrid Evaluation

Timestamp: `2026-09-12T22:33:45.746291+00:00`<br>
Model: `gpt-5.6-luna`<br>
Prompt version: `semantic_extractor_v1`<br>
Dataset: `hybrid_semantics_live_subset_k1`

## Summary

Calls: 12 | Completed/schema-valid: 12/12 | Provider failures: 0
Final hybrid semantic accuracy: 83.3%
Hard safety: `{"silent_hard_constraint_corruption": 0, "wrong_hard_scope_promoted": 0, "soft_to_hard_unsafe_promotion": 0, "hallucinated_hard_constraints_accepted": 0, "unsupported_hard_constraints_silently_dropped": 0}`
Latency ms: `{"average": 2591.424166666666, "median": 2321.755, "max": 3999.68}`
Token usage: `{"input_tokens": 7620, "output_tokens": 1418, "total_tokens": 9038, "average_per_case": 753.1666666666666}`

## Case records

### HYBRID-014
Input: I really can't go above $400 for the hotel.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I really can't go above $400  for the hotel", "Unresolved hard hotel scope"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": []}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 400.0, "currency": "USD", "strength": "HARD", "source_text": "I really can't go above $400 for the hotel.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Extractor: `{"input_tokens": 635, "output_tokens": 75, "total_tokens": 710, "latency_ms": 3999.68, "error": null}`
Merge: `{"decisions": ["DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED"], "conflicts": ["AMBIGUOUS_SCOPE"], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Failures: `[]`

### HYBRID-015
Input: I want a $200 hotel.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I want a $200  hotel"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": []}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "UNSPECIFIED", "operator": "LTE", "value": 200.0, "currency": "USD", "strength": "HARD", "source_text": "$200 hotel", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "$200 hotel", "reason": "It is unclear whether $200 is the total hotel budget or the nightly hotel rate."}]}`
Extractor: `{"input_tokens": 631, "output_tokens": 101, "total_tokens": 732, "latency_ms": 2399.97, "error": null}`
Merge: `{"decisions": ["UNSUPPORTED_RETAINED", "CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING", "BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Failures: `[]`

### HYBRID-017
Input: My hotel budget is $300.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["My hotel budget is $300"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": []}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "UNSPECIFIED", "operator": "LTE", "value": 300.0, "currency": "USD", "strength": "HARD", "source_text": "My hotel budget is $300.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "My hotel budget is $300.", "reason": "It is unclear whether the $300 hotel budget applies to the entire stay or is a per-night limit."}]}`
Extractor: `{"input_tokens": 631, "output_tokens": 164, "total_tokens": 795, "latency_ms": 3611.7, "error": null}`
Merge: `{"decisions": ["UNSUPPORTED_RETAINED", "CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING", "BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Failures: `[]`

### HYBRID-018
Input: Spend no more than $250 on food.
Coverage: `{"needs_llm": true, "reasons": ["UNSUPPORTED_HARD_REQUIREMENT"], "evidence": ["Spend no more than $250  on food"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["FOOD_TOTAL"]}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "FOOD_TOTAL", "operator": "LTE", "value": 250.0, "currency": "USD", "strength": "HARD", "source_text": "Spend no more than $250 on food.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Extractor: `{"input_tokens": 633, "output_tokens": 73, "total_tokens": 706, "latency_ms": 1535.5, "error": null}`
Merge: `{"decisions": ["UNSUPPORTED_RETAINED", "CLARIFICATION_REQUIRED"], "conflicts": [], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "requires_clarification": true}`
Failures: `[]`

### HYBRID-019
Input: Keep transportation below $100.
Coverage: `{"needs_llm": true, "reasons": ["UNSUPPORTED_HARD_REQUIREMENT"], "evidence": ["Keep transportation below $100", "Unresolved hard monetary scope"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["TRANSPORT_TOTAL"]}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "UNSPECIFIED", "operator": "LTE", "value": 100.0, "currency": "USD", "strength": "HARD", "source_text": "Keep transportation below $100.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "transportation", "reason": "The schema has no transportation-specific budget scope, so it is unclear whether the $100 limit applies to the total trip, hotel, food, or another unspecified scope."}]}`
Extractor: `{"input_tokens": 630, "output_tokens": 118, "total_tokens": 748, "latency_ms": 2255.57, "error": null}`
Merge: `{"decisions": ["UNSUPPORTED_RETAINED", "CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING", "BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "requires_clarification": true}`
Failures: `[]`

### HYBRID-020
Input: Activities must stay under $150.
Coverage: `{"needs_llm": true, "reasons": ["UNSUPPORTED_HARD_REQUIREMENT"], "evidence": ["Activities must stay under $150", "Unresolved hard monetary scope"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["ACTIVITIES_TOTAL"], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["ACTIVITIES_TOTAL"]}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "UNSPECIFIED", "operator": "LTE", "value": 150.0, "currency": "USD", "strength": "HARD", "source_text": "Activities must stay under $150.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Extractor: `{"input_tokens": 631, "output_tokens": 71, "total_tokens": 702, "latency_ms": 2029.35, "error": null}`
Merge: `{"decisions": ["UNSUPPORTED_RETAINED", "CLARIFICATION_REQUIRED"], "conflicts": [], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": ["ACTIVITIES_TOTAL"], "requires_clarification": true}`
Failures: `[]`

### HYBRID-022
Input: I'd rather pay a little more for a better hotel but still keep the whole trip below $1000.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Trade-off language with multiple monetary statements"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1000.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1000.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1000.0, "currency": "USD", "strength": "HARD", "source_text": "still keep the whole trip below $1000", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "prefer a better hotel, willing to pay a little more", "source_text": "I'd rather pay a little more for a better hotel"}], "objectives": [], "ambiguities": []}`
Extractor: `{"input_tokens": 645, "output_tokens": 109, "total_tokens": 754, "latency_ms": 2033.73, "error": null}`
Merge: `{"decisions": ["DUPLICATE_CONFIRMED", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1000.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "prefer a better hotel, willing to pay a little more"}], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Failures: `["PREFERENCE_ERROR"]`

### HYBRID-049
Input: Keep the whole trip below $700. The hotel alone must cost at least $900.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["The hotel alone must cost at least $900"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 700.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 700.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": []}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 700.0, "currency": "USD", "strength": "HARD", "source_text": "Keep the whole trip below $700.", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 900.0, "currency": "USD", "strength": "HARD", "source_text": "The hotel alone must cost at least $900.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Extractor: `{"input_tokens": 642, "output_tokens": 221, "total_tokens": 863, "latency_ms": 2852.41, "error": null}`
Merge: `{"decisions": ["DUPLICATE_CONFIRMED", "DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED"], "conflicts": ["AMBIGUOUS_SCOPE"], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 700.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Failures: `[]`

### HOLDOUT-005
Input: Lodging budget is $350.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Lodging budget is $350"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": []}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 350.0, "currency": "USD", "strength": "HARD", "source_text": "Lodging budget is $350.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Extractor: `{"input_tokens": 632, "output_tokens": 72, "total_tokens": 704, "latency_ms": 2216.25, "error": null}`
Merge: `{"decisions": ["DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED"], "conflicts": ["AMBIGUOUS_SCOPE"], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Failures: `[]`

### HOLDOUT-008
Input: Flight spending must stay below $180.
Coverage: `{"needs_llm": true, "reasons": ["UNSUPPORTED_HARD_REQUIREMENT"], "evidence": ["Flight spending must stay below $180"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": []}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "UNSPECIFIED", "operator": "LTE", "value": 180.0, "currency": "USD", "strength": "HARD", "source_text": "Flight spending must stay below $180.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Extractor: `{"input_tokens": 632, "output_tokens": 72, "total_tokens": 704, "latency_ms": 2175.19, "error": null}`
Merge: `{"decisions": ["UNSUPPORTED_RETAINED", "CLARIFICATION_REQUIRED"], "conflicts": [], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "requires_clarification": true}`
Failures: `[]`

### HOLDOUT-009
Input: Restaurant costs should stay under $240.
Coverage: `{"needs_llm": true, "reasons": ["UNSUPPORTED_HARD_REQUIREMENT"], "evidence": ["Restaurant costs should stay under $240", "Unresolved hard monetary scope"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["FOOD_TOTAL"]}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "FOOD_TOTAL", "operator": "LTE", "value": 240.0, "currency": "USD", "strength": "HARD", "source_text": "Restaurant costs should stay under $240.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Extractor: `{"input_tokens": 632, "output_tokens": 72, "total_tokens": 704, "latency_ms": 2387.94, "error": null}`
Merge: `{"decisions": ["UNSUPPORTED_RETAINED", "CLARIFICATION_REQUIRED"], "conflicts": [], "requires_clarification": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "requires_clarification": true}`
Failures: `[]`

### HOLDOUT-016
Input: I can stretch the hotel budget if the location is excellent, but the trip should stay under $1000.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Trade-off language with multiple monetary statements"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": null, "allow_hybrid_gap": true, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1000.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": []}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1000.0, "currency": "USD", "strength": "HARD", "source_text": "the trip should stay under $1000", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "excellent location, even if it requires stretching the hotel budget", "source_text": "I can stretch the hotel budget if the location is excellent"}], "objectives": [], "ambiguities": [{"level": "ASSUMABLE", "source_text": "I can stretch the hotel budget", "reason": "No specific hotel-budget amount or limit is provided; the stated total-trip cap remains the explicit budget constraint."}, {"level": "ASSUMABLE", "source_text": "if the location is excellent", "reason": "“Excellent” hotel location is subjective and not operationally defined."}]}`
Extractor: `{"input_tokens": 646, "output_tokens": 270, "total_tokens": 916, "latency_ms": 3599.8, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1000.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "excellent location, even if it requires stretching the hotel budget"}], "ambiguity_levels": ["ASSUMABLE", "ASSUMABLE"], "unsupported_scopes": [], "requires_clarification": false}`
Failures: `["PREFERENCE_ERROR", "AMBIGUITY_ERROR"]`
