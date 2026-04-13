"""Evaluation metrics for Phase 2D models.

Includes ROC-AUC, PR-AUC, Brier score, per-source AUC, and a bootstrap
95% confidence interval on the delta between two models — which is
**the** capstone finding.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score


def safe_auc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """AUC that returns NaN on degenerate single-class inputs."""
    y_true = np.asarray(y_true)
    if len(np.unique(y_true)) < 2:
        return float("nan")
    return float(roc_auc_score(y_true, y_pred))


def compute_metrics(y_true, y_pred) -> dict:
    return {
        "roc_auc": safe_auc(y_true, y_pred),
        "pr_auc": float(average_precision_score(y_true, y_pred))
        if len(np.unique(y_true)) >= 2
        else float("nan"),
        "brier": float(brier_score_loss(y_true, y_pred)),
        "n": int(len(y_true)),
        "positive_rate": float(np.mean(y_true)),
    }


def per_source_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    sources: np.ndarray,
) -> pd.DataFrame:
    rows = []
    for src in np.unique(sources):
        mask = sources == src
        if mask.sum() == 0:
            continue
        m = compute_metrics(y_true[mask], y_pred[mask])
        m["source"] = src
        rows.append(m)
    return pd.DataFrame(rows).set_index("source")


def bootstrap_auc_delta(
    y_true: np.ndarray,
    y_pred_a: np.ndarray,
    y_pred_b: np.ndarray,
    *,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict:
    """Paired bootstrap on AUC(B) - AUC(A). Returns mean and 95% CI.

    A and B must be scored on the same test set in the same order.
    """
    rng = np.random.default_rng(seed)
    n = len(y_true)
    y_true = np.asarray(y_true)
    y_a = np.asarray(y_pred_a)
    y_b = np.asarray(y_pred_b)
    deltas = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        yt = y_true[idx]
        if len(np.unique(yt)) < 2:
            deltas[i] = np.nan
            continue
        deltas[i] = safe_auc(yt, y_b[idx]) - safe_auc(yt, y_a[idx])
    mean = float(np.nanmean(deltas))
    lo, hi = np.nanpercentile(deltas, [2.5, 97.5])
    return {
        "delta_mean": mean,
        "ci_low": float(lo),
        "ci_high": float(hi),
        "ci_excludes_zero": bool(lo > 0 or hi < 0),
        "n_boot": n_boot,
    }
