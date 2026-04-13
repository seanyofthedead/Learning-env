# Grammar of Failure — Model Results

_Generated at 2026-04-13T20:51:56+00:00_

## Hypothesis

> The linguistic quality of a safety incident narrative predicts whether a similar incident will recur at the same entity within 365 days, controlling for source, temporal, and entity-history features.

## Setup

- **Train/test split:** time-based, cutoff = 2024-01-01
- **Training reports:** 985,764
- **Test reports:** 716,904
- **Classifier:** `HistGradientBoostingClassifier(max_iter=200, max_depth=7, lr=0.08)`

## Results

| Model | Features | ROC-AUC | PR-AUC | Brier | Positive rate |
|---|---|---:|---:|---:|---:|
| M0 baseline | 26 structured | 0.9210 | 0.9643 | 0.1025 | 70.8% |
| M1 text-augmented | 44 combined | 0.9207 | 0.9641 | 0.1029 | 70.8% |

## Per-source ROC-AUC

| Source | M0 baseline | M1 text-augmented |
|---|---:|---:|
| msha | 0.9178 | 0.9174 |
| nrc | 1.0000 | 1.0000 |
| osha_ita | 0.9147 | 0.9143 |
| osha_sir | 0.9900 | 0.9901 |

## Δ AUC (M1 − M0) — capstone finding

- **Mean delta:** -0.0004
- **95% bootstrap CI:** [-0.0005, -0.0002]
- **CI excludes zero:** True
- **Bootstrap resamples:** 1000

### Hypothesis verdict: **UNSUPPORTED**: Text-quality features do not improve over the structured baseline at this window / match level.

## Top 20 features in M1 (text-augmented)

| Feature | Permutation importance |
|---|---:|
| entity_total_reports | 0.5040 |
| prior_report_count | 0.1434 |
| days_since_first_seen | 0.0174 |
| month | 0.0058 |
| fam_exposure | 0.0044 |
| fam_transport | 0.0032 |
| fam_fire_explosion | 0.0014 |
| fam_struck_by | 0.0007 |
| fam_overexertion | 0.0004 |
| fam_electrical | 0.0003 |
| numeric_density_per100 | 0.0003 |
| flesch_kincaid_grade | 0.0003 |
| fam_caught_in | 0.0003 |
| src_osha_ita | 0.0002 |
| first_third_ratio | 0.0001 |
| gunning_fog | 0.0001 |
| third_person_density_per100 | 0.0001 |
| passive_per_sentence | 0.0001 |
| first_person_density_per100 | 0.0001 |
| causal_density_per100 | 0.0000 |

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

