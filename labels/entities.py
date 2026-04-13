"""Canonical entity extraction and linking.

For sources with clean native IDs (MSHA mine_id, OSHA ITA establishment_id,
NRC docket), we pass through. For sources without, we normalize names and
rely on the raw key as a coarse surrogate. Cross-source entity linking is
out of scope for v1.
"""

from __future__ import annotations

import re

import pandas as pd


def normalize_name(s: str | None) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return ""
    t = str(s).lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _normalize_series(s: pd.Series) -> pd.Series:
    """Vectorized version of ``normalize_name`` for a whole series."""
    s = s.fillna("").astype(str).str.lower()
    s = s.str.replace(r"[^a-z0-9\s]", " ", regex=True)
    s = s.str.replace(r"\s+", " ", regex=True).str.strip()
    return s


def _compute_entity_keys(df: pd.DataFrame) -> pd.Series:
    """Vectorized per-source canonical key assignment."""
    keys = pd.Series("", index=df.index, dtype="object")
    src = df["source"]
    raw = df["entity_raw_key"].fillna("").astype(str)
    name_n = _normalize_series(df["entity_name"])
    addr_n = _normalize_series(df["entity_address"])
    loc_n = _normalize_series(df["location"])
    row_idx = pd.Series(df.index.astype(str), index=df.index)

    # msha
    m = src == "msha"
    keys.loc[m] = "msha:mine:" + raw.loc[m]
    # Where raw is empty, fall back to name.
    mf = m & (raw == "")
    keys.loc[mf] = "msha:name:" + name_n.loc[mf]

    # osha_ita
    m = src == "osha_ita"
    keys.loc[m] = "ita:est:" + raw.loc[m]
    mf = m & (raw == "")
    keys.loc[mf] = "ita:name:" + name_n.loc[mf]

    # nrc
    m = src == "nrc"
    keys.loc[m] = "nrc:docket:" + raw.loc[m]
    mf = m & (raw == "")
    keys.loc[mf] = "nrc:name:" + name_n.loc[mf]

    # osha_sir — composite name + address
    m = src == "osha_sir"
    comp = (name_n.loc[m] + "|" + addr_n.loc[m]).str.strip("|")
    keys.loc[m] = "sir:comp:" + comp
    mf = m & (comp == "")
    keys.loc[mf] = "sir:row:" + row_idx.loc[mf]

    # asrs — composite location + aircraft/name
    m = src == "asrs"
    comp = (loc_n.loc[m] + "|" + name_n.loc[m]).str.strip("|")
    keys.loc[m] = "asrs:comp:" + comp
    mf = m & (comp == "")
    keys.loc[mf] = "asrs:row:" + row_idx.loc[mf]

    # ntsb — operator name or raw
    m = src == "ntsb"
    op = name_n.loc[m].where(name_n.loc[m] != "", raw.loc[m])
    keys.loc[m] = "ntsb:op:" + op

    return keys


def build_entities(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return ``(df_with_entity_id, entities_df)``.

    ``entity_id`` is a dense int64 surrogate. ``entities_df`` has one row
    per unique entity with aggregated first/last/count stats.
    """
    df = df.copy()
    df["_entity_key"] = _compute_entity_keys(df)

    # Surrogate entity_id via factorize (stable, dense ints).
    codes, _ = pd.factorize(df["_entity_key"], sort=True)
    df["entity_id"] = codes.astype("int64")

    # Build the entities table.
    agg = df.groupby("entity_id", sort=False).agg(
        source=("source", "first"),
        native_key=("entity_raw_key", "first"),
        canonical_name=("entity_name", "first"),
        canonical_address=("entity_address", "first"),
        canonical_location=("location", "first"),
        first_seen=("event_date", "min"),
        last_seen=("event_date", "max"),
        report_count=("report_id", "count"),
    ).reset_index()

    df = df.drop(columns=["_entity_key"])
    return df, agg
