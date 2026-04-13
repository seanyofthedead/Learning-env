"""Phase 2C orchestrator.

Loads ``reports_with_labels.parquet`` (Phase 2B output), builds both
the structured baseline feature table and the text-quality treatment
feature table, and writes:

- ``data/features/structured.parquet``
- ``data/features/text_quality.parquet``
- ``data/features/features_stats.md``

CLI::

    python -m features.run_all
    python -m features.run_all --sample 50000   # for fast iteration
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from features.structured import build_structured_features
from features.text_quality import build_text_features

LOG = logging.getLogger("grammar_of_failure.features")

REPO = Path(__file__).resolve().parent.parent
LABELS_PATH = REPO / "data" / "processed" / "reports_with_labels.parquet"
FEATURES_DIR = REPO / "data" / "features"
STRUCTURED_PATH = FEATURES_DIR / "structured.parquet"
TEXT_PATH = FEATURES_DIR / "text_quality.parquet"
STATS_PATH = FEATURES_DIR / "features_stats.md"


def _setup_logging() -> None:
    handler = logging.StreamHandler(sys.stderr)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s", "%H:%M:%S")
    handler.setFormatter(fmt)
    LOG.addHandler(handler)
    LOG.setLevel(logging.INFO)
    LOG.propagate = False


def _render_stats(
    structured: pd.DataFrame,
    text: pd.DataFrame,
) -> str:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# Phase 2C stats — structured + text features",
        "",
        f"_Generated at {ts}_",
        "",
        f"**Structured features:** {structured.shape[0]:,} rows × {structured.shape[1]} cols",
        f"**Text features:** {text.shape[0]:,} rows × {text.shape[1]} cols",
        "",
        "## Text-quality feature summary",
        "",
        "| Feature | Mean | Median | Min | Max | Null% |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for col in text.columns:
        if col == "report_id":
            continue
        s = text[col]
        try:
            lines.append(
                f"| {col} | {s.mean():.3f} | {s.median():.3f} | {s.min():.3f} | "
                f"{s.max():.3f} | {s.isna().mean():.1%} |"
            )
        except (TypeError, ValueError):
            lines.append(f"| {col} | — | — | — | — | {s.isna().mean():.1%} |")

    lines += ["", "## Structured feature columns", ""]
    for col in structured.columns:
        if col == "report_id":
            continue
        s = structured[col]
        try:
            lines.append(
                f"- `{col}` (mean={s.mean():.2f}, min={s.min()}, max={s.max()})"
            )
        except (TypeError, ValueError):
            lines.append(f"- `{col}`")
    return "\n".join(lines) + "\n"


def main(sample: int | None) -> int:
    _setup_logging()
    if not LABELS_PATH.exists():
        LOG.error("features: missing %s — run `python -m labels.run_all` first", LABELS_PATH)
        return 1

    LOG.info("features: loading labels")
    df = pd.read_parquet(LABELS_PATH)
    LOG.info("features: loaded %d reports", len(df))
    if sample and sample < len(df):
        LOG.info("features: sampling %d reports", sample)
        df = df.sample(n=sample, random_state=42).reset_index(drop=True)

    LOG.info("features: building structured features")
    structured = build_structured_features(df)
    LOG.info("features: structured shape %s", structured.shape)

    LOG.info("features: building text-quality features (textstat is slow on large input)")
    text = build_text_features(df)
    LOG.info("features: text shape %s", text.shape)

    FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    LOG.info("features: writing parquets")
    structured.to_parquet(STRUCTURED_PATH, index=False)
    text.to_parquet(TEXT_PATH, index=False)

    STATS_PATH.write_text(_render_stats(structured, text))
    LOG.info("features: wrote stats to %s", STATS_PATH)
    return 0


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Phase 2C: structured + text features")
    ap.add_argument(
        "--sample",
        type=int,
        default=None,
        help="If set, compute features on a random sample of N reports (for iteration speed).",
    )
    return ap.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    raise SystemExit(main(sample=args.sample))
