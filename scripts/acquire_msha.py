"""MSHA Accident/Injury reports (Form 7000-1, 2000–present).

Pipe-delimited text file wrapped in a single ZIP. Mine IDs provide clean
facility-level tracking, but narratives are typically terse ("fell from
ladder"). We download the whole archive and filter to 2018+ only during
summary (preserving raw data verbatim).

Source portal: https://arlweb.msha.gov/opengovernmentdata/ogimsha.asp
Direct URL:    https://www.msha.gov/OpenGovernmentData/DataSets/Accidents.zip
"""

from __future__ import annotations

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
    narrative_wc_stats,
    run_with_logging,
    write_manifest,
)

SOURCE = "msha"
SOURCE_DIR = DATA_RAW / SOURCE

ACCIDENTS_URL = "https://arlweb.msha.gov/OpenGovernmentData/DataSets/Accidents.zip"
DEFINITION_URL = (
    "https://arlweb.msha.gov/OpenGovernmentData/DataSets/Accidents_Definition_File.txt"
)

# Candidate narrative / date column names (MSHA has used various casings).
DATE_COL_CANDIDATES = ["ACCIDENT_DT", "ACCIDENT_DATE", "ACCIDENT_DTE", "ACCIDENTDATE"]
NARRATIVE_COL_CANDIDATES = ["NARRATIVE", "NARRATIVE_DESC", "NARRATIVETEXT", "NARRATIVE_TEXT"]


def _read_pipe_delimited(path: Path) -> pd.DataFrame:
    """Try latin-1 first, fall back to cp1252 (historical MSHA encoding)."""
    for enc in ("latin-1", "cp1252"):
        try:
            return pd.read_csv(
                path,
                sep="|",
                dtype=str,
                encoding=enc,
                on_bad_lines="warn",
                low_memory=False,
            )
        except (UnicodeDecodeError, pd.errors.ParserError) as exc:
            LOG.warning("MSHA: %s decode failed with %s: %s", path.name, enc, exc)
    raise RuntimeError(f"Could not read {path} with any supported encoding")


def _pick_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    upper = {col.upper(): col for col in df.columns}
    for c in candidates:
        if c.upper() in upper:
            return upper[c.upper()]
    return None


def _summarize(extracted: list[Path]) -> dict:
    """Read the Accidents data file and compute summary stats filtered to 2018+."""
    data_file = None
    for path in extracted:
        name = path.name.lower()
        if "accident" in name and ("txt" in name or "dat" in name or "csv" in name):
            data_file = path
            break
    if data_file is None and extracted:
        # Fall back to the first non-definition file.
        for p in extracted:
            if "definition" not in p.name.lower():
                data_file = p
                break
    if data_file is None:
        return {"row_count": 0}

    df = _read_pipe_delimited(data_file)
    LOG.info("MSHA: %s has %d rows, %d columns", data_file.name, df.shape[0], df.shape[1])

    date_col = _pick_col(df, DATE_COL_CANDIDATES)
    narrative_col = _pick_col(df, NARRATIVE_COL_CANDIDATES)

    out: dict = {"columns": list(df.columns)}
    if date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce")
        recent = df[dates >= pd.Timestamp("2018-01-01")]
        out["row_count_total"] = int(df.shape[0])
        out["row_count"] = int(recent.shape[0])
        valid = pd.to_datetime(recent[date_col], errors="coerce").dropna()
        if not valid.empty:
            out["date_range"] = (str(valid.min().date()), str(valid.max().date()))
        if narrative_col:
            out["narrative_stats"] = narrative_wc_stats(recent[narrative_col])
    else:
        out["row_count"] = int(df.shape[0])
        if narrative_col:
            out["narrative_stats"] = narrative_wc_stats(df[narrative_col])
    return out


def run(session: requests.Session | None = None, *, force: bool = False) -> AcquisitionResult:
    session = session or make_session()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    zip_name = "Accidents.zip"
    definition_name = "Accidents_Definition_File.txt"
    zip_path = SOURCE_DIR / zip_name
    definition_path = SOURCE_DIR / definition_name

    # Download archive + data dictionary (dictionary is best-effort).
    if force or not is_already_downloaded(SOURCE_DIR, [zip_name]):
        download_with_progress(session, ACCIDENTS_URL, zip_path)
    else:
        LOG.info("MSHA: %s already present, skipping download", zip_name)

    try:
        download_with_progress(session, DEFINITION_URL, definition_path)
    except requests.RequestException as exc:
        LOG.warning("MSHA: could not download data dictionary: %s", exc)

    extracted = extract_zip(zip_path, SOURCE_DIR / "extracted")
    stats = _summarize(extracted)

    entries = [
        manifest_entry(
            url=ACCIDENTS_URL,
            filename=zip_name,
            path=zip_path,
            notes="MSHA Accidents/Injuries/Illnesses (Form 7000-1), all history",
            extra={"extracted_files": [str(p.relative_to(SOURCE_DIR)) for p in extracted]},
        )
    ]
    if definition_path.exists():
        entries.append(
            manifest_entry(
                url=DEFINITION_URL,
                filename=definition_name,
                path=definition_path,
                notes="MSHA Accidents data dictionary",
            )
        )
    write_manifest(SOURCE_DIR, entries)

    return AcquisitionResult(
        source=SOURCE,
        status="ok",
        row_count=stats.get("row_count"),
        date_range=stats.get("date_range"),
        columns=stats.get("columns"),
        narrative_stats=stats.get("narrative_stats"),
        files=[zip_path],
        notes=f"row_count is 2018+ only (total archive rows={stats.get('row_count_total')})",
    )


def main() -> int:
    result = run_with_logging(SOURCE, run)
    return 0 if result.status in {"ok", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
