# SEM200 Failure Clusters

## EVALUATOR_BUG

Cases: SEM200-116, SEM200-117, SEM200-118, SEM200-119, SEM200-121, SEM200-123, SEM200-124, SEM200-125, SEM200-126, SEM200-127, SEM200-128, SEM200-129, SEM200-130
Count: 13
Recommended treatment: Evaluation-only: model retained ambiguity details before comparing semantic views.

## GOLD_LABEL_ERROR

Cases: SEM200-193, SEM200-197, SEM200-198, SEM200-200
Count: 4
Recommended treatment: Benchmark-only: align gold with the Phase-J executable/ambiguity contract.

## INTENTIONAL_HYBRID_BOUNDARY

Cases: SEM200-166, SEM200-167, SEM200-168, SEM200-169, SEM200-170, SEM200-171, SEM200-172, SEM200-173, SEM200-174, SEM200-175
Count: 10
Recommended treatment: Keep hybrid; add coverage only where semantic augmentation is warranted.

## REAL_AMBIGUITY_BUG

Cases: SEM200-042, SEM200-045, SEM200-046, SEM200-047, SEM200-051, SEM200-054, SEM200-059, SEM200-062, SEM200-070, SEM200-071
Count: 10
Recommended treatment: Phase M P2: review explicit scope-anchor recognition.

## REAL_AMOUNT_BUG

Cases: SEM200-024, SEM200-026, SEM200-027, SEM200-028, SEM200-030, SEM200-032, SEM200-061, SEM200-064, SEM200-066, SEM200-068, SEM200-075, SEM200-080, SEM200-082, SEM200-085, SEM200-091, SEM200-097, SEM200-099, SEM200-115, SEM200-134, SEM200-135, SEM200-136, SEM200-138, SEM200-141, SEM200-142
Count: 24
Recommended treatment: Phase M: triage P0 hard drops/corrections before broad parser work.

## REAL_CORRECTION_BUG

Cases: SEM200-081, SEM200-086, SEM200-089, SEM200-090, SEM200-092, SEM200-093, SEM200-095, SEM200-096, SEM200-098, SEM200-100
Count: 10
Recommended treatment: Phase M P2: investigate bounded correction bridges as one family.

## REAL_COVERAGE_FALSE_NEGATIVE

Cases: SEM200-132, SEM200-137, SEM200-186, SEM200-187, SEM200-188, SEM200-189, SEM200-191, SEM200-192, SEM200-194, SEM200-195, SEM200-196
Count: 11
Recommended treatment: Phase M P1: coverage must request augmentation when deterministic semantics are incomplete.

## REAL_PARSER_BUG

Cases: SEM200-001, SEM200-006, SEM200-012, SEM200-021, SEM200-022, SEM200-023, SEM200-029, SEM200-031, SEM200-034, SEM200-035, SEM200-036, SEM200-038, SEM200-040, SEM200-048, SEM200-050, SEM200-053, SEM200-067, SEM200-122, SEM200-199
Count: 19
Recommended treatment: Phase M P2: group by destination and hard-ceiling phrase family.

## REAL_PREFERENCE_BUG

Cases: SEM200-008, SEM200-009, SEM200-013, SEM200-014, SEM200-016, SEM200-018, SEM200-058, SEM200-065, SEM200-069, SEM200-072, SEM200-074, SEM200-104, SEM200-107, SEM200-108, SEM200-114, SEM200-146, SEM200-147, SEM200-148, SEM200-149, SEM200-150, SEM200-151, SEM200-152, SEM200-153, SEM200-154, SEM200-155, SEM200-190
Count: 26
Recommended treatment: Defer as P3 until hard safety and coverage are stable.

## REAL_SCOPE_BUG

Cases: SEM200-057, SEM200-120
Count: 2
Recommended treatment: Phase M P0: prevent executable scope corruption.

## UNSUPPORTED_BY_DESIGN

Cases: SEM200-156, SEM200-157, SEM200-158, SEM200-159, SEM200-160, SEM200-161, SEM200-162, SEM200-163, SEM200-164, SEM200-165
Count: 10
Recommended treatment: Keep non-executable; decide later whether explicit exclusion representation is in scope.
