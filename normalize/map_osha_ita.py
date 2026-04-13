"""Map OSHA ITA Case Detail raw CSVs -> unified schema.

Fully vectorized. Only Case Detail files (not Summary/300A) carry the
five narrative fields; earlier-year Summary files have no narratives
and are skipped.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

import pandas as pd

from normalize._common import DATA_RAW, coerce_normalized
from normalize.schema import NORMALIZED_COLUMNS

SOURCE = "osha_ita"
CASE_DETAIL_RE = re.compile(r"Case[_-]?Detail", re.IGNORECASE)

NARRATIVE_COLS = [
    "NEW_NAR_BEFORE_INCIDENT",
    "NEW_NAR_WHAT_HAPPENED",
    "NEW_NAR_INJURY_ILLNESS",
    "NEW_NAR_OBJECT_SUBSTANCE",
    "NEW_INCIDENT_DESCRIPTION",
]
SECTION_LABELS = {
    "NEW_NAR_BEFORE_INCIDENT": "[before]",
    "NEW_NAR_WHAT_HAPPENED": "[what_happened]",
    "NEW_NAR_INJURY_ILLNESS": "[injury_illness]",
    "NEW_NAR_OBJECT_SUBSTANCE": "[object_substance]",
    "NEW_INCIDENT_DESCRIPTION": "[description]",
}


def _load_raw() -> pd.DataFrame:
    src_dir = DATA_RAW / SOURCE
    frames: list[pd.DataFrame] = []
    for zip_path in sorted(src_dir.glob("*.zip")):
        if not CASE_DETAIL_RE.search(zip_path.name):
            continue
        try:
            with zipfile.ZipFile(zip_path) as zf:
                csvs = [n for n in zf.namelist() if n.lower().endswith(".csv")]
                if not csvs:
                    continue
                df: pd.DataFrame | None = None
                for enc in ("utf-8", "latin-1", "cp1252"):
                    try:
                        with zf.open(csvs[0]) as f:
                            df = pd.read_csv(f, dtype=str, low_memory=False, encoding=enc)
                        break
                    except UnicodeDecodeError:
                        continue
                if df is not None:
                    frames.append(df)
        except (zipfile.BadZipFile, pd.errors.ParserError):
            continue
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _vectorized_narrative(df: pd.DataFrame) -> pd.Series:
    """Concatenate the five NEW_NAR_* fields with section headers."""
    parts: list[pd.Series] = []
    for col in NARRATIVE_COLS:
        if col not in df.columns:
            continue
        label = SECTION_LABELS[col]
        cleaned = df[col].fillna("").astype(str).str.strip()
        # Only prefix non-empty values with the section label.
        prefixed = cleaned.where(cleaned == "", label + " " + cleaned)
        parts.append(prefixed)
    if not parts:
        return pd.Series("", index=df.index)
    joined = parts[0]
    for extra in parts[1:]:
        # Join with newline only when both sides are non-empty.
        empty_mask = joined.eq("") | extra.eq("")
        joined = (joined + "\n" + extra).where(~empty_mask, joined + extra)
    return joined


def _vectorized_address(df: pd.DataFrame) -> pd.Series:
    street = df.get("street_address", pd.Series("", index=df.index)).fillna("")
    city = df.get("city", pd.Series("", index=df.index)).fillna("")
    state = df.get("state", pd.Series("", index=df.index)).fillna("")
    zip_code = df.get("zip_code", pd.Series("", index=df.index)).fillna("")
    locality = (
        city.str.strip()
        + ", "
        + state.str.strip()
        + " "
        + zip_code.str.strip()
    ).str.strip(", ").str.strip()
    full = (street.str.strip() + ", " + locality).str.strip(", ").str.strip()
    return full.replace({"": None})


def to_normalized(raw_df: pd.DataFrame) -> pd.DataFrame:
    if raw_df.empty:
        return pd.DataFrame(columns=NORMALIZED_COLUMNS)

    out = pd.DataFrame(index=raw_df.index)
    out["report_id"] = SOURCE + ":" + raw_df["id"].astype(str)
    out["source"] = SOURCE
    out["event_date"] = pd.to_datetime(raw_df["date_of_incident"], errors="coerce")
    out["entity_raw_key"] = raw_df["establishment_id"].fillna("").astype(str)
    out["entity_name"] = raw_df["establishment_name"].where(
        raw_df["establishment_name"].notna(), raw_df["company_name"]
    )
    out["entity_address"] = _vectorized_address(raw_df)
    # Prefer the explicit incident location, else fall back to city/state.
    city_state = (
        raw_df["city"].fillna("").str.strip()
        + ", "
        + raw_df["state"].fillna("").str.strip()
    ).str.strip(", ")
    out["location"] = raw_df.get("NEW_INCIDENT_LOCATION", pd.Series(None, index=raw_df.index))
    out["location"] = out["location"].where(out["location"].notna(), city_state).replace({"": None})
    out["event_type"] = raw_df.get(
        "event_title_pred", pd.Series(None, index=raw_df.index)
    ).where(
        raw_df.get("event_title_pred", pd.Series(None, index=raw_df.index)).notna(),
        raw_df.get("type_of_incident"),
    )
    out["severity"] = raw_df.get("incident_outcome")
    out["narrative"] = _vectorized_narrative(raw_df)
    out["synopsis"] = raw_df.get("NEW_NAR_WHAT_HAPPENED")

    meta_cols = [
        c
        for c in [
            "ein",
            "naics_code",
            "naics_year",
            "industry_description",
            "establishment_type",
            "size",
            "annual_average_employees",
            "job_description",
            "soc_code",
            "soc_description",
            "dafw_num_away",
            "djtr_num_tr",
            "type_of_incident",
            "time_of_incident",
            "date_of_death",
            "year_of_filing",
            "nature_title_pred",
            "part_title_pred",
            "source_title_pred",
        ]
        if c in raw_df.columns
    ]
    out["meta"] = raw_df[meta_cols].to_dict(orient="records")

    return coerce_normalized(out, SOURCE)


def run() -> pd.DataFrame:
    return to_normalized(_load_raw())


if __name__ == "__main__":
    df = run()
    print(f"{SOURCE}: {df.shape[0]} rows")
