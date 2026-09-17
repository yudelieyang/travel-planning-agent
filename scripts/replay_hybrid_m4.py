"""Replay the frozen M4 proposals through the M5 merge policy without API calls."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.replay_hybrid_m3 import render_markdown, replay_recorded  # noqa: E402

M4_PATH = PROJECT_ROOT / "evals/results/hybrid_semantics_200_live_m4.json"
OUTPUT_PATH = PROJECT_ROOT / "evals/results/hybrid_semantics_200_m4_replay_m5.json"
MARKDOWN_PATH = PROJECT_ROOT / "evals/results/hybrid_semantics_200_m4_replay_m5.md"


def replay() -> dict:
    return replay_recorded(M4_PATH, "hybrid_semantics_200_m4_replay_m5")


def main() -> int:
    report = replay()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    MARKDOWN_PATH.write_text(
        render_markdown(report, "Phase M5 — M4 Recorded-Proposal Replay"),
        encoding="utf-8",
    )
    print(json.dumps(report["replay_summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
