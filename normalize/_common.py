"""Helpers shared across ``normalize/map_*`` modules."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd

from normalize.schema import NORMALIZED_COLUMNS

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
DATA_PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"


def empty_frame() -> pd.DataFrame:
    """Return an empty dataframe with the canonical column order."""
    return pd.DataFrame({c: pd.Series(dtype="object") for c in NORMALIZED_COLUMNS})


def coerce_normalized(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """Ensure ``df`` has the canonical column order and correct dtypes.

    ``event_date`` is coerced to pandas datetime (coerce="errors"). Rows
    with unparseable dates are dropped. ``event_date`` < 2018-01-01 is
    filtered out (per plan). ``narrative`` is coerced to a non-null
    string (""). ``meta`` is left as a list of dicts — the downstream
    parquet writer serializes to JSON strings in bulk, which is much
    faster than ``.apply(json.dumps)`` on large frames.
    """
    df = df.copy()
    for col in NORMALIZED_COLUMNS:
        if col not in df.columns:
            df[col] = None
    df["source"] = source
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df = df.dropna(subset=["event_date"])
    df = df[df["event_date"] >= pd.Timestamp("2018-01-01")]
    df["narrative"] = df["narrative"].fillna("").astype(str)
    df["report_id"] = df["report_id"].astype(str)
    # Meta is left as list-of-dicts; the run_all orchestrator converts to
    # JSON strings in a single vectorized pass before writing parquet.
    return df[NORMALIZED_COLUMNS].reset_index(drop=True)


def _clean_meta(value) -> dict:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return {}
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:  # noqa: BLE001
            return {"_raw": value}
    if isinstance(value, dict):
        # Drop NaN values and convert numpy types to python natives.
        out = {}
        for k, v in value.items():
            if v is None:
                continue
            if isinstance(v, float) and pd.isna(v):
                continue
            try:
                json.dumps(v, default=str)
                out[k] = v
            except TypeError:
                out[k] = str(v)
        return out
    return {"_raw": str(value)}


def concat_strings(parts: Iterable[str | None], sep: str = "\n") -> str:
    """Join non-empty string parts, skipping None/empty/NaN."""
    out: list[str] = []
    for p in parts:
        if p is None:
            continue
        if isinstance(p, float) and pd.isna(p):
            continue
        s = str(p).strip()
        if s and s.lower() != "nan":
            out.append(s)
    return sep.join(out)


def first_nonempty(*values: str | None) -> str | None:
    for v in values:
        if v is None:
            continue
        if isinstance(v, float) and pd.isna(v):
            continue
        s = str(v).strip()
        if s and s.lower() != "nan":
            return s
    return None
