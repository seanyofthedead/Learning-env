"""Text-quality features — the treatment variable for the hypothesis test.

All features operate on the ``narrative`` column. Fully vectorized: no
spaCy or transformer calls, because 1M narratives * spaCy = hours.
The features here capture the *style* of the prose (readability,
specificity, hedging, causal language) without needing NLP models.

If you want NER density / POS-based passive voice / concreteness
proxies, those can be added on a 10k-row sample of the reports after
Phase 2D establishes a baseline signal.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

try:
    import textstat  # type: ignore
except ImportError:  # pragma: no cover
    textstat = None

# Regex patterns compiled once for speed.
_WORD_RE = re.compile(r"\b\w+\b")
_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")
_CAUSAL_RE = re.compile(
    r"\b(because|due to|caused by|resulted in|led to|as a result|owing to|since|therefore|thus|hence)\b",
    re.IGNORECASE,
)
_HEDGE_WORDS = {
    "maybe", "probably", "might", "could", "possibly", "approximately",
    "about", "around", "some", "several", "few", "perhaps", "seemed",
    "apparently", "likely", "unlikely", "unclear", "somewhat",
}
_HEDGE_RE = re.compile(
    r"\b(" + "|".join(_HEDGE_WORDS) + r")\b",
    re.IGNORECASE,
)
_NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?\b")
_TEMPORAL_RE = re.compile(
    r"\b(today|yesterday|tomorrow|minute|minutes|hour|hours|morning|afternoon|evening|"
    r"night|am|pm|january|february|march|april|may|june|july|august|september|october|"
    r"november|december|monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"\d{1,2}:\d{2})\b",
    re.IGNORECASE,
)
_FIRST_PERSON_RE = re.compile(r"\b(i|me|my|mine|we|our|us)\b", re.IGNORECASE)
_THIRD_PERSON_RE = re.compile(r"\b(he|she|it|they|him|her|his|hers|them|their)\b", re.IGNORECASE)
_PASSIVE_VERB_RE = re.compile(
    r"\b(was|were|been|being|is|are|am|be)\s+\w+ed\b",
    re.IGNORECASE,
)


def _count_matches(series: pd.Series, pattern: re.Pattern) -> pd.Series:
    return series.apply(lambda s: len(pattern.findall(s or "")))


def _readability(text: str) -> dict:
    """textstat-based readability metrics; returns NaN on short text."""
    if textstat is None or not text or len(text) < 20:
        return {
            "flesch_kincaid_grade": np.nan,
            "gunning_fog": np.nan,
            "dale_chall": np.nan,
            "ari": np.nan,
        }
    try:
        return {
            "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
            "gunning_fog": textstat.gunning_fog(text),
            "dale_chall": textstat.dale_chall_readability_score(text),
            "ari": textstat.automated_readability_index(text),
        }
    except Exception:  # noqa: BLE001
        return {
            "flesch_kincaid_grade": np.nan,
            "gunning_fog": np.nan,
            "dale_chall": np.nan,
            "ari": np.nan,
        }


def build_text_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a text-quality feature dataframe keyed by report_id."""
    narr = df["narrative"].fillna("").astype(str)
    out = pd.DataFrame({"report_id": df["report_id"].values})

    # --- Basic counts ---
    # Word count
    word_counts = narr.apply(lambda s: len(_WORD_RE.findall(s)))
    out["word_count"] = word_counts.astype("int32")

    # Sentence count
    sent_counts = narr.apply(
        lambda s: len([x for x in _SENTENCE_SPLIT_RE.split(s) if x.strip()])
    )
    out["sentence_count"] = sent_counts.astype("int32").clip(lower=1)

    # Mean sentence length (words per sentence)
    out["mean_sentence_length"] = (word_counts / out["sentence_count"]).astype("float32")

    # Type-token ratio (unique words / total words)
    def ttr(s: str) -> float:
        words = _WORD_RE.findall(s.lower())
        if not words:
            return 0.0
        return len(set(words)) / len(words)

    out["type_token_ratio"] = narr.apply(ttr).astype("float32")

    # Character count and word length
    char_counts = narr.str.len()
    out["char_count"] = char_counts.astype("int32")
    out["mean_word_length"] = (
        char_counts / word_counts.replace(0, 1)
    ).astype("float32")

    # --- Causal markers (density per 100 words) ---
    causal_hits = _count_matches(narr, _CAUSAL_RE)
    out["causal_density_per100"] = (
        100 * causal_hits / word_counts.replace(0, 1)
    ).astype("float32")

    # --- Hedging ---
    hedge_hits = _count_matches(narr, _HEDGE_RE)
    out["hedge_density_per100"] = (
        100 * hedge_hits / word_counts.replace(0, 1)
    ).astype("float32")

    # --- Numeric density ---
    numeric_hits = _count_matches(narr, _NUMBER_RE)
    out["numeric_density_per100"] = (
        100 * numeric_hits / word_counts.replace(0, 1)
    ).astype("float32")

    # --- Temporal density ---
    temporal_hits = _count_matches(narr, _TEMPORAL_RE)
    out["temporal_density_per100"] = (
        100 * temporal_hits / word_counts.replace(0, 1)
    ).astype("float32")

    # --- First / third person ---
    first_hits = _count_matches(narr, _FIRST_PERSON_RE)
    third_hits = _count_matches(narr, _THIRD_PERSON_RE)
    out["first_person_density_per100"] = (
        100 * first_hits / word_counts.replace(0, 1)
    ).astype("float32")
    out["third_person_density_per100"] = (
        100 * third_hits / word_counts.replace(0, 1)
    ).astype("float32")
    out["first_third_ratio"] = (
        (first_hits + 1) / (third_hits + 1)
    ).astype("float32")

    # --- Passive voice rate (regex approximation) ---
    passive_hits = _count_matches(narr, _PASSIVE_VERB_RE)
    out["passive_per_sentence"] = (
        passive_hits / out["sentence_count"].astype("float32")
    ).astype("float32")

    # --- Readability (textstat). Slowest per-row operation. ---
    read_df = pd.DataFrame(
        [_readability(s) for s in narr],
        index=df.index,
    ).astype("float32")
    out = pd.concat([out.reset_index(drop=True), read_df.reset_index(drop=True)], axis=1)

    return out
