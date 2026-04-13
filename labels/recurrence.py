"""Recurrence labeling — did the same entity have a similar event within W days?"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import yaml

FAMILY_YAML = Path(__file__).resolve().parent / "event_families.yaml"


def load_family_patterns(path: Path = FAMILY_YAML) -> dict[str, dict[str, list[str]]]:
    with open(path) as f:
        return yaml.safe_load(f)


def assign_family(event_type: str | None, source: str, patterns: dict) -> str:
    """Return the family label for ``event_type`` under ``source``.

    If no pattern matches, returns ``"other"``. Case-insensitive substring
    match. Multiple matches take the first listed family.
    """
    if event_type is None or (isinstance(event_type, float) and pd.isna(event_type)):
        return "other"
    text = str(event_type).lower()
    src_patterns = patterns.get(source, {})
    for family, needles in src_patterns.items():
        for needle in needles:
            if needle.lower() in text:
                return family
    return "other"


def assign_family_vectorized(event_type: pd.Series, source: pd.Series, patterns: dict) -> pd.Series:
    """Vectorized family assignment per (source, event_type) pair."""
    result = pd.Series("other", index=event_type.index, dtype="object")
    text = event_type.fillna("").astype(str).str.lower()
    # For each source, apply that source's patterns in order.
    for src, src_patterns in patterns.items():
        mask_src = source == src
        if not mask_src.any():
            continue
        # Track which rows in this source are still "other" (unassigned).
        remaining = mask_src & (result == "other")
        for family, needles in src_patterns.items():
            if not remaining.any():
                break
            needle_pat = "|".join(needles).lower()
            hit = remaining & text.str.contains(needle_pat, regex=True, na=False)
            result.loc[hit] = family
            remaining = remaining & (result == "other")
    return result


def compute_recurrence(
    df: pd.DataFrame,
    *,
    window_days: int = 365,
    match_level: str = "family",
) -> pd.DataFrame:
    """Assign a ``recurred_within`` boolean label per report.

    For each report, positive iff another report exists with:
      - same ``entity_id``
      - same match key (family or exact event_type)
      - ``event_date`` in ``(event_date, event_date + window_days]``

    Adds columns: ``event_family``, ``match_key``, ``recurred_within``,
    ``label_window_days``, ``label_match_level``.

    Implementation: sort by (entity_id, match_key, event_date), then for
    each group check whether the next record (ordered by date) falls
    within the window. This is O(n log n) which is fine on 1M rows.
    """
    if df.empty:
        return df.assign(
            event_family="other",
            match_key="",
            recurred_within=False,
            label_window_days=window_days,
            label_match_level=match_level,
        )

    patterns = load_family_patterns()
    df = df.copy()
    df["event_family"] = assign_family_vectorized(df["event_type"], df["source"], patterns)

    if match_level == "family":
        df["match_key"] = df["source"] + ":" + df["event_family"]
    elif match_level == "exact-code":
        df["match_key"] = (
            df["source"] + ":" + df["event_type"].fillna("").astype(str).str.lower()
        )
    else:
        raise ValueError(f"Unknown match_level: {match_level}")

    # Sort so we can use grouped cumulative logic.
    df = df.sort_values(["entity_id", "match_key", "event_date"]).reset_index(drop=True)

    # For each (entity_id, match_key) group, look forward for any event
    # whose date is within window_days of the current event. We do this by
    # shifting the date column negatively within the group, then checking
    # the minimum forward date inside the window.
    window = pd.Timedelta(days=window_days)

    # Group by (entity_id, match_key) and compute "next event date" inside the group.
    grouped = df.groupby(["entity_id", "match_key"], sort=False)
    # Next event date strictly after current, in sorted order.
    df["_next_event_date"] = grouped["event_date"].shift(-1)

    # Recurrence = next event exists and is within window.
    df["recurred_within"] = (
        df["_next_event_date"].notna()
        & ((df["_next_event_date"] - df["event_date"]) <= window)
    )

    df = df.drop(columns=["_next_event_date"])
    df["label_window_days"] = window_days
    df["label_match_level"] = match_level
    return df
