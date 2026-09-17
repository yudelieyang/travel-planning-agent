"""Validate the explicit offline snapshot configuration before a recruiter demo."""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.core.config import Settings  # noqa: E402
from app.tools.candidate_providers import (  # noqa: E402
    CandidateProviderError,
    MixedCandidateProvider,
    create_candidate_provider,
)


def main() -> int:
    try:
        settings = Settings()
        if settings.candidate_data_mode != "snapshot":
            raise ValueError("CANDIDATE_DATA_MODE must be snapshot")
        if settings.candidate_snapshot_path is None:
            raise ValueError("CANDIDATE_SNAPSHOT_PATH is required")
        if settings.agent_planner != "deterministic":
            raise ValueError("AGENT_PLANNER must be deterministic")
        if settings.semantic_augmentation_mode != "deterministic":
            raise ValueError("SEMANTIC_AUGMENTATION_MODE must be deterministic")
        provider = create_candidate_provider("snapshot", settings.candidate_snapshot_path)
        if not isinstance(provider, MixedCandidateProvider):
            raise ValueError("Recruiter demo requires the migration manifest")
    except (CandidateProviderError, OSError, ValidationError, ValueError) as exc:
        print(f"Recruiter demo preflight failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Recruiter demo preflight passed: "
        f"{len(provider.routes)} snapshot routes; deterministic planner; offline candidate retrieval."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
