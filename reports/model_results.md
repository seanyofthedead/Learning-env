# Grammar of Failure — Model Results

_Generated at 2026-04-13T20:08:53+00:00_

## Hypothesis

> The linguistic quality of a safety incident narrative predicts whether a similar incident will recur at the same entity within 365 days, controlling for source, temporal, and entity-history features.

## Setup

- **Train/test split:** time-based, cutoff = 2024-01-01
- **Training reports:** 985,138
- **Test reports:** 28,909
- **Classifier:** `HistGradientBoostingClassifier(max_iter=200, max_depth=7, lr=0.08)`

## Results

| Model | Features | ROC-AUC | PR-AUC | Brier | Positive rate |
|---|---|---:|---:|---:|---:|
| M0 baseline | 26 structured | 0.9708 | 0.9046 | 0.0608 | 25.4% |
| M1 text-augmented | 44 combined | 0.9704 | 0.9044 | 0.0615 | 25.4% |

## Per-source ROC-AUC

| Source | M0 baseline | M1 text-augmented |
|---|---:|---:|
| msha | 0.9099 | 0.9084 |
| nrc | 1.0000 | 1.0000 |
| osha_ita | 0.9181 | 0.9156 |
| osha_sir | 0.9898 | 0.9900 |

## Δ AUC (M1 − M0) — capstone finding

- **Mean delta:** -0.0005
- **95% bootstrap CI:** [-0.0007, -0.0003]
- **CI excludes zero:** True
- **Bootstrap resamples:** 1000

### Hypothesis verdict: **UNSUPPORTED**: Text-quality features do not improve over the structured baseline at this window / match level.

## Top 20 features in M1 (text-augmented)

| Feature | Permutation importance |
|---|---:|
| entity_total_reports | 0.6905 |
| prior_report_count | 0.0280 |
| days_since_first_seen | 0.0024 |
| fam_caught_in | 0.0012 |
| fam_fire_explosion | 0.0011 |
| fam_exposure | 0.0007 |
| src_msha | 0.0006 |
| fam_electrical | 0.0005 |
| fam_fall | 0.0003 |
| char_count | 0.0002 |
| fam_other | 0.0001 |
| month | 0.0001 |
| mean_word_length | 0.0001 |
| src_osha_ita | 0.0001 |
| src_osha_sir | 0.0001 |
| type_token_ratio | 0.0000 |
| fam_struck_by | 0.0000 |
| narrative_word_count | 0.0000 |
| passive_per_sentence | 0.0000 |
| word_count | 0.0000 |

## Interpretation

**Why does text quality not help?** The baseline is dominated by the
`entity_total_reports` feature (entity history): a single integer
counting how many reports a given mine/establishment/licensee has
filed. Once you know an entity files hundreds of reports per year,
the prior probability of another similar report within 365 days is
extremely high — the linguistic style of any individual narrative
at that entity adds no further signal.

This is a **valid negative finding** for the hypothesis as stated,
but it does not rule out text quality being predictive in a
different formulation:

1. **Within-entity modeling**: given a fixed entity, does text
   quality distinguish the reports that DO recur from those that
   DON'T? This requires a within-entity train/test split and is
   not tested here.
2. **Low-volume entities only**: the top 10 entities account for
   tens of thousands of reports. Restricting to entities with < 5
   reports might give text features a chance to matter.
3. **Earlier-prediction window**: a 30-day or 90-day window might
   benefit more from narrative specificity than a 365-day window,
   because 365 days is long enough that entity history dominates.

## Figures

- `figures/roc_curves.png` — ROC comparison of M0 vs M1
- `figures/calibration.png` — Calibration curves (both models)

