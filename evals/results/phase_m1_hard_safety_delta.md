# Phase M1 — Hard-Safety Delta

Scope: the 26 P0 cases manually audited in Phase L. This does not reinterpret unrelated SEM200 coverage or preference failures.

## Audited P0 result

P0 cases safe: 26/26
Remaining P0 hard-safety cases: none

| Metric | Phase L baseline | Phase M1 |
| --- | ---: | ---: |
| silent hard constraint corruption | 8 | 0 |
| wrong hard scope | 1 | 0 |
| wrong hard amount | 5 | 0 |
| soft to hard unsafe promotion | 1 | 0 |
| hard to soft unsafe downgrade | 0 | 0 |
| unsupported hard constraints silently dropped | 6 | 0 |

## Residual generic-evaluator observations

These are not retained P0 hard-safety defects:
- SEM200-024: PARSER_MISS
- SEM200-027: PARSER_MISS
- SEM200-028: PARSER_MISS
- SEM200-057: PARSER_MISS
- SEM200-061: PARSER_MISS
- SEM200-120: AMBIGUITY_ERROR

`PARSER_MISS` records above are unrelated destination parsing misses; `SEM200-120` is the Phase L evaluator-contract ambiguity observation. The P0 semantic oracle confirms their money safety state.
