# Phase M6 — Final Extractor-Only Correction Experiment

Timestamp: `2026-09-15T21:43:45.260338+00:00`<br>
Model: `gpt-5.6-luna`<br>
Prompt version: `semantic_extractor_v3`<br>
Dataset: `hybrid_semantics_live_subset_m6`

## Summary

Calls: 12 | Completed/schema-valid: 12/12 | Provider failures: 0
Final hybrid semantic accuracy: 75.0%
Correction recall: `{"clear_positive_cases": 8, "correct_replacement_proposals": 8, "proposal_recall": 1.0, "correct_accepted_replacements": 7, "end_to_end_recall": 0.875}`
Open-world valid additions: 0
Evaluation-gold stale cases: `[]`
Unsupported-scope recognition: `{"live": "not_applicable", "local_shadow_controls": "4/4"}`
Hard safety: `{"silent_hard_constraint_corruption": 0, "wrong_hard_scope_accepted": 0, "wrong_hard_amount_accepted": 0, "soft_to_hard_unsafe_promotion": 0, "hard_to_soft_unsafe_downgrade": 0, "hallucinated_hard_constraints_accepted": 0, "unsupported_hard_constraints_silently_dropped": 0}`
Latency ms: `{"average": 2554.1541666666667, "median": 2168.335, "p95": 4129.07, "max": 4129.07}`
Token usage: `{"input_tokens": 11225, "output_tokens": 1543, "total_tokens": 12768, "average_per_case": 1064.0}`

## Selection

Frozen before execution: 6 clear corrections, 2 genuine ambiguities, 1 hard-to-soft correction, 1 soft-to-hard correction, 1 noisy clear correction, and 1 multi-scope correction; no normalized overlap with M5 or earlier datasets.
Category mix: `{"clear_correction": 6, "ambiguous_correction": 2, "hard_to_soft": 1, "soft_to_hard": 1, "noisy_clear_correction": 1, "multi_scope_correction": 1}`
Case IDs: `["M6-001", "M6-002", "M6-003", "M6-004", "M6-005", "M6-006", "M6-007", "M6-008", "M6-009", "M6-010", "M6-011", "M6-012"]`

## Extractor and grounding

Constraint: `{"matched": 10, "expected": 10, "proposed": 13, "false_positive": 3, "precision": 0.7692307692307693, "recall": 1.0, "f1": 0.8695652173913043}`
Scope: `{"matched": 10, "expected": 10, "proposed": 13, "false_positive": 3, "precision": 0.7692307692307693, "recall": 1.0, "f1": 0.8695652173913043}`
Amount: `{"matched": 10, "expected": 10, "proposed": 13, "false_positive": 3, "precision": 0.7692307692307693, "recall": 1.0, "f1": 0.8695652173913043}`
Strength: `{"matched": 10, "expected": 10, "proposed": 13, "false_positive": 3, "precision": 0.7692307692307693, "recall": 1.0, "f1": 0.8695652173913043}`
Operator: `{"matched": 10, "expected": 10, "proposed": 13, "false_positive": 3, "precision": 0.7692307692307693, "recall": 1.0, "f1": 0.8695652173913043}`
Preference: `{"matched": 0, "expected": 1, "proposed": 0, "false_positive": 0, "precision": null, "recall": 0.0, "f1": 0.0}`
Ambiguity: `{"matched": 2, "expected": 3, "proposed": 2, "false_positive": 0, "precision": 1.0, "recall": 0.6666666666666666, "f1": 0.8}`
Grounding: `{"proposed_items": 15, "grounded_items": 15, "ungrounded_items": 0, "cases_with_ungrounded_rejection": 0, "accepted_grounded_additions": 13, "rejected_ungrounded_additions": 0}`

## Merge and failure taxonomy

Merge: `{"accepted_augmentations": 2, "rejected_proposals": 0, "duplicates": 1, "conflicts": 4, "clarifications": 4, "unsupported_semantics_retained": {"retained": 0, "expected": 0}, "ungrounded_rejections": 0, "accepted_augmentation_precision": {"matched_items": 10, "accepted_items": 13, "precision": 0.7692307692307693}}`
Failure classes: `{"AMBIGUITY_OVERRESOLUTION": 2, "AMBIGUITY_UNDERDETECTION": 1, "EXTRACTOR_SEMANTIC_MISS": 1, "MERGE_FALSE_ACCEPT": 1, "MERGE_FALSE_REJECT": 1}`

## Category outcomes

- clear_correction: 5/6 (83.3%)
- ambiguous_correction: 2/2 (100.0%)
- hard_to_soft: 0/1 (0.0%)
- soft_to_hard: 0/1 (0.0%)
- noisy_clear_correction: 1/1 (100.0%)
- multi_scope_correction: 1/1 (100.0%)

## Local controls (zero live calls)

Controls: 0; targeted checks passed: 0


## Case records

### M6-001
Input: Hotel spending for the whole trip must stay under $575. Sorry, revise lodging to $525.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Sorry, revise lodging to $525", "Sorry, revise lodging to $525"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 575.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 525.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 525.0, "currency": "USD", "strength": "HARD", "source_text": "Sorry, revise lodging to $525.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 935, "output_tokens": 120, "total_tokens": 1055, "latency_ms": 4129.07, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 525.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M6-002
Input: Keep the entire trip under $1,850. Actually, the trip cap should be $1,700.
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Actually, the trip cap should be $1,700", "Actually, the trip cap should be $1,700"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1850.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1700.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1700.0, "currency": "USD", "strength": "HARD", "source_text": "Actually, the trip cap should be $1,700.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 937, "output_tokens": 77, "total_tokens": 1014, "latency_ms": 2299.04, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1700.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M6-003
Input: Hotel total must not exceed $680. Please change it to $620.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["change it to $620"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 680.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 620.0, "currency": "USD", "strength": "HARD", "source_text": "Please change it to $620.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 930, "output_tokens": 71, "total_tokens": 1001, "latency_ms": 2171.02, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M6-004
Input: Trip maximum is $1,500. On second thought, no, use $1,380.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["use $1,380"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1380.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1380.0, "currency": "USD", "strength": "HARD", "source_text": "use $1,380", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 935, "output_tokens": 71, "total_tokens": 1006, "latency_ms": 1929.44, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_REPLACEMENT_REJECTED", "CLARIFICATION_REQUIRED", "STALE_PROPOSAL_REJECTED"], "conflicts": ["UNRESOLVED_CORRECTION"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": true, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_REJECT"]` | Origin: `["merge"]` | Evaluation gold stale: `False`

### M6-005
Input: All lodging combined must stay below $760. Correction: sorry, I meant $710 for the hotel total.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Correction: sorry, I meant $710  for the hotel total", "sorry, I meant $710 for the hotel total"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 760.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 710.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 710.0, "currency": "USD", "strength": "HARD", "source_text": "sorry, I meant $710 for the hotel total.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 937, "output_tokens": 75, "total_tokens": 1012, "latency_ms": 1564.44, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 710.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M6-006
Input: The whole trip ceiling is $2,100. For the revision, make the total $1,950.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["make the total $1,950"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1950.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1950.0, "currency": "USD", "strength": "HARD", "source_text": "make the total $1,950", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 937, "output_tokens": 73, "total_tokens": 1010, "latency_ms": 2165.65, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1950.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M6-007
Input: Trip max $1,400. Hotel total max $600. After those, actually set it at $950.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["actually set it at $950"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1400.0, "currency": "USD", "strength": "HARD", "source_text": "Trip max $1,400.", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 600.0, "currency": "USD", "strength": "HARD", "source_text": "Hotel total max $600.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "After those, actually set it at $950.", "reason": "The correction amount is explicit, but its target is unclear: it could modify the total trip budget or the hotel total budget."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["HOTEL_TOTAL", 600.0, "HARD"], ["TOTAL_TRIP", 1400.0, "HARD"]], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 938, "output_tokens": 347, "total_tokens": 1285, "latency_ms": 3992.82, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "STALE_VALUE_REMOVED", "CORRECTION_REPLACEMENT_REJECTED", "CLARIFICATION_REQUIRED", "STALE_PROPOSAL_REJECTED", "STALE_PROPOSAL_REJECTED", "ADDED_FROM_LLM"], "conflicts": ["UNRESOLVED_CORRECTION"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_OVERRESOLUTION"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`

### M6-008
Input: Hotel total must stay below $500. Actually use either $440 or $460 depending on rooms.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Actually use either $440 or $460 depending on rooms"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "Actually use either $440 or $460 depending on rooms.", "reason": "The corrected hotel-total amount is conditional and provides multiple alternatives without specifying which amount applies to which room situation; the superseded $500 constraint cannot be retained."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 935, "output_tokens": 213, "total_tokens": 1148, "latency_ms": 3088.9, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_REPLACEMENT_REJECTED", "CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": ["UNRESOLVED_CORRECTION"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M6-009
Input: Hotel total must stay under $640. Actually, around $560 would be nice.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Actually, around $560 would be nice"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "around usd 560"}], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 560.0, "currency": "USD", "strength": "SOFT", "source_text": "Actually, around $560 would be nice.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["HOTEL_TOTAL", 560.0, "SOFT"]], "missing_preferences": [["HOTEL", "around usd 560"]], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 932, "output_tokens": 223, "total_tokens": 1155, "latency_ms": 3967.91, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_REPLACEMENT_REJECTED", "CLARIFICATION_REQUIRED", "STALE_PROPOSAL_REJECTED"], "conflicts": ["UNRESOLVED_CORRECTION"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["EXTRACTOR_SEMANTIC_MISS", "AMBIGUITY_OVERRESOLUTION", "AMBIGUITY_UNDERDETECTION"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`

### M6-010
Input: I'd prefer hotel around $520. Actually it must stay below $450 total for lodging.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Actually it must stay below $450 total for lodging"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "around usd 520"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 450.0, "currency": "USD", "strength": "HARD", "source_text": "Actually it must stay below $450 total for lodging.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 933, "output_tokens": 75, "total_tokens": 1008, "latency_ms": 1811.41, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "around usd 520"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_ACCEPT"]` | Origin: `["merge"]` | Evaluation gold stale: `False`

### M6-011
Input: lodging all-trip max usd 830... sry actually make teh hotel total usd 780
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["sry actually make teh hotel total usd 780", "actually make teh hotel total usd 780"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 830.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 780.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 780.0, "currency": "USD", "strength": "HARD", "source_text": "actually make teh hotel total usd 780", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 934, "output_tokens": 73, "total_tokens": 1007, "latency_ms": 1671.82, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 780.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`

### M6-012
Input: Whole trip must stay under $1,600; hotel total under $620. For the hotel revision, make hotel total $570.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["For the hotel revision, make hotel total $570", "make hotel total $570"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 570.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1600.0, "currency": "USD", "strength": "HARD", "source_text": "Whole trip must stay under $1,600", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 570.0, "currency": "USD", "strength": "HARD", "source_text": "For the hotel revision, make hotel total $570", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 942, "output_tokens": 125, "total_tokens": 1067, "latency_ms": 1858.33, "error": null}`
Merge: `{"decisions": ["CORRECTION_SCOPE_QUARANTINED", "STALE_VALUE_REMOVED", "CORRECTION_APPLIED", "DUPLICATE_CONFIRMED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 570.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `[]` | Evaluation gold stale: `False`
