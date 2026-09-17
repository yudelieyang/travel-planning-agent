# Phase M3 — Bounded Live Hybrid Evaluation

Timestamp: `2026-09-14T23:53:52.539521+00:00`<br>
Model: `gpt-5.6-luna`<br>
Prompt version: `semantic_extractor_v1`<br>
Dataset: `hybrid_semantics_200_live_subset_m3`

## Summary

Calls: 25 | Completed/schema-valid: 25/25 | Provider failures: 0
Final hybrid semantic accuracy: 20.0%
Open-world valid additions: 0
Evaluation-gold stale cases: `["SEM200-081", "SEM200-093", "SEM200-095", "SEM200-149", "SEM200-150", "SEM200-154"]`
Unsupported-scope recognition: `{"live": "not_applicable", "local_shadow_controls": "4/4"}`
Hard safety: `{"silent_hard_constraint_corruption": 3, "wrong_hard_scope_accepted": 1, "wrong_hard_amount_accepted": 3, "soft_to_hard_unsafe_promotion": 0, "hard_to_soft_unsafe_downgrade": 0, "hallucinated_hard_constraints_accepted": 3, "unsupported_hard_constraints_silently_dropped": 0}`
Latency ms: `{"average": 2474.09, "median": 2152.91, "p95": 4622.14, "max": 5336.03}`
Token usage: `{"input_tokens": 15943, "output_tokens": 3368, "total_tokens": 19311, "average_per_case": 772.44}`

## Selection

Nearest balanced gate-positive mix. M2 marks every retained unsupported-hard scope deterministic-complete, so sending FOOD_TOTAL, TRANSPORT_TOTAL, ATTRACTIONS_TOTAL, or HOTEL_PER_NIGHT live would violate the M3 needs_llm=true rule. Those four scopes are audited as zero-call shadow controls instead.
Category mix: `{"ambiguous_monetary_scope": 7, "unsupported_hard_scope": 0, "tradeoff_compositional": 4, "negation_exclusion": 3, "correction_unresolved": 3, "noisy_imperfect_english": 4, "complex_preference_requirement": 4}`
Case IDs: `["SEM200-116", "SEM200-117", "SEM200-118", "SEM200-119", "SEM200-122", "SEM200-125", "SEM200-130", "SEM200-166", "SEM200-169", "SEM200-172", "SEM200-175", "SEM200-156", "SEM200-158", "SEM200-163", "SEM200-081", "SEM200-093", "SEM200-095", "SEM200-186", "SEM200-189", "SEM200-192", "SEM200-194", "SEM200-149", "SEM200-150", "SEM200-154", "SEM200-199"]`

## Extractor and grounding

Constraint: `{"matched": 16, "expected": 16, "proposed": 24, "false_positive": 8, "precision": 0.6666666666666666, "recall": 1.0, "f1": 0.8}`
Scope: `{"matched": 16, "expected": 16, "proposed": 24, "false_positive": 8, "precision": 0.6666666666666666, "recall": 1.0, "f1": 0.8}`
Amount: `{"matched": 16, "expected": 16, "proposed": 24, "false_positive": 8, "precision": 0.6666666666666666, "recall": 1.0, "f1": 0.8}`
Strength: `{"matched": 16, "expected": 16, "proposed": 24, "false_positive": 8, "precision": 0.6666666666666666, "recall": 1.0, "f1": 0.8}`
Preference: `{"matched": 9, "expected": 10, "proposed": 22, "false_positive": 13, "precision": 0.4090909090909091, "recall": 0.9, "f1": 0.5625}`
Ambiguity: `{"matched": 2, "expected": 15, "proposed": 8, "false_positive": 6, "precision": 0.25, "recall": 0.13333333333333333, "f1": 0.17391304347826086}`
Grounding: `{"proposed_items": 54, "grounded_items": 53, "ungrounded_items": 1, "cases_with_ungrounded_rejection": 3, "accepted_grounded_additions": 40, "rejected_ungrounded_additions": 3}`

## Merge and failure taxonomy

Merge: `{"accepted_augmentations": 19, "rejected_proposals": 3, "duplicates": 5, "conflicts": 8, "clarifications": 7, "unsupported_semantics_retained": {"retained": 7, "expected": 15}, "ungrounded_rejections": 3, "accepted_augmentation_precision": {"matched_items": 18, "accepted_items": 40, "precision": 0.45}}`
Failure classes: `{"AMBIGUITY_OVERRESOLUTION": 8, "AMBIGUITY_UNDERDETECTION": 13, "EXTRACTOR_SEMANTIC_MISS": 3, "MERGE_FALSE_ACCEPT": 16, "MERGE_FALSE_REJECT": 3, "UNGROUNDED_PROPOSAL": 1}`

## Category outcomes

- ambiguous_monetary_scope: 4/7 (57.1%)
- tradeoff_compositional: 0/4 (0.0%)
- negation_exclusion: 0/3 (0.0%)
- correction_unresolved: 0/3 (0.0%)
- noisy_imperfect_english: 0/4 (0.0%)
- complex_preference_requirement: 1/4 (25.0%)

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

### SEM200-116
Input: I want a $240 hotel in Boston.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I want a $240  hotel in Boston"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 240.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 240.0, "currency": "USD", "strength": "HARD", "source_text": "$240 hotel", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "Boston", "source_text": "hotel in Boston"}], "objectives": [], "ambiguities": [{"level": "ASSUMABLE", "source_text": "$240 hotel", "reason": "The time basis is unspecified; interpreted as a total hotel budget rather than a nightly rate."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["HOTEL_TOTAL", 240.0, "HARD"]], "missing_preferences": [], "extra_preferences": [["HOTEL", "boston"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["ASSUMABLE"]}`
Extractor: `{"input_tokens": 633, "output_tokens": 120, "total_tokens": 753, "latency_ms": 4622.14, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 240.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "Boston"}], "ambiguity_levels": ["BLOCKING", "ASSUMABLE"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": true, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_OVERRESOLUTION", "AMBIGUITY_UNDERDETECTION", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-117
Input: My hotel budget is $375 for Chicago.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["My hotel budget is $375  for Chicago"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 375.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 375.0, "currency": "USD", "strength": "HARD", "source_text": "My hotel budget is $375 for Chicago.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["HOTEL_TOTAL", 375.0, "HARD"]], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 633, "output_tokens": 73, "total_tokens": 706, "latency_ms": 3680.43, "error": null}`
Merge: `{"decisions": ["DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED"], "conflicts": ["AMBIGUOUS_SCOPE"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_OVERRESOLUTION", "AMBIGUITY_UNDERDETECTION"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`

### SEM200-118
Input: $480 for lodging in Miami.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["$480  for lodging in Miami"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 480.0, "currency": "USD", "strength": "HARD", "source_text": "$480 for lodging in Miami.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["HOTEL_TOTAL", 480.0, "HARD"]], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 631, "output_tokens": 71, "total_tokens": 702, "latency_ms": 2488.9, "error": null}`
Merge: `{"decisions": ["DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED"], "conflicts": ["AMBIGUOUS_SCOPE"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_OVERRESOLUTION", "AMBIGUITY_UNDERDETECTION"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`

### SEM200-119
Input: I can spend $550 on the hotel in Seattle.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I can spend $550  on the hotel in Seattle"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 550.0, "currency": "USD", "strength": "HARD", "source_text": "I can spend $550 on the hotel in Seattle.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["HOTEL_TOTAL", 550.0, "HARD"]], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 635, "output_tokens": 75, "total_tokens": 710, "latency_ms": 1713.68, "error": null}`
Merge: `{"decisions": ["DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED"], "conflicts": ["AMBIGUOUS_SCOPE"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_OVERRESOLUTION", "AMBIGUITY_UNDERDETECTION"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`

### SEM200-122
Input: A $700 place to stay in New York City is okay.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["$700 place to stay"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "New York City is okay", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 700.0, "currency": "USD", "strength": "HARD", "source_text": "A $700 place to stay in New York City is okay.", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "place to stay in New York City", "source_text": "A $700 place to stay in New York City is okay."}], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "A $700 place to stay in New York City is okay.", "reason": "The timeframe and whether $700 is a total stay budget or a per-night budget are unspecified."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["HOTEL_TOTAL", 700.0, "HARD"]], "missing_preferences": [], "extra_preferences": [["HOTEL", "place to stay in new york city"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 637, "output_tokens": 154, "total_tokens": 791, "latency_ms": 1943.85, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": "New York City is okay", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 700.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "place to stay in New York City"}], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": true, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_OVERRESOLUTION", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-125
Input: I need a $820 hotel in San Francisco.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I need a $820  hotel in San Francisco"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 820.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 820.0, "currency": "USD", "strength": "HARD", "source_text": "$820 hotel", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "San Francisco", "source_text": "hotel in San Francisco"}], "objectives": [], "ambiguities": [{"level": "ASSUMABLE", "source_text": "$820 hotel", "reason": "The time period or number of nights is unspecified, so the budget is interpreted as a hotel-total budget rather than a per-night budget."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["HOTEL_TOTAL", 820.0, "HARD"]], "missing_preferences": [], "extra_preferences": [["HOTEL", "san francisco"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["ASSUMABLE"]}`
Extractor: `{"input_tokens": 634, "output_tokens": 131, "total_tokens": 765, "latency_ms": 2784.91, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 820.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "San Francisco"}], "ambiguity_levels": ["BLOCKING", "ASSUMABLE"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": true, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_OVERRESOLUTION", "AMBIGUITY_UNDERDETECTION", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-130
Input: For Denver I can do a $350 hotel.
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["For Denver I can do a $350  hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "UNSPECIFIED", "operator": "LTE", "value": 350.0, "currency": "USD", "strength": "HARD", "source_text": "I can do a $350 hotel.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": [{"level": "BLOCKING", "source_text": "$350 hotel", "reason": "It is unclear whether the $350 limit applies to the total hotel stay or the nightly hotel rate."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["UNSPECIFIED", 350.0, "HARD"]], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["BLOCKING"]}`
Extractor: `{"input_tokens": 634, "output_tokens": 206, "total_tokens": 840, "latency_ms": 2631.91, "error": null}`
Merge: `{"decisions": ["UNSUPPORTED_RETAINED", "CLARIFICATION_REQUIRED", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": true, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_OVERRESOLUTION"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`

### SEM200-166
Input: Spend more on the Boston hotel if it is downtown, but keep the whole trip below $1,300.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Spend more on the Boston hotel if"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1300.0, "currency": "USD", "strength": "HARD", "source_text": "keep the whole trip below $1,300", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "downtown Boston", "source_text": "if it is downtown"}], "objectives": ["maximize_budget_utilization"], "ambiguities": [{"level": "ASSUMABLE", "source_text": "Spend more on the Boston hotel if it is downtown", "reason": "The additional amount or hotel budget is unspecified; this is interpreted as a preference for a downtown hotel with willingness to allocate more toward it, subject to the total-trip budget."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": true}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "downtown boston"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["ASSUMABLE"]}`
Extractor: `{"input_tokens": 646, "output_tokens": 349, "total_tokens": 995, "latency_ms": 5336.03, "error": null}`
Merge: `{"decisions": ["DUPLICATE_CONFIRMED", "ADDED_FROM_LLM", "ADDED_FROM_LLM", "LLM_REJECTED_UNGROUNDED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": true, "actual": false, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["TRADEOFF"], "semantic_safety_retained": false}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "downtown Boston"}], "ambiguity_levels": ["ASSUMABLE"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_UNDERDETECTION", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-169
Input: I would pay more for a better Seattle location, while keeping total trip under $1,800.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["pay more for a better Seattle location, while"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1800.0, "currency": "USD", "strength": "HARD", "source_text": "keeping total trip under $1,800", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "better Seattle location", "source_text": "a better Seattle location"}], "objectives": ["maximize_budget_utilization"], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": true}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "better seattle location"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 644, "output_tokens": 99, "total_tokens": 743, "latency_ms": 2142.85, "error": null}`
Merge: `{"decisions": ["DUPLICATE_CONFIRMED", "ADDED_FROM_LLM", "LLM_REJECTED_UNGROUNDED"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": true, "actual": false, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["TRADEOFF"], "semantic_safety_retained": false}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "better Seattle location"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_UNDERDETECTION", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-172
Input: I value location over room size in New York City, up to a total of $2,100.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["value location over"], "signals": {"monetary_expressions": 0, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 2100.0, "currency": "USD", "strength": "HARD", "source_text": "up to a total of $2,100", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "location over room size in New York City", "source_text": "I value location over room size in New York City"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "location over room size in new york city"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 645, "output_tokens": 106, "total_tokens": 751, "latency_ms": 2043.72, "error": null}`
Merge: `{"decisions": ["DUPLICATE_CONFIRMED", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": true, "actual": false, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["TRADEOFF"], "semantic_safety_retained": false}`
Final: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "location over room size in New York City"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_UNDERDETECTION", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-175
Input: For San Francisco, prioritize seafood over attractions if choices conflict.
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["prioritize seafood over"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "seafood", "source_text": "prioritize seafood over attractions if choices conflict"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["FOOD", "seafood"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 636, "output_tokens": 47, "total_tokens": 683, "latency_ms": 1750.06, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": true, "actual": false, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["TRADEOFF"], "semantic_safety_retained": false}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_UNDERDETECTION", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-156
Input: Boston is fine, but do not include zoos.
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["Boston is fine, but do not include zoos"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "exclude zoos", "source_text": "do not include zoos"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["ACTIVITY", "exclude zoos"]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 635, "output_tokens": 45, "total_tokens": 680, "latency_ms": 1327.66, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": true, "actual": false, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["EXCLUSION"], "semantic_safety_retained": false}`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "exclude zoos"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_UNDERDETECTION", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-158
Input: No luxury hotels in Miami.
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["No luxury hotels in Miami"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [{"category": "HOTEL", "value": "No luxury hotels in Miami.", "source_text": "No luxury hotels in Miami."}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "no luxury hotels in miami."]], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 630, "output_tokens": 151, "total_tokens": 781, "latency_ms": 2846.41, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": true, "actual": false, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["EXCLUSION"], "semantic_safety_retained": false}`
Final: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "No luxury hotels in Miami."}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_UNDERDETECTION", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-163
Input: Don't schedule a casino in Las Vegas.
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["Don't schedule a casino in Las Vegas"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [], "objectives": [], "ambiguities": [{"level": "RESOLVED", "source_text": "Don't schedule a casino in Las Vegas.", "reason": "Explicit exclusion of casino-related activities in Las Vegas."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": ["RESOLVED"]}`
Extractor: `{"input_tokens": 632, "output_tokens": 55, "total_tokens": 687, "latency_ms": 2126.79, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": true, "actual": false, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["EXCLUSION"], "semantic_safety_retained": false}`
Final: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["RESOLVED"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["AMBIGUITY_UNDERDETECTION"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`

### SEM200-081
Input: Hotel spending cannot exceed $580 total. Actually, $530.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Actually, $530"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 580.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 530.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 530.0, "currency": "USD", "strength": "HARD", "source_text": "Actually, $530.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 1, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 637, "output_tokens": 129, "total_tokens": 766, "latency_ms": 2321.74, "error": null}`
Merge: `{"decisions": ["DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED"], "conflicts": ["EXPLICIT_CONSTRAINT_CONFLICT"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 580.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": true, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": true, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_REJECT", "MERGE_FALSE_ACCEPT"]` | Origin: `["evaluator", "merge"]` | Evaluation gold stale: `True`

### SEM200-093
Input: Trip ceiling $1,800 and lodging ceiling $750 total; sorry, make the trip $1,600.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["sorry, make the trip $1,600"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 1600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 750.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1600.0, "currency": "USD", "strength": "HARD", "source_text": "sorry, make the trip $1,600.", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 750.0, "currency": "USD", "strength": "HARD", "source_text": "lodging ceiling $750 total", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 647, "output_tokens": 121, "total_tokens": 768, "latency_ms": 2288.75, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED"], "conflicts": ["EXPLICIT_CONSTRAINT_CONFLICT"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 1600.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": true, "wrong_hard_scope_accepted": true, "wrong_hard_amount_accepted": true, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_REJECT", "MERGE_FALSE_ACCEPT"]` | Origin: `["evaluator", "merge"]` | Evaluation gold stale: `True`

### SEM200-095
Input: The total is capped at $1,350. Hotel total is capped at $500. Change total to $1,200 only.
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Change total to $1,200 only"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1200.0, "currency": "USD", "strength": "HARD", "source_text": "Change total to $1,200 only.", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 500.0, "currency": "USD", "strength": "HARD", "source_text": "Hotel total is capped at $500.", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 651, "output_tokens": 190, "total_tokens": 841, "latency_ms": 2175.11, "error": null}`
Merge: `{"decisions": ["DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED", "DUPLICATE_CONFIRMED"], "conflicts": ["EXPLICIT_CONSTRAINT_CONFLICT"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": true, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": true, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_REJECT", "MERGE_FALSE_ACCEPT"]` | Origin: `["evaluator", "merge"]` | Evaluation gold stale: `True`

### SEM200-186
Input: hotel money should not more then 470 total in Boston
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["hotel money should not more then 470 total in Boston"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 470.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 470.0, "currency": "USD", "strength": "HARD", "source_text": "hotel money should not more then 470 total in Boston", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "Boston", "source_text": "in Boston"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "boston"]], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 635, "output_tokens": 92, "total_tokens": 727, "latency_ms": 1707.21, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 470.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "Boston"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_ACCEPT"]` | Origin: `["merge"]` | Evaluation gold stale: `False`

### SEM200-189
Input: seattle trip budgt under 1500 and hotel 600 total
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["seattle trip budgt under 1500 and hotel 600 total"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1500.0, "currency": "USD", "strength": "HARD", "source_text": "budgt under 1500", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 600.0, "currency": "USD", "strength": "HARD", "source_text": "hotel 600 total", "extractor_source": "llm"}], "preferences": [{"category": "UNSPECIFIED", "value": "Seattle trip", "source_text": "seattle trip"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["UNSPECIFIED", "seattle trip"]], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 638, "output_tokens": 135, "total_tokens": 773, "latency_ms": 1882.02, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD"}], "preferences": [{"category": "UNSPECIFIED", "value": "Seattle trip"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_ACCEPT"]` | Origin: `["merge"]` | Evaluation gold stale: `False`

### SEM200-192
Input: nyc hotel money cant above 780 total and trip 1900 max
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["nyc hotel money cant above 780 total and trip 1900 max"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 780.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 780.0, "currency": "USD", "strength": "HARD", "source_text": "nyc hotel money cant above 780 total", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1900.0, "currency": "USD", "strength": "HARD", "source_text": "trip 1900 max", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "NYC", "source_text": "nyc hotel"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "nyc"]], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 639, "output_tokens": 138, "total_tokens": 777, "latency_ms": 1714.61, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 780.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "NYC"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["MERGE_FALSE_ACCEPT"]` | Origin: `["merge"]` | Evaluation gold stale: `False`

### SEM200-194
Input: wash dc accomodation total under 620, all trip under 1350
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["wash dc accomodation total under 620, all trip under 1350"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 620.0, "currency": "UNS", "strength": "HARD", "source_text": "wash dc accomodation total under 620", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1350.0, "currency": "UNS", "strength": "HARD", "source_text": "all trip under 1350", "extractor_source": "llm"}], "preferences": [{"category": "HOTEL", "value": "Accommodation in Washington, DC", "source_text": "wash dc accomodation"}], "objectives": [], "ambiguities": [{"level": "ASSUMABLE", "source_text": "620; 1350", "reason": "Currency is not specified."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 1, "grounded": false, "ungrounded_rejected": true}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [["HOTEL", "accommodation in washington, dc"]], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": ["ASSUMABLE"]}`
Extractor: `{"input_tokens": 639, "output_tokens": 303, "total_tokens": 942, "latency_ms": 3890.17, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED", "ADDED_FROM_LLM", "LLM_REJECTED_UNGROUNDED"], "conflicts": ["EXPLICIT_CONSTRAINT_CONFLICT"], "requires_clarification": true}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "Accommodation in Washington, DC"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["UNGROUNDED_PROPOSAL", "MERGE_FALSE_ACCEPT"]` | Origin: `["extractor", "merge"]` | Evaluation gold stale: `False`

### SEM200-149
Input: In Seattle I want seafood, coffee shops, and art museums.
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I want "], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Seattle I want seafood", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "seafood"}, {"category": "FOOD", "value": "coffee shops"}, {"category": "ACTIVITY", "value": "art museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "seafood", "source_text": "seafood"}, {"category": "FOOD", "value": "coffee shops", "source_text": "coffee shops"}, {"category": "ACTIVITY", "value": "art museums", "source_text": "art museums"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 637, "output_tokens": 73, "total_tokens": 710, "latency_ms": 1524.28, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": "Seattle I want seafood", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "seafood"}, {"category": "FOOD", "value": "coffee shops"}, {"category": "ACTIVITY", "value": "art museums"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["EXTRACTOR_SEMANTIC_MISS"]` | Origin: `["evaluator", "extractor"]` | Evaluation gold stale: `True`

### SEM200-150
Input: Denver: downtown hotel, public transit, and museums.
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["downtown hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "downtown hotel"}, {"category": "TRANSPORT", "value": "public transit"}, {"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [{"category": "HOTEL", "value": "downtown hotel", "source_text": "downtown hotel"}, {"category": "TRANSPORT", "value": "public transit", "source_text": "public transit"}, {"category": "ACTIVITY", "value": "museums", "source_text": "museums"}], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 3, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 635, "output_tokens": 155, "total_tokens": 790, "latency_ms": 2152.91, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "downtown hotel"}, {"category": "TRANSPORT", "value": "public transit"}, {"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `True` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `[]` | Origin: `["evaluator"]` | Evaluation gold stale: `True`

### SEM200-154
Input: Washington DC, please include museums, seafood, and a downtown hotel.
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["downtown hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "museums"}, {"category": "FOOD", "value": "seafood"}, {"category": "HOTEL", "value": "downtown hotel"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "museums", "source_text": "include museums"}, {"category": "FOOD", "value": "seafood", "source_text": "seafood"}, {"category": "HOTEL", "value": "downtown hotel", "source_text": "a downtown hotel"}], "objectives": [], "ambiguities": [{"level": "ASSUMABLE", "source_text": "Washington DC", "reason": "Destination is stated, but no destination field is available in the supplied schema."}]}`
Proposal validation: `{"schema_valid": true, "grounded_items": 4, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [], "missing_preferences": [], "extra_preferences": [], "expected_ambiguity_levels": [], "proposed_ambiguity_levels": ["ASSUMABLE"]}`
Extractor: `{"input_tokens": 638, "output_tokens": 107, "total_tokens": 745, "latency_ms": 2028.12, "error": null}`
Merge: `{"decisions": ["ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM", "ADDED_FROM_LLM"], "conflicts": [], "requires_clarification": false}`
Clarification: `{"expected": false, "actual": false, "correct": true}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": [], "semantic_safety_retained": true}`
Final: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "museums"}, {"category": "FOOD", "value": "seafood"}, {"category": "HOTEL", "value": "downtown hotel"}], "ambiguity_levels": ["ASSUMABLE"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["EXTRACTOR_SEMANTIC_MISS"]` | Origin: `["evaluator", "extractor"]` | Evaluation gold stale: `True`

### SEM200-199
Input: Seattle hotel around $600 total, but the whole trip cannot exceed $1,500.
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["hotel around $6"], "signals": {"monetary_expressions": 0, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "around usd 600"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Expected: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "HOTEL", "value": "around usd 600"}], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["HARD_SOFT_BOUNDARY"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Proposal: `{"constraints": [{"kind": "BUDGET", "scope": "HOTEL_TOTAL", "operator": "LTE", "value": 600.0, "currency": "USD", "strength": "SOFT", "source_text": "Seattle hotel around $600 total", "extractor_source": "llm"}, {"kind": "BUDGET", "scope": "TOTAL_TRIP", "operator": "LTE", "value": 1500.0, "currency": "USD", "strength": "HARD", "source_text": "the whole trip cannot exceed $1,500", "extractor_source": "llm"}], "preferences": [], "objectives": [], "ambiguities": []}`
Proposal validation: `{"schema_valid": true, "grounded_items": 2, "ungrounded_items": 0, "grounded": true, "ungrounded_rejected": false}`
Extractor correctness: `{"missing_constraints": [], "extra_constraints": [["HOTEL_TOTAL", 600.0, "SOFT"]], "missing_preferences": [["HOTEL", "around usd 600"]], "extra_preferences": [], "expected_ambiguity_levels": ["BLOCKING"], "proposed_ambiguity_levels": []}`
Extractor: `{"input_tokens": 642, "output_tokens": 243, "total_tokens": 885, "latency_ms": 2727.99, "error": null}`
Merge: `{"decisions": ["DETERMINISTIC_PRESERVED", "CLARIFICATION_REQUIRED", "DUPLICATE_CONFIRMED"], "conflicts": ["HARD_SOFT_CONFLICT"], "requires_clarification": true}`
Clarification: `{"expected": true, "actual": false, "correct": false}`
Unsupported handling: `{"expected_scopes": [], "final_scopes": [], "preserved": true, "expected_semantics": ["HARD_SOFT_BOUNDARY"], "semantic_safety_retained": false}`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "around usd 600"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Correct: `False` | Safety: `{"silent_hard_constraint_corruption": false, "wrong_hard_scope_accepted": false, "wrong_hard_amount_accepted": false, "soft_to_hard_unsafe_promotion": false, "hard_to_soft_unsafe_downgrade": false, "hallucinated_hard_constraints_accepted": false, "unsupported_hard_constraints_silently_dropped": false}`
Failure classes: `["EXTRACTOR_SEMANTIC_MISS", "AMBIGUITY_OVERRESOLUTION", "AMBIGUITY_UNDERDETECTION"]` | Origin: `["extractor"]` | Evaluation gold stale: `False`
