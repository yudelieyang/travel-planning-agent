# Phase M4 — Fresh Bounded Live Hybrid Validation

Timestamp: `2026-09-15T00:30:33.211204+00:00`<br>
Model: `gpt-5.6-luna`<br>
Prompt version: `semantic_extractor_v2`<br>
Dataset: `hybrid_semantics_200_live_subset_m4`

## Summary

Calls: 18 | Completed/schema-valid: 18/18 | Provider failures: 0
Final hybrid semantic accuracy: 77.8%
Open-world valid additions: 0
Evaluation-gold stale cases: `["SEM200-096", "SEM200-098", "SEM200-100"]`
Unsupported-scope recognition: `{"live": "not_applicable", "local_shadow_controls": "4/4"}`
Hard safety: `{"silent_hard_constraint_corruption": 0, "wrong_hard_scope_accepted": 0, "wrong_hard_amount_accepted": 2, "soft_to_hard_unsafe_promotion": 0, "hard_to_soft_unsafe_downgrade": 0, "hallucinated_hard_constraints_accepted": 0, "unsupported_hard_constraints_silently_dropped": 0}`
Latency ms: `{"average": 3211.7827777777784, "median": 2797.8, "p95": 7085.83, "max": 7085.83}`
Token usage: `{"input_tokens": 13235, "output_tokens": 2589, "total_tokens": 15824, "average_per_case": 879.1111111111111}`

## Selection

Fresh SEM200 calibration holdout: no case ID was used in the M3 live subset. Selection was frozen only after merge replay, mocked regressions, M1/M2 oracles, full backend pytest, and Ruff passed.
Category mix: `{"ambiguous_monetary_scope": 5, "correction": 3, "negation_exclusion": 3, "tradeoff_compositional": 4, "noisy_imperfect_english": 3}`
Case IDs: `["SEM200-120", "SEM200-121", "SEM200-123", "SEM200-124", "SEM200-126", "SEM200-096", "SEM200-098", "SEM200-100", "SEM200-157", "SEM200-159", "SEM200-160", "SEM200-167", "SEM200-168", "SEM200-170", "SEM200-173", "SEM200-187", "SEM200-188", "SEM200-191"]`

## Extractor and grounding

Constraint: `{"matched": 8, "expected": 10, "proposed": 10, "false_positive": 2, "precision": 0.8, "recall": 0.8, "f1": 0.8}`
Scope: `{"matched": 10, "expected": 10, "proposed": 10, "false_positive": 0, "precision": 1.0, "recall": 1.0, "f1": 1.0}`
Amount: `{"matched": 8, "expected": 10, "proposed": 10, "false_positive": 2, "precision": 0.8, "recall": 0.8, "f1": 0.8}`
Strength: `{"matched": 10, "expected": 10, "proposed": 10, "false_positive": 0, "precision": 1.0, "recall": 1.0, "f1": 1.0}`
Preference: `{"matched": 0, "expected": 0, "proposed": 4, "false_positive": 4, "precision": 0.0, "recall": null, "f1": 0.0}`
Ambiguity: `{"matched": 12, "expected": 12, "proposed": 14, "false_positive": 2, "precision": 0.8571428571428571, "recall": 1.0, "f1": 0.9230769230769231}`
Grounding: `{"proposed_items": 28, "grounded_items": 28, "ungrounded_items": 0, "cases_with_ungrounded_rejection": 0, "accepted_grounded_additions": 27, "rejected_ungrounded_additions": 0}`

## Merge and failure taxonomy

Merge: `{"accepted_augmentations": 15, "rejected_proposals": 7, "duplicates": 4, "conflicts": 10, "clarifications": 16, "unsupported_semantics_retained": {"retained": 12, "expected": 12}, "ungrounded_rejections": 0, "accepted_augmentation_precision": {"matched_items": 14, "accepted_items": 27, "precision": 0.5185185185185185}}`
Failure classes: `{"EXTRACTOR_SEMANTIC_MISS": 2, "EXTRACTOR_WRONG_AMOUNT": 2, "MERGE_FALSE_ACCEPT": 2, "MERGE_FALSE_REJECT": 2}`

## Category outcomes

- ambiguous_monetary_scope: 5/5 (100.0%)
- correction: 1/3 (33.3%)
- negation_exclusion: 3/3 (100.0%)
- tradeoff_compositional: 4/4 (100.0%)
- noisy_imperfect_english: 1/3 (33.3%)

## Local controls (zero live calls)

Controls: 8; targeted checks passed: 8

- HYBRID-005: PASS `{"zero_live_calls": true, "coverage_skipped_llm": true, "supported_constraints_match": true, "preferences_preserved": true, "unsupported_scopes_preserved": true, "blocking_ambiguity_preserved_when_unsupported": true}`
- SEM200-021: PASS `{"zero_live_calls": true, "coverage_skipped_llm": true, "supported_constraints_match": true, "preferences_preserved": true, "unsupported_scopes_preserved": true, "blocking_ambiguity_preserved_when_unsupported": true}`
- SEM200-041: PASS `{"zero_live_calls": true, "coverage_skipped_llm": true, "supported_constraints_match": true, "preferences_preserved": true, "unsupported_scopes_preserved": true, "blocking_ambiguity_preserved_when_unsupported": true}`
- SEM200-082: PASS `{"zero_live_calls": true, "coverage_skipped_llm": true, "supported_constraints_match": true, "preferences_preserved": true, "unsupported_scopes_preserved": true, "blocking_ambiguity_preserved_when_unsupported": true}`
- SEM200-131: PASS `{"zero_live_calls": true, "coverage_skipped_llm": true, "supported_constraints_match": true, "preferences_preserved": true, "unsupported_scopes_preserved": true, "blocking_ambiguity_preserved_when_unsupported": true}`
- SEM200-132: PASS `{"zero_live_calls": true, "coverage_skipped_llm": true, "supported_constraints_match": true, "preferences_preserved": true, "unsupported_scopes_preserved": true, "blocking_ambiguity_preserved_when_unsupported": true}`
- SEM200-133: PASS `{"zero_live_calls": true, "coverage_skipped_llm": true, "supported_constraints_match": true, "preferences_preserved": true, "unsupported_scopes_preserved": true, "blocking_ambiguity_preserved_when_unsupported": true}`
- SEM200-134: PASS `{"zero_live_calls": true, "coverage_skipped_llm": true, "supported_constraints_match": true, "preferences_preserved": true, "unsupported_scopes_preserved": true, "blocking_ambiguity_preserved_when_unsupported": true}`

## Case records

### SEM200-120
Input: Denver hotel budget: $460.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Denver hotel budget: $460"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Denver hotel budget: $460.", "reason": "The hotel budget does not specify whether $460 is for the total stay or per night."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 730, "output_tokens": 61, "total_tokens": 791, "latency_ms": 4084.81, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-121
Input: Reserve a $315 accommodation in Austin.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Reserve a $315  accommodation in Austin"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "$315 accommodation", "reason": "The lodging amount lacks an explicit total-stay or per-night basis."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 731, "output_tokens": 107, "total_tokens": 838, "latency_ms": 2737.55, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-123
Input: Hotel money is $430 in Las Vegas.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Hotel money is $430  in Las Vegas"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Hotel money is $430 in Las Vegas.", "reason": "The hotel amount lacks an explicit total-stay or per-night basis, so its scope is ambiguous."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 732, "output_tokens": 65, "total_tokens": 797, "latency_ms": 5559.83, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-124
Input: Washington DC lodging for $390, please.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Washington DC lodging for $390 , please"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [{"category": "HOTEL", "value": "lodging in Washington, DC", "source_text": "Washington DC lodging"}], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "$390", "reason": "The hotel/lodging amount does not specify whether it is for the total stay or per night."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "lodging in washington, dc"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 732, "output_tokens": 153, "total_tokens": 885, "latency_ms": 3082.53, "error": null}`
Merge: `{"decisions": ["LLM_REJECTED_UNSAFE", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-126
Input: A hotel price of $290 for Boston.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["A hotel price of $290  for Boston"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [{"category": "HOTEL", "value": "Boston", "source_text": "Boston"}], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "A hotel price of $290", "reason": "The hotel amount does not specify whether it is a total-stay price or a per-night price."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "boston"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 732, "output_tokens": 78, "total_tokens": 810, "latency_ms": 2497.68, "error": null}`
Merge: `{"decisions": ["LLM_REJECTED_UNSAFE", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-096
Input: Keep the whole trip below $1,100 and accommodation below $420 total. Adjust hotel only: $380.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Adjust hotel only: $380"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 420.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 380.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1100.0, "currency": "USD", "strength": "HARD", "source_text": "Keep the whole trip below $1,100", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 420.0, "currency": "USD", "strength": "HARD", "source_text": "accommodation below $420 total", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Adjust hotel only: $380", "reason": "The hotel amount does not explicitly specify whether it is a total-stay or per-night amount, so no lodging constraint can be extracted."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [["HOTEL_TOTAL", 380.0, "HARD"]], "extra_constraints": [["HOTEL_TOTAL", 420.0, "HARD"]], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 746, "output_tokens": 302, "total_tokens": 1048, "latency_ms": 3858.31, "error": null}`
Merge: `{"decisions": ["CLARIFICATION_REQUIRED", "DUPLICATE_CONFIRMED", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": ["UNRESOLVED_CORRECTION"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": true, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 420.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": true, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["EXTRACTOR_WRONG_AMOUNT", "EXTRACTOR_SEMANTIC_MISS", "MERGE_FALSE_ACCEPT"]` | Origin: `["evaluator", "extractor", "merge"]` | Evaluation gold stale: `True`

### SEM200-098
Input: Lodging must not exceed $460 total; entire trip must not exceed $980. Make lodging $400 instead.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Make lodging $400  instead", "Make lodging $400 instead"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 460.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 400.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 460.0, "currency": "USD", "strength": "HARD", "source_text": "Lodging must not exceed $460 total", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 980.0, "currency": "USD", "strength": "HARD", "source_text": "entire trip must not exceed $980", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Make lodging $400 instead.", "reason": "This may replace the $460 lodging cap, but it is unclear whether $400 is intended as a total-stay budget, a revised maximum, or an exact lodging spend."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [["HOTEL_TOTAL", 400.0, "HARD"]], "extra_constraints": [["HOTEL_TOTAL", 460.0, "HARD"]], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 747, "output_tokens": 449, "total_tokens": 1196, "latency_ms": 7085.83, "error": null}`
Merge: `{"decisions": ["DUPLICATE_CONFIRMED", "DUPLICATE_CONFIRMED", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": true, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 460.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": true, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["EXTRACTOR_WRONG_AMOUNT", "EXTRACTOR_SEMANTIC_MISS", "MERGE_FALSE_ACCEPT"]` | Origin: `["evaluator", "extractor", "merge"]` | Evaluation gold stale: `True`

### SEM200-100
Input: Whole trip under $1,600; hotel under $700 total. Sorry, hotel should be $640.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["hotel should be $640", "Sorry, hotel should be $640"], "signals": {"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 700.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1600.0, "currency": "USD", "strength": "HARD", "source_text": "Whole trip under $1,600", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 640.0, "currency": "USD", "strength": "HARD", "source_text": "hotel should be $640", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 745, "output_tokens": 204, "total_tokens": 949, "latency_ms": 3464.06, "error": null}`
Merge: `{"decisions": ["CORRECTION_APPLIED", "DUPLICATE_CONFIRMED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `["evaluator"]` | Evaluation gold stale: `True`

### SEM200-157
Input: I do not care about nightlife in Chicago.
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["I do not care about nightlife in Chicago"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "I do not care about nightlife in Chicago.", "reason": "This expresses an exclusion or lack of interest, which cannot be converted into a positive executable preference."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 732, "output_tokens": 64, "total_tokens": 796, "latency_ms": 1965.49, "error": null}`
Merge: `{"decisions": ["CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": ["UNSUPPORTED_SEMANTIC"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["EXCLUSION"], "semantic_safety_retained": true}`
Final: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-159
Input: Avoid expensive restaurants in Seattle.
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["Avoid expensive restaurants in Seattle"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Avoid expensive restaurants in Seattle.", "reason": "Exclusion language ('Avoid') is not executable as a positive preference or constraint."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 729, "output_tokens": 58, "total_tokens": 787, "latency_ms": 1563.87, "error": null}`
Merge: `{"decisions": ["CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": ["UNSUPPORTED_SEMANTIC"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["EXCLUSION"], "semantic_safety_retained": true}`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-160
Input: I don't need museums in Denver.
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["I don't need museums in Denver"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "I don't need museums in Denver.", "reason": "This is exclusionary language about an activity; it cannot be converted into a positive executable preference."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 730, "output_tokens": 62, "total_tokens": 792, "latency_ms": 1837.66, "error": null}`
Merge: `{"decisions": ["CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": ["UNSUPPORTED_SEMANTIC"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["EXCLUSION"], "semantic_safety_retained": true}`
Final: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-167
Input: Save on food in Chicago so we can spend more on activities.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Save on food in Chicago so"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Chicago so we can spend more", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Save on food in Chicago so we can spend more on activities.", "reason": "This expresses a conditional budget tradeoff between food and activities; it cannot be reduced to independent preferences without implying an unstated priority or allocation."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 736, "output_tokens": 166, "total_tokens": 902, "latency_ms": 2896.46, "error": null}`
Merge: `{"decisions": ["CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": ["UNSUPPORTED_SEMANTIC"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["TRADEOFF"], "semantic_safety_retained": true}`
Final: `{"destination": "Chicago so we can spend more", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-168
Input: Prioritize hotel quality over restaurants for Miami.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Prioritize hotel quality over"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Prioritize hotel quality over restaurants for Miami.", "reason": "This expresses a conditional priority/tradeoff between hotel quality and restaurants, but does not specify an executable preference or constraint without implying completeness."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 732, "output_tokens": 72, "total_tokens": 804, "latency_ms": 1619.51, "error": null}`
Merge: `{"decisions": ["CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": ["UNSUPPORTED_SEMANTIC"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["TRADEOFF"], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-170
Input: For Denver, choose a cheaper hotel only if museums remain easy to reach.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["cheaper hotel only if"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "reach", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "choose a cheaper hotel only if museums remain easy to reach", "reason": "Conditional tradeoff between hotel price and museum accessibility; cannot be reduced to independent executable requirements without changing the intended priority."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 738, "output_tokens": 71, "total_tokens": 809, "latency_ms": 2336.74, "error": null}`
Merge: `{"decisions": ["CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": ["UNSUPPORTED_SEMANTIC"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["TRADEOFF"], "semantic_safety_retained": true}`
Final: `{"destination": "reach", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-173
Input: Spend less on shows in Las Vegas so the hotel can be nicer.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Spend less on shows in Las Vegas so"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Las Vegas so the hotel can be nicer", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Spend less on shows in Las Vegas so the hotel can be nicer.", "reason": "This expresses a conditional budget tradeoff and priority between show spending and hotel quality, but does not specify executable limits, amounts, or priorities."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 737, "output_tokens": 173, "total_tokens": 910, "latency_ms": 2657.07, "error": null}`
Merge: `{"decisions": ["CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": ["UNSUPPORTED_SEMANTIC"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["TRADEOFF"], "semantic_safety_retained": true}`
Final: `{"destination": "Las Vegas so the hotel can be nicer", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-187
Input: whole Chicago trip cost less 1180 pls
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["whole Chicago trip cost less 1180 pls"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1180.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1180.0, "currency": "USD", "strength": "HARD", "source_text": "whole Chicago trip cost less 1180 pls", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 732, "output_tokens": 75, "total_tokens": 807, "latency_ms": 2406.46, "error": null}`
Merge: `{"decisions": ["LLM_REJECTED_UNSAFE", "CLARIFICATION_REQUIRED"], "conflicts": ["UNSAFE_HARD_PROPOSAL"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": true, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_REJECT"]` | Origin: `["merge"]` | Evaluation gold stale: `False`

### SEM200-188
Input: miami hotel 390 not 490 make it max total
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["miami hotel 390 not 490 make it max total"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 390.0, "currency": "USD", "strength": "HARD", "source_text": "miami hotel 390 not 490 make it max total", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "Miami", "source_text": "miami hotel"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "miami"]], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 735, "output_tokens": 233, "total_tokens": 968, "latency_ms": 5300.18, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "LLM_REJECTED_UNSAFE"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### SEM200-191
Input: austin all trip no more 1100; lodge total no more 430
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["austin all trip no more 1100", "lodge total no more 430"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1100.0, "currency": "USD", "strength": "HARD", "source_text": "all trip no more 1100", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 430.0, "currency": "USD", "strength": "HARD", "source_text": "lodge total no more 430", "extractor_source": "llm"}], "preferences": [{"category": "UNSPECIFIED", "value": "Austin", "source_text": "austin"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["UNSPECIFIED", "austin"]], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 739, "output_tokens": 196, "total_tokens": 935, "latency_ms": 2858.05, "error": null}`
Merge: `{"decisions": ["LLM_REJECTED_UNSAFE", "CLARIFICATION_REQUIRED", "LLM_REJECTED_UNSAFE", "CLARIFICATION_REQUIRED", "LLM_REJECTED_UNSAFE"], "conflicts": ["UNSAFE_HARD_PROPOSAL", "UNSAFE_HARD_PROPOSAL"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": true, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_REJECT"]` | Origin: `["merge"]` | Evaluation gold stale: `False`
