import importlib.util
import json

from app.core.config import PROJECT_ROOT

SPEC = importlib.util.spec_from_file_location(
    "audit_hybrid_semantics_200", PROJECT_ROOT / "scripts/audit_hybrid_semantics_200.py"
)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def test_phase_l_audit_covers_every_raw_failure_and_reclassifies_safety_metrics():
    raw = json.loads(
        (PROJECT_ROOT / "evals/results/hybrid_semantics_200_v1_offline.json").read_text("utf-8")
    )
    audit = AUDIT.build_audit(raw)

    assert audit["failed_case_count"] == 139
    assert len(audit["records"]) == 139
    assert audit["summary"]["true_silent_hard_corruption"] == [
        "SEM200-057",
        "SEM200-080",
        "SEM200-085",
        "SEM200-091",
        "SEM200-097",
        "SEM200-099",
        "SEM200-115",
        "SEM200-120",
    ]
    assert audit["summary"]["true_unsupported_hard_drops"] == [
        "SEM200-134",
        "SEM200-135",
        "SEM200-136",
        "SEM200-138",
        "SEM200-141",
        "SEM200-142",
    ]
    assert audit["summary"]["functional_coverage"] == {
        "TP": 43,
        "TN": 68,
        "FP": 0,
        "FN": 89,
        "precision": 1.0,
        "recall": 43 / 132,
        "f1": 86 / 175,
    }
