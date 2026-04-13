"""NRC Licensee Event Reports / Event Notifications.

NRC publishes a single pipe-delimited text file containing **the last
month** of Event Notifications. Each row has ~71 fields including a rich
``Event Text`` narrative column (multi-paragraph, with embedded update
sections). There is no documented bulk archive — historical coverage
requires scraping per-day HTML pages at
``/reading-rm/doc-collections/event-status/event/{YEAR}/YYYYMMDDen``.

For this capstone we download the last-month snapshot and report
``partial`` status. The hypothesis test can use this as a smaller-volume
cross-domain validation corpus (nuclear narratives are long and technical).
Extending to full 2018–2024 coverage is a documented future step in the
acquisition log.

Canonical URL: https://www.nrc.gov/reading-rm/doc-collections/event-status/event/event-notification-rpt-lastmonth.txt
"""

from __future__ import annotations

import pandas as pd
import requests

from scripts.common import (
    DATA_RAW,
    LOG,
    AcquisitionResult,
    download_with_progress,
    is_already_downloaded,
    make_session,
    manifest_entry,
    narrative_wc_stats,
    run_with_logging,
    write_manifest,
)

SOURCE = "nrc"
SOURCE_DIR = DATA_RAW / SOURCE

LAST_MONTH_URL = (
    "https://www.nrc.gov/reading-rm/doc-collections/event-status/event/"
    "event-notification-rpt-lastmonth.txt"
)
DATA_DICT_URL = (
    "https://www.nrc.gov/reading-rm/doc-collections/event-status/event/"
    "event-notification-rpt-datadictionary.xls"
)

NARRATIVE_CANDIDATES = ["Event Text", "Event_Text", "EventText", "event_text"]
DATE_CANDIDATES = ["Event Dt", "Event_Dt", "EventDt", "Notification Dt"]


def _pick(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    lower = {col.lower(): col for col in df.columns}
    for c in candidates:
        if c.lower() in lower:
            return lower[c.lower()]
    return None


def _summarize(df: pd.DataFrame) -> dict:
    narrative_col = _pick(df, NARRATIVE_CANDIDATES)
    date_col = _pick(df, DATE_CANDIDATES)
    out: dict = {"row_count": int(df.shape[0]), "columns": list(df.columns)}
    if date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
        if not dates.empty:
            out["date_range"] = (str(dates.min().date()), str(dates.max().date()))
    if narrative_col:
        out["narrative_stats"] = narrative_wc_stats(df[narrative_col])
    return out


def run(session: requests.Session | None = None, *, force: bool = False) -> AcquisitionResult:
    session = session or make_session()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    txt_name = "event-notification-rpt-lastmonth.txt"
    dict_name = "event-notification-rpt-datadictionary.xls"
    txt_path = SOURCE_DIR / txt_name
    dict_path = SOURCE_DIR / dict_name

    if force or not is_already_downloaded(SOURCE_DIR, [txt_name]):
        download_with_progress(session, LAST_MONTH_URL, txt_path)
    else:
        LOG.info("NRC: %s already present, skipping", txt_name)

    try:
        download_with_progress(session, DATA_DICT_URL, dict_path)
    except requests.RequestException as exc:
        LOG.warning("NRC: could not fetch data dictionary: %s", exc)

    # Pipe-delimited, sometimes has trailing empty columns because of a
    # terminal pipe — read tolerantly.
    try:
        df = pd.read_csv(
            txt_path,
            sep="|",
            dtype=str,
            on_bad_lines="warn",
            encoding="latin-1",
            engine="python",
        )
    except Exception as exc:  # noqa: BLE001
        return AcquisitionResult(
            source=SOURCE,
            status="failed",
            error=f"Parse failed: {exc}",
        )

    # Drop trailing unnamed empty columns that sometimes appear.
    df = df.loc[:, ~df.columns.astype(str).str.fullmatch(r"Unnamed:\s*\d+")]
    stats = _summarize(df)
    LOG.info("NRC: %d rows, %d columns, narrative=%s", df.shape[0], df.shape[1], bool(stats.get("narrative_stats")))

    entries = [
        manifest_entry(
            url=LAST_MONTH_URL,
            filename=txt_name,
            path=txt_path,
            notes="NRC Event Notifications, most recent ~month only",
        )
    ]
    if dict_path.exists():
        entries.append(
            manifest_entry(
                url=DATA_DICT_URL,
                filename=dict_name,
                path=dict_path,
                notes="Data dictionary (XLS)",
            )
        )
    write_manifest(SOURCE_DIR, entries)

    return AcquisitionResult(
        source=SOURCE,
        status="partial",
        row_count=stats.get("row_count"),
        date_range=stats.get("date_range"),
        columns=stats.get("columns"),
        narrative_stats=stats.get("narrative_stats"),
        files=[txt_path],
        notes=(
            "Only last-month snapshot; historical 2018-2024 coverage "
            "requires scraping daily HTML pages at "
            "/reading-rm/doc-collections/event-status/event/{YEAR}/YYYYMMDDen "
            "and is deferred as a future enhancement."
        ),
    )


def main() -> int:
    result = run_with_logging(SOURCE, run)
    return 0 if result.status in {"ok", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
