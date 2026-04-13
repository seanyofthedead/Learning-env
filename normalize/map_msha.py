"""Map MSHA Accidents raw pipe-delimited data -> unified schema. Vectorized."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd

from normalize._common import DATA_RAW, coerce_normalized
from normalize.schema import NORMALIZED_COLUMNS

SOURCE = "msha"


def _load_raw() -> pd.DataFrame:
    src_dir = DATA_RAW / SOURCE
    path = src_dir / "Accidents.zip"
    if not path.exists():
        return pd.DataFrame()
    with zipfile.ZipFile(path) as zf:
        members = [
            n
            for n in zf.namelist()
            if n.lower().endswith(".txt") and "definition" not in n.lower()
        ]
        if not members:
            return pd.DataFrame()
        for enc in ("latin-1", "cp1252"):
            try:
                with zf.open(members[0]) as f:
                    return pd.read_csv(
                        f,
                        sep="|",
                        dtype=str,
                        encoding=enc,
                        engine="python",
                        on_bad_lines="warn",
                    )
            except UnicodeDecodeError:
                continue
    return pd.DataFrame()


def to_normalized(raw_df: pd.DataFrame) -> pd.DataFrame:
    if raw_df.empty:
        return pd.DataFrame(columns=NORMALIZED_COLUMNS)

    out = pd.DataFrame(index=raw_df.index)
    out["report_id"] = SOURCE + ":" + raw_df["DOCUMENT_NO"].astype(str)
    out["source"] = SOURCE
    out["event_date"] = pd.to_datetime(raw_df["ACCIDENT_DT"], errors="coerce")
    out["entity_raw_key"] = raw_df["MINE_ID"].fillna("").astype(str)
    out["entity_name"] = raw_df["OPERATOR_NAME"].where(
        raw_df["OPERATOR_NAME"].notna(), raw_df["CONTROLLER_NAME"]
    )
    out["entity_address"] = None  # not in MSHA data
    subunit = raw_df.get("SUBUNIT", pd.Series("", index=raw_df.index)).fillna("")
    fips = raw_df.get("FIPS_STATE_CD", pd.Series("", index=raw_df.index)).fillna("")
    out["location"] = (
        subunit.str.strip() + ", " + fips.str.strip()
    ).str.strip(", ").replace({"": None})
    classification = raw_df.get("CLASSIFICATION", pd.Series("", index=raw_df.index)).fillna("")
    acctype = raw_df.get("ACCIDENT_TYPE", pd.Series("", index=raw_df.index)).fillna("")
    out["event_type"] = (
        classification.str.strip() + " / " + acctype.str.strip()
    ).str.strip(" /").replace({"": None})
    out["severity"] = raw_df["DEGREE_INJURY"]
    out["narrative"] = raw_df["NARRATIVE"].fillna("")
    out["synopsis"] = None

    meta_cols = [
        c
        for c in [
            "CONTROLLER_ID",
            "OPERATOR_ID",
            "CONTRACTOR_ID",
            "SUBUNIT_CD",
            "FIPS_STATE_CD",
            "UG_LOCATION",
            "MINING_EQUIP",
            "NATURE_INJURY",
            "INJ_BODY_PART",
            "OCCUPATION",
            "ACTIVITY",
            "DAYS_LOST",
            "COAL_METAL_IND",
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
