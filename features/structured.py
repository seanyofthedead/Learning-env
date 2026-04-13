"""Baseline structured features — the non-text control for Phase 2D.

Computed fully vectorized. No narrative text is used here — that's
what text_quality.py is for. The point of this module is to produce a
feature matrix that captures everything we know about a report EXCEPT
the linguistic quality of its narrative, so that Phase 2D can measure
how much additional signal text quality adds over the baseline.
"""

from __future__ import annotations

import pandas as pd


def build_structured_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a wide dataframe of structured features keyed by report_id.

    Columns:
      - one-hot source
      - temporal: year, month, day_of_week, quarter
      - log narrative length (purely length — not quality)
      - entity-level rolling counts (leakage-safe: prior reports only)
      - severity_flag (has any severity indicator)
      - has_address, has_location (presence flags)
    """
    df = df.copy()
    df["event_date"] = pd.to_datetime(df["event_date"])

    # Sort so leakage-safe rolling counts are valid.
    df = df.sort_values(["entity_id", "event_date"]).reset_index(drop=True)

    # --- Temporal features ---
    out = pd.DataFrame({"report_id": df["report_id"]})
    out["year"] = df["event_date"].dt.year
    out["month"] = df["event_date"].dt.month
    out["quarter"] = df["event_date"].dt.quarter
    out["day_of_week"] = df["event_date"].dt.dayofweek

    # --- Source one-hot ---
    source_dummies = pd.get_dummies(df["source"], prefix="src", dtype="int8")
    out = pd.concat([out, source_dummies], axis=1)

    # --- Entity history (leakage-safe) ---
    # prior_report_count: how many earlier reports this entity had before this one
    grouped = df.groupby("entity_id", sort=False)
    out["prior_report_count"] = grouped.cumcount()
    # days_since_first_seen: elapsed days since the entity's first report
    first_date = grouped["event_date"].transform("min")
    out["days_since_first_seen"] = (df["event_date"] - first_date).dt.days
    # entity_total_reports: total reports for this entity across full corpus
    # (NOT leakage-safe in a strict sense, but reflects entity scale)
    out["entity_total_reports"] = grouped["report_id"].transform("count")

    # --- Narrative length (structural, not quality) ---
    import numpy as np
    word_count = df["narrative"].fillna("").str.split().str.len().astype("float")
    out["narrative_word_count"] = word_count
    out["log_narrative_word_count"] = np.log1p(word_count)

    # --- Severity flag ---
    out["has_severity"] = df["severity"].notna().astype("int8")

    # --- Presence flags ---
    out["has_address"] = df["entity_address"].notna().astype("int8")
    out["has_location"] = df["location"].notna().astype("int8")

    # --- Event family one-hot (top 10 overall) ---
    top_families = df["event_family"].value_counts().head(10).index.tolist()
    for fam in top_families:
        out[f"fam_{fam}"] = (df["event_family"] == fam).astype("int8")

    return out
