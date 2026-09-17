# Phase J scope and correction policy

## Monetary scope resolution

The deterministic parser treats scope as independent from ceiling strength.
It creates executable constraints only for a supported scope with hard
modality. The policy is deliberately small:

| Evidence | Result |
| --- | --- |
| Explicit `hotel`, `lodging`, or `accommodation` total ceiling | `HOTEL_TOTAL` |
| Explicit `total`, `whole trip`, `trip budget`, or `trip` followed by a hard ceiling | `TOTAL_TRIP` |
| Immediate monetary correction of the preceding supported hard constraint | Inherit that constraint's scope |
| Unsupported explicit subject such as food, transport, or activities | Retain a non-executable ambiguity |
| Standalone or otherwise insufficient money context | Preserve legacy `UNKNOWN` scope; do not create a V2 hard constraint |

This means that `Plan a trip to Boston under $800`, `No more than $900`, and
`My budget is $900` remain intentionally unresolved. The parser does not
default them to total-trip ceilings.

## Bounded correction inheritance

Inheritance is allowed only when all of the following are true:

1. The current monetary amount has no explicit scope.
2. The immediately preceding monetary candidate produced a supported hard
   constraint.
3. The local prefix has an unambiguous correction cue: `actually`, `sorry`,
   `I meant`, `make that`, `make it`, `change that`, `change it`, or `instead`.

The inherited correction is made hard only because the predecessor is an
explicit hard ceiling. A soft amount is never upgraded. Explicit scopes always
win, so a subsequent hotel constraint cannot be mistaken for a correction of a
trip constraint.

## Evaluation interpretation

`needs_llm` records the historical semantic-difficulty label. The optional
`expected_runtime_llm_need` records whether the current deterministic boundary
would lose required semantics by skipping augmentation. This avoids treating a
fully deterministic case as a functional coverage failure merely because it
was originally a hybrid example.

`allow_hybrid_gap` marks an offline-only semantic field deliberately deferred
to the LLM and deterministic merge. It is only used when the coverage gate
does request augmentation; a missed gate still fails the evaluation.

## Phase J classifications

| Cases | Classification | Rationale |
| --- | --- | --- |
| HYBRID-001, -009, -031, -032, -033 | `TRUE_AMBIGUITY` / legacy `UNKNOWN` | The inputs lack a sufficiently explicit scope anchor. |
| HOLDOUT-007 | fixed deterministically | Explicit trip and hotel anchors plus hard ceilings support two independent constraints. |
| HOLDOUT-015 | fixed deterministically | `make it` is an immediate, scope-free correction of an explicit hotel ceiling. |
| HOLDOUT-016 | `INTENTIONAL_HYBRID` | The hotel-location tradeoff needs augmentation; offline evaluation defers the proposed final semantic field after the gate requests it. |
| HYBRID-007 | `EVALUATION_GOLD_STALE` | Its historical difficulty label remains true, but deterministic output is now complete, so runtime LLM need is false. |
