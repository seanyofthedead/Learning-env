"""Map NRC Event Notifications raw pipe-delimited file -> unified schema."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from normalize._common import DATA_RAW, coerce_normalized
from normalize.schema import NORMALIZED_COLUMNS

SOURCE = "nrc"


def _load_raw() -> pd.DataFrame:
    path = DATA_RAW / SOURCE / "event-notification-rpt-lastmonth.txt"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(
        path,
        sep="|",
        dtype=str,
        encoding="latin-1",
        engine="python",
        on_bad_lines="warn",
    )
    return df.loc[:, ~df.columns.astype(str).str.fullmatch(r"Unnamed:\s*\d+")]


def to_normalized(raw_df: pd.DataFrame) -> pd.DataFrame:
    if raw_df.empty:
        return pd.DataFrame(columns=NORMALIZED_COLUMNS)

    out = pd.DataFrame(index=raw_df.index)
    out["report_id"] = SOURCE + ":" + raw_df["En No"].astype(str)
    out["source"] = SOURCE
    out["event_date"] = pd.to_datetime(raw_df["Event Dt"], errors="coerce")
    out["entity_raw_key"] = raw_df["Docket No"].fillna("").astype(str)
    out["entity_name"] = raw_df["Licensee Name"].where(
        raw_df["Licensee Name"].notna(), raw_df["Site Name"]
    )
    city = raw_df.get("City Name", pd.Series("", index=raw_df.index)).fillna("")
    state = raw_df.get("State Cd", pd.Series("", index=raw_df.index)).fillna("")
    county = raw_df.get("County Name", pd.Series("", index=raw_df.index)).fillna("")
    out["entity_address"] = (
        city.str.strip() + ", " + state.str.strip() + ", " + county.str.strip()
    ).str.strip(", ").replace({"": None})
    out["location"] = raw_df["Site Name"]
    out["event_type"] = raw_df["Event Desc"]
    out["severity"] = raw_df["Emergency Class"]
    out["narrative"] = raw_df["Event Text"].fillna("")
    out["synopsis"] = None

    meta_cols = [
        c
        for c in [
            "Region No",
            "Unit Ind1",
            "Unit Ind2",
            "Unit Ind3",
            "Reactor Type",
            "Notification Dt",
            "Notification Time",
            "Cfr Descr1",
            "Cfr Descr2",
            "Cfr Descr3",
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
