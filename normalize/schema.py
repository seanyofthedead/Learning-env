"""Unified NormalizedReport schema for Phase 2.

Every source-specific mapper in ``normalize/map_*.py`` must return a
``pd.DataFrame`` whose columns match ``NORMALIZED_COLUMNS`` below.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

# Column order for the normalized dataframe. Keep stable — downstream
# phases reference by name.
NORMALIZED_COLUMNS: list[str] = [
    "report_id",       # "{source}:{native_id}"
    "source",          # asrs | osha_sir | osha_ita | msha | ntsb | nrc
    "event_date",      # pandas Timestamp (will be cast to date32 in parquet)
    "entity_raw_key",  # native facility/operator key, verbatim
    "entity_name",     # free-text name (may be None)
    "entity_address",  # free-text address for fuzzy matching (may be None)
    "location",        # airport code, state, site name, etc. (may be None)
    "event_type",      # source-native classification label (may be None)
    "severity",        # hospitalization/amputation/fatality indicator
    "narrative",       # concatenated full narrative text (required, may be "")
    "synopsis",        # short summary if available (may be None)
    "meta",            # json-serializable dict of everything else we keep
]

SOURCE_NAMES = {"asrs", "osha_sir", "osha_ita", "msha", "ntsb", "nrc"}


@dataclass
class NormalizedReport:
    """Dataclass equivalent for documentation / unit tests.

    At runtime mappers return a ``pd.DataFrame`` for efficiency — this
    class just names the fields and provides type hints.
    """

    report_id: str
    source: str
    event_date: date
    entity_raw_key: str
    entity_name: str | None
    entity_address: str | None
    location: str | None
    event_type: str | None
    severity: str | None
    narrative: str
    synopsis: str | None
    meta: dict
