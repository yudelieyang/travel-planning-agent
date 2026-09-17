# Phase M5 — Persistent Correction Quarantine Validation

Timestamp: `2026-09-15T18:50:22.737447+00:00`<br>
Model: `gpt-5.6-luna`<br>
Prompt version: `semantic_extractor_v2`<br>
Dataset: `hybrid_semantics_live_subset_m5`

## Summary

Calls: 10 | Completed/schema-valid: 10/10 | Provider failures: 0
Final hybrid semantic accuracy: 70.0%
Open-world valid additions: 0
Evaluation-gold stale cases: `[]`
Unsupported-scope recognition: `{"live": "not_applicable", "local_shadow_controls": "4/4"}`
Hard safety: `{"silent_hard_constraint_corruption": 0, "wrong_hard_scope_accepted": 0, "wrong_hard_amount_accepted": 0, "soft_to_hard_unsafe_promotion": 0, "hard_to_soft_unsafe_downgrade": 0, "hallucinated_hard_constraints_accepted": 0, "unsupported_hard_constraints_silently_dropped": 0}`
Latency ms: `{"average": 3877.6169999999997, "median": 2718.63, "p95": 8906.15, "max": 8906.15}`
Token usage: `{"input_tokens": 7406, "output_tokens": 1682, "total_tokens": 9088, "average_per_case": 908.8}`

## Selection

Frozen before execution: 5 correction cases, 2 ambiguous monetary cases, 1 multi-scope correction, 1 noisy correction, and 1 negative correction guard; no input overlaps prior datasets.
Category mix: `{"correction": 5, "ambiguous_monetary": 2, "multi_scope_correction": 1, "noisy_correction": 1, "negative_correction_guard": 1}`
Case IDs: `["M5-001", "M5-002", "M5-003", "M5-004", "M5-005", "M5-006", "M5-007", "M5-008", "M5-009", "M5-010"]`

## Extractor and grounding

Constraint: `{"matched": 6, "expected": 8, "proposed": 7, "false_positive": 1, "precision": 0.8571428571428571, "recall": 0.75, "f1": 0.8}`
Scope: `{"matched": 7, "expected": 8, "proposed": 7, "false_positive": 0, "precision": 1.0, "recall": 0.875, "f1": 0.9333333333333333}`
Amount: `{"matched": 6, "expected": 8, "proposed": 7, "false_positive": 1, "precision": 0.8571428571428571, "recall": 0.75, "f1": 0.8}`
Strength: `{"matched": 7, "expected": 8, "proposed": 7, "false_positive": 0, "precision": 1.0, "recall": 0.875, "f1": 0.9333333333333333}`
Preference: `{"matched": 0, "expected": 0, "proposed": 0, "false_positive": 0, "precision": null, "recall": null, "f1": null}`
Ambiguity: `{"matched": 3, "expected": 3, "proposed": 5, "false_positive": 2, "precision": 0.6, "recall": 1.0, "f1": 0.75}`
Grounding: `{"proposed_items": 12, "grounded_items": 12, "ungrounded_items": 0, "cases_with_ungrounded_rejection": 0, "accepted_grounded_additions": 13, "rejected_ungrounded_additions": 0}`

## Merge and failure taxonomy

Merge: `{"accepted_augmentations": 5, "rejected_proposals": 0, "duplicates": 1, "conflicts": 4, "clarifications": 6, "unsupported_semantics_retained": {"retained": 0, "expected": 0}, "ungrounded_rejections": 0, "accepted_augmentation_precision": {"matched_items": 7, "accepted_items": 13, "precision": 0.5384615384615384}}`
Failure classes: `{"EXTRACTOR_SEMANTIC_MISS": 2, "EXTRACTOR_WRONG_AMOUNT": 1, "MERGE_FALSE_REJECT": 1}`

## Category outcomes

- correction: 3/5 (60.0%)
- ambiguous_monetary: 2/2 (100.0%)
- multi_scope_correction: 0/1 (0.0%)
- noisy_correction: 1/1 (100.0%)
- negative_correction_guard: 1/1 (100.0%)

## Local controls (zero live calls)

Controls: 0; targeted checks passed: 0


## Case records

### M5-001
Input: Hotel spending for the entire stay must stay under $610. Sorry, revised lodging limit: $560.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Sorry, revised lodging limit: $560", "Sorry, revised lodging limit: $560"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 610.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 560.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 560.0, "currency": "USD", "strength": "HARD", "source_text": "Sorry, revised lodging limit: $560.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 744, "output_tokens": 127, "total_tokens": 871, "latency_ms": 6432.97, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_REPLACEMENT_REJECTED", "CLARIFICATION_REQUIRED", "STALE_PROPOSAL_REJECTED"], "conflicts": ["UNRESOLVED_CORRECTION"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": true, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_REJECT"]` | Origin: `["merge"]` | Evaluation gold stale: `False`

### M5-002
Input: Keep the whole trip under $1,740. Sorry, change the trip cap to $1,520.
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Sorry, change the trip cap to $1,520", "Sorry, change the trip cap to $1,520"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1740.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1520.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1520.0, "currency": "USD", "strength": "HARD", "source_text": "Sorry, change the trip cap to $1,520.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 745, "output_tokens": 77, "total_tokens": 822, "latency_ms": 2792.72, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1520.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M5-003
Input: All lodging for the trip cannot exceed $690. Actually, revise the lodging limit to $640.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Actually, revise the lodging limit to $640", "Actually, revise the lodging limit to $640"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 690.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 640.0, "currency": "USD", "strength": "HARD", "source_text": "Actually, revise the lodging limit to $640.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 743, "output_tokens": 74, "total_tokens": 817, "latency_ms": 2644.54, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M5-004
Input: The total trip must stay below $2,050. Sorry, lower the trip cap to $1,850.
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Sorry, lower the trip cap to $1,850", "Sorry, lower the trip cap to $1,850"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2050.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1850.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1850.0, "currency": "USD", "strength": "HARD", "source_text": "Sorry, lower the trip cap to $1,850.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 746, "output_tokens": 77, "total_tokens": 823, "latency_ms": 1770.33, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1850.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M5-005
Input: Hotel total ceiling is $720. Adjust the hotel total to $660.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Adjust the hotel total to $660"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 720.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 660.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 720.0, "currency": "USD", "strength": "HARD", "source_text": "Hotel total ceiling is $720.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Adjust the hotel total to $660.", "reason": "It is unclear whether $660 replaces the existing hard ceiling or specifies an exact hotel total; the operator and intended polarity are not explicit."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [["HOTEL_TOTAL", 660.0, "HARD"]], "extra_constraints": [["HOTEL_TOTAL", 720.0, "HARD"]], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 738, "output_tokens": 420, "total_tokens": 1158, "latency_ms": 7080.29, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_REPLACEMENT_REJECTED", "CLARIFICATION_REQUIRED", "STALE_PROPOSAL_REJECTED", "ADDED_FROM_LLM"], "conflicts": ["UNRESOLVED_CORRECTION"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": true, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["EXTRACTOR_WRONG_AMOUNT", "EXTRACTOR_SEMANTIC_MISS"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`

### M5-006
Input: Set aside $475 for the hotel.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Set aside $475  for the hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Set aside $475 for the hotel.", "reason": "The hotel amount does not specify whether $475 is for the total stay or per night."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 731, "output_tokens": 62, "total_tokens": 793, "latency_ms": 2193.04, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M5-007
Input: I can do $215 for lodging.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I can do $215  for lodging"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "$215 for lodging", "reason": "The lodging amount does not specify whether it is a total-stay budget or a per-night budget."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 731, "output_tokens": 61, "total_tokens": 792, "latency_ms": 1908.07, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M5-008
Input: Keep the entire trip under $1,300 and hotel total under $520. Actually make hotel total $470.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Actually make hotel total $470", "Actually make hotel total $470"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 520.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 470.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1300.0, "currency": "USD", "strength": "HARD", "source_text": "Keep the entire trip under $1,300", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Actually make hotel total $470.", "reason": "The hotel total scope is explicit, but the wording does not specify whether $470 is a hard maximum, an exact spend, or a soft target."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [["HOTEL_TOTAL", 470.0, "HARD"]], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 746, "output_tokens": 559, "total_tokens": 1305, "latency_ms": 8906.15, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_REPLACEMENT_REJECTED", "CLARIFICATION_REQUIRED", "DUPLICATE_CONFIRMED", "ADDED_FROM_LLM"], "conflicts": ["UNRESOLVED_CORRECTION"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": true, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["EXTRACTOR_SEMANTIC_MISS"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`

### M5-009
Input: hotel all nites max usd 640... wait actually pls make teh hotel total usd 590
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["wait actually pls make teh hotel total usd 590", "actually pls make teh hotel total usd 590"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 590.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 590.0, "currency": "USD", "strength": "HARD", "source_text": "pls make teh hotel total usd 590", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 742, "output_tokens": 156, "total_tokens": 898, "latency_ms": 3370.72, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 590.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M5-010
Input: Do not make the hotel total $650; I have not set a hotel cap.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Do not make the hotel total $650", "make the hotel total $650"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 650.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Do not make the hotel total $650; I have not set a hotel cap.", "reason": "The statement explicitly rejects a hotel total cap and provides no executable hotel budget constraint."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 740, "output_tokens": 69, "total_tokens": 809, "latency_ms": 1677.34, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "CORRECTION_REPLACEMENT_REJECTED", "CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": ["UNRESOLVED_CORRECTION"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`
