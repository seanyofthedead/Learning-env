# Phase 2C stats — structured + text features

_Generated at 2026-04-13T20:04:45+00:00_

**Structured features:** 1,014,047 rows × 27 cols
**Text features:** 1,014,047 rows × 19 cols

## Text-quality feature summary

| Feature | Mean | Median | Min | Max | Null% |
|---|---:|---:|---:|---:|---:|
| word_count | 50.247 | 44.000 | 0.000 | 836.000 | 0.0% |
| sentence_count | 2.236 | 1.000 | 1.000 | 67.000 | 0.0% |
| mean_sentence_length | 30.458 | 24.500 | 0.000 | 468.000 | 0.0% |
| type_token_ratio | 0.653 | 0.659 | 0.000 | 1.000 | 0.0% |
| char_count | 330.195 | 299.000 | 0.000 | 4467.000 | 0.0% |
| mean_word_length | 6.861 | 6.731 | 0.000 | 62.182 | 0.0% |
| causal_density_per100 | 0.134 | 0.000 | 0.000 | 20.000 | 0.0% |
| hedge_density_per100 | 0.173 | 0.000 | 0.000 | 20.000 | 0.0% |
| numeric_density_per100 | 0.935 | 0.000 | 0.000 | 50.000 | 0.0% |
| temporal_density_per100 | 0.064 | 0.000 | 0.000 | 20.000 | 0.0% |
| first_person_density_per100 | 0.400 | 0.000 | 0.000 | 33.333 | 0.0% |
| third_person_density_per100 | 2.742 | 1.538 | 0.000 | 28.261 | 0.0% |
| first_third_ratio | 0.834 | 1.000 | 0.011 | 77.000 | 0.0% |
| passive_per_sentence | 0.076 | 0.000 | 0.000 | 16.000 | 0.0% |
| flesch_kincaid_grade | 16.112 | 14.886 | -2.230 | 238.470 | 0.0% |
| gunning_fog | 19.058 | 17.733 | 1.200 | 185.383 | 0.0% |
| dale_chall | 11.830 | 11.609 | 0.198 | 30.723 | 0.0% |
| ari | 21.778 | 21.197 | -4.358 | 480.004 | 0.0% |

## Structured feature columns

- `year` (mean=2022.80, min=2018, max=2026)
- `month` (mean=6.45, min=1, max=12)
- `quarter` (mean=2.49, min=1, max=4)
- `day_of_week` (mean=2.55, min=0, max=6)
- `src_msha` (mean=0.05, min=0, max=1)
- `src_nrc` (mean=0.00, min=0, max=1)
- `src_osha_ita` (mean=0.88, min=0, max=1)
- `src_osha_sir` (mean=0.07, min=0, max=1)
- `prior_report_count` (mean=51.40, min=0, max=3531)
- `days_since_first_seen` (mean=194.59, min=0, max=3012)
- `entity_total_reports` (mean=103.79, min=1, max=3532)
- `narrative_word_count` (mean=49.71, min=0.0, max=794.0)
- `log_narrative_word_count` (mean=3.80, min=0.0, max=6.678342114654332)
- `has_severity` (mean=1.00, min=1, max=1)
- `has_address` (mean=0.95, min=0, max=1)
- `has_location` (mean=1.00, min=1, max=1)
- `fam_other` (mean=0.24, min=0, max=1)
- `fam_struck_by` (mean=0.22, min=0, max=1)
- `fam_overexertion` (mean=0.20, min=0, max=1)
- `fam_fall` (mean=0.19, min=0, max=1)
- `fam_exposure` (mean=0.09, min=0, max=1)
- `fam_caught_in` (mean=0.05, min=0, max=1)
- `fam_transport` (mean=0.02, min=0, max=1)
- `fam_fire_explosion` (mean=0.00, min=0, max=1)
- `fam_cut_pierce` (mean=0.00, min=0, max=1)
- `fam_electrical` (mean=0.00, min=0, max=1)
