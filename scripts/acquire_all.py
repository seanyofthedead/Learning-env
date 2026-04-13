"""Orchestrator — runs every ``acquire_*`` module and writes ACQUISITION_LOG.md.

CLI::

    python -m scripts.acquire_all                      # run everything
    python -m scripts.acquire_all --source osha_sir    # run one source
    python -m scripts.acquire_all --force              # re-download even if cached
"""

from __future__ import annotations

import argparse
import importlib
from datetime import datetime, timezone
from typing import Callable

from scripts.common import (
    DATA_RAW,
    LOG,
    AcquisitionResult,
    make_session,
    run_with_logging,
    setup_logging,
)

# Registry: ordered by phase so easier sources run first and validate the
# shared utilities before the ASRS scraper is attempted.
REGISTRY: list[tuple[str, str, str]] = [
    # (source name, module path, callable name)
    ("osha_sir", "scripts.acquire_osha_sir", "run"),  # Phase 1A
    ("msha", "scripts.acquire_msha", "run"),  # Phase 1A
    ("osha_ita", "scripts.acquire_osha_ita", "run"),  # Phase 1B
    ("nrc", "scripts.acquire_nrc", "run"),  # Phase 1B
    ("ntsb", "scripts.acquire_ntsb", "run"),  # Phase 1C
    ("asrs", "scripts.acquire_asrs", "run"),  # Phase 1D
]


def _load(module_path: str, attr: str) -> Callable[..., AcquisitionResult] | None:
    try:
        mod = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        LOG.warning("%s not yet implemented: %s", module_path, exc)
        return None
    return getattr(mod, attr, None)


def _format_narrative_stats(stats: dict | None) -> str:
    if not stats:
        return "—"
    return (
        f"n={stats.get('n', '—')}, "
        f"mean={stats.get('mean', 0):.1f}, "
        f"median={stats.get('median', 0):.1f}, "
        f"p25={stats.get('p25', 0):.1f}, "
        f"p75={stats.get('p75', 0):.1f}"
    )


def _format_date_range(dr: tuple[str, str] | None) -> str:
    if not dr:
        return "—"
    return f"{dr[0]} → {dr[1]}"


def _render_log(results: list[AcquisitionResult]) -> str:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    total_rows = sum((r.row_count or 0) for r in results)
    lines = [
        "# Acquisition Log",
        "",
        f"_Generated at {ts}_",
        "",
        f"**Sources attempted:** {len(results)}  ",
        f"**Combined row count (summary):** {total_rows:,}",
        "",
        "## Summary",
        "",
        "| Source | Status | Rows | Date range | Narrative (words) | Duration |",
        "|---|---|---:|---|---|---:|",
    ]
    for r in results:
        rows = f"{r.row_count:,}" if r.row_count is not None else "—"
        lines.append(
            "| {src} | {st} | {rows} | {dr} | {nar} | {dur:.1f}s |".format(
                src=r.source,
                st=r.status,
                rows=rows,
                dr=_format_date_range(r.date_range),
                nar=_format_narrative_stats(r.narrative_stats),
                dur=r.duration_s,
            )
        )

    lines += ["", "## Details", ""]
    for r in results:
        lines.append(f"### {r.source} — `{r.status}`")
        lines.append("")
        if r.error:
            lines.append(f"**Error:** `{r.error}`")
            lines.append("")
        if r.notes:
            lines.append(f"**Notes:** {r.notes}")
            lines.append("")
        if r.columns:
            preview = ", ".join(f"`{c}`" for c in r.columns[:15])
            suffix = f" …(+{len(r.columns) - 15} more)" if len(r.columns) > 15 else ""
            lines.append(f"**Columns ({len(r.columns)}):** {preview}{suffix}")
            lines.append("")
        if r.files:
            lines.append("**Files:**")
            for p in r.files:
                lines.append(f"- `{p}`")
            lines.append("")
    return "\n".join(lines) + "\n"


def main(sources: list[str] | None = None, force: bool = False) -> int:
    setup_logging()
    session = make_session()
    results: list[AcquisitionResult] = []

    for name, module_path, attr in REGISTRY:
        if sources and name not in sources:
            continue
        fn = _load(module_path, attr)
        if fn is None:
            results.append(
                AcquisitionResult(
                    source=name,
                    status="skipped",
                    notes="module not implemented yet",
                )
            )
            continue
        result = run_with_logging(name, lambda f=fn: f(session=session, force=force))
        results.append(result)

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    log_path = DATA_RAW / "ACQUISITION_LOG.md"
    log_path.write_text(_render_log(results))
    LOG.info("Wrote %s", log_path)

    # Exit 0 if everything landed ok/partial/skipped; non-zero only on real failures.
    failed = [r for r in results if r.status == "failed"]
    return 1 if failed else 0


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run all Grammar of Failure acquirers.")
    ap.add_argument(
        "--source",
        action="append",
        choices=[name for name, _, _ in REGISTRY],
        help="Restrict to one or more sources (repeatable).",
    )
    ap.add_argument("--force", action="store_true", help="Re-download even if cached.")
    return ap.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    raise SystemExit(main(sources=args.source, force=args.force))
