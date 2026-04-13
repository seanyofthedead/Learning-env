"""NASA ASRS DBOL — the hardest Phase 1 source.

DBOL is an ASP.NET WebForms application at
``https://akama.arc.nasa.gov/ASRSDBOnline/QueryWizard_Filter.aspx``. It
exposes a multi-step wizard (Filter → Results → View/Export) with
hidden ``__VIEWSTATE``, ``__VIEWSTATEGENERATOR``, and
``__EVENTVALIDATION`` tokens that change every request. The underlying
export endpoint is only reachable after the wizard has been walked, and
the export button is wired via JavaScript-emitted postbacks. This makes
a robust headless scraper difficult without a full browser automation
stack (Playwright or Selenium), which is a heavy dependency to pull in
for a single source.

This module takes a conservative escape-hatch approach:

1. **Form introspection** is always attempted and its output is written
   to ``data/raw/asrs/form_schema.json`` for debugging.
2. **Manual-chunk loader** is the primary path: drop any CSV file into
   ``data/raw/asrs/chunks/`` and the combine step will concatenate them
   verbatim into ``asrs_combined.csv`` for downstream normalization.
3. **Escape-hatch instructions** are written whenever no chunks exist.
   The instructions pre-generate the exact DBOL filter combinations
   (anomaly × quarter) that a human should export.

Volume target: 10,000+ reports for 2018-01 through 2024-12, filtered to
major US airports and the eight anomaly categories listed below.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests

from scripts.common import (
    DATA_RAW,
    LOG,
    AcquisitionResult,
    make_session,
    manifest_entry,
    narrative_wc_stats,
    run_with_logging,
    write_manifest,
)

SOURCE = "asrs"
SOURCE_DIR = DATA_RAW / SOURCE
CHUNKS_DIR = SOURCE_DIR / "chunks"
COMBINED_FILE = SOURCE_DIR / "asrs_combined.csv"
SCHEMA_FILE = SOURCE_DIR / "form_schema.json"
INSTRUCTIONS_FILE = SOURCE_DIR / "asrs_manual_instructions.md"

DBOL_LANDING_URL = "https://asrs.arc.nasa.gov/search/database.html"
DBOL_FORM_URL = "https://akama.arc.nasa.gov/ASRSDBOnline/QueryWizard_Filter.aspx"

ANOMALIES = [
    "Deviation-Altitude",
    "Deviation-Procedural",
    "Conflict",
    "ATC Issue",
    "Aircraft Equipment Problem",
    "Airspace Violation",
    "Runway Incursion",
    "Ground Incursion",
]

TOP_AIRPORTS = [
    "ATL", "ORD", "LAX", "DFW", "DEN", "JFK", "SFO", "CLT", "PHX", "LAS",
    "MIA", "SEA", "EWR", "MSP", "DTW", "BOS", "FLL", "IAH", "SAN", "SLC",
]

YEAR_RANGE = (2018, 2024)


def quarter_strings(year_range: tuple[int, int]) -> list[str]:
    """Return ['2018Q1', '2018Q2', ...] for the range."""
    out: list[str] = []
    for y in range(year_range[0], year_range[1] + 1):
        for q in range(1, 5):
            out.append(f"{y}Q{q}")
    return out


def planned_chunks() -> list[dict]:
    """Pre-compute the list of (anomaly, quarter) chunks the user should export."""
    out: list[dict] = []
    for anomaly in ANOMALIES:
        for qstr in quarter_strings(YEAR_RANGE):
            out.append(
                {
                    "anomaly": anomaly,
                    "quarter": qstr,
                    "filename": (
                        f"asrs_{anomaly.replace(' ', '_').replace('-', '_')}"
                        f"_{qstr}.csv"
                    ),
                }
            )
    return out


def parse_dbol_form(html: str) -> dict:
    """Extract ASP.NET WebForms state tokens from the DBOL form HTML.

    Pure function — testable offline with a captured HTML fixture.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "lxml")
    form = soup.find("form")
    action = form.get("action") if form else None
    inputs: dict[str, str] = {}
    selects: dict[str, list[str]] = {}
    for inp in soup.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        inputs[name] = inp.get("value", "")
    for sel in soup.find_all("select"):
        name = sel.get("name")
        if not name:
            continue
        options = [o.get("value", "") for o in sel.find_all("option")]
        selects[name] = options
    return {
        "form_action": action,
        "tokens": {
            k: inputs.get(k, "")
            for k in ("__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION")
        },
        "all_inputs": inputs,
        "selects": selects,
    }


def _introspect_form(session: requests.Session) -> dict | None:
    """Fetch the DBOL form and persist schema to disk for debugging."""
    try:
        r = session.get(DBOL_FORM_URL, timeout=60)
        r.raise_for_status()
    except requests.RequestException as exc:
        LOG.warning("ASRS: could not fetch DBOL form: %s", exc)
        return None
    schema = parse_dbol_form(r.text)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMA_FILE.write_text(json.dumps(schema, indent=2, default=str))
    LOG.info(
        "ASRS: form introspection complete — %d inputs, %d selects, tokens=%s",
        len(schema["all_inputs"]),
        len(schema["selects"]),
        {k: bool(v) for k, v in schema["tokens"].items()},
    )
    return schema


def _load_chunks() -> list[Path]:
    if not CHUNKS_DIR.exists():
        return []
    return sorted(p for p in CHUNKS_DIR.iterdir() if p.suffix.lower() == ".csv")


def _combine_chunks(chunk_files: list[Path]) -> tuple[pd.DataFrame | None, str | None]:
    """Concatenate chunk CSVs, verifying header consistency."""
    if not chunk_files:
        return None, None

    frames: list[pd.DataFrame] = []
    reference_cols: list[str] | None = None
    for path in chunk_files:
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                df = pd.read_csv(path, dtype=str, encoding=enc, low_memory=False)
                break
            except UnicodeDecodeError:
                continue
            except pd.errors.ParserError as exc:
                return None, f"Parse error in {path.name}: {exc}"
        else:
            return None, f"Could not decode {path.name} in any supported encoding"
        if reference_cols is None:
            reference_cols = list(df.columns)
        elif list(df.columns) != reference_cols:
            return None, (
                f"Header mismatch in {path.name}: expected {len(reference_cols)} cols, "
                f"got {len(df.columns)}"
            )
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(COMBINED_FILE, index=False)
    return combined, None


def _summarize(df: pd.DataFrame) -> dict:
    """Best-effort summary: find date, narrative, and synopsis columns."""
    out: dict = {"row_count": int(df.shape[0]), "columns": list(df.columns)}
    narrative_col: str | None = None
    date_col: str | None = None
    for col in df.columns:
        lc = col.lower().replace(" ", "_")
        if narrative_col is None and "narrative" in lc:
            narrative_col = col
        if date_col is None and ("date" in lc or "time" in lc):
            # Prefer ``event_date`` or ``time_date`` over ``reporter_date``.
            if "event" in lc or "time" == lc or lc == "date":
                date_col = col
    if date_col is None:
        for col in df.columns:
            if "date" in col.lower():
                date_col = col
                break
    if date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
        if not dates.empty:
            out["date_range"] = (str(dates.min().date()), str(dates.max().date()))
    if narrative_col:
        out["narrative_stats"] = narrative_wc_stats(df[narrative_col])
    return out


def _write_instructions(plan: list[dict]) -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NASA ASRS Manual Export Instructions",
        "",
        "The DBOL (Database Online) tool is an ASP.NET WebForms wizard at",
        f"**{DBOL_FORM_URL}** whose export endpoint is only reachable after",
        "walking a multi-step form with hidden `__VIEWSTATE` tokens. Scripted",
        "scraping is fragile without a headless browser — the pragmatic path",
        "is to drive the UI yourself and drop the exports into this directory.",
        "",
        "## Procedure",
        "",
        "1. Open DBOL: <https://asrs.arc.nasa.gov/search/database.html>",
        "2. Click **Begin Query**.",
        "3. For each row in the plan below, configure these filters:",
        "   - **Incident Date**: start and end of the quarter",
        "   - **Anomaly**: select the anomaly from the list",
        "   - **Airports** (multi-select): " + ", ".join(TOP_AIRPORTS),
        "4. Run the query. On the results page, click **Export → CSV**.",
        "5. Save the CSV into `data/raw/asrs/chunks/` using the filename in",
        "   the table — this lets the combine step pick it up on re-run.",
        "6. Re-run `python -m scripts.acquire_asrs`. It will concatenate all",
        "   chunks into `asrs_combined.csv` and report summary stats.",
        "",
        "## Chunk plan",
        "",
        f"{len(plan)} chunks = {len(ANOMALIES)} anomalies × "
        f"{len(quarter_strings(YEAR_RANGE))} quarters",
        "",
        "| # | Anomaly | Quarter | Save as |",
        "|---:|---|---|---|",
    ]
    for i, c in enumerate(plan, 1):
        lines.append(f"| {i} | {c['anomaly']} | {c['quarter']} | `{c['filename']}` |")
    lines += [
        "",
        "## If a quarter returns exactly 10,000 rows",
        "",
        "DBOL caps results at 10,000 per query. If any quarterly chunk hits",
        "the cap, split it into months (e.g. 2022M01…2022M03 for 2022Q1) and",
        "rename the files accordingly — the combine step concatenates all",
        "CSVs in the chunks directory regardless of filename.",
        "",
        "## Status",
        "",
        "This file was generated by `scripts/acquire_asrs.py`. It is kept in",
        "git so anyone rebuilding the corpus has a concrete playbook.",
    ]
    INSTRUCTIONS_FILE.write_text("\n".join(lines) + "\n")
    LOG.info("ASRS: wrote manual export instructions to %s", INSTRUCTIONS_FILE)


def run(session: requests.Session | None = None, *, force: bool = False) -> AcquisitionResult:
    session = session or make_session()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    # Best-effort form introspection for debugging (never blocks).
    schema = _introspect_form(session)
    form_ok = schema is not None and bool(schema["tokens"].get("__VIEWSTATE"))

    # Load and combine any manually-dropped chunk files.
    chunks = _load_chunks()
    LOG.info("ASRS: found %d chunk CSVs in %s", len(chunks), CHUNKS_DIR)

    plan = planned_chunks()
    _write_instructions(plan)

    if not chunks:
        # No data yet — escape-hatch mode.
        entries = [
            {
                "url": DBOL_FORM_URL,
                "filename": INSTRUCTIONS_FILE.name,
                "notes": (
                    "escape-hatch: no chunks present. "
                    f"form_introspected={form_ok}. "
                    "See asrs_manual_instructions.md for the export plan."
                ),
                "sha256": None,
                "bytes": INSTRUCTIONS_FILE.stat().st_size,
            }
        ]
        if schema:
            entries.append(
                {
                    "url": DBOL_FORM_URL,
                    "filename": SCHEMA_FILE.name,
                    "notes": "DBOL form state introspection",
                    "sha256": None,
                    "bytes": SCHEMA_FILE.stat().st_size,
                }
            )
        write_manifest(SOURCE_DIR, entries)
        return AcquisitionResult(
            source=SOURCE,
            status="failed",
            files=[INSTRUCTIONS_FILE],
            error="No ASRS chunk CSVs present and DBOL scripted export unavailable",
            notes=(
                f"Manual export plan written with {len(plan)} chunks. "
                f"Form introspection {'succeeded' if form_ok else 'failed'}. "
                "Drop CSVs into data/raw/asrs/chunks/ and re-run to combine."
            ),
        )

    # Combine and summarize existing chunks.
    combined_df, err = _combine_chunks(chunks)
    if err or combined_df is None:
        return AcquisitionResult(
            source=SOURCE,
            status="failed",
            error=err or "Could not combine ASRS chunks",
            files=chunks,
        )

    stats = _summarize(combined_df)

    entries = [
        manifest_entry(
            url=DBOL_FORM_URL,
            filename=COMBINED_FILE.name,
            path=COMBINED_FILE,
            notes=f"Concatenated from {len(chunks)} chunk CSVs",
            extra={"chunk_count": len(chunks)},
        ),
        {
            "url": DBOL_FORM_URL,
            "filename": INSTRUCTIONS_FILE.name,
            "notes": "manual export plan",
            "sha256": None,
            "bytes": INSTRUCTIONS_FILE.stat().st_size,
        },
    ]
    if schema:
        entries.append(
            {
                "url": DBOL_FORM_URL,
                "filename": SCHEMA_FILE.name,
                "notes": "DBOL form state introspection",
                "sha256": None,
                "bytes": SCHEMA_FILE.stat().st_size,
            }
        )
    write_manifest(SOURCE_DIR, entries)

    status = "partial" if len(chunks) < len(plan) else "ok"
    return AcquisitionResult(
        source=SOURCE,
        status=status,
        row_count=stats.get("row_count"),
        date_range=stats.get("date_range"),
        columns=stats.get("columns"),
        narrative_stats=stats.get("narrative_stats"),
        files=[COMBINED_FILE],
        notes=f"Combined {len(chunks)}/{len(plan)} planned chunks",
    )


def main() -> int:
    result = run_with_logging(SOURCE, run)
    return 0 if result.status in {"ok", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
