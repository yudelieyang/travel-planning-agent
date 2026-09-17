# Phase L — 200-Case Failure Audit

Failed cases audited: 139

## Corrected baseline

Audited semantic pass: 39.5%
Functional coverage: `{"TP": 43, "TN": 68, "FP": 0, "FN": 89, "precision": 1.0, "recall": 0.32575757575757575, "f1": 0.49142857142857144}`

## Classification counts

- EVALUATOR_BUG: 13
- GOLD_LABEL_ERROR: 4
- INTENTIONAL_HYBRID_BOUNDARY: 10
- REAL_AMBIGUITY_BUG: 10
- REAL_AMOUNT_BUG: 24
- REAL_CORRECTION_BUG: 10
- REAL_COVERAGE_FALSE_NEGATIVE: 11
- REAL_PARSER_BUG: 19
- REAL_PREFERENCE_BUG: 26
- REAL_SCOPE_BUG: 2
- UNSUPPORTED_BY_DESIGN: 10

## Hard-safety audit

### Raw silent_hard_corruption

| Case | Gold hard constraints | Actual hard constraints | Blocking state | Audit |
| --- | --- | --- | --- | --- |
| SEM200-057 | `[{'scope': 'TOTAL_TRIP', 'value': 1550.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 640.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 1550.0, 'strength': 'HARD'}]` | False | REAL_SCOPE_BUG |
| SEM200-080 | `[{'scope': 'TOTAL_TRIP', 'value': 1450.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 1650.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-085 | `[{'scope': 'HOTEL_TOTAL', 'value': 700.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 800.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-091 | `[{'scope': 'TOTAL_TRIP', 'value': 1280.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 620.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 1500.0, 'strength': 'HARD'}, {'scope': 'HOTEL_TOTAL', 'value': 620.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-092 | `[{'scope': 'TOTAL_TRIP', 'value': 1250.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 480.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 540.0, 'strength': 'HARD'}, {'scope': 'TOTAL_TRIP', 'value': 1250.0, 'strength': 'HARD'}]` | True | REAL_CORRECTION_BUG |
| SEM200-096 | `[{'scope': 'TOTAL_TRIP', 'value': 1100.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 380.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 420.0, 'strength': 'HARD'}]` | True | REAL_CORRECTION_BUG |
| SEM200-097 | `[{'scope': 'TOTAL_TRIP', 'value': 1750.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 850.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 2000.0, 'strength': 'HARD'}, {'scope': 'HOTEL_TOTAL', 'value': 850.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-098 | `[{'scope': 'TOTAL_TRIP', 'value': 980.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 400.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 460.0, 'strength': 'HARD'}, {'scope': 'TOTAL_TRIP', 'value': 980.0, 'strength': 'HARD'}]` | True | REAL_CORRECTION_BUG |
| SEM200-099 | `[{'scope': 'TOTAL_TRIP', 'value': 1300.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 600.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 1450.0, 'strength': 'HARD'}, {'scope': 'HOTEL_TOTAL', 'value': 600.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-100 | `[{'scope': 'TOTAL_TRIP', 'value': 1600.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 640.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 1600.0, 'strength': 'HARD'}, {'scope': 'HOTEL_TOTAL', 'value': 700.0, 'strength': 'HARD'}]` | True | REAL_CORRECTION_BUG |
| SEM200-115 | `[]` | `[{'scope': 'TOTAL_TRIP', 'value': 1200.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-120 | `[]` | `[{'scope': 'HOTEL_TOTAL', 'value': 460.0, 'strength': 'HARD'}]` | False | REAL_SCOPE_BUG |

### Raw unsupported_hard_drops

| Case | Gold hard constraints | Actual hard constraints | Blocking state | Audit |
| --- | --- | --- | --- | --- |
| SEM200-134 | `[]` | `[]` | False | REAL_AMOUNT_BUG |
| SEM200-135 | `[]` | `[]` | False | REAL_AMOUNT_BUG |
| SEM200-136 | `[]` | `[]` | False | REAL_AMOUNT_BUG |
| SEM200-137 | `[]` | `[]` | False | REAL_COVERAGE_FALSE_NEGATIVE |
| SEM200-138 | `[]` | `[]` | False | REAL_AMOUNT_BUG |
| SEM200-141 | `[]` | `[]` | False | REAL_AMOUNT_BUG |
| SEM200-142 | `[]` | `[]` | False | REAL_AMOUNT_BUG |
| SEM200-197 | `[{'scope': 'TOTAL_TRIP', 'value': 1400.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 500.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 500.0, 'strength': 'HARD'}, {'scope': 'TOTAL_TRIP', 'value': 1400.0, 'strength': 'HARD'}]` | False | GOLD_LABEL_ERROR |

### Raw wrong_hard_amount

| Case | Gold hard constraints | Actual hard constraints | Blocking state | Audit |
| --- | --- | --- | --- | --- |
| SEM200-057 | `[{'scope': 'TOTAL_TRIP', 'value': 1550.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 640.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 1550.0, 'strength': 'HARD'}]` | False | REAL_SCOPE_BUG |
| SEM200-080 | `[{'scope': 'TOTAL_TRIP', 'value': 1450.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 1650.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-085 | `[{'scope': 'HOTEL_TOTAL', 'value': 700.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 800.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-091 | `[{'scope': 'TOTAL_TRIP', 'value': 1280.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 620.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 1500.0, 'strength': 'HARD'}, {'scope': 'HOTEL_TOTAL', 'value': 620.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-092 | `[{'scope': 'TOTAL_TRIP', 'value': 1250.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 480.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 540.0, 'strength': 'HARD'}, {'scope': 'TOTAL_TRIP', 'value': 1250.0, 'strength': 'HARD'}]` | True | REAL_CORRECTION_BUG |
| SEM200-096 | `[{'scope': 'TOTAL_TRIP', 'value': 1100.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 380.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 420.0, 'strength': 'HARD'}]` | True | REAL_CORRECTION_BUG |
| SEM200-097 | `[{'scope': 'TOTAL_TRIP', 'value': 1750.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 850.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 2000.0, 'strength': 'HARD'}, {'scope': 'HOTEL_TOTAL', 'value': 850.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-098 | `[{'scope': 'TOTAL_TRIP', 'value': 980.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 400.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 460.0, 'strength': 'HARD'}, {'scope': 'TOTAL_TRIP', 'value': 980.0, 'strength': 'HARD'}]` | True | REAL_CORRECTION_BUG |
| SEM200-099 | `[{'scope': 'TOTAL_TRIP', 'value': 1300.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 600.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 1450.0, 'strength': 'HARD'}, {'scope': 'HOTEL_TOTAL', 'value': 600.0, 'strength': 'HARD'}]` | False | REAL_AMOUNT_BUG |
| SEM200-100 | `[{'scope': 'TOTAL_TRIP', 'value': 1600.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 640.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'TOTAL_TRIP', 'value': 1600.0, 'strength': 'HARD'}, {'scope': 'HOTEL_TOTAL', 'value': 700.0, 'strength': 'HARD'}]` | True | REAL_CORRECTION_BUG |

### Raw wrong_hard_scope

| Case | Gold hard constraints | Actual hard constraints | Blocking state | Audit |
| --- | --- | --- | --- | --- |
| SEM200-057 | `[{'scope': 'TOTAL_TRIP', 'value': 1550.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}, {'scope': 'HOTEL_TOTAL', 'value': 640.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[{'scope': 'HOTEL_TOTAL', 'value': 1550.0, 'strength': 'HARD'}]` | False | REAL_SCOPE_BUG |

### Raw hard_to_soft

| Case | Gold hard constraints | Actual hard constraints | Blocking state | Audit |
| --- | --- | --- | --- | --- |
| SEM200-199 | `[{'scope': 'TOTAL_TRIP', 'value': 1500.0, 'strength': 'HARD', 'operator': 'LTE', 'supported_for_execution': True}]` | `[]` | False | REAL_PARSER_BUG |

## Category triage

| Category | Raw pass | Real bugs | Evaluator/gold | Hybrid | Unsupported |
| --- | ---: | ---: | ---: | ---: | ---: |
| A_simple_deterministic | 55.0% | 9 | 0 | 0 | 0 |
| B_total_trip_hard | 20.0% | 16 | 0 | 0 | 0 |
| C_hotel_total_hard | 40.0% | 9 | 0 | 0 | 0 |
| D_multi_scope | 20.0% | 16 | 0 | 0 | 0 |
| E_same_scope_correction | 53.3% | 7 | 0 | 0 | 0 |
| F_mixed_scope_correction | 10.0% | 9 | 0 | 0 | 0 |
| G_soft_approximate | 66.7% | 5 | 0 | 0 | 0 |
| H_ambiguous_scope | 0.0% | 2 | 13 | 0 | 0 |
| I_unsupported_hard_scope | 46.7% | 8 | 0 | 0 | 0 |
| J_preferences | 0.0% | 10 | 0 | 0 | 0 |
| K_negation_exclusion | 0.0% | 0 | 0 | 0 | 10 |
| L_tradeoff_objective | 0.0% | 0 | 0 | 10 | 0 |
| M_false_money | 100.0% | 0 | 0 | 0 | 0 |
| N_noisy_english | 0.0% | 9 | 1 | 0 | 0 |
| O_adversarial_boundary | 0.0% | 2 | 3 | 0 | 0 |

## Failed-case audit table

### SEM200-001 — REAL_PARSER_BUG
Category: A_simple_deterministic
Input: Please plan a 2-day visit to Boston for one traveler.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": 2, "travelers": 1, "constraints": [], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "to Boston", "duration_days": 2, "travelers": 1, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-006 — REAL_PARSER_BUG
Category: A_simple_deterministic
Input: A 1-day Austin getaway for 2 travelers.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": 1, "travelers": 2, "constraints": [], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": 1, "travelers": 2, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-008 — REAL_PREFERENCE_BUG
Category: A_simple_deterministic
Input: Find me zoos in Columbus.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Columbus", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Columbus", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-009 — REAL_PREFERENCE_BUG
Category: A_simple_deterministic
Input: Three days in San Francisco; I enjoy seafood.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "San Francisco", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-012 — REAL_PARSER_BUG
Category: A_simple_deterministic
Input: New York City, 4 days, two of us.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": 4, "travelers": 2, "constraints": [], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "New York City", "duration_days": 4, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-013 — REAL_PREFERENCE_BUG
Category: A_simple_deterministic
Input: I like fried chicken in Chicago.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken in chicago"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-014 — REAL_PREFERENCE_BUG
Category: A_simple_deterministic
Input: Boston for 3 days. I enjoy walking.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [{"category": "TRANSPORT", "value": "walking"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-016 — REAL_PREFERENCE_BUG
Category: A_simple_deterministic
Input: I want coffee shops in Seattle.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "coffee shops"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-018 — REAL_PREFERENCE_BUG
Category: A_simple_deterministic
Input: Denver for one day; public transit is preferred.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": 1, "travelers": null, "constraints": [], "preferences": [{"category": "TRANSPORT", "value": "public transit"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Denver", "duration_days": 1, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-021 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: Keep the total cost of my Boston trip under $875.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 875.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 875.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-022 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: For Chicago, the whole trip must stay below $1,250.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1250.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1250.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-023 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: No more than $760 total for a Miami vacation.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 760.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 760.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-024 — REAL_AMOUNT_BUG
Category: B_total_trip_hard
Input: The entire Seattle trip cannot exceed $1,480.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1480.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-026 — REAL_AMOUNT_BUG
Category: B_total_trip_hard
Input: I can't go above $990 for the whole trip to Austin.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 990.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-027 — REAL_AMOUNT_BUG
Category: B_total_trip_hard
Input: Please keep everything within $1,600 for New York City.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-028 — REAL_AMOUNT_BUG
Category: B_total_trip_hard
Input: My absolute ceiling for the full Las Vegas trip is $2,000.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2000.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-029 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: The trip budget for Washington DC is $1,175 maximum.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1175.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1175.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-030 — REAL_AMOUNT_BUG
Category: B_total_trip_hard
Input: Do not let the total trip go over $845 in Columbus.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Columbus", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 845.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Columbus", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-031 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: For San Francisco, stay under $1,900 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-032 — REAL_AMOUNT_BUG
Category: B_total_trip_hard
Input: I only have $720 for the entire trip to Boston.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 720.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-034 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: The total for Miami has to stay at or below $1,010.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1010.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1010.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-035 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: Keep the full trip below $1,550; Seattle is the destination.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1550.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1550.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-036 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: My trip budget must not exceed $680 for Denver.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 680.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 680.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-038 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: Budget the total New York City trip at $1,800 or less.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-040 — REAL_PARSER_BUG
Category: B_total_trip_hard
Input: For Washington DC, keep the trip under $1,095—not a penny more.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1095.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1095.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-042 — REAL_AMBIGUITY_BUG
Category: C_hotel_total_hard
Input: Lodging total for Chicago cannot exceed $610.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 610.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Lodging total for Chicago cannot exceed $610"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-045 — REAL_AMBIGUITY_BUG
Category: C_hotel_total_hard
Input: Cap my Denver hotel bill at $475 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 475.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Cap my Denver hotel bill at $475  total"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-046 — REAL_AMBIGUITY_BUG
Category: C_hotel_total_hard
Input: Austin lodging cannot go above $560 in total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 560.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "total", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Austin lodging cannot go above $560  in total", "Unresolved hard hotel scope"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-047 — REAL_AMBIGUITY_BUG
Category: C_hotel_total_hard
Input: Keep hotel spending within $820 total for New York City.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 820.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Keep hotel spending within $820  total for New York City"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-048 — REAL_PARSER_BUG
Category: C_hotel_total_hard
Input: For Las Vegas, the accommodation total must not exceed $740.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 740.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 740.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-050 — REAL_PARSER_BUG
Category: C_hotel_total_hard
Input: My San Francisco hotel must cost at most $900 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-051 — REAL_AMBIGUITY_BUG
Category: C_hotel_total_hard
Input: Boston lodging spending has an absolute ceiling of $360 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 360.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Boston lodging spending has an absolute ceiling of $360  total"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-053 — REAL_PARSER_BUG
Category: C_hotel_total_hard
Input: Accommodation in Miami: under $410 total, please.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 410.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 410.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-054 — REAL_AMBIGUITY_BUG
Category: C_hotel_total_hard
Input: Do not let Seattle hotel spending exceed $635 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 635.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Do not let Seattle hotel spending exceed $635  total"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-057 — REAL_SCOPE_BUG
Category: D_multi_scope
Input: Hotel spending in Chicago must stay below $640 total, while the whole trip cannot exceed $1,550.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1550.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 1550.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS, WRONG_SCOPE
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-058 — REAL_PREFERENCE_BUG
Category: D_multi_scope
Input: Miami, 3 days: total max $1,120. I like parks. Lodging total max $430.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": 3, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1120.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "parks"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Miami", "duration_days": 3, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1120.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-059 — REAL_AMBIGUITY_BUG
Category: D_multi_scope
Input: Keep the entire Seattle trip within $1,700, and keep accommodation within $760 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1700.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 760.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["accommodation within $760  total"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-061 — REAL_AMOUNT_BUG
Category: D_multi_scope
Input: For Austin
trip budget under $980 total
hotel budget under $390 total
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS, WRONG_AMOUNT
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-062 — REAL_AMBIGUITY_BUG
Category: D_multi_scope
Input: New York City: cap the whole trip at $2,100; hotel spending cannot exceed $950 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 950.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["hotel spending cannot exceed $950  total"], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, WRONG_AMOUNT, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-064 — REAL_AMOUNT_BUG
Category: D_multi_scope
Input: Washington DC for 4 days, total under $1,420, with a hotel total under $610.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": 4, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1420.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 610.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Washington DC", "duration_days": 4, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 610.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: WRONG_AMOUNT
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-065 — REAL_PREFERENCE_BUG
Category: D_multi_scope
Input: I enjoy seafood. San Francisco trip maximum is $2,200; accommodation maximum is $1,020 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 1020.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2200.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 1020.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS, PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-066 — REAL_AMOUNT_BUG
Category: D_multi_scope
Input: Boston, 2 travelers. Keep everything under $1,450 and the lodging total under $600.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": 2, "constraints": [{"scope": "TOTAL_TRIP", "value": 1450.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": null, "travelers": 2, "constraints": [{"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: WRONG_AMOUNT
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-067 — REAL_PARSER_BUG
Category: D_multi_scope
Input: Trip budget: $1,520 maximum for Chicago. Hotel total: $590 maximum.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1520.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 590.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1520.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 590.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-068 — REAL_AMOUNT_BUG
Category: D_multi_scope
Input: In Miami, no more than $1,050 for the full trip and no more than $470 for lodging total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1050.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 470.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 470.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: WRONG_AMOUNT
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-069 — REAL_PREFERENCE_BUG
Category: D_multi_scope
Input: Seattle: hotel under $725 total; total trip under $1,880. Museums please.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1880.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 725.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 725.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1880.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-070 — REAL_AMBIGUITY_BUG
Category: D_multi_scope
Input: Hotel total cannot exceed $460 in Denver; the trip total cannot exceed $1,180.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1180.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 460.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Hotel total cannot exceed $460  in Denver"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-071 — REAL_AMBIGUITY_BUG
Category: D_multi_scope
Input: Austin has a $1,110 total-trip ceiling, plus a $440 hotel-total ceiling.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1110.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 440.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Austin has a $1,110 total-trip ceiling, plus a $440  hotel-total ceiling"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: Explicit executable scope is retained as blocking ambiguity instead of a canonical supported hard constraint.
Risk: P2
Disposition: Investigate scope anchors after P0 triage.

### SEM200-072 — REAL_PREFERENCE_BUG
Category: D_multi_scope
Input: New York City: whole trip under $2,350. Quiet hotel, under $990 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2350.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 990.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "HOTEL", "value": "quiet hotel"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 990.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-074 — REAL_PREFERENCE_BUG
Category: D_multi_scope
Input: Washington DC trip must stay under $1,360, hotel total must stay under $540, and I like parks.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1360.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 540.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "parks"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1360.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 540.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-075 — REAL_AMOUNT_BUG
Category: D_multi_scope
Input: San Francisco: no more than $2,050 overall; lodging no more than $880 total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2050.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 880.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 880.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: WRONG_AMOUNT
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-080 — REAL_AMOUNT_BUG
Category: E_same_scope_correction
Input: Trip budget $1,650 maximum. No, use $1,450 for the total trip.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1450.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1650.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: CORRECTION_ERROR
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-081 — REAL_CORRECTION_BUG
Category: E_same_scope_correction
Input: Hotel spending cannot exceed $580 total. Actually, $530.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 530.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Hotel spending cannot exceed $580  total"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-082 — REAL_AMOUNT_BUG
Category: E_same_scope_correction
Input: My whole-trip cap is $900; change that to $840.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 840.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: CORRECTION_ERROR
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-085 — REAL_AMOUNT_BUG
Category: E_same_scope_correction
Input: Hotel total $800 maximum; sorry, make that $700.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 700.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: CORRECTION_ERROR
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-086 — REAL_CORRECTION_BUG
Category: E_same_scope_correction
Input: The full trip must stay below $1,090. Actually, I prefer museums.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1090.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1090.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-089 — REAL_CORRECTION_BUG
Category: E_same_scope_correction
Input: Lodging must stay below $450 total. I'd rather stay downtown.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "HOTEL", "value": "downtown"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-090 — REAL_CORRECTION_BUG
Category: E_same_scope_correction
Input: The trip maximum is $1,300. Actually, I want seafood.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-091 — REAL_AMOUNT_BUG
Category: F_mixed_scope_correction
Input: Total trip max $1,500; hotel total max $620. Actually make the total $1,280.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1280.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: CORRECTION_ERROR
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-092 — REAL_CORRECTION_BUG
Category: F_mixed_scope_correction
Input: Hotel total under $540. Whole trip under $1,250. Change the hotel to $480.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1250.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 480.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 540.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1250.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Change the hotel to $480"], "signals": {"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-093 — REAL_CORRECTION_BUG
Category: F_mixed_scope_correction
Input: Trip ceiling $1,800 and lodging ceiling $750 total; sorry, make the trip $1,600.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 750.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING", "BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Trip ceiling $1,800  and lodging ceiling $750 total", "Trip ceiling $1,800 and lodging ceiling $750  total"], "signals": {"monetary_expressions": 3, "resolved_constraints": 0, "blocking_ambiguities": 2}}`
Reported: COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-095 — REAL_CORRECTION_BUG
Category: F_mixed_scope_correction
Input: The total is capped at $1,350. Hotel total is capped at $500. Change total to $1,200 only.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Hotel total is capped at $500"], "signals": {"monetary_expressions": 3, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-096 — REAL_CORRECTION_BUG
Category: F_mixed_scope_correction
Input: Keep the whole trip below $1,100 and accommodation below $420 total. Adjust hotel only: $380.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 380.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 420.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Adjust hotel only: $380"], "signals": {"monetary_expressions": 3, "resolved_constraints": 1, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-097 — REAL_AMOUNT_BUG
Category: F_mixed_scope_correction
Input: Trip max $2,000, hotel max $850 total. Actually change the total trip to $1,750.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1750.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 850.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2000.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 850.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: CORRECTION_ERROR
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-098 — REAL_CORRECTION_BUG
Category: F_mixed_scope_correction
Input: Lodging must not exceed $460 total; entire trip must not exceed $980. Make lodging $400 instead.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 400.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 460.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 980.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Make lodging $400  instead"], "signals": {"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-099 — REAL_AMOUNT_BUG
Category: F_mixed_scope_correction
Input: Total trip: $1,450 maximum. Hotel: $600 total maximum. No, use $1,300 for the trip.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1450.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: CORRECTION_ERROR
Root cause: explicit hard requirement was dropped, scoped incorrectly, or retained at a superseded value
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-100 — REAL_CORRECTION_BUG
Category: F_mixed_scope_correction
Input: Whole trip under $1,600; hotel under $700 total. Sorry, hotel should be $640.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 640.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 700.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["hotel should be $640"], "signals": {"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, CORRECTION_ERROR, AMBIGUITY_ERROR
Root cause: Correction cue or scope linkage is not resolved deterministically; blocking ambiguity prevents this from being silent in this case.
Risk: P2
Disposition: Audit correction bridge/segmentation together, after P0 cases.

### SEM200-104 — REAL_PREFERENCE_BUG
Category: G_soft_approximate
Input: Try to keep lodging roughly $560 total in Seattle.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "around usd 560"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Try to keep lodging roughly $560  total in Seattle"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR, AMBIGUITY_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-107 — REAL_PREFERENCE_BUG
Category: G_soft_approximate
Input: I can spend roughly $700 on a New York City hotel total.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "around usd 700"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I can spend roughly $700  on a New York City hotel total"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR, AMBIGUITY_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-108 — REAL_PREFERENCE_BUG
Category: G_soft_approximate
Input: Keep the Las Vegas hotel near $640 total if possible.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "around usd 640"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Keep the Las Vegas hotel near $640  total if possible"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR, AMBIGUITY_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-114 — REAL_PREFERENCE_BUG
Category: G_soft_approximate
Input: Seattle accommodation roughly $630 total, please.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "around usd 630"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Seattle accommodation roughly $630  total, please"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: COVERAGE_FALSE_POSITIVE, PREFERENCE_ERROR, AMBIGUITY_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-115 — REAL_AMOUNT_BUG
Category: G_soft_approximate
Input: Denver total under $1,200 would be ideal, though flexible.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS
Root cause: soft total target was promoted to an executable hard total
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-116 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: I want a $240 hotel in Boston.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 240.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I want a $240  hotel in Boston"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-117 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: My hotel budget is $375 for Chicago.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 375.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["My hotel budget is $375  for Chicago"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-118 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: $480 for lodging in Miami.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["$480  for lodging in Miami"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-119 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: I can spend $550 on the hotel in Seattle.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I can spend $550  on the hotel in Seattle"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-120 — REAL_SCOPE_BUG
Category: H_ambiguous_scope
Input: Denver hotel budget: $460.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 460.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PARSER_MISS, AMBIGUITY_ERROR
Root cause: ambiguous hotel amount was promoted to executable HOTEL_TOTAL
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-121 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: Reserve a $315 accommodation in Austin.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Reserve a $315  accommodation in Austin"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-122 — REAL_PARSER_BUG
Category: H_ambiguous_scope
Input: A $700 place to stay in New York City is okay.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "New York City is okay", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-123 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: Hotel money is $430 in Las Vegas.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Hotel money is $430  in Las Vegas"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-124 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: Washington DC lodging for $390, please.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Washington DC lodging for $390 , please"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-125 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: I need a $820 hotel in San Francisco.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [{"scope": "HOTEL_TOTAL", "value": 820.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["I need a $820  hotel in San Francisco"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-126 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: A hotel price of $290 for Boston.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["A hotel price of $290  for Boston"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-127 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: Chicago accommodation costs $510 in my plan.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "my plan", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Chicago accommodation costs $510  in my plan"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-128 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: Can you find Miami lodging at $405?
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Can you find Miami lodging at $405"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-129 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: Seattle hotel: $660.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["Seattle hotel: $660"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-130 — EVALUATOR_BUG
Category: H_ambiguous_scope
Input: For Denver I can do a $350 hotel.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": true}`
Coverage: `{"needs_llm": true, "reasons": ["AMBIGUOUS_SCOPE"], "evidence": ["For Denver I can do a $350  hotel"], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 1}}`
Reported: AMBIGUITY_ERROR
Root cause: Gold requires an unsupported_semantics detail, but the evaluator's actual view always emits an empty list despite the retained blocking ambiguity.
Risk: none
Disposition: Keep the case; revise only the evaluation contract after Phase L.

### SEM200-132 — REAL_COVERAGE_FALSE_NEGATIVE
Category: I_unsupported_hard_scope
Input: Chicago transportation cannot exceed $140.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_constraints": [{"scope": "TRANSPORT_TOTAL", "value": 140.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["ASSUMABLE"], "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-134 — REAL_AMOUNT_BUG
Category: I_unsupported_hard_scope
Input: Seattle hotel must stay under $210 per night.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_constraints": [{"scope": "HOTEL_PER_NIGHT", "value": 210.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR, UNSUPPORTED_SCOPE_ERROR
Root cause: unsupported hard requirement disappeared without a blocking semantic record
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-135 — REAL_AMOUNT_BUG
Category: I_unsupported_hard_scope
Input: No more than $310 for restaurants in Denver.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_constraints": [{"scope": "FOOD_TOTAL", "value": 310.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR, UNSUPPORTED_SCOPE_ERROR
Root cause: unsupported hard requirement disappeared without a blocking semantic record
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-136 — REAL_AMOUNT_BUG
Category: I_unsupported_hard_scope
Input: Austin transit spending must stay under $95.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["TRANSPORT_TOTAL"], "unsupported_constraints": [{"scope": "TRANSPORT_TOTAL", "value": 95.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR, UNSUPPORTED_SCOPE_ERROR
Root cause: unsupported hard requirement disappeared without a blocking semantic record
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-137 — REAL_COVERAGE_FALSE_NEGATIVE
Category: I_unsupported_hard_scope
Input: Attractions for New York City cannot exceed $275.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_constraints": [{"scope": "ATTRACTIONS_TOTAL", "value": 275.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["ASSUMABLE"], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR, UNSUPPORTED_SCOPE_ERROR
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-138 — REAL_AMOUNT_BUG
Category: I_unsupported_hard_scope
Input: Las Vegas accommodation must be under $180 per night.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_constraints": [{"scope": "HOTEL_PER_NIGHT", "value": 180.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR, UNSUPPORTED_SCOPE_ERROR
Root cause: unsupported hard requirement disappeared without a blocking semantic record
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-141 — REAL_AMOUNT_BUG
Category: I_unsupported_hard_scope
Input: Boston museum tickets must stay below $160.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["ATTRACTIONS_TOTAL"], "unsupported_constraints": [{"scope": "ATTRACTIONS_TOTAL", "value": 160.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR, UNSUPPORTED_SCOPE_ERROR
Root cause: unsupported hard requirement disappeared without a blocking semantic record
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-142 — REAL_AMOUNT_BUG
Category: I_unsupported_hard_scope
Input: Chicago hotel is capped at $155 per night.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["HOTEL_PER_NIGHT"], "unsupported_constraints": [{"scope": "HOTEL_PER_NIGHT", "value": 155.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR, UNSUPPORTED_SCOPE_ERROR
Root cause: unsupported hard requirement disappeared without a blocking semantic record
Risk: P0
Disposition: Phase-M hard-safety investigation.

### SEM200-146 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: Boston: zoos, parks, and seafood please.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "ACTIVITY", "value": "parks"}, {"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-147 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: I like fried chicken, art museums, and coffee shops in Chicago.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}, {"category": "ACTIVITY", "value": "art museums"}, {"category": "FOOD", "value": "coffee shops"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}, {"category": "ACTIVITY", "value": "art museums"}, {"category": "FOOD", "value": "coffee shops in chicago"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-148 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: Miami should have a quiet hotel and nearby parks.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "quiet hotel"}, {"category": "ACTIVITY", "value": "parks"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-149 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: In Seattle I want seafood, coffee shops, and art museums.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "seafood"}, {"category": "FOOD", "value": "coffee shops"}, {"category": "ACTIVITY", "value": "art museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle I want seafood", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS, PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-150 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: Denver: downtown hotel, public transit, and museums.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "downtown hotel"}, {"category": "TRANSPORT", "value": "public transit"}, {"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-151 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: For Austin, I enjoy parks, fried chicken, and walking.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "parks"}, {"category": "FOOD", "value": "fried chicken"}, {"category": "TRANSPORT", "value": "walking"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS, PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-152 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: New York City needs a quiet hotel, seafood, and zoos.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "quiet hotel"}, {"category": "FOOD", "value": "seafood"}, {"category": "ACTIVITY", "value": "zoo"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-153 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: Las Vegas: parks, coffee shops, and public transit are important.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "parks"}, {"category": "FOOD", "value": "coffee shops"}, {"category": "TRANSPORT", "value": "public transit"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-154 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: Washington DC, please include museums, seafood, and a downtown hotel.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "museums"}, {"category": "FOOD", "value": "seafood"}, {"category": "HOTEL", "value": "downtown hotel"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-155 — REAL_PREFERENCE_BUG
Category: J_preferences
Input: San Francisco with zoos, fried chicken, and a quiet hotel.
Gold: `{"needs_llm": false, "expected_runtime_llm_need": false, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chicken"}, {"category": "HOTEL", "value": "quiet hotel"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": true, "assumable_ambiguities": false}}`
Actual: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-156 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: Boston is fine, but do not include zoos.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-157 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: I do not care about nightlife in Chicago.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-158 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: No luxury hotels in Miami.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-159 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: Avoid expensive restaurants in Seattle.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-160 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: I don't need museums in Denver.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Denver", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-161 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: Please exclude parks from the Austin plan.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-162 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: No seafood for New York City.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-163 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: Don't schedule a casino in Las Vegas.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Las Vegas", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-164 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: Washington DC, no crowded hotel areas.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-165 — UNSUPPORTED_BY_DESIGN
Category: K_negation_exclusion
Input: San Francisco without tourist-trap restaurants.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["EXCLUSION"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Exclusion semantics have no canonical representation; the input must be preserved or clarified before any future execution support is considered.
Risk: P2
Disposition: Keep outside executable semantics; decide later whether to add an explicit exclusion ambiguity.

### SEM200-166 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: Spend more on the Boston hotel if it is downtown, but keep the whole trip below $1,300.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Trade-off language with multiple monetary statements"], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: none
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-167 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: Save on food in Chicago so we can spend more on activities.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Chicago so we can spend more", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: P1
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-168 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: Prioritize hotel quality over restaurants for Miami.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: P1
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-169 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: I would pay more for a better Seattle location, while keeping total trip under $1,800.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: P1
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-170 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: For Denver, choose a cheaper hotel only if museums remain easy to reach.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "reach", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: P1
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-171 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: Austin food can be simpler if the hotel is closer to downtown.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "downtown", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: P1
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-172 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: I value location over room size in New York City, up to a total of $2,100.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: P1
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-173 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: Spend less on shows in Las Vegas so the hotel can be nicer.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Las Vegas so the hotel can be nicer", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: P1
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-174 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: Pay extra for a quiet Washington DC hotel if it cuts commute time.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: P1
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-175 — INTENTIONAL_HYBRID_BOUNDARY
Category: L_tradeoff_objective
Input: For San Francisco, prioritize seafood over attractions if choices conflict.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["TRADEOFF"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Tradeoff/objective language requires grounded augmentation or clarification; it is not an executable planner constraint.
Risk: P1
Disposition: Keep hybrid; prioritize coverage only for the cases where the gate did not request augmentation.

### SEM200-186 — REAL_COVERAGE_FALSE_NEGATIVE
Category: N_noisy_english
Input: hotel money should not more then 470 total in Boston
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 470.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PARSER_MISS
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-187 — REAL_COVERAGE_FALSE_NEGATIVE
Category: N_noisy_english
Input: whole Chicago trip cost less 1180 pls
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1180.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PARSER_MISS
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-188 — REAL_COVERAGE_FALSE_NEGATIVE
Category: N_noisy_english
Input: miami hotel 390 not 490 make it max total
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PARSER_MISS
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-189 — REAL_COVERAGE_FALSE_NEGATIVE
Category: N_noisy_english
Input: seattle trip budgt under 1500 and hotel 600 total
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PARSER_MISS
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-190 — REAL_PREFERENCE_BUG
Category: N_noisy_english
Input: denver 3 days i like zoo and fried chiken
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Denver", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Denver", "duration_days": 3, "travelers": null, "constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chiken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PREFERENCE_ERROR
Root cause: Required grounded preference is missing or normalization includes unrelated location text.
Risk: P3
Disposition: Defer until hard safety and coverage are resolved.

### SEM200-191 — REAL_COVERAGE_FALSE_NEGATIVE
Category: N_noisy_english
Input: austin all trip no more 1100; lodge total no more 430
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Austin", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Austin", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PARSER_MISS
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-192 — REAL_COVERAGE_FALSE_NEGATIVE
Category: N_noisy_english
Input: nyc hotel money cant above 780 total and trip 1900 max
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "New York City", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 780.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "New York City", "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PARSER_MISS
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-193 — GOLD_LABEL_ERROR
Category: N_noisy_english
Input: vegas 2 day, trip max 1400, hotel max 550 totl
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Las Vegas", "duration_days": 2, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 550.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Las Vegas", "duration_days": 2, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 550.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE
Root cause: Gold demands hybrid/ambiguity semantics that the established contract does not require for this input.
Risk: none
Disposition: Correct gold in a later benchmark-only change.

### SEM200-194 — REAL_COVERAGE_FALSE_NEGATIVE
Category: N_noisy_english
Input: wash dc accomodation total under 620, all trip under 1350
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Washington DC", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PARSER_MISS, WRONG_AMOUNT
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-195 — REAL_COVERAGE_FALSE_NEGATIVE
Category: N_noisy_english
Input: san fran hotel shud be 800 total max; trip 2050 max
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 2050.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 800.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "merge_decisions": [], "requires_clarification": false, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": null, "duration_days": null, "travelers": null, "constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, PARSER_MISS
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-196 — REAL_COVERAGE_FALSE_NEGATIVE
Category: O_adversarial_boundary
Input: Boston trip max $1,200. Hotel rating at least 4 stars.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["HOTEL_RATING"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Boston", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Deterministic output loses required semantics while the coverage gate does not request augmentation.
Risk: P1
Disposition: Phase-M coverage investigation after P0 triage.

### SEM200-197 — GOLD_LABEL_ERROR
Category: O_adversarial_boundary
Input: Chicago hotel total max $500. Dinner around $90. Whole trip max $1,400.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": ["FOOD_TOTAL"], "unsupported_constraints": [{"scope": "FOOD_TOTAL", "value": 90.0, "strength": "SOFT", "operator": "LTE", "supported_for_execution": false}], "unsupported_semantics": [], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Chicago", "duration_days": null, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1400.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR, UNSUPPORTED_SCOPE_ERROR
Root cause: Gold demands hybrid/ambiguity semantics that the established contract does not require for this input.
Risk: none
Disposition: Correct gold in a later benchmark-only change.

### SEM200-198 — GOLD_LABEL_ERROR
Category: O_adversarial_boundary
Input: Miami total trip under $1,100. Visit 3 museums. Hotel total under $450.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["NUMERIC_SCOPE_BOUNDARY"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Miami", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Gold demands hybrid/ambiguity semantics that the established contract does not require for this input.
Risk: none
Disposition: Correct gold in a later benchmark-only change.

### SEM200-199 — REAL_PARSER_BUG
Category: O_adversarial_boundary
Input: Seattle hotel around $600 total, but the whole trip cannot exceed $1,500.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "HOTEL", "value": "around usd 600"}], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["HARD_SOFT_BOUNDARY"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "Seattle", "duration_days": null, "travelers": null, "constraints": [], "preferences": [{"category": "HOTEL", "value": "around usd 600"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": true, "reasons": ["TRADEOFF_LANGUAGE"], "evidence": ["Trade-off language with multiple monetary statements"], "signals": {"monetary_expressions": 2, "resolved_constraints": 0, "blocking_ambiguities": 0}}`
Reported: PARSER_MISS, AMBIGUITY_ERROR
Root cause: Deterministic extraction misses a required destination, traveler, or hard semantic without a justified contract boundary.
Risk: P2
Disposition: Cluster with the relevant parser-family audit; do not calibrate in Phase L.

### SEM200-200 — GOLD_LABEL_ERROR
Category: O_adversarial_boundary
Input: San Francisco hotel total max $900; actually make the trip 4 days, not $900.
Gold: `{"needs_llm": true, "expected_runtime_llm_need": true, "allow_hybrid_gap": false, "destination": "San Francisco", "duration_days": 4, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "merge_decisions": [], "requires_clarification": true, "unsupported_scopes": [], "unsupported_constraints": [], "unsupported_semantics": ["CORRECTION_SCOPE_BOUNDARY"], "forbidden_constraints": [], "forbidden_preferences": [], "allowed_grounded_additions": {"preferences": false, "assumable_ambiguities": false}}`
Actual: `{"destination": "San Francisco", "duration_days": 4, "travelers": null, "constraints": [{"scope": "HOTEL_TOTAL", "value": 900.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": [], "requires_clarification": false}`
Coverage: `{"needs_llm": false, "reasons": [], "evidence": [], "signals": {"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}}`
Reported: COVERAGE_FALSE_NEGATIVE, AMBIGUITY_ERROR
Root cause: Gold demands hybrid/ambiguity semantics that the established contract does not require for this input.
Risk: none
Disposition: Correct gold in a later benchmark-only change.
