"""Run every mapper and write the unified ``data/processed/normalized.parquet``.

CLI::

    python -m normalize.run_all
    python -m normalize.run_all --source osha_sir
"""

from __future__ import annotations

import argparse
import importlib
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import pandas as pd

from normalize._common import DATA_PROCESSED
from normalize.schema import NORMALIZED_COLUMNS, SOURCE_NAMES

LOG = logging.getLogger("grammar_of_failure.normalize")

MAPPERS: list[tuple[str, str]] = [
    ("osha_sir", "normalize.map_osha_sir"),
    ("osha_ita", "normalize.map_osha_ita"),
    ("msha", "normalize.map_msha"),
    ("nrc", "normalize.map_nrc"),
    ("ntsb", "normalize.map_ntsb"),
    ("asrs", "normalize.map_asrs"),
]

OUTPUT_PATH = DATA_PROCESSED / "normalized.parquet"
STATS_PATH = DATA_PROCESSED / "normalized_stats.md"


def _serialize_meta_vectorized(meta_series: pd.Series) -> pd.Series:
    """Convert a list-of-dicts series to JSON strings without per-row apply.

    Uses ``json.dumps`` in a generator expression which is O(n) but
    avoids the pandas apply overhead. For dicts that are already plain
    Python (no NaN contamination), ``str()`` would be faster but not
    JSON-valid.
    """
    import json

    def _one(d):
        if d is None:
            return "{}"
        if isinstance(d, dict):
            clean = {
                k: (None if (isinstance(v, float) and pd.isna(v)) else v)
                for k, v in d.items()
            }
            try:
                return json.dumps(clean, default=str)
            except TypeError:
                return json.dumps({k: str(v) for k, v in clean.items()})
        return json.dumps({"_raw": str(d)})

    return pd.Series([_one(d) for d in meta_series], index=meta_series.index, dtype="object")


def _setup_logging() -> None:
    handler = logging.StreamHandler(sys.stderr)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s", "%H:%M:%S")
    handler.setFormatter(fmt)
    LOG.addHandler(handler)
    LOG.setLevel(logging.INFO)
    LOG.propagate = False


def _load_mapper(module_path: str) -> Callable[[], pd.DataFrame]:
    mod = importlib.import_module(module_path)
    return getattr(mod, "run")


def _per_source_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"row_count": 0, "date_range": None, "narrative_wc": {}}
    dates = pd.to_datetime(df["event_date"], errors="coerce").dropna()
    wc = df["narrative"].fillna("").str.split().str.len()
    wc_stats = {
        "n": int(len(wc)),
        "mean": float(wc.mean()) if not wc.empty else 0.0,
        "median": float(wc.median()) if not wc.empty else 0.0,
        "p25": float(wc.quantile(0.25)) if not wc.empty else 0.0,
        "p75": float(wc.quantile(0.75)) if not wc.empty else 0.0,
        "min": int(wc.min()) if not wc.empty else 0,
        "max": int(wc.max()) if not wc.empty else 0,
    }
    return {
        "row_count": int(df.shape[0]),
        "date_range": (
            (str(dates.min().date()), str(dates.max().date())) if not dates.empty else None
        ),
        "narrative_wc": wc_stats,
        "null_rates": {
            col: float(df[col].isna().mean())
            for col in NORMALIZED_COLUMNS
            if col not in {"source", "meta"}
        },
    }


def _render_stats(per_source: dict[str, dict], total_rows: int) -> str:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# Normalized corpus statistics",
        "",
        f"_Generated at {ts}_",
        "",
        f"**Total normalized rows:** {total_rows:,}",
        f"**Output:** `data/processed/normalized.parquet`",
        "",
        "## Per-source breakdown",
        "",
        "| Source | Rows | Date range | Narrative (mean/median words) |",
        "|---|---:|---|---|",
    ]
    for src, stats in per_source.items():
        row_count = stats.get("row_count", 0)
        dr = stats.get("date_range")
        dr_str = f"{dr[0]} → {dr[1]}" if dr else "—"
        wc = stats.get("narrative_wc", {})
        wc_str = (
            f"{wc.get('mean', 0):.1f} / {wc.get('median', 0):.1f}"
            if wc.get("n", 0) > 0
            else "—"
        )
        lines.append(f"| {src} | {row_count:,} | {dr_str} | {wc_str} |")

    lines += ["", "## Null rates (per-column, excluding `source` and `meta`)", ""]
    for src, stats in per_source.items():
        lines.append(f"### {src}")
        lines.append("")
        lines.append("| Column | Null rate |")
        lines.append("|---|---:|")
        for col, rate in stats.get("null_rates", {}).items():
            lines.append(f"| {col} | {rate:.1%} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def main(sources: list[str] | None = None) -> int:
    _setup_logging()
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    frames: list[pd.DataFrame] = []
    per_source_stats: dict[str, dict] = {}

    for name, module_path in MAPPERS:
        if sources and name not in sources:
            continue
        LOG.info("normalize: running %s mapper", name)
        try:
            run_fn = _load_mapper(module_path)
        except ModuleNotFoundError as exc:
            LOG.warning("normalize: %s module missing: %s", name, exc)
            continue
        df = run_fn()
        LOG.info("normalize: %s -> %d normalized rows", name, df.shape[0])
        per_source_stats[name] = _per_source_stats(df)
        if not df.empty:
            frames.append(df)

    if not frames:
        LOG.warning("normalize: no source produced data, writing empty parquet")
        empty = pd.DataFrame(columns=NORMALIZED_COLUMNS)
        empty.to_parquet(OUTPUT_PATH, index=False)
        total_rows = 0
    else:
        combined = pd.concat(frames, ignore_index=True)
        # Parquet needs a consistent dtype for meta; serialize in one pass.
        LOG.info("normalize: serializing meta column to JSON strings")
        combined["meta"] = _serialize_meta_vectorized(combined["meta"])
        combined["event_date"] = pd.to_datetime(combined["event_date"])
        LOG.info("normalize: writing parquet")
        combined.to_parquet(OUTPUT_PATH, index=False)
        total_rows = int(combined.shape[0])
        LOG.info("normalize: wrote %d total rows to %s", total_rows, OUTPUT_PATH)

    STATS_PATH.write_text(_render_stats(per_source_stats, total_rows))
    LOG.info("normalize: wrote stats to %s", STATS_PATH)
    return 0


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Normalize all Phase 1 sources.")
    ap.add_argument(
        "--source",
        action="append",
        choices=sorted(SOURCE_NAMES),
        help="Restrict to one or more sources (repeatable).",
    )
    return ap.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    raise SystemExit(main(sources=args.source))
