# Hybrid Semantic Evaluation hybrid_semantics_200_v1

Mode: `offline`<br>
Cases: 200<br>
Case pass rate: 38.0%
Offline-deferred hybrid cases: 0

## Coverage gate

TP: 44 | TN: 104 | FP: 31 | FN: 21
Precision: 58.7% | Recall: 67.7% | F1: 62.9%

## Hard-constraint safety

Silent hard corruption: 7
Wrong hard scope: 1
Wrong hard amount: 6
Soft → hard unsafe promotion: 0
Hard → soft unsafe downgrade: 0
Unsupported hard constraints silently dropped: 1

## Category pass rates

- A_simple_deterministic: 11/20 (55.0%)
- B_total_trip_hard: 7/20 (35.0%)
- C_hotel_total_hard: 7/15 (46.7%)
- D_multi_scope: 11/20 (55.0%)
- E_same_scope_correction: 11/15 (73.3%)
- F_mixed_scope_correction: 5/10 (50.0%)
- G_soft_approximate: 14/15 (93.3%)
- H_ambiguous_scope: 0/15 (0.0%)
- I_unsupported_hard_scope: 0/15 (0.0%)
- J_preferences: 0/10 (0.0%)
- K_negation_exclusion: 0/10 (0.0%)
- L_tradeoff_objective: 0/10 (0.0%)
- M_false_money: 10/10 (100.0%)
- N_noisy_english: 0/10 (0.0%)
- O_adversarial_boundary: 0/5 (0.0%)

## Failed cases by category and root cause

### A_simple_deterministic

#### SEM200-001 — PARSER_MISS
Input: Please plan a 2-day visit to Boston for one traveler.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": 2, "travelers": 1, "constraints": [], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "to Boston", "duration_days": 2, "travelers": 1, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "to Boston", "duration_days": 2, "travelers": 1, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-006 — PARSER_MISS
Input: A 1-day Austin getaway for 2 travelers.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": 1, "travelers": 2, "constraints": [], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": 1, "travelers": 2, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": 1, "travelers": 2, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-008 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Find me zoos in Columbus.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Columbus", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Columbus", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["Find me zoos"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Columbus", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-009 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Three days in San Francisco; I enjoy seafood.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "San Francisco", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I enjoy"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "San Francisco", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-012 — PARSER_MISS
Input: New York City, 4 days, two of us.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": 4, "travelers": 2, "constraints": [], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "New York City", "duration_days": 4, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "New York City", "duration_days": 4, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-013 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: I like fried chicken in Chicago.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken in chicago"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I like"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken in chicago"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-014 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Boston for 3 days. I enjoy walking.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [{"category": "TRANSPORT", "value": "walking"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Boston", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I enjoy"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-016 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: I want coffee shops in Seattle.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "coffee shops"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I want "], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-018 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Denver for one day; public transit is preferred.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": 1, "travelers": null, "constraints": [], "preferences": [{"category": "TRANSPORT", "value": "public transit"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Denver", "duration_days": 1, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["public transit is preferred"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Denver", "duration_days": 1, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

### B_total_trip_hard

#### SEM200-021 — PARSER_MISS
Input: Keep the total cost of my Boston trip under $875.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 875.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 875.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 875.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-022 — PARSER_MISS
Input: For Chicago, the whole trip must stay below $1,250.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1250.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1250.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1250.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-023 — PARSER_MISS
Input: No more than $760 total for a Miami vacation.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 760.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 760.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 760.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-024 — PARSER_MISS
Input: The entire Seattle trip cannot exceed $1,480.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1480.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1480.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1480.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-027 — PARSER_MISS
Input: Please keep everything within $1,600 for New York City.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-028 — PARSER_MISS
Input: My absolute ceiling for the full Las Vegas trip is $2,000.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2000.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2000.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2000.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-029 — PARSER_MISS
Input: The trip budget for Washington DC is $1,175 maximum.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1175.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1175.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1175.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-031 — PARSER_MISS
Input: For San Francisco, stay under $1,900 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-034 — PARSER_MISS
Input: The total for Miami has to stay at or below $1,010.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1010.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1010.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1010.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-035 — PARSER_MISS
Input: Keep the full trip below $1,550; Seattle is the destination.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1550.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1550.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1550.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-036 — PARSER_MISS
Input: My trip budget must not exceed $680 for Denver.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 680.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 680.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 680.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-038 — PARSER_MISS
Input: Budget the total New York City trip at $1,800 or less.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-040 — PARSER_MISS
Input: For Washington DC, keep the trip under $1,095—not a penny more.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1095.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1095.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1095.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

### C_hotel_total_hard

#### SEM200-042 — PARSER_MISS
Input: Lodging total for Chicago cannot exceed $610.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 610.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 610.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 610.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-045 — PARSER_MISS
Input: Cap my Denver hotel bill at $475 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 475.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 475.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 475.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-046 — PARSER_MISS
Input: Austin lodging cannot go above $560 in total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 560.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "total", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 560.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "total", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 560.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-047 — PARSER_MISS
Input: Keep hotel spending within $820 total for New York City.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 820.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 820.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 820.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-048 — PARSER_MISS
Input: For Las Vegas, the accommodation total must not exceed $740.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 740.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 740.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 740.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-050 — PARSER_MISS
Input: My San Francisco hotel must cost at most $900 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-053 — PARSER_MISS
Input: Accommodation in Miami: under $410 total, please.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 410.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 410.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 410.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-054 — COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Input: Do not let Seattle hotel spending exceed $635 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 635.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Do not let Seattle hotel spending exceed $635  total"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

### D_multi_scope

#### SEM200-057 — PARSER_MISS
Input: Hotel spending in Chicago must stay below $640 total, while the whole trip cannot exceed $1,550.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1550.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1550.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1550.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-058 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Miami, 3 days: total max $1,120. I like parks. Lodging total max $430.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": 3, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1120.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "parks"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Miami", "duration_days": 3, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1120.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I like"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Miami", "duration_days": 3, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1120.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-059 — COVERAGE_FALSE_POSITIVE, PARSER_MISS, WRONG_AMOUNT
Input: Keep the entire Seattle trip within $1,700, and keep accommodation within $760 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1700.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 760.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 760.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["Keep the entire Seattle trip within $1,700, and keep accommodation within $760 total"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 760.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-061 — PARSER_MISS
Input: For Austin
trip budget under $980 total
hotel budget under $390 total
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-065 — COVERAGE_FALSE_POSITIVE, PARSER_MISS, PREFERENCE_ERROR
Input: I enjoy seafood. San Francisco trip maximum is $2,200; accommodation maximum is $1,020 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 1020.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2200.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 1020.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I enjoy"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2200.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 1020.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-067 — PARSER_MISS
Input: Trip budget: $1,520 maximum for Chicago. Hotel total: $590 maximum.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1520.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 590.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1520.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 590.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1520.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 590.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-069 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Seattle: hotel under $725 total; total trip under $1,880. Museums please.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1880.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 725.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 725.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1880.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["Museums please"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 725.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1880.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-072 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: New York City: whole trip under $2,350. Quiet hotel, under $990 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2350.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 990.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "HOTEL", "value": "quiet hotel"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 990.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["Quiet hotel"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 990.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-074 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Washington DC trip must stay under $1,360, hotel total must stay under $540, and I like parks.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1360.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 540.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "parks"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1360.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 540.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I like"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1360.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 540.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

### E_same_scope_correction

#### SEM200-081 — COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR
Input: Hotel spending cannot exceed $580 total. Actually, $530.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 530.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 580.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Actually, $530"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 580.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-086 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: The full trip must stay below $1,090. Actually, I prefer museums.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1090.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1090.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I prefer"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1090.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-089 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Lodging must stay below $450 total. I'd rather stay downtown.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "HOTEL", "value": "downtown"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I'd rather stay"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-090 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: The trip maximum is $1,300. Actually, I want seafood.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I want "], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

### F_mixed_scope_correction

#### SEM200-093 — COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR
Input: Trip ceiling $1,800 and lodging ceiling $750 total; sorry, make the trip $1,600.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 750.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 1600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["sorry, make the trip $1,600"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 1600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-095 — COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR
Input: The total is capped at $1,350. Hotel total is capped at $500. Change total to $1,200 only.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Change total to $1,200 only"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-096 — COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Input: Keep the whole trip below $1,100 and accommodation below $420 total. Adjust hotel only: $380.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 380.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 420.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Adjust hotel only: $380"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 420.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-098 — COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Input: Lodging must not exceed $460 total; entire trip must not exceed $980. Make lodging $400 instead.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 400.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 460.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["Make lodging $400  instead", "Make lodging $400 instead"], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 460.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-100 — COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Input: Whole trip under $1,600; hotel under $700 total. Sorry, hotel should be $640.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 700.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE", "CORRECTION_TARGET_UNRESOLVED"], "evidence": ["hotel should be $640", "Sorry, hotel should be $640"], "signals": {"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 700.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

### G_soft_approximate

#### SEM200-105 — COVERAGE_FALSE_POSITIVE, PARSER_MISS
Input: About $1,100 total is my target for Denver, not a strict cap.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["not a strict cap"], "signals": {"monetary_expressions": 0, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

### H_ambiguous_scope

#### SEM200-116 — AMBIGUITY_ERROR
Input: I want a $240 hotel in Boston.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 240.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I want a $240  hotel in Boston"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-117 — AMBIGUITY_ERROR
Input: My hotel budget is $375 for Chicago.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 375.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["My hotel budget is $375  for Chicago"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-118 — AMBIGUITY_ERROR
Input: $480 for lodging in Miami.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["$480  for lodging in Miami"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-119 — AMBIGUITY_ERROR
Input: I can spend $550 on the hotel in Seattle.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I can spend $550  on the hotel in Seattle"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-120 — AMBIGUITY_ERROR
Input: Denver hotel budget: $460.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Denver hotel budget: $460"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-121 — AMBIGUITY_ERROR
Input: Reserve a $315 accommodation in Austin.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Reserve a $315  accommodation in Austin"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-122 — AMBIGUITY_ERROR
Input: A $700 place to stay in New York City is okay.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "New York City is okay", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["$700 place to stay"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "New York City is okay", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-123 — AMBIGUITY_ERROR
Input: Hotel money is $430 in Las Vegas.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Hotel money is $430  in Las Vegas"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-124 — AMBIGUITY_ERROR
Input: Washington DC lodging for $390, please.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Washington DC lodging for $390 , please"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-125 — AMBIGUITY_ERROR
Input: I need a $820 hotel in San Francisco.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 820.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I need a $820  hotel in San Francisco"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-126 — AMBIGUITY_ERROR
Input: A hotel price of $290 for Boston.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["A hotel price of $290  for Boston"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-127 — AMBIGUITY_ERROR
Input: Chicago accommodation costs $510 in my plan.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "my plan", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Chicago accommodation costs $510  in my plan"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "my plan", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-128 — AMBIGUITY_ERROR
Input: Can you find Miami lodging at $405?
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Can you find Miami lodging at $405"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-129 — AMBIGUITY_ERROR
Input: Seattle hotel: $660.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Seattle hotel: $660"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-130 — AMBIGUITY_ERROR
Input: For Denver I can do a $350 hotel.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["For Denver I can do a $350  hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`

### I_unsupported_hard_scope

#### SEM200-131 — COVERAGE_FALSE_NEGATIVE
Input: Food must stay below $260 in Boston.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_constraints": [{"scope": "FOOD_TOTAL", "value": 260.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-132 — COVERAGE_FALSE_NEGATIVE
Input: Chicago transportation cannot exceed $140.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_constraints": [{"scope": "TRANSPORT_TOTAL", "value": 140.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-133 — COVERAGE_FALSE_NEGATIVE
Input: Activities in Miami must cost no more than $190.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_constraints": [{"scope": "ATTRACTIONS_TOTAL", "value": 190.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-134 — COVERAGE_FALSE_NEGATIVE
Input: Seattle hotel must stay under $210 per night.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_constraints": [{"scope": "HOTEL_PER_NIGHT", "value": 210.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-135 — COVERAGE_FALSE_NEGATIVE
Input: No more than $310 for restaurants in Denver.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_constraints": [{"scope": "FOOD_TOTAL", "value": 310.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-136 — COVERAGE_FALSE_NEGATIVE
Input: Austin transit spending must stay under $95.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_constraints": [{"scope": "TRANSPORT_TOTAL", "value": 95.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-137 — COVERAGE_FALSE_NEGATIVE
Input: Attractions for New York City cannot exceed $275.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_constraints": [{"scope": "ATTRACTIONS_TOTAL", "value": 275.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-138 — COVERAGE_FALSE_NEGATIVE
Input: Las Vegas accommodation must be under $180 per night.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_constraints": [{"scope": "HOTEL_PER_NIGHT", "value": 180.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-139 — COVERAGE_FALSE_NEGATIVE
Input: Washington DC meal budget must not exceed $230.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_constraints": [{"scope": "FOOD_TOTAL", "value": 230.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-140 — COVERAGE_FALSE_NEGATIVE
Input: Keep transport below $120 in San Francisco.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_constraints": [{"scope": "TRANSPORT_TOTAL", "value": 120.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-141 — COVERAGE_FALSE_NEGATIVE
Input: Boston museum tickets must stay below $160.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_constraints": [{"scope": "ATTRACTIONS_TOTAL", "value": 160.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-142 — COVERAGE_FALSE_NEGATIVE
Input: Chicago hotel is capped at $155 per night.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_constraints": [{"scope": "HOTEL_PER_NIGHT", "value": 155.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-143 — COVERAGE_FALSE_NEGATIVE
Input: Food in Miami: $290 maximum.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_constraints": [{"scope": "FOOD_TOTAL", "value": 290.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-144 — COVERAGE_FALSE_NEGATIVE
Input: Denver flights and transport must stay under $210.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_constraints": [{"scope": "TRANSPORT_TOTAL", "value": 210.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

#### SEM200-145 — COVERAGE_FALSE_NEGATIVE
Input: Austin activities max $145.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_constraints": [{"scope": "ATTRACTIONS_TOTAL", "value": 145.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_semantics": [], "requires_clarification": true}`

### J_preferences

#### SEM200-146 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Boston: zoos, parks, and seafood please.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "ACTIVITY", "value": "parks"}, {"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["zoos, parks, and seafood please"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-147 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: I like fried chicken, art museums, and coffee shops in Chicago.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}, {"category": "ACTIVITY", "value": "art museums"}, {"category": "FOOD", "value": "coffee shops"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}, {"category": "ACTIVITY", "value": "art museums"}, {"category": "FOOD", "value": "coffee shops in chicago"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I like"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}, {"category": "ACTIVITY", "value": "art museums"}, {"category": "FOOD", "value": "coffee shops in chicago"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-148 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Miami should have a quiet hotel and nearby parks.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "quiet hotel"}, {"category": "ACTIVITY", "value": "parks"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["quiet hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-149 — COVERAGE_FALSE_POSITIVE, PARSER_MISS, PREFERENCE_ERROR
Input: In Seattle I want seafood, coffee shops, and art museums.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "seafood"}, {"category": "FOOD", "value": "coffee shops"}, {"category": "ACTIVITY", "value": "art museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Seattle I want seafood", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["I want "], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Seattle I want seafood", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-150 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Denver: downtown hotel, public transit, and museums.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "downtown hotel"}, {"category": "TRANSPORT", "value": "public transit"}, {"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["downtown hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-151 — PARSER_MISS, PREFERENCE_ERROR
Input: For Austin, I enjoy parks, fried chicken, and walking.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "parks"}, {"category": "FOOD", "value": "fried chicken"}, {"category": "TRANSPORT", "value": "walking"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-152 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: New York City needs a quiet hotel, seafood, and zoos.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "quiet hotel"}, {"category": "FOOD", "value": "seafood"}, {"category": "ACTIVITY", "value": "zoo"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["quiet hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-153 — PREFERENCE_ERROR
Input: Las Vegas: parks, coffee shops, and public transit are important.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "parks"}, {"category": "FOOD", "value": "coffee shops"}, {"category": "TRANSPORT", "value": "public transit"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-154 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: Washington DC, please include museums, seafood, and a downtown hotel.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "museums"}, {"category": "FOOD", "value": "seafood"}, {"category": "HOTEL", "value": "downtown hotel"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["downtown hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-155 — COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR
Input: San Francisco with zoos, fried chicken, and a quiet hotel.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chicken"}, {"category": "HOTEL", "value": "quiet hotel"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["quiet hotel"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

### K_negation_exclusion

#### SEM200-156 — AMBIGUITY_ERROR
Input: Boston is fine, but do not include zoos.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["Boston is fine, but do not include zoos"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-157 — AMBIGUITY_ERROR
Input: I do not care about nightlife in Chicago.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["I do not care about nightlife in Chicago"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-158 — AMBIGUITY_ERROR
Input: No luxury hotels in Miami.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["No luxury hotels in Miami"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-159 — AMBIGUITY_ERROR
Input: Avoid expensive restaurants in Seattle.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["Avoid expensive restaurants in Seattle"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-160 — AMBIGUITY_ERROR
Input: I don't need museums in Denver.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["I don't need museums in Denver"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-161 — AMBIGUITY_ERROR
Input: Please exclude parks from the Austin plan.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["Please exclude parks from the Austin plan"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-162 — AMBIGUITY_ERROR
Input: No seafood for New York City.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["No seafood for New York City"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-163 — AMBIGUITY_ERROR
Input: Don't schedule a casino in Las Vegas.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["Don't schedule a casino in Las Vegas"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-164 — AMBIGUITY_ERROR
Input: Washington DC, no crowded hotel areas.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["Washington DC, no crowded hotel areas"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-165 — AMBIGUITY_ERROR
Input: San Francisco without tourist-trap restaurants.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNREPRESENTED_NEGATION"], "evidence": ["San Francisco without tourist-trap restaurants"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

### L_tradeoff_objective

#### SEM200-166 — AMBIGUITY_ERROR
Input: Spend more on the Boston hotel if it is downtown, but keep the whole trip below $1,300.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Spend more on the Boston hotel if"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-167 — AMBIGUITY_ERROR
Input: Save on food in Chicago so we can spend more on activities.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Chicago so we can spend more", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Save on food in Chicago so"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Chicago so we can spend more", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-168 — AMBIGUITY_ERROR
Input: Prioritize hotel quality over restaurants for Miami.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Prioritize hotel quality over"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-169 — AMBIGUITY_ERROR
Input: I would pay more for a better Seattle location, while keeping total trip under $1,800.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["pay more for a better Seattle location, while"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-170 — AMBIGUITY_ERROR
Input: For Denver, choose a cheaper hotel only if museums remain easy to reach.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "reach", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["cheaper hotel only if"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "reach", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-171 — AMBIGUITY_ERROR
Input: Austin food can be simpler if the hotel is closer to downtown.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "downtown", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["simpler if"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "downtown", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-172 — AMBIGUITY_ERROR
Input: I value location over room size in New York City, up to a total of $2,100.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["value location over"], "signals": {"monetary_expressions": 0, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-173 — AMBIGUITY_ERROR
Input: Spend less on shows in Las Vegas so the hotel can be nicer.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Las Vegas so the hotel can be nicer", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Spend less on shows in Las Vegas so"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Las Vegas so the hotel can be nicer", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-174 — AMBIGUITY_ERROR
Input: Pay extra for a quiet Washington DC hotel if it cuts commute time.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Pay extra for a quiet Washington DC hotel if"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-175 — AMBIGUITY_ERROR
Input: For San Francisco, prioritize seafood over attractions if choices conflict.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["prioritize seafood over"], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

### N_noisy_english

#### SEM200-186 — PARSER_MISS
Input: hotel money should not more then 470 total in Boston
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 470.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["hotel money should not more then 470 total in Boston"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-187 — PARSER_MISS
Input: whole Chicago trip cost less 1180 pls
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1180.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["whole Chicago trip cost less 1180 pls"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-188 — PARSER_MISS
Input: miami hotel 390 not 490 make it max total
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["miami hotel 390 not 490 make it max total"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-189 — PARSER_MISS
Input: seattle trip budgt under 1500 and hotel 600 total
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["seattle trip budgt under 1500 and hotel 600 total"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-190 — COVERAGE_FALSE_NEGATIVE, PREFERENCE_ERROR
Input: denver 3 days i like zoo and fried chiken
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Denver", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chiken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Denver", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chiken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-191 — PARSER_MISS
Input: austin all trip no more 1100; lodge total no more 430
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["austin all trip no more 1100", "lodge total no more 430"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-192 — PARSER_MISS
Input: nyc hotel money cant above 780 total and trip 1900 max
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 780.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["nyc hotel money cant above 780 total and trip 1900 max"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-193 — COVERAGE_FALSE_NEGATIVE
Input: vegas 2 day, trip max 1400, hotel max 550 totl
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Las Vegas", "duration_days": 2, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 550.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Las Vegas", "duration_days": 2, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 550.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Las Vegas", "duration_days": 2, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 550.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-194 — PARSER_MISS, WRONG_AMOUNT
Input: wash dc accomodation total under 620, all trip under 1350
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["wash dc accomodation total under 620, all trip under 1350"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-195 — PARSER_MISS
Input: san fran hotel shud be 800 total max; trip 2050 max
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2050.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 800.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["MONETARY_SEMANTIC_GAP"], "evidence": ["san fran hotel shud be 800 total max", "trip 2050 max"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

### O_adversarial_boundary

#### SEM200-196 — COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Input: Boston trip max $1,200. Hotel rating at least 4 stars.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["HOTEL_RATING"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-197 — COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR, UNSUPPORTED_SCOPE_ERROR
Input: Chicago hotel total max $500. Dinner around $90. Whole trip max $1,400.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_constraints": [{"scope": "FOOD_TOTAL", "value": 90.0, "strength": "SOFT", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-198 — COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Input: Miami total trip under $1,100. Visit 3 museums. Hotel total under $450.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["NUMERIC_SCOPE_BOUNDARY"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-199 — AMBIGUITY_ERROR
Input: Seattle hotel around $600 total, but the whole trip cannot exceed $1,500.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "HOTEL", "value": "around usd 600"}], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["HARD_SOFT_BOUNDARY"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "around usd 600"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["UNRESOLVED_REQUIREMENT_CLAUSE"], "evidence": ["hotel around $6"], "signals": {"monetary_expressions": 0, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD"}], "preferences": [{"category": "HOTEL", "value": "around usd 600"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`

#### SEM200-200 — COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Input: San Francisco hotel total max $900; actually make the trip 4 days, not $900.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": 4, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["CORRECTION_SCOPE_BOUNDARY"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Deterministic: `{"destination": "San Francisco", "duration_days": 4, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Proposal: `null`
Merge: `null`
Final: `{"destination": "San Francisco", "duration_days": 4, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
