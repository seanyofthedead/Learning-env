"""Shared HTTP / manifest / logging utilities for Phase 1 acquisition.

Every ``scripts.acquire_*`` module uses these helpers so they have uniform
retry behavior, resume semantics, provenance tracking, and summary stats.

Network-free helpers (``sha256_file``, ``extract_zip``,
``narrative_wc_stats``, manifest round-trip) are unit-testable offline.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
import time
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Literal

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

# ---------------------------------------------------------------------------
# Paths and logging
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = REPO_ROOT / "data" / "raw"

LOG = logging.getLogger("grammar_of_failure")


def setup_logging(level: int = logging.INFO) -> None:
    """Configure stderr logging once per process. Idempotent."""
    if LOG.handlers:
        return
    handler = logging.StreamHandler(sys.stderr)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s", "%H:%M:%S")
    handler.setFormatter(fmt)
    LOG.addHandler(handler)
    LOG.setLevel(level)
    LOG.propagate = False


# ---------------------------------------------------------------------------
# HTTP session with retries
# ---------------------------------------------------------------------------

DEFAULT_USER_AGENT = "UVA-MSBA-Capstone-Research/1.0"


def make_session(user_agent: str | None = None) -> requests.Session:
    """Build a requests Session with urllib3 retry/backoff for robustness."""
    ua = user_agent or os.environ.get("HTTP_USER_AGENT", DEFAULT_USER_AGENT)
    session = requests.Session()
    session.headers.update({"User-Agent": ua, "Accept": "*/*"})

    retry = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET", "POST", "HEAD"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# ---------------------------------------------------------------------------
# File IO helpers
# ---------------------------------------------------------------------------


def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    """Compute sha256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def download_with_progress(
    session: requests.Session,
    url: str,
    dest: Path,
    *,
    resume: bool = False,
    chunk_size: int = 1 << 16,
    timeout: float = 60.0,
) -> Path:
    """Stream-download ``url`` to ``dest`` with a tqdm progress bar.

    Uses an atomic ``.part`` suffix and renames on success so partial files
    don't pollute the raw data directory.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    headers: dict[str, str] = {}
    mode = "wb"
    start = 0
    if resume and part.exists():
        start = part.stat().st_size
        headers["Range"] = f"bytes={start}-"
        mode = "ab"
        LOG.info("Resuming %s from byte %d", dest.name, start)

    with session.get(url, stream=True, headers=headers, timeout=timeout) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0)) + start
        with open(part, mode) as f, tqdm(
            total=total if total > 0 else None,
            initial=start,
            unit="B",
            unit_scale=True,
            desc=dest.name,
            leave=False,
        ) as bar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if not chunk:
                    continue
                f.write(chunk)
                bar.update(len(chunk))
    part.replace(dest)
    return dest


def extract_zip(zip_path: Path, dest_dir: Path) -> list[Path]:
    """Extract a ZIP archive and return the list of extracted file paths."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    extracted: list[Path] = []
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            out_path = dest_dir / info.filename
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, open(out_path, "wb") as dst:
                dst.write(src.read())
            extracted.append(out_path)
    return extracted


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


def _manifest_path(source_dir: Path) -> Path:
    return source_dir / "manifest.json"


def write_manifest(source_dir: Path, entries: list[dict]) -> Path:
    """Write ``manifest.json`` for a source directory."""
    source_dir.mkdir(parents=True, exist_ok=True)
    path = _manifest_path(source_dir)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, default=str)
    return path


def load_manifest(source_dir: Path) -> list[dict]:
    """Return the entries list from ``manifest.json``, or [] if missing."""
    path = _manifest_path(source_dir)
    if not path.exists():
        return []
    with open(path) as f:
        payload = json.load(f)
    if isinstance(payload, list):
        return payload
    return payload.get("entries", [])


def manifest_entry(
    *,
    url: str,
    filename: str,
    path: Path,
    notes: str = "",
    extra: dict | None = None,
) -> dict:
    """Build a standardized manifest entry for one downloaded file."""
    entry = {
        "url": url,
        "download_ts": datetime.now(timezone.utc).isoformat(),
        "filename": filename,
        "bytes": path.stat().st_size if path.exists() else None,
        "sha256": sha256_file(path) if path.exists() else None,
        "notes": notes,
    }
    if extra:
        entry.update(extra)
    return entry


# ---------------------------------------------------------------------------
# Narrative and CSV summarization
# ---------------------------------------------------------------------------


def narrative_wc_stats(series: pd.Series) -> dict[str, Any]:
    """Word-count summary stats for a narrative column.

    Returns ``{}`` if the series is empty or all-null.
    """
    if series is None:
        return {}
    s = series.dropna().astype(str)
    if s.empty:
        return {}
    wc = s.str.split().str.len()
    return {
        "n": int(wc.shape[0]),
        "mean": float(wc.mean()),
        "median": float(wc.median()),
        "p25": float(wc.quantile(0.25)),
        "p75": float(wc.quantile(0.75)),
        "min": int(wc.min()),
        "max": int(wc.max()),
    }


def summarize_dataframe(
    df: pd.DataFrame,
    *,
    date_col: str | None,
    narrative_col: str | None,
) -> dict[str, Any]:
    """Build a summary dict suitable for AcquisitionResult."""
    out: dict[str, Any] = {
        "row_count": int(df.shape[0]),
        "columns": list(df.columns),
    }
    if date_col and date_col in df.columns:
        try:
            dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
            if not dates.empty:
                out["date_range"] = (str(dates.min().date()), str(dates.max().date()))
        except Exception as exc:  # noqa: BLE001
            LOG.warning("Date parse failed for %s: %s", date_col, exc)
    if narrative_col and narrative_col in df.columns:
        out["narrative_stats"] = narrative_wc_stats(df[narrative_col])
    return out


# ---------------------------------------------------------------------------
# Result dataclass + orchestration helper
# ---------------------------------------------------------------------------

StatusT = Literal["ok", "partial", "failed", "skipped"]


@dataclass
class AcquisitionResult:
    source: str
    status: StatusT
    row_count: int | None = None
    date_range: tuple[str, str] | None = None
    columns: list[str] | None = None
    narrative_stats: dict[str, Any] | None = None
    files: list[Path] = field(default_factory=list)
    error: str | None = None
    duration_s: float = 0.0
    notes: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["files"] = [str(p) for p in self.files]
        return d


def run_with_logging(
    source: str,
    fn: Callable[[], AcquisitionResult],
) -> AcquisitionResult:
    """Run an acquisition function, catch exceptions, time it, log the outcome."""
    setup_logging()
    LOG.info("=== %s: starting ===", source)
    t0 = time.monotonic()
    try:
        result = fn()
    except KeyboardInterrupt:
        raise
    except Exception as exc:  # noqa: BLE001
        LOG.exception("%s: FAILED with %s", source, exc)
        result = AcquisitionResult(
            source=source,
            status="failed",
            error=f"{type(exc).__name__}: {exc}",
        )
    result.duration_s = time.monotonic() - t0
    LOG.info(
        "=== %s: %s (rows=%s, %.1fs) ===",
        source,
        result.status,
        result.row_count,
        result.duration_s,
    )
    return result


# ---------------------------------------------------------------------------
# Idempotency helpers
# ---------------------------------------------------------------------------


def is_already_downloaded(source_dir: Path, expected_filenames: list[str]) -> bool:
    """Return True if every expected file exists and sha256 matches manifest."""
    entries = load_manifest(source_dir)
    if not entries:
        return False
    by_name = {e["filename"]: e for e in entries}
    for name in expected_filenames:
        entry = by_name.get(name)
        if entry is None:
            return False
        path = source_dir / name
        if not path.exists():
            return False
        if entry.get("sha256") and entry["sha256"] != sha256_file(path):
            return False
    return True
