"""OSHA Severe Injury Reports (2015–present).

Single-ZIP direct download. The file republishes monthly with a new
``{StartMonth}{StartYear}to{EndMonth}{EndYear}.zip`` name, so we try a
few candidate URLs before giving up. Narratives are short ("Final Narrative")
but we keep them — this is a cross-domain validation corpus.

Source page: https://www.osha.gov/severe-injury-reports
"""

from __future__ import annotations

import calendar
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

from scripts.common import (
    DATA_RAW,
    LOG,
    AcquisitionResult,
    download_with_progress,
    extract_zip,
    is_already_downloaded,
    make_session,
    manifest_entry,
    run_with_logging,
    summarize_dataframe,
    write_manifest,
)

SOURCE = "osha_sir"
SOURCE_DIR = DATA_RAW / SOURCE

KNOWN_URL = "https://www.osha.gov/sites/default/files/January2015toAugust2025.zip"
# Fallbacks: OSHA re-publishes monthly with a rotating end-month name.
CANDIDATE_URL_TEMPLATE = (
    "https://www.osha.gov/sites/default/files/January2015to{end_month}{end_year}.zip"
)


def candidate_urls() -> list[str]:
    """Return a prioritized list of plausible download URLs."""
    urls: list[str] = [KNOWN_URL]
    now = datetime.utcnow()
    # Probe last 18 months in reverse chronological order.
    seen = set(urls)
    for months_back in range(0, 18):
        y = now.year
        m = now.month - months_back
        while m <= 0:
            m += 12
            y -= 1
        name = calendar.month_name[m]
        url = CANDIDATE_URL_TEMPLATE.format(end_month=name, end_year=y)
        if url not in seen:
            urls.append(url)
            seen.add(url)
    return urls


def _head_ok(session: requests.Session, url: str) -> bool:
    try:
        r = session.head(url, allow_redirects=True, timeout=30)
        return r.status_code == 200
    except requests.RequestException:
        return False


def _find_live_url(session: requests.Session) -> str | None:
    for url in candidate_urls():
        if _head_ok(session, url):
            LOG.info("OSHA SIR: using %s", url)
            return url
    return None


def _summarize_extracted(extracted: list[Path]) -> dict:
    """Find the CSV/XLSX inside the ZIP and compute summary stats."""
    for path in extracted:
        if path.suffix.lower() in {".csv", ".xlsx", ".xls"}:
            try:
                if path.suffix.lower() == ".csv":
                    df = pd.read_csv(path, dtype=str, low_memory=False, encoding="latin-1")
                else:
                    df = pd.read_excel(path, dtype=str)
            except Exception as exc:  # noqa: BLE001
                LOG.warning("OSHA SIR: failed to read %s: %s", path.name, exc)
                continue
            # Find likely date + narrative columns (OSHA historically uses "EventDate"
            # and "Final Narrative"; tolerate spacing/case variations).
            date_col = _match_col(df, ["EventDate", "Event Date", "event_date"])
            narrative_col = _match_col(
                df, ["Final Narrative", "FinalNarrative", "final_narrative", "Narrative"]
            )
            LOG.info(
                "OSHA SIR: %s rows=%d date_col=%s narrative_col=%s",
                path.name,
                df.shape[0],
                date_col,
                narrative_col,
            )
            return summarize_dataframe(df, date_col=date_col, narrative_col=narrative_col)
    return {"row_count": 0, "columns": []}


def _match_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    lower = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns:
            return cand
        if cand.lower().strip() in lower:
            return lower[cand.lower().strip()]
    return None


def run(session: requests.Session | None = None, *, force: bool = False) -> AcquisitionResult:
    """Download + summarize the OSHA Severe Injury Reports ZIP."""
    session = session or make_session()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    url = _find_live_url(session)
    if url is None:
        return AcquisitionResult(
            source=SOURCE,
            status="failed",
            error="No candidate OSHA SIR URL returned HTTP 200",
        )

    zip_name = url.rsplit("/", 1)[-1]
    zip_path = SOURCE_DIR / zip_name

    if not force and is_already_downloaded(SOURCE_DIR, [zip_name]):
        LOG.info("OSHA SIR: %s already present, skipping download", zip_name)
    else:
        download_with_progress(session, url, zip_path)

    extracted = extract_zip(zip_path, SOURCE_DIR / "extracted")
    stats = _summarize_extracted(extracted)

    entries = [
        manifest_entry(
            url=url,
            filename=zip_name,
            path=zip_path,
            notes="OSHA Severe Injury Reports (federal OSHA only)",
            extra={"extracted_files": [str(p.relative_to(SOURCE_DIR)) for p in extracted]},
        )
    ]
    write_manifest(SOURCE_DIR, entries)

    return AcquisitionResult(
        source=SOURCE,
        status="ok",
        row_count=stats.get("row_count"),
        date_range=stats.get("date_range"),
        columns=stats.get("columns"),
        narrative_stats=stats.get("narrative_stats"),
        files=[zip_path],
        notes=f"downloaded from {url}",
    )


def main() -> int:
    result = run_with_logging(SOURCE, run)
    return 0 if result.status in {"ok", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
