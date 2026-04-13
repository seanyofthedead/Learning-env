"""OSHA ITA Case Detail + Summary Data (Forms 300/301 and 300A).

ITA Case Detail is the source with **five free-text narrative fields**:
pre-incident activity, how the injury occurred, nature/body parts, harmful
object, and additional description (OIICS-coded starting 2024). Per-year
ZIPs are linked from the ITA page with heterogeneous filename patterns —
we scrape the page and download every ZIP we find for 2018+.

Source page: https://www.osha.gov/Establishment-Specific-Injury-and-Illness-Data
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

from scripts.common import (
    DATA_RAW,
    LOG,
    AcquisitionResult,
    download_with_progress,
    is_already_downloaded,
    make_session,
    manifest_entry,
    narrative_wc_stats,
    run_with_logging,
    write_manifest,
)

SOURCE = "osha_ita"
SOURCE_DIR = DATA_RAW / SOURCE
INDEX_URL = "https://www.osha.gov/Establishment-Specific-Injury-and-Illness-Data"
OSHA_BASE = "https://www.osha.gov"

YEAR_RE = re.compile(r"(20\d{2})")
CASE_DETAIL_HINTS = ("case_detail", "case-detail", "casedetail", "300_301", "300-301")
SUMMARY_HINTS = ("300a_summary", "300a-summary", "summary_data", "summary-data", "ita-data-cy", "ita data cy")


def _classify(href: str) -> tuple[str, int | None]:
    """Return (kind, year) for an ITA ZIP href.

    ``kind`` is one of ``"case_detail"``, ``"summary"``, or ``"unknown"``.
    """
    lower = unquote(href).lower()
    year_match = YEAR_RE.search(lower)
    year = int(year_match.group(1)) if year_match else None
    if any(h in lower for h in CASE_DETAIL_HINTS):
        return "case_detail", year
    if any(h in lower for h in SUMMARY_HINTS):
        return "summary", year
    return "unknown", year


def parse_ita_page(html: str) -> list[dict]:
    """Extract every ZIP link on the OSHA ITA establishment page.

    Returns a list of ``{href, absolute_url, kind, year, filename}`` dicts.
    Pure function — unit-testable without network access.
    """
    soup = BeautifulSoup(html, "lxml")
    out: list[dict] = []
    seen: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.lower().endswith(".zip"):
            continue
        absolute = urljoin(OSHA_BASE, href)
        if absolute in seen:
            continue
        seen.add(absolute)
        kind, year = _classify(href)
        filename = Path(unquote(urlparse(absolute).path)).name
        out.append(
            {
                "href": href,
                "absolute_url": absolute,
                "kind": kind,
                "year": year,
                "filename": filename,
            }
        )
    return out


def discover_files(session: requests.Session) -> list[dict]:
    """Fetch the ITA page and parse all ZIP links."""
    r = session.get(INDEX_URL, timeout=60)
    r.raise_for_status()
    links = parse_ita_page(r.text)
    # Restrict to year >= 2018 (unknown years kept — Case Detail filenames
    # like ``ITA_Case_Detail_Data_2024_through_12-31-2025.zip`` always have
    # a year, but Summary filenames sometimes don't parse cleanly).
    return [l for l in links if l["year"] is None or l["year"] >= 2018]


def _sanitize(name: str) -> str:
    """Replace spaces and problematic chars so filesystems stay happy."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)


def _read_case_detail_zip(zip_path: Path) -> pd.DataFrame | None:
    """Load the first CSV inside a Case Detail ZIP. Tolerant of encoding."""
    try:
        with zipfile.ZipFile(zip_path) as zf:
            csvs = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not csvs:
                return None
            with zf.open(csvs[0]) as f:
                for enc in ("utf-8", "latin-1", "cp1252"):
                    try:
                        return pd.read_csv(
                            f, dtype=str, low_memory=False, encoding=enc
                        )
                    except UnicodeDecodeError:
                        f.seek(0)
                        continue
    except (zipfile.BadZipFile, pd.errors.ParserError) as exc:
        LOG.warning("OSHA ITA: could not read %s: %s", zip_path.name, exc)
        return None
    return None


def _case_detail_summary(zip_paths: list[Path]) -> dict:
    """Aggregate summary across all Case Detail ZIPs."""
    # The five OSHA ITA Case Detail narrative fields (OIICS, 2023+):
    #   NEW_NAR_WHAT_HAPPENED        -- how the injury occurred
    #   NEW_NAR_BEFORE_INCIDENT      -- what the employee was doing before
    #   NEW_NAR_INJURY_ILLNESS       -- nature of injury / body part
    #   NEW_NAR_OBJECT_SUBSTANCE     -- harmful object or substance
    #   NEW_INCIDENT_DESCRIPTION     -- free-text description
    narrative_cols_hints = [
        "new_nar_what_happened",
        "new_nar_before_incident",
        "new_nar_injury_illness",
        "new_nar_object_substance",
        "new_incident_description",
    ]
    all_rows = 0
    all_columns: list[str] = []
    narrative_series: list[pd.Series] = []
    date_min = date_max = None
    for p in zip_paths:
        df = _read_case_detail_zip(p)
        if df is None:
            continue
        all_rows += df.shape[0]
        if not all_columns:
            all_columns = list(df.columns)
        # Combine any column whose lowercased name contains a hint.
        parts = []
        for col in df.columns:
            lc = col.lower().replace(" ", "_")
            if any(h in lc for h in narrative_cols_hints):
                parts.append(df[col].fillna("").astype(str))
        if parts:
            combined = parts[0]
            for extra in parts[1:]:
                combined = combined.str.cat(extra, sep=" \n")
            narrative_series.append(combined.str.strip())
        # Pull a date column
        for cand in ("year_filed_for", "year", "date_of_incident", "incident_date"):
            for col in df.columns:
                if col.lower().replace(" ", "_") == cand:
                    dates = pd.to_datetime(df[col], errors="coerce").dropna()
                    if not dates.empty:
                        dmin, dmax = dates.min(), dates.max()
                        date_min = dmin if date_min is None or dmin < date_min else date_min
                        date_max = dmax if date_max is None or dmax > date_max else date_max
                    break
    out: dict = {"row_count": all_rows, "columns": all_columns}
    if narrative_series:
        out["narrative_stats"] = narrative_wc_stats(pd.concat(narrative_series, ignore_index=True))
    if date_min is not None and date_max is not None:
        out["date_range"] = (str(date_min.date()), str(date_max.date()))
    return out


def run(session: requests.Session | None = None, *, force: bool = False) -> AcquisitionResult:
    session = session or make_session()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        links = discover_files(session)
    except requests.RequestException as exc:
        return AcquisitionResult(
            source=SOURCE,
            status="failed",
            error=f"Could not fetch ITA index page: {exc}",
        )

    if not links:
        return AcquisitionResult(
            source=SOURCE,
            status="failed",
            error="No ZIP links found on ITA index page",
        )

    LOG.info("OSHA ITA: found %d links on index page", len(links))

    downloaded: list[Path] = []
    case_detail_zips: list[Path] = []
    entries: list[dict] = []
    errors: list[str] = []

    for link in links:
        filename = _sanitize(link["filename"])
        dest = SOURCE_DIR / filename
        try:
            if force or not is_already_downloaded(SOURCE_DIR, [filename]):
                download_with_progress(session, link["absolute_url"], dest)
            else:
                LOG.info("OSHA ITA: %s already present, skipping", filename)
            downloaded.append(dest)
            if link["kind"] == "case_detail":
                case_detail_zips.append(dest)
            entries.append(
                manifest_entry(
                    url=link["absolute_url"],
                    filename=filename,
                    path=dest,
                    notes=f"kind={link['kind']}, year={link['year']}",
                )
            )
        except requests.RequestException as exc:
            LOG.warning("OSHA ITA: failed to download %s: %s", link["absolute_url"], exc)
            errors.append(f"{link['filename']}: {exc}")

    write_manifest(SOURCE_DIR, entries)

    summary = _case_detail_summary(case_detail_zips) if case_detail_zips else {}
    status = "ok" if not errors else ("partial" if downloaded else "failed")

    return AcquisitionResult(
        source=SOURCE,
        status=status,
        row_count=summary.get("row_count"),
        date_range=summary.get("date_range"),
        columns=summary.get("columns"),
        narrative_stats=summary.get("narrative_stats"),
        files=downloaded,
        error="; ".join(errors) if errors else None,
        notes=(
            f"case_detail_zips={len(case_detail_zips)}, "
            f"total_zips={len(downloaded)}; "
            "row_count reflects case_detail only (summary has no narratives)"
        ),
    )


def main() -> int:
    result = run_with_logging(SOURCE, run)
    return 0 if result.status in {"ok", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
