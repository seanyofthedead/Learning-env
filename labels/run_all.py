"""Phase 2B orchestrator.

Loads the Phase 2A ``normalized.parquet``, builds canonical entities,
computes the binary recurrence label, and writes:

- ``data/processed/entities.parquet``
- ``data/processed/reports_with_labels.parquet``
- ``data/processed/labels_stats.md``

CLI::

    python -m labels.run_all                        # defaults: 365 days, family
    python -m labels.run_all --window-days 90 --match-level exact-code
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from labels.entities import build_entities
from labels.recurrence import compute_recurrence
from normalize._common import DATA_PROCESSED

LOG = logging.getLogger("grammar_of_failure.labels")

NORMALIZED_PATH = DATA_PROCESSED / "normalized.parquet"
ENTITIES_PATH = DATA_PROCESSED / "entities.parquet"
LABELS_PATH = DATA_PROCESSED / "reports_with_labels.parquet"
STATS_PATH = DATA_PROCESSED / "labels_stats.md"


def _setup_logging() -> None:
    handler = logging.StreamHandler(sys.stderr)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s", "%H:%M:%S")
    handler.setFormatter(fmt)
    LOG.addHandler(handler)
    LOG.setLevel(logging.INFO)
    LOG.propagate = False


def _render_stats(
    reports: pd.DataFrame,
    entities: pd.DataFrame,
    window_days: int,
    match_level: str,
) -> str:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    total = int(reports.shape[0])
    positive = int(reports["recurred_within"].sum())
    rate = positive / total if total else 0.0

    lines = [
        "# Phase 2B stats — entity linking + recurrence labels",
        "",
        f"_Generated at {ts}_",
        "",
        f"**Window:** {window_days} days  ",
        f"**Match level:** {match_level}  ",
        f"**Total reports:** {total:,}  ",
        f"**Positive recurrence labels:** {positive:,} ({rate:.1%})  ",
        f"**Unique entities:** {int(entities.shape[0]):,}",
        "",
        "## Per-source breakdown",
        "",
        "| Source | Reports | Entities | Reports/entity | Positive rate |",
        "|---|---:|---:|---:|---:|",
    ]
    src_report = reports.groupby("source").agg(
        reports=("report_id", "count"),
        positives=("recurred_within", "sum"),
    )
    src_entities = entities.groupby("source").agg(entities=("entity_id", "count"))
    src = src_report.join(src_entities, how="left").fillna(0)
    src["reports_per_entity"] = src["reports"] / src["entities"].where(src["entities"] > 0, 1)
    src["positive_rate"] = src["positives"] / src["reports"].where(src["reports"] > 0, 1)
    for source, row in src.iterrows():
        lines.append(
            f"| {source} | {int(row['reports']):,} | {int(row['entities']):,} | "
            f"{row['reports_per_entity']:.2f} | {row['positive_rate']:.1%} |"
        )

    lines += ["", "## Event-family distribution (top 20)", ""]
    fam = reports.groupby(["source", "event_family"]).size().reset_index(name="n")
    fam = fam.sort_values("n", ascending=False).head(20)
    lines.append("| Source | Family | Count |")
    lines.append("|---|---|---:|")
    for _, row in fam.iterrows():
        lines.append(f"| {row['source']} | {row['event_family']} | {int(row['n']):,} |")

    lines += ["", "## Entities with most reports (top 10)", ""]
    top = entities.sort_values("report_count", ascending=False).head(10)
    lines.append("| Source | Canonical name | Reports | First seen | Last seen |")
    lines.append("|---|---|---:|---|---|")
    for _, row in top.iterrows():
        name = row.get("canonical_name") or "—"
        first = str(row["first_seen"].date()) if pd.notna(row["first_seen"]) else "—"
        last = str(row["last_seen"].date()) if pd.notna(row["last_seen"]) else "—"
        lines.append(
            f"| {row['source']} | {str(name)[:60]} | {int(row['report_count']):,} | "
            f"{first} | {last} |"
        )
    return "\n".join(lines) + "\n"


def main(window_days: int, match_level: str) -> int:
    _setup_logging()
    if not NORMALIZED_PATH.exists():
        LOG.error("labels: missing %s — run `python -m normalize.run_all` first", NORMALIZED_PATH)
        return 1

    LOG.info("labels: loading %s", NORMALIZED_PATH)
    df = pd.read_parquet(NORMALIZED_PATH)
    LOG.info("labels: loaded %d reports", len(df))

    LOG.info("labels: building canonical entities")
    df_with_ids, entities = build_entities(df)
    LOG.info("labels: %d unique entities", entities.shape[0])

    LOG.info(
        "labels: computing recurrence (window=%dd, match=%s)",
        window_days,
        match_level,
    )
    labeled = compute_recurrence(
        df_with_ids,
        window_days=window_days,
        match_level=match_level,
    )
    positive = int(labeled["recurred_within"].sum())
    LOG.info(
        "labels: %d/%d positive labels (%.2f%%)",
        positive,
        len(labeled),
        100 * positive / len(labeled) if len(labeled) else 0,
    )

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    LOG.info("labels: writing entities")
    entities.to_parquet(ENTITIES_PATH, index=False)
    LOG.info("labels: writing labeled reports")
    labeled.to_parquet(LABELS_PATH, index=False)

    STATS_PATH.write_text(_render_stats(labeled, entities, window_days, match_level))
    LOG.info("labels: wrote stats to %s", STATS_PATH)
    return 0


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Phase 2B: entity linking + recurrence labels")
    ap.add_argument("--window-days", type=int, default=365, help="Recurrence window in days")
    ap.add_argument(
        "--match-level",
        choices=["family", "exact-code"],
        default="family",
        help="How to decide two events are the 'same kind'",
    )
    return ap.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    raise SystemExit(main(window_days=args.window_days, match_level=args.match_level))
