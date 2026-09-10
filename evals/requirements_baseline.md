# Requirements extraction baseline — Phase 5B

Phase 5A Git baseline: `c1eea83d2547a2d54e313f6e565950c64e2ce927`.

Dataset: `requirements_eval_v1` — 44 cases, 28 core and 16 robustness.
Languages: 41 English, 3 Chinese (capability probes, not supported input).
SHA-256: `0b5d9c29f2a9aabe2b8cbf96cd08d87310bab81855809a71afd2a74543517739`.
The dataset bytes and expectations were identical before and after parser changes.
The robustness split was fixed beforehand; this is not an independent blind benchmark.

## Before and after

| Metric | Before | After |
|---|---:|---:|
| Full-case exact match | 9/44 (20.5%) | 33/44 (75.0%) |
| Core exact match | 7/28 (25.0%) | 27/28 (96.4%) |
| Robustness exact match | 2/16 (12.5%) | 6/16 (37.5%) |
| Field-level accuracy | 466/528 (88.3%) | 506/528 (95.8%) |
| Preflight status | 30/44 (68.2%) | 40/44 (90.9%) |

## Field groups after changes

Group accuracy requires every expected field in that group to match. Lists compare as sets.
All-case accuracy includes correctly absent values. Nonempty targets exclude cases whose
expected group contains only null, empty lists, or UNKNOWN. Denominators are therefore explicit.

| Group | All cases | Nonempty targets |
|---|---:|---:|
| Destination | 40/44 | 32/36 |
| Duration | 42/44 | 33/35 |
| Dates (both endpoints) | 42/44 | 1/3 |
| Travelers | 43/44 | 6/7 |
| Budget amount | 43/44 | 6/7 |
| Budget scope | 44/44 | 4/4 |
| Preferences (all four lists) | 41/44 | 4/6 |
| Negation / constraints | 37/44 | 10/16 |

## Unresolved failures

| Case | Gap |
|---|---|
| REQ-005 | Long weekend has no exact duration; nested `to spend ... in Boston` is misread as a destination. No ambiguity marker is produced. |
| REQ-031 | Month-name date range is not extracted. |
| REQ-032 | Abbreviated month range without year: destination and missing-year constraint are not extracted. No year is guessed. |
| REQ-033 | Slash-date range is not extracted. |
| REQ-036 | `skip museums` is incorrectly retained as a positive interest. |
| REQ-037 | Postposed `museums are not my thing` is incorrectly positive. |
| REQ-038 | `not only museums` is incorrectly treated as negative. |
| REQ-039 | `dislike loud hotels` constraint is missed. |
| REQ-042 | Chinese destination, duration and amount are missed. |
| REQ-043 | Chinese negative preference is missed. |
| REQ-044 | Chinese destination, duration and travelers are missed. |

11 cases fail. Strict evaluation returns 1. These failures are not pytest skips/xfails.

Failure taxonomy counts **field/status mismatches**, not cases. Priority is negation,
ambiguity, normalization, missing/false-positive, then wrong value. Thus a false positive
on a negation-tagged preference is counted as NEGATION_ERROR rather than FALSE_POSITIVE.

| Category | Count |
|---|---:|
| MISSING_EXTRACTION | 12 |
| FALSE_POSITIVE | 0 |
| WRONG_VALUE | 4 |
| NEGATION_ERROR | 8 |
| AMBIGUITY_ERROR | 2 |
| NORMALIZATION_ERROR | 0 |

No LLM, travel tools, external APIs, or CoT are used in extraction evaluation.
Negative constraints are extracted, not enforced by the mock travel tools.
The only old travel smoke expectation corrected was TRAVEL-015: `no walking` no longer
means a positive walking preference. Requirements evaluation expectations were not edited.

## Reproduce

```powershell
python evals/evaluate_requirements.py
python evals/evaluate_requirements.py --strict
python evals/evaluate_travel.py
pytest
ruff check .
```

Runtime JSON reports are ignored under `evals/results/`; this small baseline document is
reviewable source documentation, not an automatically committed runtime log.
