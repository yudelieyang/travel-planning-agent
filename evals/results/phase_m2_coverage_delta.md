# Phase M2 — Functional Coverage Delta

LLM needed iff deterministic semantics are incomplete or carry an unresolved supported ambiguity; retained unsupported hard scopes are complete.

## Coverage metrics

| View | TP | TN | FP | FN | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Audited M1 | 20 | 105 | 16 | 59 | 55.6% | 25.3% | 34.8% |
| Audited M2 | 75 | 121 | 0 | 4 | 100.0% | 94.9% | 97.4% |
| Raw M1 | 31 | 130 | 5 | 34 | 86.1% | 47.7% | 61.4% |
| Raw M2 | 44 | 104 | 31 | 21 | 58.7% | 67.7% | 62.9% |

Functional FN reduction: 59 → 4
Functional FP reduction: 16 → 0
Raw overall pass: 45.5% → 38.0%

Raw metrics retain historical runtime labels. In particular, they count already-retained unsupported hard scopes as model-call positives; the audited view measures semantic sufficiency.

## FN clusters

| Cluster | Starting cases | Fixed | Remaining | Final FP introduced |
| --- | ---: | ---: | ---: | ---: |
| P1 hard-money gap | 10 | 10 | 0 | 0 |
| P1 exclusion gap | 10 | 10 | 0 | 0 |
| P2 correction or ambiguity gap | 4 | 4 | 0 | 0 |
| P3 tradeoff gap | 9 | 9 | 0 | 0 |
| P3 preference gap | 25 | 22 | 3 | 0 |
| P3 rating enrichment | 1 | 0 | 1 | 0 |

## Remaining functional FNs

SEM200-151, SEM200-153, SEM200-190, SEM200-196

These are low-risk partial/list preference enrichment (`151`, `153`), typo preference normalization (`190`), and hotel-rating enrichment (`196`).

## M1 hard-safety oracle

- silent hard constraint corruption: 0
- wrong hard scope: 0
- wrong hard amount: 0
- soft to hard unsafe promotion: 0
- hard to soft unsafe downgrade: 0
- unsupported hard constraints silently dropped: 0

## Starting true-FN delta

| Case | Missing semantic | Old decision | New decision | New reason | Hard safety changed |
| --- | --- | --- | --- | --- | --- |
| SEM200-008 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-009 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-013 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-014 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-016 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-018 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-058 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-059 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-065 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-069 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-072 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-074 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-081 | hard constraint amount/scope | false | true | CORRECTION_TARGET_UNRESOLVED | no |
| SEM200-086 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-089 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-090 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-093 | hard constraint amount/scope | false | true | CORRECTION_TARGET_UNRESOLVED | no |
| SEM200-095 | hard constraint amount/scope | false | true | CORRECTION_TARGET_UNRESOLVED | no |
| SEM200-105 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-122 | unsupported ambiguous_monetary_scope, blocking ambiguity | false | true | AMBIGUOUS_SCOPE | no |
| SEM200-146 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-147 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-148 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-149 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-150 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-151 | preference | false | false | none | no |
| SEM200-152 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-153 | preference | false | false | none | no |
| SEM200-154 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-155 | preference | false | true | UNRESOLVED_REQUIREMENT_CLAUSE | no |
| SEM200-156 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-157 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-158 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-159 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-160 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-161 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-162 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-163 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-164 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-165 | unsupported exclusion, blocking ambiguity | false | true | UNREPRESENTED_NEGATION | no |
| SEM200-167 | unsupported tradeoff, blocking ambiguity | false | true | TRADEOFF_LANGUAGE | no |
| SEM200-168 | unsupported tradeoff, blocking ambiguity | false | true | TRADEOFF_LANGUAGE | no |
| SEM200-169 | unsupported tradeoff, blocking ambiguity | false | true | TRADEOFF_LANGUAGE | no |
| SEM200-170 | unsupported tradeoff, blocking ambiguity | false | true | TRADEOFF_LANGUAGE | no |
| SEM200-171 | unsupported tradeoff, blocking ambiguity | false | true | TRADEOFF_LANGUAGE | no |
| SEM200-172 | unsupported tradeoff, blocking ambiguity | false | true | TRADEOFF_LANGUAGE | no |
| SEM200-173 | unsupported tradeoff, blocking ambiguity | false | true | TRADEOFF_LANGUAGE | no |
| SEM200-174 | unsupported tradeoff, blocking ambiguity | false | true | TRADEOFF_LANGUAGE | no |
| SEM200-175 | unsupported tradeoff, blocking ambiguity | false | true | TRADEOFF_LANGUAGE | no |
| SEM200-186 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-187 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-188 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-189 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-190 | preference | false | false | none | no |
| SEM200-191 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-192 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-194 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-195 | hard constraint amount/scope | false | true | MONETARY_SEMANTIC_GAP | no |
| SEM200-196 | unsupported hotel_rating, blocking ambiguity | false | false | none | no |

## Full starting FN inventory

### SEM200-008 — P3 preference gap

- Category: A_simple_deterministic
- Input: Find me zoos in Columbus.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-009 — P3 preference gap

- Category: A_simple_deterministic
- Input: Three days in San Francisco; I enjoy seafood.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-013 — P3 preference gap

- Category: A_simple_deterministic
- Input: I like fried chicken in Chicago.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken in chicago"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-014 — P3 preference gap

- Category: A_simple_deterministic
- Input: Boston for 3 days. I enjoy walking.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "TRANSPORT", "value": "walking"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-016 — P3 preference gap

- Category: A_simple_deterministic
- Input: I want coffee shops in Seattle.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "coffee shops"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-018 — P3 preference gap

- Category: A_simple_deterministic
- Input: Denver for one day; public transit is preferred.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "TRANSPORT", "value": "public transit"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-058 — P3 preference gap

- Category: D_multi_scope
- Input: Miami, 3 days: total max $1,120. I like parks. Lodging total max $430.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1120.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "parks"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1120.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-059 — P1 hard-money gap

- Category: D_multi_scope
- Input: Keep the entire Seattle trip within $1,700, and keep accommodation within $760 total.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1700.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 760.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "HOTEL_TOTAL", "value": 760.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-065 — P3 preference gap

- Category: D_multi_scope
- Input: I enjoy seafood. San Francisco trip maximum is $2,200; accommodation maximum is $1,020 total.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 2200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 1020.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 2200.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 1020.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-069 — P3 preference gap

- Category: D_multi_scope
- Input: Seattle: hotel under $725 total; total trip under $1,880. Museums please.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1880.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 725.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "HOTEL_TOTAL", "value": 725.0, "strength": "HARD"}, {"scope": "TOTAL_TRIP", "value": 1880.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-072 — P3 preference gap

- Category: D_multi_scope
- Input: New York City: whole trip under $2,350. Quiet hotel, under $990 total.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 2350.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 990.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "HOTEL", "value": "quiet hotel"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 2350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 990.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-074 — P3 preference gap

- Category: D_multi_scope
- Input: Washington DC trip must stay under $1,360, hotel total must stay under $540, and I like parks.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1360.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 540.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "parks"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1360.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 540.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 2, "resolved_constraints": 2, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-081 — P2 correction or ambiguity gap

- Category: E_same_scope_correction
- Input: Hotel spending cannot exceed $580 total. Actually, $530.
- Expected semantic information: `{"constraints": [{"scope": "HOTEL_TOTAL", "value": 530.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "HOTEL_TOTAL", "value": 580.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 2, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not inspect unresolved correction targets or unrepresented hotel money.
- Risk without augmentation: A superseded or ambiguous amount can be treated as final.

### SEM200-086 — P3 preference gap

- Category: E_same_scope_correction
- Input: The full trip must stay below $1,090. Actually, I prefer museums.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1090.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1090.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-089 — P3 preference gap

- Category: E_same_scope_correction
- Input: Lodging must stay below $450 total. I'd rather stay downtown.
- Expected semantic information: `{"constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "HOTEL", "value": "downtown"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "HOTEL_TOTAL", "value": 450.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-090 — P3 preference gap

- Category: E_same_scope_correction
- Input: The trip maximum is $1,300. Actually, I want seafood.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [{"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1300.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-093 — P2 correction or ambiguity gap

- Category: F_mixed_scope_correction
- Input: Trip ceiling $1,800 and lodging ceiling $750 total; sorry, make the trip $1,600.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 750.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "HOTEL_TOTAL", "value": 1600.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 3, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not inspect unresolved correction targets or unrepresented hotel money.
- Risk without augmentation: A superseded or ambiguous amount can be treated as final.

### SEM200-095 — P2 correction or ambiguity gap

- Category: F_mixed_scope_correction
- Input: The total is capped at $1,350. Hotel total is capped at $500. Change total to $1,200 only.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}, {"scope": "HOTEL_TOTAL", "value": 500.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 3, "resolved_constraints": 2, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not inspect unresolved correction targets or unrepresented hotel money.
- Risk without augmentation: A superseded or ambiguous amount can be treated as final.

### SEM200-105 — P1 hard-money gap

- Category: G_soft_approximate
- Input: About $1,100 total is my target for Denver, not a strict cap.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-122 — P2 correction or ambiguity gap

- Category: H_ambiguous_scope
- Input: A $700 place to stay in New York City is okay.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["AMBIGUOUS_MONETARY_SCOPE"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported ambiguous_monetary_scope, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 1, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not inspect unresolved correction targets or unrepresented hotel money.
- Risk without augmentation: A superseded or ambiguous amount can be treated as final.

### SEM200-146 — P3 preference gap

- Category: J_preferences
- Input: Boston: zoos, parks, and seafood please.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "ACTIVITY", "value": "parks"}, {"category": "FOOD", "value": "seafood"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-147 — P3 preference gap

- Category: J_preferences
- Input: I like fried chicken, art museums, and coffee shops in Chicago.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}, {"category": "ACTIVITY", "value": "art museums"}, {"category": "FOOD", "value": "coffee shops"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}, {"category": "ACTIVITY", "value": "art museums"}, {"category": "FOOD", "value": "coffee shops in chicago"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-148 — P3 preference gap

- Category: J_preferences
- Input: Miami should have a quiet hotel and nearby parks.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "HOTEL", "value": "quiet hotel"}, {"category": "ACTIVITY", "value": "parks"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-149 — P3 preference gap

- Category: J_preferences
- Input: In Seattle I want seafood, coffee shops, and art museums.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "seafood"}, {"category": "FOOD", "value": "coffee shops"}, {"category": "ACTIVITY", "value": "art museums"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-150 — P3 preference gap

- Category: J_preferences
- Input: Denver: downtown hotel, public transit, and museums.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "HOTEL", "value": "downtown hotel"}, {"category": "TRANSPORT", "value": "public transit"}, {"category": "ACTIVITY", "value": "museums"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-151 — P3 preference gap

- Category: J_preferences
- Input: For Austin, I enjoy parks, fried chicken, and walking.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "parks"}, {"category": "FOOD", "value": "fried chicken"}, {"category": "TRANSPORT", "value": "walking"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [{"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-152 — P3 preference gap

- Category: J_preferences
- Input: New York City needs a quiet hotel, seafood, and zoos.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "HOTEL", "value": "quiet hotel"}, {"category": "FOOD", "value": "seafood"}, {"category": "ACTIVITY", "value": "zoo"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-153 — P3 preference gap

- Category: J_preferences
- Input: Las Vegas: parks, coffee shops, and public transit are important.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "parks"}, {"category": "FOOD", "value": "coffee shops"}, {"category": "TRANSPORT", "value": "public transit"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-154 — P3 preference gap

- Category: J_preferences
- Input: Washington DC, please include museums, seafood, and a downtown hotel.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "museums"}, {"category": "FOOD", "value": "seafood"}, {"category": "HOTEL", "value": "downtown hotel"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-155 — P3 preference gap

- Category: J_preferences
- Input: San Francisco with zoos, fried chicken, and a quiet hotel.
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chicken"}, {"category": "HOTEL", "value": "quiet hotel"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-156 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: Boston is fine, but do not include zoos.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-157 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: I do not care about nightlife in Chicago.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-158 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: No luxury hotels in Miami.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-159 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: Avoid expensive restaurants in Seattle.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-160 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: I don't need museums in Denver.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-161 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: Please exclude parks from the Austin plan.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-162 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: No seafood for New York City.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-163 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: Don't schedule a casino in Las Vegas.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-164 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: Washington DC, no crowded hotel areas.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-165 — P1 exclusion gap

- Category: K_negation_exclusion
- Input: San Francisco without tourist-trap restaurants.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["EXCLUSION"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported exclusion, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Negative travel requirements had no coverage signal.
- Risk without augmentation: An excluded item can be silently included.

### SEM200-167 — P3 tradeoff gap

- Category: L_tradeoff_objective
- Input: Save on food in Chicago so we can spend more on activities.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["TRADEOFF"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported tradeoff, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Tradeoff detection required narrow wording and usually a monetary symbol.
- Risk without augmentation: The plan can ignore the requested allocation tradeoff.

### SEM200-168 — P3 tradeoff gap

- Category: L_tradeoff_objective
- Input: Prioritize hotel quality over restaurants for Miami.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["TRADEOFF"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported tradeoff, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Tradeoff detection required narrow wording and usually a monetary symbol.
- Risk without augmentation: The plan can ignore the requested allocation tradeoff.

### SEM200-169 — P3 tradeoff gap

- Category: L_tradeoff_objective
- Input: I would pay more for a better Seattle location, while keeping total trip under $1,800.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["TRADEOFF"]}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1800.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported tradeoff, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: Tradeoff detection required narrow wording and usually a monetary symbol.
- Risk without augmentation: The plan can ignore the requested allocation tradeoff.

### SEM200-170 — P3 tradeoff gap

- Category: L_tradeoff_objective
- Input: For Denver, choose a cheaper hotel only if museums remain easy to reach.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["TRADEOFF"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported tradeoff, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Tradeoff detection required narrow wording and usually a monetary symbol.
- Risk without augmentation: The plan can ignore the requested allocation tradeoff.

### SEM200-171 — P3 tradeoff gap

- Category: L_tradeoff_objective
- Input: Austin food can be simpler if the hotel is closer to downtown.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["TRADEOFF"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported tradeoff, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Tradeoff detection required narrow wording and usually a monetary symbol.
- Risk without augmentation: The plan can ignore the requested allocation tradeoff.

### SEM200-172 — P3 tradeoff gap

- Category: L_tradeoff_objective
- Input: I value location over room size in New York City, up to a total of $2,100.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["TRADEOFF"]}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 2100.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported tradeoff, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: Tradeoff detection required narrow wording and usually a monetary symbol.
- Risk without augmentation: The plan can ignore the requested allocation tradeoff.

### SEM200-173 — P3 tradeoff gap

- Category: L_tradeoff_objective
- Input: Spend less on shows in Las Vegas so the hotel can be nicer.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["TRADEOFF"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported tradeoff, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Tradeoff detection required narrow wording and usually a monetary symbol.
- Risk without augmentation: The plan can ignore the requested allocation tradeoff.

### SEM200-174 — P3 tradeoff gap

- Category: L_tradeoff_objective
- Input: Pay extra for a quiet Washington DC hotel if it cuts commute time.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["TRADEOFF"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported tradeoff, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Tradeoff detection required narrow wording and usually a monetary symbol.
- Risk without augmentation: The plan can ignore the requested allocation tradeoff.

### SEM200-175 — P3 tradeoff gap

- Category: L_tradeoff_objective
- Input: For San Francisco, prioritize seafood over attractions if choices conflict.
- Expected semantic information: `{"constraints": [], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["TRADEOFF"]}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported tradeoff, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: Tradeoff detection required narrow wording and usually a monetary symbol.
- Risk without augmentation: The plan can ignore the requested allocation tradeoff.

### SEM200-186 — P1 hard-money gap

- Category: N_noisy_english
- Input: hotel money should not more then 470 total in Boston
- Expected semantic information: `{"constraints": [{"scope": "HOTEL_TOTAL", "value": 470.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-187 — P1 hard-money gap

- Category: N_noisy_english
- Input: whole Chicago trip cost less 1180 pls
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1180.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-188 — P1 hard-money gap

- Category: N_noisy_english
- Input: miami hotel 390 not 490 make it max total
- Expected semantic information: `{"constraints": [{"scope": "HOTEL_TOTAL", "value": 390.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-189 — P1 hard-money gap

- Category: N_noisy_english
- Input: seattle trip budgt under 1500 and hotel 600 total
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1500.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 600.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-190 — P3 preference gap

- Category: N_noisy_english
- Input: denver 3 days i like zoo and fried chiken
- Expected semantic information: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chicken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [{"category": "ACTIVITY", "value": "zoo"}, {"category": "FOOD", "value": "fried chiken"}], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: preference
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: The gate did not detect explicit preference clauses left without a canonical preference.
- Risk without augmentation: The plan can omit a requested experience or accommodation preference.

### SEM200-191 — P1 hard-money gap

- Category: N_noisy_english
- Input: austin all trip no more 1100; lodge total no more 430
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1100.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 430.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-192 — P1 hard-money gap

- Category: N_noisy_english
- Input: nyc hotel money cant above 780 total and trip 1900 max
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1900.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 780.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-194 — P1 hard-money gap

- Category: N_noisy_english
- Input: wash dc accomodation total under 620, all trip under 1350
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 620.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1350.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-195 — P1 hard-money gap

- Category: N_noisy_english
- Input: san fran hotel shud be 800 total max; trip 2050 max
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 2050.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}, {"scope": "HOTEL_TOTAL", "value": 800.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Deterministic output: `{"constraints": [], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: hard constraint amount/scope
- Current M1 coverage signals: `{"monetary_expressions": 0, "resolved_constraints": 0, "blocking_ambiguities": 0}`
- Why the gate failed: No represented-vs-source hard-money sufficiency check.
- Risk without augmentation: A hard cap can disappear or retain the wrong amount/scope.

### SEM200-196 — P3 rating enrichment

- Category: O_adversarial_boundary
- Input: Boston trip max $1,200. Hotel rating at least 4 stars.
- Expected semantic information: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD", "operator": "LTE", "supported_for_execution": true}], "preferences": [], "ambiguity_levels": ["BLOCKING"], "unsupported_scopes": [], "unsupported_semantics": ["HOTEL_RATING"]}`
- Deterministic output: `{"constraints": [{"scope": "TOTAL_TRIP", "value": 1200.0, "strength": "HARD"}], "preferences": [], "ambiguity_levels": [], "unsupported_scopes": [], "unsupported_semantics": []}`
- Missing semantic information: unsupported hotel_rating, blocking ambiguity
- Current M1 coverage signals: `{"monetary_expressions": 1, "resolved_constraints": 1, "blocking_ambiguities": 0}`
- Why the gate failed: Hotel-rating requirements are outside the bounded M2 signals.
- Risk without augmentation: The hotel star-rating request can be omitted.
