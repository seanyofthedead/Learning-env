"""Map NASA ASRS combined chunks -> unified schema.

Runs only if the user has manually exported DBOL query results into
``data/raw/asrs/chunks/`` (the combine step in ``scripts.acquire_asrs``
concatenates them into ``asrs_combined.csv``). ASRS column names vary
slightly across export formats so we use hint-based discovery.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from normalize._common import DATA_RAW, coerce_normalized, first_nonempty
from normalize.schema import NORMALIZED_COLUMNS

SOURCE = "asrs"

ID_HINTS = ("acn", "accession")
DATE_HINTS = ("time/date", "event_date", "date", "time_date")
NARRATIVE_HINTS = ("narrative", "narrative_1", "narrative_2")
SYNOPSIS_HINTS = ("synopsis",)
LOCATION_HINTS = ("location", "airport", "state_reference")
AIRCRAFT_HINTS = ("aircraft_make", "make_model", "aircraft_make_model")
REPORTER_HINTS = ("reporter_function", "reporter", "reporter_1")
ANOMALY_HINTS = ("anomaly", "anomaly_label")


def _find_col(df: pd.DataFrame, hints: tuple[str, ...]) -> str | None:
    lower = {col.lower().replace(" ", "_").replace(".", "_"): col for col in df.columns}
    for hint in hints:
        if hint in lower:
            return lower[hint]
        for key, orig in lower.items():
            if hint in key:
                return orig
    return None


def _load_raw() -> pd.DataFrame:
    combined = DATA_RAW / SOURCE / "asrs_combined.csv"
    if combined.exists():
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                return pd.read_csv(combined, dtype=str, encoding=enc, low_memory=False)
            except UnicodeDecodeError:
                continue
    # Fall back to raw chunks if combined doesn't exist yet.
    chunks_dir = DATA_RAW / SOURCE / "chunks"
    if not chunks_dir.exists():
        return pd.DataFrame()
    frames: list[pd.DataFrame] = []
    for path in sorted(chunks_dir.glob("*.csv")):
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                frames.append(pd.read_csv(path, dtype=str, encoding=enc, low_memory=False))
                break
            except UnicodeDecodeError:
                continue
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def to_normalized(raw_df: pd.DataFrame) -> pd.DataFrame:
    if raw_df.empty:
        return pd.DataFrame(columns=NORMALIZED_COLUMNS)

    id_col = _find_col(raw_df, ID_HINTS)
    date_col = _find_col(raw_df, DATE_HINTS)
    narrative_col = _find_col(raw_df, NARRATIVE_HINTS)
    synopsis_col = _find_col(raw_df, SYNOPSIS_HINTS)
    location_col = _find_col(raw_df, LOCATION_HINTS)
    aircraft_col = _find_col(raw_df, AIRCRAFT_HINTS)
    reporter_col = _find_col(raw_df, REPORTER_HINTS)
    anomaly_col = _find_col(raw_df, ANOMALY_HINTS)

    out = pd.DataFrame()
    if id_col:
        out["report_id"] = raw_df[id_col].apply(lambda v: f"{SOURCE}:{v}")
    else:
        out["report_id"] = [f"{SOURCE}:row{i}" for i in range(len(raw_df))]
    out["source"] = SOURCE
    out["event_date"] = (
        pd.to_datetime(raw_df[date_col], format="%Y%m", errors="coerce")
        if date_col
        else pd.NaT
    )
    # ASRS Time/Date is often YYYYMM format; fall back to generic parsing.
    if date_col:
        alt = pd.to_datetime(raw_df[date_col], errors="coerce")
        out["event_date"] = out["event_date"].fillna(alt)
    out["entity_raw_key"] = raw_df.apply(
        lambda r: first_nonempty(r.get(location_col), r.get(aircraft_col)) or "",
        axis=1,
    )
    out["entity_name"] = raw_df.get(aircraft_col) if aircraft_col else None
    out["entity_address"] = None
    out["location"] = raw_df.get(location_col) if location_col else None
    out["event_type"] = raw_df.get(anomaly_col) if anomaly_col else None
    out["severity"] = None
    out["narrative"] = raw_df[narrative_col].fillna("") if narrative_col else ""
    out["synopsis"] = raw_df.get(synopsis_col) if synopsis_col else None

    meta_cols = [c for c in raw_df.columns if c not in {id_col, date_col, narrative_col, synopsis_col}]
    out["meta"] = raw_df[meta_cols].to_dict(orient="records") if meta_cols else [{}] * len(raw_df)

    return coerce_normalized(out, SOURCE)


def run() -> pd.DataFrame:
    return to_normalized(_load_raw())


if __name__ == "__main__":
    df = run()
    print(f"{SOURCE}: {df.shape[0]} rows")
