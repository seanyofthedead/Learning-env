"""Map OSHA Severe Injury Reports raw CSV -> unified schema.

Fully vectorized — on ~100k rows this runs in a few seconds, not minutes.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from normalize._common import DATA_RAW, coerce_normalized
from normalize.schema import NORMALIZED_COLUMNS

SOURCE = "osha_sir"


def _load_raw() -> pd.DataFrame:
    src_dir = DATA_RAW / SOURCE
    zips = sorted(src_dir.glob("*.zip"))
    if not zips:
        return pd.DataFrame()
    with zipfile.ZipFile(zips[0]) as zf:
        csvs = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        with zf.open(csvs[0]) as f:
            return pd.read_csv(f, dtype=str, low_memory=False, encoding="latin-1")


def _is_truthy(series: pd.Series) -> pd.Series:
    """Return True where the value is a non-zero numeric or 'true'."""
    if series is None:
        return pd.Series(False, index=[])
    s = series.fillna("0").astype(str).str.strip()
    return ~s.isin(["0", "0.00", "0.0", "", "nan", "NaN", "false", "False"])


def _vectorized_address(df: pd.DataFrame) -> pd.Series:
    """Build 'Street1 Street2, City, State Zip' as a vectorized string op."""
    street = (
        df["Address1"].fillna("").str.strip()
        + " "
        + df["Address2"].fillna("").str.strip()
    ).str.strip()
    locality = (
        df["City"].fillna("").str.strip()
        + ", "
        + df["State"].fillna("").str.strip()
        + " "
        + df["Zip"].fillna("").str.strip()
    ).str.strip(", ").str.strip()
    full = (street + ", " + locality).str.strip(", ").str.strip()
    return full.replace({"": None})


def _vectorized_severity(df: pd.DataFrame) -> pd.Series:
    hosp = _is_truthy(df["Hospitalized"])
    amp = _is_truthy(df["Amputation"])
    eye = _is_truthy(df["Loss of Eye"])
    out = pd.Series("", index=df.index)
    out = np.where(hosp, out + "hospitalized;", out)
    out = pd.Series(out, index=df.index)
    out = np.where(amp, out + "amputation;", out)
    out = pd.Series(out, index=df.index)
    out = np.where(eye, out + "eye_loss;", out)
    out = pd.Series(out, index=df.index).str.rstrip(";")
    return out.replace({"": None})


def to_normalized(raw_df: pd.DataFrame) -> pd.DataFrame:
    if raw_df.empty:
        return pd.DataFrame(columns=NORMALIZED_COLUMNS)

    out = pd.DataFrame(index=raw_df.index)
    out["report_id"] = SOURCE + ":" + raw_df["ID"].astype(str)
    out["source"] = SOURCE
    out["event_date"] = pd.to_datetime(raw_df["EventDate"], errors="coerce")
    out["entity_raw_key"] = raw_df["UPA"].fillna("").astype(str)
    out["entity_name"] = raw_df["Employer"]
    out["entity_address"] = _vectorized_address(raw_df)
    out["location"] = (
        raw_df["City"].fillna("").str.strip()
        + ", "
        + raw_df["State"].fillna("").str.strip()
    ).str.strip(", ").replace({"": None})
    out["event_type"] = raw_df["EventTitle"].where(
        raw_df["EventTitle"].notna(), raw_df["Event"]
    )
    out["severity"] = _vectorized_severity(raw_df)
    out["narrative"] = raw_df["Final Narrative"].fillna("")
    out["synopsis"] = None

    meta_cols = [
        c
        for c in [
            "Primary NAICS",
            "NatureTitle",
            "Part of Body Title",
            "SourceTitle",
            "Secondary Source Title",
            "FederalState",
            "Latitude",
            "Longitude",
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
