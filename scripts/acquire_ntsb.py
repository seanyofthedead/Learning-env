"""NTSB Aviation investigations via the CAROL public API.

**Status: escape-hatch mode.** The CAROL public API at
``https://data.ntsb.gov/carol-main-public/api/Query/Main`` requires a
POST body shape that the NTSB does not publish openly — every plausible
``QueryRule`` schema I probed returned
``{"Error":"QueryGroups does not contain valid QueryRules"}``. The SPA is
Polymer-based and only surfaces the live query format through
runtime-bundled JavaScript, which is not readable in a plain HTTP client
context. Similar story for ``carol-repgen``: GET/POST both return 200 with
empty bodies unless the request matches an internal contract that is not
documented.

Rather than block Phase 1 on reverse-engineering a moving target, this
module takes a best-effort attempt at the documented endpoint and, on
failure, writes a manual-export instructions file. The NTSB corpus was
noted in the original capstone prompt as "useful for validation but not
the primary test of the hypothesis" — losing it is acceptable; what is
not acceptable is Phase 1 stalling.

If/when someone captures a working ``QueryRule`` body from their browser's
DevTools Network panel, drop the JSON into ``CAROL_QUERY_BODY`` below and
this module will paginate automatically.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

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

SOURCE = "ntsb"
SOURCE_DIR = DATA_RAW / SOURCE

CAROL_QUERY_URL = "https://data.ntsb.gov/carol-main-public/api/Query/Main"
CAROL_UI_URL = "https://data.ntsb.gov/carol-main-public/basic-search"

# Populate this with a captured working query body and this module will
# switch from escape-hatch mode to real pagination.
CAROL_QUERY_BODY: dict | None = None

INSTRUCTIONS_FILE = SOURCE_DIR / "MANUAL_EXPORT_INSTRUCTIONS.md"


MANUAL_INSTRUCTIONS = """\
# NTSB CAROL Manual Export Instructions

The CAROL public API at `{api}` requires an undocumented `QueryRule`
schema. Scripted queries receive HTTP 400 with
`{{"Error":"QueryGroups does not contain valid QueryRules"}}`. Rather
than block Phase 1, this file was generated automatically so the
acquisition pipeline can complete; you can fill in NTSB data manually.

## Manual export procedure

1. Open the CAROL basic search UI in a browser:
   **{ui}**
2. Event Type: **Aviation**
3. Event Date: **2018-01-01** through **2025-12-31**
4. Run the search.
5. Click the "Export" button (CSV or JSON).
6. Save the exported file into this directory
   (`data/raw/ntsb/`) with any filename — for example
   `carol_aviation_2018_2025.csv`.
7. Re-run `python -m scripts.acquire_ntsb` and the script will pick up
   any CSV/JSON file in this directory, compute summary stats, and
   update the manifest.

## Capturing a working API body (for full automation)

If you want the acquirer to paginate automatically:

1. Open the CAROL UI above.
2. Open browser DevTools → Network tab.
3. Run any search.
4. Find the POST request to `/carol-main-public/api/Query/Main`.
5. Copy the JSON request body from the "Request" panel.
6. Paste it into `scripts/acquire_ntsb.py` as the value of
   `CAROL_QUERY_BODY` at the top of the file.
7. Re-run the acquirer.

The pagination loop is already written — it just needs a known-good
base query body.
"""


def _find_manual_files() -> list[Path]:
    """Return any user-dropped CSV/JSON files in the source dir.

    Excludes the manifest and instructions file that this script writes
    itself.
    """
    if not SOURCE_DIR.exists():
        return []
    excluded = {"manifest.json", "MANUAL_EXPORT_INSTRUCTIONS.md"}
    return [
        p
        for p in SOURCE_DIR.iterdir()
        if (
            p.is_file()
            and p.suffix.lower() in {".csv", ".json", ".jsonl"}
            and p.name not in excluded
        )
    ]


def _summarize_manual_files(files: list[Path]) -> dict:
    import pandas as pd

    rows = 0
    narratives: list[pd.Series] = []
    columns: list[str] = []
    date_min = date_max = None
    for path in files:
        try:
            if path.suffix.lower() == ".csv":
                df = pd.read_csv(path, dtype=str, low_memory=False)
            else:
                df = pd.read_json(path, dtype=False)
        except Exception as exc:  # noqa: BLE001
            LOG.warning("NTSB: could not read %s: %s", path.name, exc)
            continue
        rows += df.shape[0]
        if not columns:
            columns = list(df.columns)
        for col in df.columns:
            lc = col.lower().replace(" ", "_")
            if any(h in lc for h in ("narrative", "probable_cause", "findings")):
                narratives.append(df[col].fillna("").astype(str))
        for col in df.columns:
            lc = col.lower().replace(" ", "_")
            if "event_date" in lc or "eventdate" in lc:
                dates = pd.to_datetime(df[col], errors="coerce").dropna()
                if not dates.empty:
                    dmin, dmax = dates.min(), dates.max()
                    date_min = dmin if date_min is None or dmin < date_min else date_min
                    date_max = dmax if date_max is None or dmax > date_max else date_max
                break
    out: dict = {"row_count": rows, "columns": columns}
    if narratives:
        out["narrative_stats"] = narrative_wc_stats(pd.concat(narratives, ignore_index=True))
    if date_min is not None and date_max is not None:
        out["date_range"] = (str(date_min.date()), str(date_max.date()))
    return out


def _try_automated_query(session: requests.Session) -> tuple[list[Path], str | None]:
    """Attempt to drive the CAROL API if a working query body is configured.

    Returns ``(saved_files, error_message_or_None)``.
    """
    if CAROL_QUERY_BODY is None:
        return [], "CAROL_QUERY_BODY not configured"

    saved: list[Path] = []
    page = 1
    size = 500
    while True:
        body = dict(CAROL_QUERY_BODY)
        body.setdefault("PageNo", page)
        body.setdefault("PageSize", size)
        try:
            r = session.post(CAROL_QUERY_URL, json=body, timeout=90)
        except requests.RequestException as exc:
            return saved, f"HTTP error on page {page}: {exc}"
        if r.status_code != 200:
            return saved, f"HTTP {r.status_code} on page {page}: {r.text[:200]}"
        try:
            payload = r.json()
        except ValueError:
            return saved, f"Non-JSON response on page {page}"
        out = SOURCE_DIR / f"aviation_page_{page:04d}.json"
        out.write_text(json.dumps(payload, indent=2))
        saved.append(out)
        rows = payload.get("rows") or payload.get("Rows") or payload.get("data") or []
        if len(rows) < size:
            break
        page += 1
        time.sleep(1.0)
    return saved, None


def run(session: requests.Session | None = None, *, force: bool = False) -> AcquisitionResult:
    session = session or make_session()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    # 1. If user has already dropped manual files, pick them up.
    manual_files = _find_manual_files()
    if manual_files:
        LOG.info("NTSB: found %d manual file(s), summarizing", len(manual_files))
        stats = _summarize_manual_files(manual_files)
        entries = [
            manifest_entry(
                url=CAROL_UI_URL,
                filename=p.name,
                path=p,
                notes="manually exported from CAROL UI",
            )
            for p in manual_files
        ]
        write_manifest(SOURCE_DIR, entries)
        return AcquisitionResult(
            source=SOURCE,
            status="ok",
            row_count=stats.get("row_count"),
            date_range=stats.get("date_range"),
            columns=stats.get("columns"),
            narrative_stats=stats.get("narrative_stats"),
            files=manual_files,
            notes="loaded from manual CAROL export",
        )

    # 2. Try automated query if configured.
    saved, err = _try_automated_query(session)
    if saved and not err:
        stats = _summarize_manual_files(saved)
        entries = [
            manifest_entry(
                url=CAROL_QUERY_URL,
                filename=p.name,
                path=p,
                notes="auto-fetched via CAROL Query/Main",
            )
            for p in saved
        ]
        write_manifest(SOURCE_DIR, entries)
        return AcquisitionResult(
            source=SOURCE,
            status="ok",
            row_count=stats.get("row_count"),
            date_range=stats.get("date_range"),
            columns=stats.get("columns"),
            narrative_stats=stats.get("narrative_stats"),
            files=saved,
            notes="auto-fetched from CAROL API",
        )

    # 3. Escape hatch: write manual instructions so the user can finish by hand.
    INSTRUCTIONS_FILE.write_text(
        MANUAL_INSTRUCTIONS.format(api=CAROL_QUERY_URL, ui=CAROL_UI_URL)
    )
    write_manifest(
        SOURCE_DIR,
        [
            {
                "url": CAROL_UI_URL,
                "filename": INSTRUCTIONS_FILE.name,
                "notes": "escape-hatch: manual export required",
                "sha256": None,
                "bytes": INSTRUCTIONS_FILE.stat().st_size,
            }
        ],
    )
    return AcquisitionResult(
        source=SOURCE,
        status="failed",
        files=[INSTRUCTIONS_FILE],
        error=err or "CAROL API query schema undocumented; manual export required",
        notes=(
            "See data/raw/ntsb/MANUAL_EXPORT_INSTRUCTIONS.md for manual steps. "
            "Once CAROL_QUERY_BODY is populated with a DevTools-captured "
            "request body, this module will paginate automatically."
        ),
    )


def main() -> int:
    result = run_with_logging(SOURCE, run)
    return 0 if result.status in {"ok", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
