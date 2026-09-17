# Phase I failure clusters

## Baseline parser misses

| Cases | Cluster | Root cause | Resolution |
| --- | --- | --- | --- |
| HYBRID-001, 031, 034, 035 | Hard total ceilings | Scope was lost when a ceiling phrase carried the only trip signal. | Added bounded `below`, `go over`, `cap … at`, trailing-currency, and trip-plan scope handling. |
| HYBRID-006, 010 | Multi-scope clauses | A following hotel clause could affect the preceding total amount; introductory wording was excluded from scope resolution. | Kept introductory words in local scope evaluation and bounded `and the hotel` clauses. |
| HYBRID-009 | Same-scope correction | The correction omitted its repeated scope. | Inherit only the immediately prior supported scope after explicit correction language. |
| HYBRID-011, 022, 049 | `below` hard limits | `below` was not a hard-budget marker. | Classified `below` as a hard ceiling; hotel context takes precedence over a trailing `total`. |
| HYBRID-004 | Visit activity | `visit zoos in <city>` was treated as a destination phrase. | Resolve the city after `in` and recognize unquantified visit activities. |

## Result

Nine of the 14 original parser misses are resolved. HYBRID-001, 009, 031, 032, and 033 remain intentionally scope-free: promoting them to canonical total-trip constraints would break the established `UNKNOWN` legacy budget-scope contract. HYBRID-007 now parses deterministically but intentionally retains its original LLM-needed gold label, so it is the one reported coverage-label mismatch.

## Intentional hybrid boundaries

- Bare hotel budgets remain blocking ambiguous.
- Contradictions and tradeoffs remain eligible for semantic augmentation.
- Per-night hotel and non-hotel budget scopes remain non-executable.
- No fuzzy parsing or new execution support was added.
