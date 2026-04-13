"""Map NTSB CAROL Aviation data -> unified schema.

This mapper runs only if the user has manually exported CAROL data into
``data/raw/ntsb/``. It does best-effort column discovery because the
manual export format depends on which "Export" button the user clicked
in the CAROL UI (CSV vs JSON, with different column casings).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from normalize._common import DATA_RAW, coerce_normalized, first_nonempty
from normalize.schema import NORMALIZED_COLUMNS

SOURCE = "ntsb"

NARRATIVE_HINTS = ("narrative", "probable_cause", "findings", "factual")
DATE_HINTS = ("eventdate", "event_date", "date_of_event")
ID_HINTS = ("ntsb_no", "ntsbnumber", "case_number", "event_id")
OPERATOR_HINTS = ("operator", "owner", "registration")


def _find_col(df: pd.DataFrame, hints: tuple[str, ...]) -> str | None:
    lower = {col.lower().replace(" ", "_"): col for col in df.columns}
    for hint in hints:
        for key, orig in lower.items():
            if hint in key:
                return orig
    return None


def _load_raw() -> pd.DataFrame:
    src_dir = DATA_RAW / SOURCE
    if not src_dir.exists():
        return pd.DataFrame()
    excluded = {"manifest.json", "MANUAL_EXPORT_INSTRUCTIONS.md"}
    frames: list[pd.DataFrame] = []
    for path in sorted(src_dir.iterdir()):
        if not path.is_file() or path.name in excluded:
            continue
        try:
            if path.suffix.lower() == ".csv":
                frames.append(pd.read_csv(path, dtype=str, low_memory=False))
            elif path.suffix.lower() in {".json", ".jsonl"}:
                frames.append(pd.read_json(path, dtype=False))
        except Exception:  # noqa: BLE001
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
    operator_col = _find_col(raw_df, OPERATOR_HINTS)

    out = pd.DataFrame()
    if id_col:
        out["report_id"] = raw_df[id_col].apply(lambda v: f"{SOURCE}:{v}")
    else:
        out["report_id"] = [f"{SOURCE}:row{i}" for i in range(len(raw_df))]
    out["source"] = SOURCE
    out["event_date"] = (
        pd.to_datetime(raw_df[date_col], errors="coerce") if date_col else pd.NaT
    )
    out["entity_raw_key"] = raw_df[operator_col].astype(str) if operator_col else ""
    out["entity_name"] = raw_df[operator_col] if operator_col else None
    out["entity_address"] = None
    out["location"] = raw_df.get("Location") if "Location" in raw_df.columns else None
    out["event_type"] = raw_df.get("EventType") if "EventType" in raw_df.columns else None
    out["severity"] = None
    out["narrative"] = (
        raw_df[narrative_col].fillna("") if narrative_col else ""
    )
    out["synopsis"] = None
    out["meta"] = raw_df.drop(
        columns=[c for c in [id_col, date_col, narrative_col] if c],
        errors="ignore",
    ).to_dict(orient="records")

    return coerce_normalized(out, SOURCE)


def run() -> pd.DataFrame:
    return to_normalized(_load_raw())


if __name__ == "__main__":
    df = run()
    print(f"{SOURCE}: {df.shape[0]} rows")
