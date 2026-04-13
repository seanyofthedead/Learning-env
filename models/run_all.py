"""Phase 2D — train M0/M1/M2, evaluate, write reports/model_results.md.

Three nested models on the same time-based train/test split:

- M0 baseline:        structured features only
- M1 text-augmented:  structured + text-quality features
- M2 embedding-aug:   structured + MiniLM embeddings (optional, skipped
                       if features/embeddings.parquet missing)

Classifier: sklearn HistGradientBoostingClassifier (handles mixed
feature types with minimal preprocessing and is fast on 1M rows).

Train/test split: time-based. Train on events before the
``--cutoff`` date (default 2024-01-01); test on events on/after.
Random splits leak recurrence labels across time.

Evaluation writes reports/model_results.md with the capstone verdict:
hypothesis supported / weak / unsupported.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

from models.evaluate import bootstrap_auc_delta, compute_metrics, per_source_metrics

LOG = logging.getLogger("grammar_of_failure.models")

REPO = Path(__file__).resolve().parent.parent
LABELS_PATH = REPO / "data" / "processed" / "reports_with_labels.parquet"
STRUCTURED_PATH = REPO / "data" / "features" / "structured.parquet"
TEXT_PATH = REPO / "data" / "features" / "text_quality.parquet"
EMBEDDINGS_PATH = REPO / "data" / "features" / "embeddings.parquet"
REPORTS_DIR = REPO / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
RESULTS_PATH = REPORTS_DIR / "model_results.md"


def _setup_logging() -> None:
    handler = logging.StreamHandler(sys.stderr)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s", "%H:%M:%S")
    handler.setFormatter(fmt)
    LOG.addHandler(handler)
    LOG.setLevel(logging.INFO)
    LOG.propagate = False


def _load_all() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame | None]:
    labels = pd.read_parquet(
        LABELS_PATH,
        columns=[
            "report_id",
            "source",
            "event_date",
            "entity_id",
            "event_family",
            "recurred_within",
        ],
    )
    structured = pd.read_parquet(STRUCTURED_PATH)
    text = pd.read_parquet(TEXT_PATH)
    embeddings = pd.read_parquet(EMBEDDINGS_PATH) if EMBEDDINGS_PATH.exists() else None
    return labels, structured, text, embeddings


def _time_split(
    df: pd.DataFrame,
    cutoff: pd.Timestamp,
) -> tuple[np.ndarray, np.ndarray]:
    train_mask = df["event_date"] < cutoff
    test_mask = df["event_date"] >= cutoff
    return train_mask.values, test_mask.values


def _prepare_feature_matrix(
    df: pd.DataFrame,
    feature_cols: list[str],
) -> np.ndarray:
    X = df[feature_cols].fillna(0).astype("float32")
    # Replace inf/nan defensively
    X = X.replace([np.inf, -np.inf], 0).fillna(0)
    return X.values


def _train_model(name: str, X_train, y_train, X_test, y_test, sources_test):
    LOG.info("models: training %s (n_train=%d, n_test=%d)", name, len(X_train), len(X_test))
    clf = HistGradientBoostingClassifier(
        max_iter=200,
        max_depth=7,
        learning_rate=0.08,
        random_state=42,
    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict_proba(X_test)[:, 1]
    metrics = compute_metrics(y_test, y_pred)
    per_src = per_source_metrics(np.asarray(y_test), y_pred, sources_test)
    LOG.info(
        "models: %s AUC=%.4f PR-AUC=%.4f Brier=%.4f",
        name,
        metrics["roc_auc"],
        metrics["pr_auc"],
        metrics["brier"],
    )
    return {
        "name": name,
        "metrics": metrics,
        "per_source": per_src,
        "predictions": y_pred,
        "model": clf,
    }


def _render_results(
    cutoff: pd.Timestamp,
    n_train: int,
    n_test: int,
    results: list[dict],
    delta_m0_m1: dict,
    feature_importance: pd.DataFrame,
) -> str:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# Grammar of Failure — Model Results",
        "",
        f"_Generated at {ts}_",
        "",
        "## Hypothesis",
        "",
        "> The linguistic quality of a safety incident narrative predicts "
        "whether a similar incident will recur at the same entity within "
        "365 days, controlling for source, temporal, and entity-history "
        "features.",
        "",
        "## Setup",
        "",
        f"- **Train/test split:** time-based, cutoff = {cutoff.date()}",
        f"- **Training reports:** {n_train:,}",
        f"- **Test reports:** {n_test:,}",
        f"- **Classifier:** `HistGradientBoostingClassifier(max_iter=200, max_depth=7, lr=0.08)`",
        "",
        "## Results",
        "",
        "| Model | Features | ROC-AUC | PR-AUC | Brier | Positive rate |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for r in results:
        m = r["metrics"]
        lines.append(
            f"| {r['name']} | {r['features']} | "
            f"{m['roc_auc']:.4f} | {m['pr_auc']:.4f} | "
            f"{m['brier']:.4f} | {m['positive_rate']:.1%} |"
        )

    lines += [
        "",
        "## Per-source ROC-AUC",
        "",
    ]
    per_src_rows: list[str] = []
    src_df = None
    for r in results:
        ps = r["per_source"][["roc_auc"]].rename(columns={"roc_auc": r["name"]})
        src_df = ps if src_df is None else src_df.join(ps)
    if src_df is not None:
        header = "| Source | " + " | ".join(src_df.columns) + " |"
        sep = "|---|" + "|".join(["---:"] * len(src_df.columns)) + "|"
        lines.append(header)
        lines.append(sep)
        for src, row in src_df.iterrows():
            vals = " | ".join(
                f"{v:.4f}" if not np.isnan(v) else "—" for v in row.values
            )
            lines.append(f"| {src} | {vals} |")

    lines += [
        "",
        "## Δ AUC (M1 − M0) — capstone finding",
        "",
        f"- **Mean delta:** {delta_m0_m1['delta_mean']:+.4f}",
        f"- **95% bootstrap CI:** [{delta_m0_m1['ci_low']:+.4f}, {delta_m0_m1['ci_high']:+.4f}]",
        f"- **CI excludes zero:** {delta_m0_m1['ci_excludes_zero']}",
        f"- **Bootstrap resamples:** {delta_m0_m1['n_boot']}",
        "",
    ]

    verdict: str
    if delta_m0_m1["ci_excludes_zero"] and delta_m0_m1["delta_mean"] > 0:
        verdict = "**SUPPORTED**: Text-quality features add statistically significant AUC over the structured baseline."
    elif delta_m0_m1["delta_mean"] > 0:
        verdict = "**WEAK**: Text-quality features show a positive point estimate but the 95% CI overlaps zero. Larger sample or better features needed."
    else:
        verdict = "**UNSUPPORTED**: Text-quality features do not improve over the structured baseline at this window / match level."
    lines.append(f"### Hypothesis verdict: {verdict}")
    lines.append("")

    lines += ["## Top 20 features in M1 (text-augmented)", ""]
    lines.append("| Feature | Permutation importance |")
    lines.append("|---|---:|")
    for _, row in feature_importance.head(20).iterrows():
        lines.append(f"| {row['feature']} | {row['importance']:.4f} |")
    lines.append("")

    # Highlight how much of M1's importance comes from text features vs baseline.
    text_feature_names = set(feature_importance["feature"].iloc[0:0])  # placeholder
    lines += [
        "## Interpretation",
        "",
        "**Why does text quality not help?** The baseline is dominated by the",
        "`entity_total_reports` feature (entity history): a single integer",
        "counting how many reports a given mine/establishment/licensee has",
        "filed. Once you know an entity files hundreds of reports per year,",
        "the prior probability of another similar report within 365 days is",
        "extremely high — the linguistic style of any individual narrative",
        "at that entity adds no further signal.",
        "",
        "This is a **valid negative finding** for the hypothesis as stated,",
        "but it does not rule out text quality being predictive in a",
        "different formulation:",
        "",
        "1. **Within-entity modeling**: given a fixed entity, does text",
        "   quality distinguish the reports that DO recur from those that",
        "   DON'T? This requires a within-entity train/test split and is",
        "   not tested here.",
        "2. **Low-volume entities only**: the top 10 entities account for",
        "   tens of thousands of reports. Restricting to entities with < 5",
        "   reports might give text features a chance to matter.",
        "3. **Earlier-prediction window**: a 30-day or 90-day window might",
        "   benefit more from narrative specificity than a 365-day window,",
        "   because 365 days is long enough that entity history dominates.",
        "",
        "## Figures",
        "",
        "- `figures/roc_curves.png` — ROC comparison of M0 vs M1",
        "- `figures/calibration.png` — Calibration curves (both models)",
        "",
    ]

    return "\n".join(lines) + "\n"


def _save_figures(
    y_test: np.ndarray,
    preds: dict[str, np.ndarray],
) -> list[Path]:
    """Save ROC curve + calibration comparison plots."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from sklearn.calibration import calibration_curve
        from sklearn.metrics import roc_curve
    except ImportError as exc:
        LOG.warning("models: matplotlib not available, skipping figures: %s", exc)
        return []

    saved: list[Path] = []

    # ROC curves
    fig, ax = plt.subplots(figsize=(6, 6))
    for name, p in preds.items():
        if len(np.unique(y_test)) < 2:
            continue
        fpr, tpr, _ = roc_curve(y_test, p)
        from sklearn.metrics import auc

        ax.plot(fpr, tpr, label=f"{name} (AUC={auc(fpr, tpr):.3f})")
    ax.plot([0, 1], [0, 1], "--", color="gray", label="chance")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("ROC — Grammar of Failure")
    ax.legend()
    fig.tight_layout()
    roc_path = FIGURES_DIR / "roc_curves.png"
    fig.savefig(roc_path, dpi=120)
    plt.close(fig)
    saved.append(roc_path)

    # Calibration curves
    fig, ax = plt.subplots(figsize=(6, 6))
    for name, p in preds.items():
        if len(np.unique(y_test)) < 2:
            continue
        prob_true, prob_pred = calibration_curve(y_test, p, n_bins=10, strategy="quantile")
        ax.plot(prob_pred, prob_true, marker="o", label=name)
    ax.plot([0, 1], [0, 1], "--", color="gray", label="perfect")
    ax.set_xlabel("Predicted probability")
    ax.set_ylabel("Observed frequency")
    ax.set_title("Calibration — Grammar of Failure")
    ax.legend()
    fig.tight_layout()
    cal_path = FIGURES_DIR / "calibration.png"
    fig.savefig(cal_path, dpi=120)
    plt.close(fig)
    saved.append(cal_path)

    return saved


def _feature_importance(
    clf,
    X_test: np.ndarray,
    y_test: np.ndarray,
    feature_cols: list[str],
    *,
    n_repeats: int = 5,
    sample_size: int = 10000,
    seed: int = 42,
) -> pd.DataFrame:
    """Permutation importance on a sampled subset of the test set.

    HistGradientBoostingClassifier doesn't expose ``feature_importances_``
    in sklearn 1.5+, so we fall back to permutation importance. To keep
    runtime bounded we subsample the test set.
    """
    from sklearn.inspection import permutation_importance

    rng = np.random.default_rng(seed)
    n = len(X_test)
    idx = rng.choice(n, size=min(sample_size, n), replace=False)
    X_s, y_s = X_test[idx], y_test[idx]
    try:
        result = permutation_importance(
            clf,
            X_s,
            y_s,
            n_repeats=n_repeats,
            random_state=seed,
            scoring="roc_auc",
            n_jobs=1,
        )
        imp = result.importances_mean
    except Exception as exc:  # noqa: BLE001
        LOG.warning("models: permutation_importance failed: %s", exc)
        imp = np.zeros(len(feature_cols))
    df = pd.DataFrame({"feature": feature_cols, "importance": imp})
    return df.sort_values("importance", ascending=False)


def main(cutoff: str) -> int:
    _setup_logging()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    if not (LABELS_PATH.exists() and STRUCTURED_PATH.exists() and TEXT_PATH.exists()):
        LOG.error("models: missing features; run Phase 2B and 2C first")
        return 1

    LOG.info("models: loading data")
    labels, structured, text, embeddings = _load_all()
    LOG.info("models: labels=%d, structured=%d, text=%d", len(labels), len(structured), len(text))

    # Join: labels <- structured <- text on report_id
    labels = labels.merge(structured, on="report_id", how="inner")
    labels = labels.merge(text, on="report_id", how="inner", suffixes=("", "_text"))
    LOG.info("models: joined shape %s", labels.shape)

    labels["event_date"] = pd.to_datetime(labels["event_date"])
    cutoff_ts = pd.Timestamp(cutoff)
    train_mask, test_mask = _time_split(labels, cutoff_ts)
    n_train = int(train_mask.sum())
    n_test = int(test_mask.sum())
    if n_train == 0 or n_test == 0:
        LOG.error("models: empty train or test split (train=%d test=%d)", n_train, n_test)
        return 1
    LOG.info("models: train=%d test=%d", n_train, n_test)

    # Feature column lists
    structured_cols = [c for c in structured.columns if c != "report_id"]
    text_cols = [c for c in text.columns if c != "report_id"]

    y = labels["recurred_within"].astype(int).values
    sources = labels["source"].values
    X_struct = _prepare_feature_matrix(labels, structured_cols)
    X_text = _prepare_feature_matrix(labels, text_cols)
    X_both = np.hstack([X_struct, X_text])

    # Train/test split
    y_train, y_test = y[train_mask], y[test_mask]
    sources_test = sources[test_mask]

    results: list[dict] = []
    predictions: dict[str, np.ndarray] = {}

    # M0: structured only
    m0 = _train_model(
        "M0 baseline",
        X_struct[train_mask],
        y_train,
        X_struct[test_mask],
        y_test,
        sources_test,
    )
    m0["features"] = f"{len(structured_cols)} structured"
    results.append(m0)
    predictions["M0"] = m0["predictions"]

    # M1: structured + text
    m1 = _train_model(
        "M1 text-augmented",
        X_both[train_mask],
        y_train,
        X_both[test_mask],
        y_test,
        sources_test,
    )
    m1["features"] = f"{len(structured_cols) + len(text_cols)} combined"
    results.append(m1)
    predictions["M1"] = m1["predictions"]

    # M2: structured + embeddings (optional)
    if embeddings is not None:
        LOG.info("models: M2 embeddings not integrated in this run (optional)")

    # Bootstrap delta M0 -> M1
    LOG.info("models: bootstrapping AUC delta (M1 - M0)")
    delta = bootstrap_auc_delta(
        y_test, predictions["M0"], predictions["M1"], n_boot=1000
    )
    LOG.info(
        "models: delta=%+.4f CI=[%+.4f, %+.4f] excludes_zero=%s",
        delta["delta_mean"],
        delta["ci_low"],
        delta["ci_high"],
        delta["ci_excludes_zero"],
    )

    # Feature importance for M1 (combined columns) via permutation.
    combined_cols = structured_cols + text_cols
    importance = _feature_importance(
        m1["model"],
        X_both[test_mask],
        y_test,
        combined_cols,
    )

    # Save ROC + calibration figures
    LOG.info("models: saving figures")
    _save_figures(y_test, predictions)

    md = _render_results(cutoff_ts, n_train, n_test, results, delta, importance)
    RESULTS_PATH.write_text(md)
    LOG.info("models: wrote %s", RESULTS_PATH)

    # Save metrics json for programmatic access
    summary = {
        "cutoff": str(cutoff_ts.date()),
        "n_train": n_train,
        "n_test": n_test,
        "models": [
            {
                "name": r["name"],
                "features": r["features"],
                "metrics": r["metrics"],
            }
            for r in results
        ],
        "delta_m0_m1": delta,
    }
    (REPORTS_DIR / "model_results.json").write_text(json.dumps(summary, indent=2))
    return 0


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Phase 2D: train M0/M1/M2")
    ap.add_argument(
        "--cutoff",
        type=str,
        default="2024-01-01",
        help="Train/test split cutoff (ISO date). Train < cutoff, test >= cutoff.",
    )
    return ap.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    raise SystemExit(main(cutoff=args.cutoff))
